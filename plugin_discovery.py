import os
import importlib
import inspect
from module import Module

def plugin_discovery(folder_path = "plugins") -> list:
        plugins = []
        
        if not os.path.isdir(folder_path):
                return plugins
                
        files = os.listdir(folder_path)
        
        for file_name in files:
                
                if not file_name.endswith(".py") or file_name == "__init__.py":
                        continue
                
                module_name = file_name[ : -3]
                try:
                        imported_module = importlib.import_module(f"{folder_path}.{module_name}")
                except ModuleNotFoundError as e:
                        print(f"The {module_name} has issues: {e}")
                        continue
                
                for name, cls in inspect.getmembers(imported_module, inspect.isclass):
                        if issubclass(cls, Module) and cls is not Module:
                                plugins.append(cls)
        return plugins
                        
                
                
                
                                

