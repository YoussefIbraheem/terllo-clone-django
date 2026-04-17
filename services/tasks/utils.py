import inspect
import yaml
import sys
import importlib
import pkgutil
import re
from flask import Flask
from app import settings
from pydantic.json_schema import models_json_schema

# Flask converter type → OpenAPI type mapping
FLASK_CONVERTER_TO_OPENAPI = {
    "int":    {"type": "integer", "format": "int64"},
    "float":  {"type": "number",  "format": "float"},
    "string": {"type": "string"},
    "str":    {"type": "string"},
    "path":   {"type": "string"},
    "uuid":   {"type": "string", "format": "uuid"},
}

def flask_path_to_openapi(flask_path: str) -> tuple[str, list[dict]]:
    """
    Converts Flask path syntax to OpenAPI path syntax and extracts path parameters.
    
    e.g. /pets/<int:pet_id>  →  ("/pets/{pet_id}", [{"name": "pet_id", "in": "path", ...}])
         /pets/<pet_id>      →  ("/pets/{pet_id}", [{"name": "pet_id", "in": "path", ...}])
    """
    parameters = []
    
    # Match both typed (<int:name>) and untyped (<name>) converters
    pattern = re.compile(r"<(?:(\w+):)?(\w+)>")
    
    def replace_param(match):
        converter = match.group(1) or "string"  # default to string if no type given
        param_name = match.group(2)
        
        schema = FLASK_CONVERTER_TO_OPENAPI.get(converter, {"type": "string"})
        parameters.append({
            "name": param_name,
            "in": "path",
            "required": True,               # path params are always required in OpenAPI
            "schema": schema,
        })
        return f"{{{param_name}}}"
    
    openapi_path = pattern.sub(replace_param, flask_path)
    return openapi_path, parameters


def get_pydantic_schemas():
    all_schemas = []
    base_module = importlib.import_module('app.schemas')
    for _, module_name, is_pkg in pkgutil.walk_packages(
        base_module.__path__, base_module.__name__ + "."
    ):
        try:
            module = importlib.import_module(module_name)
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module_name and not name.endswith('Base'):
                    all_schemas.append(obj)
        except ImportError:
            continue
    return all_schemas


# HTTP methods Flask adds automatically — exclude from OpenAPI output
IGNORED_METHODS = {"HEAD", "OPTIONS"}

def get_routes(app: Flask) -> dict:
    """
    Iterates Flask's URL map and builds an OpenAPI-compatible 'paths' dict.

    Returns a dict keyed by OpenAPI-style path strings, where each value is
    itself a dict keyed by lowercase HTTP method containing an Operation object.

    e.g. {
        "/pets": {
            "get":  { "operationId": "listPets",  "parameters": [], "responses": {"200": ...} },
            "post": { "operationId": "createPet", "parameters": [], "responses": {"200": ...} },
        },
        "/pets/{pet_id}": {
            "get":  { "operationId": "getPetById", "parameters": [...], "responses": {"200": ...} },
        }
    }
    """
    paths = {}
    
    with app.app_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint == 'static':
                continue
            
            openapi_path, path_parameters = flask_path_to_openapi(rule.rule)
            
            if openapi_path not in paths:
                paths[openapi_path] = {}
            
            # Each method on this route becomes its own Operation
            for method in rule.methods:
                if method in IGNORED_METHODS:
                    continue
                
                operation = {
                    # endpoint name is the view function name — use it as operationId
                    "operationId": f"{rule.endpoint}_{method.lower()}",
                    "parameters": path_parameters,
                    # Placeholder — real responses require per-view annotation (see note below)
                    "responses": {
                        "200": {"description": "Successful response"},
                    },
                }
                
                paths[openapi_path][method.lower()] = operation
    
    return paths


def generate_open_api_doc(app: Flask):
    try:
        routes = get_routes(app)   # pass your Flask app instance here
        
        with open("openapi.yaml", "w") as file:
            pydantic_schemas = get_pydantic_schemas()
            _, processed_schemas = models_json_schema(
                [(schema, "validation") for schema in pydantic_schemas],
                ref_template="#/components/schemas/{model}"
            )
            
            openapi_schema = {
                "openapi": "3.1.0",
                "info": {
                    "title": f"{settings.SERVICE_NAME} API DOC",
                    "version": "0.0.1",
                },
                "components": {
                    "schemas": processed_schemas.get('$defs', {}),
                },
                "paths": routes,   # ← now a properly structured dict
            }
            file.write(yaml.dump(openapi_schema, sort_keys=False))
            
    except Exception as e:
        print(f"Error generating OpenAPI documentation: {e}")