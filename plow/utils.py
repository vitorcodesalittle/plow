import os.path


def import_plow_decorated_funcs(path_or_module):
    if os.path.isfile(path_or_module):
        with open(path_or_module, "r") as f:
            script = f.read()
            print("script:")
            print(script)
            exec(script, globals())
    else:
        __import__(path_or_module)
