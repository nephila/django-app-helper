# -*- coding: utf-8 -*-
def load_from_file(module_path):
    """
    Load a python module from its absolute filesystem path

    Borrowed from django-cms
    """
    from imp import load_module, PY_SOURCE

    imported = None
    if module_path:
        with open(module_path, 'r') as openfile:
            imported = load_module("mod", openfile, module_path,
                                   ('imported', 'r', PY_SOURCE))
    return imported
