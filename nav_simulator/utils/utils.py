import importlib
def str_to_class(modulename, classname):
    return getattr(importlib.import_module(modulename), classname)