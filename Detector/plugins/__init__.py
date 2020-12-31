import pkgutil

__all__ = []


def load_plugin_modules(paths):
    """https://geoffsamuel.com/2020/03/31/plugin-class-architecture/

    :param paths:
    :return:
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(paths):
        __all__.append(module_name)
        module = loader.find_module(module_name).load_module(module_name)
        exec("{} = module".format(module_name))


load_plugin_modules(__path__)
