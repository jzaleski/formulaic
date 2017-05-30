from .attributes import Attribute
from .types import Type


class Model(object):
    """
    Class representing a "Model"

    Class Attributes:
        attribute_metadata (lazy-dict, stored as `_attribute_metadata`): the
            `Attribute` meta-data `dict`

    Instance Attributes:
        attribute_data (lazy-dict, stored as `_attribute_data`): the `Attribute`
            data `dict`
    """
    def __init__(
        self,
        *args,
        **kwargs
    ):
        """
        Set attributes on the instance based on `kwargs` or `args[0]` if it is a
        `dict` instance
        """
        # support both a positional argument of a `dict`, as well as keyword
        # arguments
        data = args[0] if args and isinstance(args[0], dict) else kwargs

        # ensure that only mapped-attributes are set
        for attribute_name, attribute in self.attribute_metadata.items():
            if attribute_name in data:
                setattr(
                    self,
                    attribute_name,
                    data[attribute_name]
                )

    @property
    def attribute_data(self):
        """
        Lazy load and return the `Attribute` data `dict`

        Returns:
            dict: the `Attribute` data `dict` (keyed by `name`)
        """
        if not hasattr(self, '_attribute_data'):
            self.__dict__['_attribute_data'] = {
                attribute_name: attribute.default()
                for attribute_name, attribute in self.attribute_metadata.items()
            }
        return self._attribute_data

    @property
    def attribute_metadata(self):
        """
        Lazy load and return the `Attribute` meta-data `dict`

        Returns:
            dict: the `Attribute` meta-data (keyed by `name`)
        """
        cls = type(self)
        if not hasattr(cls, '_attribute_metadata'):
            cls._attribute_metadata = {
                attribute_name: attribute
                for attribute_name, attribute in cls.__dict__.items()
                if isinstance(attribute, Attribute)
            }
        return cls._attribute_metadata

    def __setattr__(
        self,
        attribute_name,
        attribute_value
    ):
        """
        Set an attribute on the instance. This is called during `__init__` for
        each of the `kwargs`, as well as when a attribute value is set/updated
        after instantiation. This method formats the input and stores the
        resulting value

        Args:
            attribute_name (str): the attribute-name
            attribute_value (mixed): the attribute-value

        Raises:
            AttributeError: if the `Attribute` does not exist
            ValueError: if the `attribute_value` could not be formatted or is
                invalid
        """
        attribute = self.attribute_metadata.get(attribute_name)
        if not attribute:
            raise AttributeError('Attribute: `{}` does not exist'.format(
                attribute_name))
        formatted_attribute_value = attribute.format(attribute_value)
        if not attribute.validate(formatted_attribute_value):
            raise ValueError('Invalid value: {} for attribute: {}'.format(
                attribute_value, attribute_name))
        self.attribute_data[attribute_name] = formatted_attribute_value

    def validate(self):
        """
        Validate the `Model`

        Returns:
            bool: the result
        """
        return all(
            attribute.validate(self.attribute_data[attribute_name])
            for attribute_name, attribute in self.attribute_metadata.items()
        )
