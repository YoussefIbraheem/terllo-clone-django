from pydantic.json_schema import models_json_schema
from flask import Flask
from .path_converter import FlaskPathConverter
from .yaml_extractor import YAMLExtractor


class RouteCollector:

    def __init__(
        self, app: Flask, converter: FlaskPathConverter, yaml_extractor: YAMLExtractor
    ):
        self.app = app
        self.converter = converter
        self.yaml_extractor = yaml_extractor

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
                if rule.endpoint == "static":
                    continue

                openapi_path, path_parameters = self.converter.convert(rule.rule)

                if openapi_path not in paths:
                    paths[openapi_path] = {}

                # Each method on this route becomes its own Operation
                for method in rule.methods:
                    if method in self.IGNORED_METHODS:
                        continue

                    endpoint = rule.endpoint.rsplit(".", 1)
                    if len(endpoint) < 2:
                        continue
                    module_name, function_name = endpoint
                    yaml_data = self.yaml_extractor.extract_function_data(
                        module_name, function_name
                    )
                    parameters = []
                    properties = {}

                    for param in yaml_data.get("parameters"):
                        if param["parameter_type"] in {"path","query"}:
                            new_param = {
                                "in": param["parameter_type"],
                                "name": param.get("name", ""),
                                "description": param.get("description", ""),
                                "required": param.get("required", False),
                                "schema": {
                                    "type": param.get("type", "string"),
                                },
                            }
                            parameters.append(new_param)
                        
                        if param["parameter_type"] == "body":
                            property_name = param["name"]
                            property_type = param["type"]
                            properties[property_name] = {"type": property_type}
                            
                    operation = {
                        # endpoint name is the view function name — use it as operationId
                        "operationId": f"{rule.endpoint}_{method.lower()}",
                        "parameters": parameters,
                        "responses": {
                            "200": yaml_data.get(
                                "200", {"description": "Successful Response"}
                            )
                        },
                    }
                    
                    if method in {"POST","PUT","PATCH"}:
                        operation["requestBody"] = {
                            "required": method in {"POST", "PUT", "PATCH"},
                            "description": yaml_data.get("description", ""),
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": properties,
                                    }
                                }
                            },
                        }

                    paths[openapi_path][method.lower()] = operation

        return paths
