from .types import Type


class Attribute(object):
    """
    Class representing an "Attribute" of a "Model"

    Instance Attributes:
        default (mixed): default value for the `Attribute`
        formatter (callable): formatter method for the `Attribute`. This is
            called when setting the `Attribute` value via on the `Model`. If the
            `Attribute` expects a `list` value this method will be mapped to
            each item
        required (bool): if the `Attribute` is required
        type: the type of the `Attribute`. This value should be one of the
            constants from `Type`
        validator (callable): validator method for the `Attribute`. This is
            called by the `validate` method on the `Model` and should return
            `True` or `False` depending on the validity of the provided `value`.
            If the `Attribute` expects a `list` value, this method will be
            mapped to each item
    """
    def __init__(self, **kwargs):
        default = kwargs.get('default')
        self.default = default if callable(default) else lambda: default
        formatter = kwargs.get('formatter')
        self.formatter = formatter if callable(formatter) else lambda value: \
            value
        self.required = kwargs.get('required') or False
        self.type = kwargs.get('type')
        validator = kwargs.get('validator')
        self.validator = validator if callable(validator) else lambda value: \
            True

    def format(self, value):
        """
        Format the specified `value` based on the `Attribute` configuration

        Args:
            value (mixed): the [attribute-]value

        Returns:
            mixed: the formatted [attribute-]value (or `None` if the specified
                `value` was `None`)

        Raises:
            ValueError: if the specified `value` could not be formatted
        """
        if value is None:
            return None
        if self.type == Type.LIST and isinstance(value, Type.LIST):
            return list(map(self.formatter, value))
        return self.formatter(value)

    def validate(self, value):
        """
        Validate the specified `value` based on the `Attribute` configuration

        Args:
            value (mixed): the [attribute-]value

        Returns:
            bool: the result
        """
        if self.required and not value:
            return False
        if not value:
            return True
        if self.type == Type.LIST and isinstance(value, Type.LIST):
            return all(map(self.validator, value))
        return self.validator(value)
