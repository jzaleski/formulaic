try:
    import sqlite3
except:
    sqlite3 = None


class Persistor(object):
    """
    Class providing methods for persisting input (persistence occurs when the
    `persist` method is called on a `Model` instance)
    """
    def persist(self, attributes):
        """
        Persist the specified `attributes`

        Args:
            attributes (dict): the attributes

        Returns:
            bool: the result

        Raises:
            NotImplementedError: if this method is not overridden by an
                inheriting class
        """
        raise NotImplementedError


class SQLPersistor(Persistor):
    """
    Class providing methods for persisting input to a SQL DB (persistence occurs
    when the `persist` method is called on a `Model` instance)

    Instance Attributes:
        table_name (str): the table name
        key_attribute_names (set of str): the key-attribute names (in the future
            complex keys will likely be supported, for now only simple/singular
            keys are supported)
    """
    def __init__(
        self,
        table_name,
        key_attribute_name=None,
    ):
        self.table_name = table_name
        self.key_attribute_names = frozenset([key_attribute_name]) if \
            key_attribute_name else frozenset()

    @property
    def connection(self):
        """
        Lazy-load and return the "Connection" instance

        Returns:
            mixed: the instantiated/connected "Connection" instance

        Raises:
            NotImplementedError: if the `_connect` method is not overridden by
                an inheriting class
        """
        if not hasattr(self, '_connection'):
            self._connection = self._connect()
        return self._connection

    def persist(self, attributes):
        """
        Persist the specified `attributes`

        Args:
            attributes (dict): the attributes

        Returns:
            mixed: the mapped INSERT/UPDATE result

        Raises:
            RuntimeError: if a dependency could not be loaded or a connection to
                DB could not be established
        """
        key_attributes, non_key_attributes = \
            self._partition_attributes(attributes)
        if key_attributes and all(key_attributes.values()):
            return self._update(key_attributes, non_key_attributes)
        return self._insert(non_key_attributes)

    def _column_name(self, attribute_name):
        """
        Convert an attribute-name to a column-name

        Args:
            attribute_name (str): the attribute-name

        Returns:
            str: the column-name
        """
        return ''.join(
            str.capitalize(attribute_name_part)
            for attribute_name_part in attribute_name.split('_')
        )

    def _column_value(self, attribute_value):
        """
        Sanitize and quote an attribute-value

        Args:
            attribute_value (mixed): the attribute-value

        Returns:
            str: the sanitized and quoted attribute-value
        """
        return "'%s'" % attribute_value if attribute_value is not None else \
            'NULL'

    def _connect(self):
        """
        Establish a new connection to a DB

        Returns:
            mixed: the new connection instance

        Raises:
            NotImplementedError: if this method is not overridden by an
                inheriting class
        """
        raise NotImplementedError

    def _insert(self, non_key_attributes):
        """
        Perform an INSERT operation based on the specified `non_key_attributes`

        Args:
            non_key_attributes (dict): the non-key-attributes

        Returns:
            mixed: the mapped INSERT result
        """
        return self._map_insert_result(self.connection.execute(self._insert_sql(
            non_key_attributes)))

    def _insert_sql(self, non_key_attributes):
        """
        Generate the SQL required for an INSERT operation based on the specified
        `non_key_attributes`

        Args:
            non_key_attributes (dict): the non-key-attributes

        Returns:
            str: the SQL string
        """
        return 'INSERT INTO %s (%s) VALUES (%s)' % (
            self.table_name,
            ', '.join(
                self._column_name(attribute_name)
                for attribute_name in non_key_attributes.keys()
            ),
            ', '.join(
                self._column_value(attribute_value)
                for attribute_value in non_key_attributes.values()
            ),
        )

    def _map_insert_result(self, result):
        """
        Map the result from an INSERT operation

        Args:
            result (mixed): the unmapped INSERT result

        Returns:
            mixed: the mapped INSERT result
        """
        return result

    def _map_update_result(self, result):
        """
        Map the result from an UPDATE operation

        Args:
            result (mixed): the unmapped UPDATE result

        Returns:
            mixed: the mapped UPDATE result
        """
        return result

    def _partition_attributes(self, attributes):
        """
        Partition the specified `attributes` into two `dict(s)`, one of the
        `key_attributes` and another of the `non_key_attributes`

        Args:
            attributes (dict): the attributes

        Returns:
            tuple (of dicts): a `tuple` of the `key_attributes` and
                `non_key_attributes`
        """
        key_attributes, non_key_attributes = {}, {}
        key_attribute_names = self.key_attribute_names
        for attribute_name, attribute_value in attributes.items():
            if attribute_name in key_attribute_names:
                key_attributes[attribute_name] = attribute_value
            else:
                non_key_attributes[attribute_name] = attribute_value
        return (key_attributes, non_key_attributes)

    def _update(
        self,
        key_attributes,
        non_key_attributes
    ):
        """
        Perform an UPDATE operation based on the specified `key_attributes` and
        `non_key_attributes`

        Args:
            key_attributes (dict): the key-attributes
            non_key_attributes (dict): the non-key-attributes

        Returns:
            mixed: the mapped UPDATE result
        """
        return self._map_update_result(self.connection.execute(self._update_sql(
            key_attributes, non_key_attributes)))

    def _update_sql(
        self,
        key_attributes,
        non_key_attributes
    ):
        """
        Generate the SQL required for an UPDATE operation based on the specified
        `key_attributes` and `non_key_attributes`

        Args:
            key_attributes (dict): the key-attributes
            non_key_attributes (dict): the non-key-attributes

        Returns:
            str: the SQL string
        """
        return 'UPDATE %s SET %s WHERE %s' % (
            self.table_name,
            ', '.join(
                '%s = %s' % (self._column_name(attribute_name),
                    self._column_value(attribute_value))
                for attribute_name, attribute_value in
                    non_key_attributes.items()
            ),
            ' AND '.join(
                '%s = %s' % (self._column_name(attribute_name),
                    self._column_value(attribute_value))
                for attribute_name, attribute_value in
                    key_attributes.items()
            )
        )


class SQLitePersistor(SQLPersistor):
    """
    Class providing methods for persisting input to a SQLite DB (persistence
    occurs when the `persist` method is called on a `Model` instance)

    Instance Attributes:
        database_file_path (str): the database file-path
        table_name (str): the table name
        key_attribute_names (set of str): the key-attribute names (in the future
            complex keys will likely be supported, for now only simple/singular
            keys are supported)
    """
    def __init__(
        self,
        database_file_path,
        table_name,
        key_attribute_name=None
    ):
        super(SQLitePersistor, self).__init__(table_name, key_attribute_name)
        self.database_file_path = database_file_path

    def _connect(self):
        """
        Establish a new connection to a SQLite DB

        Returns:
            sqlite3.Connection: the new connection instance

        Raises:
            RuntimeError: if the `sqlite3` library was not successfully loaded
        """
        if sqlite3 is None:
            raise RuntimeError
        return sqlite3.connect(self.database_file_path)

    def _map_insert_result(self, result):
        """
        Map the result from an INSERT operation

        Args:
            result (mixed): the unmapped INSERT result

        Returns:
            mixed: the mapped INSERT result
        """
        return {next(iter(self.key_attribute_names)): result.lastrowid}

    def _map_update_result(self, result):
        """
        Map the result from an UPDATE operation

        Args:
            result (mixed): the unmapped UPDATE result

        Returns:
            mixed: the mapped UPDATE result
        """
        return {next(iter(self.key_attribute_names)): result.lastrowid}
