from metext.plugin_base import BaseValidator
import requests
import xml.etree.ElementTree as ET

# Helper methods slightly modified from https://github.com/khimsh/is_isbn


def check_isbn_via_oclc(isbn):
    resp = requests.get(
        r"http://classify.oclc.org/classify2/Classify?isbn={}&summary=true".format(isbn)
    )
    if resp.status_code != 200:
        return False
    x = ET.fromstring(resp.content)
    c = x.find("{http://classify.oclc.org}response")
    cc = c.get("code")
    return cc == "0"


def is_isbn(isbn: str) -> bool:
    """Check if a given ISBN is valid.

    :param isbn: String of length 10 or 13
    :return: True if isbn is valid, else False
    """
    if not isinstance(isbn, str):
        try:
            isbn = str(isbn)
        except:
            return False

    # Clean the test string of any delimiters, typos or spaces if they exist.
    isbn = "".join(filter(lambda x: x.isdigit() or x in ["x", "X"], isbn))

    # ISBN must be either 10 or 13 characters long
    if len(isbn) not in [10, 13]:
        return False

    if len(isbn) == 10:
        return check_isbn_10(isbn)
    return check_isbn_13(isbn)


def check_isbn_10(isbn: str) -> bool:
    sum_ = sum(
        (index + 1) * (int(value) if value not in ["x", "X"] else 10)
        for index, value in enumerate(isbn[::-1])
    )
    return sum_ % 11 == 0


def check_isbn_13(isbn: str) -> bool:
    sum_ = sum(
        int(value) * 3 if (index + 1) % 2 == 0 else int(value)
        for index, value in enumerate(isbn[::-1])
    )
    return sum_ % 10 == 0


class IsbnValidator(BaseValidator):
    PLUGIN_NAME = "isbn"

    @classmethod
    def run(cls, _input, **kwargs) -> bool:
        """Checks that the input string is a valid ISBN-10
        or ISBN-13 identifier.

        Input string should include only the identifier digits (with delimiters).

        :param _input: ISBN string to check
        :param kwargs:
        :return: True if input string is a ISBN-10 or ISBN-13 identifier,
        else False
        """
        isbn = _input.split(":")[-1]
        return is_isbn(isbn) and check_isbn_via_oclc(isbn)
