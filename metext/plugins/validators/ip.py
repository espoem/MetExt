import ipaddress

from metext.plugin_base import BaseValidator


class IPv4AddressValidator(BaseValidator):
    PLUGIN_NAME = "ipv4"

    @classmethod
    def run(cls, _input: str, *args, **kwargs) -> bool:
        """Checks that _input is a valid IPv4 address string

        :param _input:
        :param args:
        :param kwargs:
        :return: True if _input is a valid IPv4 address string
        """
        try:
            ipaddress.IPv4Address(_input)
            return True
        except:
            return False


class IPv6AddressValidator(BaseValidator):
    PLUGIN_NAME = "ipv6"

    @classmethod
    def run(cls, _input, *args, **kwargs) -> bool:
        """Checks that _input is a valid IPv6 address string

        :param _input:
        :param args:
        :param kwargs:
        :return: True if _input is a valid IPv6 address string
        """
        try:
            ipaddress.IPv6Address(_input)
            return True
        except:
            return False
