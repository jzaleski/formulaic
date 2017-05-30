import six


class Type(object):
    """
    Class providing type-mapping constants

    Class Attributes:
        BOOLEAN (callable): the `bool[ean]` type-mapping
        DICTIONARY (callable): the `dict` type-mapping
        FLOAT (callable): the `float` type-mapping
        INTEGER (callable): the `int[eger] type-mapping
        LONG (callable): the `long` type-mapping
        STRING (callable): the `str[ing]` type-mapping
        TEXT (callable): the `text` type-mapping
        UUID (callable): the `uuid` type-mapping
    """
    BOOLEAN = bool
    DICTIONARY = dict
    FLOAT = float
    INTEGER = six.integer_types
    LIST = list
    LONG = int if six.PY3 else long
    STRING = six.string_types
    TEXT = six.text_type
    UUID = six.string_types
