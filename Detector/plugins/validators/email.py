import re

from Detector.plugin_base import BaseValidator
from Detector.utils.uri import addr_spec
from email_validator import validate_email

RE_EMAIL = re.compile(addr_spec, re.VERBOSE)


class EmailValidator(BaseValidator):
    PLUGIN_NAME = "email"

    @classmethod
    def run(cls, _input: str, *args, **kwargs) -> bool:
        """Checks that a string has a valid e-mail address form

        :param _input:
        :param args:
        :param kwargs:
        :return: True if _input has a valid e-mail addresses from
        """
        # return RE_EMAIL.match(_input) is not None # too slow
        try:
            validate_email(_input, check_deliverability=True)
            return True
        except:
            return False
