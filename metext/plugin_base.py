from typing import Union


class RegisteredPluginMetaClass(type):
    REGISTERED = {}

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        if cls.PLUGIN_TYPE and cls.PLUGIN_NAME:
            current_types_plugins = cls.REGISTERED.get(cls.PLUGIN_TYPE, [])
            if cls.PLUGIN_NAME not in {n.PLUGIN_NAME for n in current_types_plugins}:
                current_types_plugins.append(cls)
                cls.REGISTERED[cls.PLUGIN_TYPE] = current_types_plugins


class PluginBase(metaclass=RegisteredPluginMetaClass):
    """Base abstract class for new plugin types.

    New plugins can be registered and known as available if they have non-empty
    `PLUGIN_TYPE`, `PLUGIN_NAME`.

    Pairs of (PLUGIN_TYPE, PLUGIN_NAME) should be unique to each of the plugins,
    i.e. no two plugins with the same pair (PLUGIN_TYPE, PLUGIN_NAME) can be registered.

    """

    PLUGIN_TYPE = ""
    PLUGIN_NAME = ""
    PLUGIN_DESCRIPTION = ""
    PLUGIN_ACTIVE = True

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, "run") and callable(subclass.run)

    @classmethod
    def get_plugins(cls) -> list:
        """Gets a list of registered plugins with type `PLUGIN_TYPE` with non-empty name `PLUGIN_NAME`

        :return: List of registered plugins
        """
        if cls.PLUGIN_TYPE not in cls.REGISTERED.keys():
            return []
        return [
            plug
            for plug in cls.REGISTERED[cls.PLUGIN_TYPE]
            if issubclass(plug, cls) and plug.PLUGIN_NAME != ""
        ]

    @classmethod
    def get_active_plugins(cls) -> list:
        """Gets a list of registered plugins with type `PLUGIN_TYPE` with non-empty name `PLUGIN_NAME`
        and with `PLUGIN_ACTIVE` set to True

        :return: List of registered and active plugins
        """
        return [plug for plug in cls.get_plugins() if plug.PLUGIN_ACTIVE is True]

    @classmethod
    def run(cls, _input, **kwargs):
        raise NotImplementedError("Must implement in subclass")


Decodable = Union[bytes, str]


class BaseDecoder(PluginBase):
    PLUGIN_TYPE = "Decoder"


class BaseExtractor(PluginBase):
    PLUGIN_TYPE = "Extractor"


class BaseValidator(PluginBase):
    PLUGIN_TYPE = "Validator"


class BasePrinter(PluginBase):
    PLUGIN_TYPE = "Printer"


# noinspection PyUnresolvedReferences
import metext.plugins
