import yaml

class YAMLExtractor:
    
    def __init__(self, yaml_file_path: str):
        self.yaml_file_path = yaml_file_path
    
    
    def _extract(self) -> dict:
        """
        Reads the OpenAPI YAML file and returns its contents as a dictionary.
        """
        if not self.yaml_file_path:
            print("No YAML file path provided or file not found. Returning empty dict.")
            return {}
        with open(self.yaml_file_path, 'r') as file:
            return yaml.safe_load(file)
        
    def extract_function_data(self,module_name: str, function_name: str) -> dict:
        """
        Extracts the '<function_name>' section from the YAML file, if it exists.
        Returns a dictionary of parameters or an empty dictionary if not found.
        
        Extractables:
        - name
        - description
        - method
        - parameters_type
        - parameters
        - 200
        """
        yaml_data = self._extract()
        if not yaml_data:
            print("YAML data is empty. Returning empty parameters list.")
            return {}
        
        yaml_function_data = yaml_data.get(module_name, {}).get(function_name, {})
        
        if not yaml_function_data:
            print(f"No YAML data found for module '{module_name}' and function '{function_name}'. Returning empty parameters list.")
            return {}
        
        return yaml_function_data or {} 