__all__ = ('Formatter',)


import six


class Formatter(object):
    """
    Class providing methods for formatting input (formatting occurs when an
    attribute is about to be set via a `Model` instance)
    """
    @classmethod
    def boolean(cls, value):
        """Cast a value as a `bool[ean]`

        Parameters:
            value (mixed): the value

        Returns:
            bool: the casted result
        """
        return bool(value)

    @classmethod
    def float(cls, value):
        """Cast a value as a `float`

        Parameters:
            value (mixed): the value

        Returns:
            float: the casted result

        Raises:
            ValueError: if `value` could not be casted
        """
        try:
            return float(value)
        except:
            raise ValueError('Could not convert: {} to a float value'.format(
                value))

    @classmethod
    def lower(cls, value):
        """Lowercase a value

        Parameters:
            value (mixed): the value

        Returns:
            str/unicode: the lowercased value

        Raises:
            ValueError: if `value` could not be lowercased or is an invalid
                `type`
        """
        try:
            return value.lower()
        except:
            raise ValueError('Could not lowercase value: {}'.format(value))

    @classmethod
    def integer(cls, value):
        """Cast a value as an `int[eger]`

        Parameters:
            value (mixed): the value

        Returns:
            int: the casted result

        Raises:
            ValueError: if `value` could not be casted
        """
        try:
            return int(value)
        except:
            raise ValueError('Could not convert: {} to an integer value'.format(
                value))

    @classmethod
    def long(cls, value):
        """Cast a value as a `long`

        Parameters:
            value (mixed): the value

        Returns:
            int/long: the casted result

        Raises:
            ValueError: if `value` could not be casted
        """
        try:
            return (int if six.PY3 else long)(value)
        except:
            raise ValueError('Could not convert: {} to an long value'.format(
                value))

    @classmethod
    def string(cls, value):
        """Cast a value as a `str[ing]`

        Parameters:
            value (mixed): the value

        Returns:
            str: the casted result
        """
        return str(value)

    @classmethod
    def text(cls, value):
        """Cast a value as `text`

        Parameters:
            value (mixed): the value

        Returns:
            str/unicode: the casted result
        """
        return (str if six.PY3 else unicode)(value)

    @classmethod
    def upper(cls, value):
        """Uppercase a value

        Parameters:
            value (mixed): the value

        Returns:
            str/unicode: the uppercased value

        Raises:
            ValueError: if `value` could not be uppercased or is an invalid
                `type`
        """
        try:
            return value.upper()
        except:
            raise ValueError('Could not uppercase value: {}'.format(value))
