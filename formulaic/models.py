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
        Set attributes on the instance based on `args[0]` if it's a `dict` or
        `kwargs`

        Args:
            *args (list): the positional arguments
            **kwargs (dict): the keyword arguments

        Raises:
            ValueError: if any `attribute_value` could not be formatted or is
                invalid
        """
        # store the `Persistor` instance on the `Model`. If one is not provided,
        # and `persist` is called, a `NotImplementedError` will be raised
        self.persistor = kwargs.pop('persistor', None)

        # support both a [single] positional argument of a `dict`, as well as
        # keyword arguments
        attributes = args[0] if args and isinstance(args[0], dict) else kwargs

        # ensure that only mapped-attributes are set. The `default` value will
        # be returned for any missing/omitted attribute when action is taken on
        # the `Model` (e.g. `persist` or `validate` is called)
        for attribute_name, attribute in self.attribute_metadata.items():
            if attribute_name in attributes:
                setattr(
                    self,
                    attribute_name,
                    attributes[attribute_name]
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
        each of the attributes provided, as well as when a attribute value is
        set/updated after instantiation. This method formats the input,
        validates and stores the resulting value. If the specified
        `attribute_name` does not refer to a mapped `attribute` the `super`
        implementation will be called

        Args:
            attribute_name (str): the attribute-name
            attribute_value (mixed): the attribute-value

        Raises:
            ValueError: if the `attribute_value` could not be formatted or is
                invalid
        """
        attribute = self.attribute_metadata.get(attribute_name)
        if not attribute:
            super(Model, self).__setattr__(attribute_name, attribute_value)
            return
        formatted_attribute_value = attribute.format(attribute_value)
        if not attribute.validate(formatted_attribute_value):
            raise ValueError('Invalid value: {} for attribute: {}'.format(
                attribute_value, attribute_name))
        self.attribute_data[attribute_name] = formatted_attribute_value

    def persist(self):
        """
        Persist the `Model`

        Returns:
            bool: the result

        Raises:
            RuntimeError: if the `Persistor` instance is `None`
        """
        persistor = self.persistor
        if persistor is None:
            raise RuntimeError
        if not self.validate():
            return False
        key_attributes = persistor.persist(self.attribute_data)
        if key_attributes is None:
            return False
        for attribute_name, attribute_value in key_attributes.items():
            self.attribute_data[attribute_name] = attribute_value
        return True

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
