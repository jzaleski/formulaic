import re

from .types import Type


class Validator(object):
    """
    Class providing methods for validating input (validation occurs when an
    attribute is set on a `Model` instance)
    """
    VALID_UUID_FORMAT = \
        r'[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}'

    @classmethod
    def boolean(cls, value):
        """Validate a `bool[ean]` value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        return isinstance(value, Type.BOOLEAN)

    @classmethod
    def dictionary(cls, value):
        """Validate a `dict[ionary]` value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        return isinstance(value, Type.DICTIONARY)

    @classmethod
    def float(cls, value):
        """Validate a `float` value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        return isinstance(value, Type.FLOAT)

    @classmethod
    def integer(cls, value):
        """Validate an `int[eger]` value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        return isinstance(value, Type.INTEGER)

    @classmethod
    def list(cls, value):
        """Validate a `list` value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        return isinstance(value, Type.LIST)

    @classmethod
    def long(cls, value):
        """Validate a `long` value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        return isinstance(value, Type.LONG)

    @classmethod
    def string(cls, value):
        """Validate a `str[ing]` value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        return isinstance(value, Type.STRING)

    @classmethod
    def text(cls, value):
        """Validate a `text` value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        return isinstance(value, Type.TEXT)

    @classmethod
    def uuid(cls, value):
        """Validate a UUID value

        Parameters:
            value (mixed): the value

        Returns:
            bool: the result
        """
        if not isinstance(value, Type.UUID):
            return False
        match = re.match(cls.VALID_UUID_FORMAT, value)
        return match and match.group() == value
