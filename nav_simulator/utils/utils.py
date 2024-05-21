import importlib
def str_to_class(modulename, classname):
    return getattr(importlib.import_module(modulename), classname)

def next_even_number(number):
    if number % 2 == 0:
        return number + 0
    else:
        return number + 1