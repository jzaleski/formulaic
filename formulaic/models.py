from .attributes import Attribute
from .triggers import Trigger
from .types import Type


class Model(object):
    """
    Class representing a "Model"

    Class Attributes/Properties:
        attribute_metadata (lazy-dict, stored as `_attribute_metadata`): the
            `Attribute` meta-data `dict`
        trigger_metadata (lazy-dict, stored as `_trigger_metadata`): the
            `Trigger` meta-data `dict`

    Instance Attributes/Properties:
        attribute_data (lazy-dict, stored as `_attribute_data`): the `Attribute`
            data `dict`
        changed_attribute_data (lazy-dict, stored as `_changed_attribute_data`):
            the changed `Attribute` data `dict`
        initialized (bool): the initialization status
        merged_attribute_data (derived-dict): the result of merging the
            `attribute_data` (`dict`) and `changed_attribute_data` (`dict`)
        persistor (Persistor): the `Persistor` instance
        processed_attributes (lazy-set, stored as `_processed_attributes`): the
            attribute-names of the processed `Attribute(s)`
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
        # Set the `initialized` status to `False` as we are currently _still_
        # initializing (this will toggled to `True` at the end of this method)
        self.initialized = False

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

        # Set the `initialized` to `True`, we are done
        self.initialized = True

    @property
    def attribute_data(self):
        """
        Lazy load and return the `Attribute` data `dict`

        Returns:
            dict: the `Attribute` data `dict` (key: `attribute_name`)
        """
        if not hasattr(self, '_attribute_data'):
            self.__dict__['_attribute_data'] = {
                attribute_name: attribute.default()
                for attribute_name, attribute in self.attribute_metadata.items()
            }
        return self._attribute_data

    @attribute_data.setter
    def attribute_data(self, value):
        """
        Set the `Attribute` data `dict`

        Args:
            value (dict): the _new_ `Attribute` data `dict`
        """
        self._attribute_data = value

    @property
    def attribute_metadata(self):
        """
        Lazy load and return the `Attribute` meta-data `dict`

        Returns:
            dict: the `Attribute` meta-data (key: `attribute_name`)
        """
        cls = type(self)
        if not hasattr(cls, '_attribute_metadata'):
            cls._attribute_metadata = {
                attribute_name: attribute
                for attribute_name, attribute in cls.__dict__.items()
                if isinstance(attribute, Attribute)
            }
        return cls._attribute_metadata

    @property
    def changed_attribute_data(self):
        """
        Lazy load and return the changed `Attribute` data `dict`

        Returns:
            dict: the changed `Attribute` data `dict` (key: `attribute_name`)
        """
        if not hasattr(self, '_changed_attribute_data'):
            self._changed_attribute_data = dict()
        return self._changed_attribute_data

    @property
    def initialized(self):
        """
        Get the initialization status

        Returns:
            bool: the initialization status
        """
        return self._initialized

    @initialized.setter
    def initialized(self, value):
        """
        Set the initialization status

        Args:
            value (dict): the _new_ initialization status
        """
        self._initialized = value

    @property
    def merged_attribute_data(self):
        """
        Get the merged `Attribute` data `dict` (this *is not* memoized)

        Returns:
            dict: the merged `Attribute` data `dict` (key: `attribute_name`)
        """
        return dict(self.attribute_data, **self.changed_attribute_data)

    @property
    def persistor(self):
        """
        Get the `Persistor`

        Return:
            Persistor: the `Persistor` instance
        """
        return self._persistor

    @persistor.setter
    def persistor(self, value):
        """
        Set the `Persistor`

        Args:
            value (Persistor): the _new_ `Persistor` [instance]
        """
        self._persistor = value

    @property
    def processed_attributes(self):
        """
        Lazy load and return the processed attribute-names

        Returns:
            set: the processed attribute-names
        """
        if not hasattr(self, '_processed_attributes'):
            self._processed_attributes = set()
        return self._processed_attributes

    @property
    def trigger_metadata(self):
        """
        Lazy load and return the `Trigger` meta-data `dict`

        Returns:
            dict: the `Trigger` meta-data `dict` (key: `attribute_names`)
        """
        cls = type(self)
        if not hasattr(cls, '_trigger_metadata'):
            cls._trigger_metadata = {
                trigger.attribute_names: trigger
                for trigger in cls.__dict__.values()
                if isinstance(trigger, Trigger)
            }
        return cls._trigger_metadata

    def __setattr__(
        self,
        attribute_name,
        attribute_value
    ):
        """
        Set an attribute value on the instance. This is called during `__init__`
        for each of the attributes provided, as well as whenever an attribute
        value is set/updated after instantiation. This method formats the input,
        validates, stores the formatted value and fires any applicable
        `Trigger(s)`. If the specified `attribute_name` does not refer to a
        mapped `attribute` the `super` implementation will be called

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
        new_attribute_value = attribute.format(attribute_value)
        if not attribute.validate(new_attribute_value):
            raise ValueError('Invalid value: {} for attribute: {}'.format(
                attribute_value, attribute_name))
        old_attribute_value = self.changed_attribute_data.get(attribute_name,
            self.attribute_data.get(attribute_name))
        if not self.initialized:
            self.attribute_data[attribute_name] = new_attribute_value
        elif attribute_name not in self.attribute_data or \
            new_attribute_value != old_attribute_value:
            self.changed_attribute_data[attribute_name] = new_attribute_value
        else:
            self.changed_attribute_data.pop(attribute_name, None)
            self.processed_attributes.discard(attribute_name)
            return
        self.processed_attributes.add(attribute_name)
        for attribute_names, trigger in self.trigger_metadata.items():
            if attribute_name in attribute_names and \
                self.processed_attributes >= attribute_names:
                trigger.trigger(
                    old_attribute_value,
                    new_attribute_value,
                    self
                )

    def persist(self):
        """
        Persist the `Model`

        Returns:
            bool: the result

        Raises:
            RuntimeError: if the `Persistor` [instance] is `None`
        """
        persistor = self.persistor
        if persistor is None:
            raise RuntimeError
        if not self.validate():
            return False
        merged_attribute_data = self.merged_attribute_data
        key_attribute_data = persistor.persist(merged_attribute_data)
        if key_attribute_data is None:
            return False
        self.attribute_data = dict(merged_attribute_data, **key_attribute_data)
        self.changed_attribute_data.clear()
        return True

    def validate(self):
        """
        Validate the `Model`

        Returns:
            bool: the result
        """
        merged_attribute_data = self.merged_attribute_data
        return all(
            attribute.validate(merged_attribute_data[attribute_name])
            for attribute_name, attribute in self.attribute_metadata.items()
        )
