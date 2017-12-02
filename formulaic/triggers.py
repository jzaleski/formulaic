__all__ = ('Trigger',)


class Trigger(object):
    """
    Class representing hooks/handlers to be "triggered" based on one or more
    `Attribute` value(s) being set/updated

    Instance Attributes:
        attribute_names (set of str): the attribute-names upon which the
            `Trigger` is based
        handler (callable): the handler instance
    """
    def __init__(
        self,
        attribute_names,
        handler
    ):
        assert(attribute_names)
        self.attribute_names = frozenset(attribute_names)
        assert(handler)
        self.handler = handler

    def trigger(
        self,
        old_attribute_value,
        new_attribute_value,
        model
    ):
        """
        Run the `handler` (callback) for the specified `old_value`, `new_value`
        and `attributes`

        Args:
            old_attribute_value (mixed): the old-value of the `Attribute` that
                caused the `Trigger` to fire
            new_attribute_value (mixed): the new-value of the `Attribute` that
                caused the `Trigger` to fire
            model (Model): the `Model` instance on which the trigger was fired

        Returns:
            bool: the result
        """
        return self.handler(
            old_attribute_value,
            new_attribute_value,
            model
        )
