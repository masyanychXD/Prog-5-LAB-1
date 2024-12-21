import sys
import importlib.abc
import importlib.util
import requests

class URLLoader(importlib.abc.Loader):
    def __init__(self, base_url):
        self.base_url = base_url

    def load_module(self, fullname):
        url = f"{self.base_url}/{fullname}.py"
        try:
            response = requests.get(url)
            response.raise_for_status()
            code = response.text
        except requests.RequestException as e:
            raise ImportError(f"Could not load module {fullname}: {e}")
        module = importlib.util.module_from_spec(self.create_spec(fullname))
        exec(code, module.__dict__)
        sys.modules[fullname] = module
        return module

    def create_spec(self, fullname):
        return importlib.util.spec_from_loader(fullname, self)

def url_hook(path):
    if path.startswith("http://") or path.startswith("https://"):
        return URLLoader(path)
    else:
        raise ImportError("Not a URL path")

sys.path_hooks.append(url_hook)
