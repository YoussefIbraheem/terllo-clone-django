from pydantic.json_schema import models_json_schema
from flask import Flask
from .path_converter import FlaskPathConverter
class RouteCollector:
    
    def __init__(self, app: Flask, converter: FlaskPathConverter):
        self.app = app
        self.converter = converter 
    
    
    IGNORED_METHODS = {"HEAD", "OPTIONS"}

    def collect(self) -> dict:
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

        with self.app.app_context():
            for rule in self.app.url_map.iter_rules():
                if rule.endpoint == 'static':
                    continue
                
                openapi_path, path_parameters = self.converter.convert(rule.rule)

                if openapi_path not in paths:
                    paths[openapi_path] = {}

                # Each method on this route becomes its own Operation
                for method in rule.methods:
                    if method in self.IGNORED_METHODS:
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