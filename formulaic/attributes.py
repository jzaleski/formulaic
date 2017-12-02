__all__ = (
    'Attribute',
    'BooleanAttribute',
    'FloatAttribute',
    'IntegerAttribute',
    'LongAttribute',
    'StringAttribute',
    'TextAttribute',
    'UUIDAttribute',
)


from .formatters import Formatter
from .types import Type
from .validators import Validator


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


class BooleanAttribute(Attribute):
    """
    Class representing a "[Boolean]Attribute" of a "Model." This class extends
    the `Attribute` class and applies the default configuration for `formatter`,
    `type` and `validator`
    """
    def __init__(self, **kwargs):
        super(BooleanAttribute, self).__init__(
            **dict(
                kwargs,
                formatter=Formatter.boolean,
                type=Type.BOOLEAN,
                validator=Validator.boolean,
            )
        )


class FloatAttribute(Attribute):
    """
    Class representing a "[Float]Attribute" of a "Model." This class extends the
    `Attribute` class and applies the default configuration for `formatter`,
    `type` and `validator`
    """
    def __init__(self, **kwargs):
        super(FloatAttribute, self).__init__(
            **dict(
                kwargs,
                formatter=Formatter.float,
                type=Type.FLOAT,
                validator=Validator.float,
            )
        )


class IntegerAttribute(Attribute):
    """
    Class representing a "[Integer]Attribute" of a "Model." This class extends
    the `Attribute` class and applies the default configuration for `formatter`,
    `type` and `validator`
    """
    def __init__(self, **kwargs):
        super(IntegerAttribute, self).__init__(
            **dict(
                kwargs,
                formatter=Formatter.integer,
                type=Type.INTEGER,
                validator=Validator.integer,
            )
        )


class LongAttribute(Attribute):
    """
    Class representing a "[Long]Attribute" of a "Model." This class extends the
    `Attribute` class and applies the default configuration for `formatter`,
    `type` and `validator`
    """
    def __init__(self, **kwargs):
        super(LongAttribute, self).__init__(
            **dict(
                kwargs,
                formatter=Formatter.long,
                type=Type.LONG,
                validator=Validator.long,
            )
        )


class StringAttribute(Attribute):
    """
    Class representing a "[String]Attribute" of a "Model." This class extends
    the `Attribute` class and applies the default configuration for `formatter`,
    `type` and `validator`
    """
    def __init__(self, **kwargs):
        super(StringAttribute, self).__init__(
            **dict(
                kwargs,
                formatter=Formatter.string,
                type=Type.STRING,
                validator=Validator.string,
            )
        )


class TextAttribute(Attribute):
    """
    Class representing a "[Text]Attribute" of a "Model." This class extends the
    `Attribute` class and applies the default configuration for `formatter`,
    `type` and `validator`
    """
    def __init__(self, **kwargs):
        super(TextAttribute, self).__init__(
            **dict(
                kwargs,
                formatter=Formatter.text,
                type=Type.TEXT,
                validator=Validator.text,
            )
        )


class UUIDAttribute(Attribute):
    """
    Class representing a "[UUID]Attribute" of a "Model." This class extends the
    `Attribute` class and applies the default configuration for `formatter`,
    `type` and `validator`
    """
    def __init__(self, **kwargs):
        super(UUIDAttribute, self).__init__(
            **dict(
                kwargs,
                formatter=Formatter.uuid,
                type=Type.UUID,
                validator=Validator.uuid,
            )
        )
