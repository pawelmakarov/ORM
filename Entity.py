import sqlite3

class Entity(object):
    def __init__(self, entity_id=None):
        print '__init__'
        self.entity_id = entity_id
        self.table_name = self.__class__.__name__.lower()
        
        self.connection = sqlite3.connect('my_sqlite.db')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.__fields = []
        self.data_map = {}

    def __getattr__(self, rows):
        # print rows
        if not self.__fields:
            self.__fields = self.get_values()

        if rows in self._fields:
            key = '{0}_{1}'.format(self.table_name, rows)
            return self.__fields[key]

        if rows in self._parents:
            class_name = rows.title()
            new_class = self.get_new_class(class_name)
            parent_id = '{0}_id'.format(rows)
            return new_class(self.__fields[parent_id])

        if rows in self._children:
            class_name = self.get_class_name(rows)
            lst_children = self.get_children(rows[:-1])
            return self.get_list_classes(lst_children, class_name)

        if rows in self._siblings:
            class_name = self.get_class_name(rows)
            lst_siblings = self.get_siblings(rows[:-1])
            return self.get_list_classes(lst_siblings, class_name)
        raise AttributeError()

    def __setattr__(self, key, value):
        print '{} {}'.format(key, value)
        if key in self._fields:
            self.data_map[key] = value

        if key in self._parents:
            if type(value) is int:
                self.data_map[key] = value
            else:
                self.data_map[key] = value.entity_id
        super(Entity, self).__setattr__(key, value)

    def get_values(self):
        statement = 'SELECT * FROM \'{0}\' WHERE {0}_id=?'.format(self.table_name)
        self.cursor.execute(statement, (self.entity_id,))
        return self.cursor.fetchone()

    def get_children(self, parent):
        statement = 'SELECT * FROM \'{0}\' WHERE {1}_id=?'.format(parent, self.table_name)
        self.cursor.execute(statement, (self.entity_id,))
        return self.cursor.fetchall()

    def get_siblings(self, sibling):
        join_column = self.get_join_column(sibling)

        statement = ('SELECT * FROM {0} natural join {1} WHERE {2}_id=?'
                    .format(sibling, join_column, self.table_name))
        self.cursor.execute(statement, (self.entity_id,))
        return self.cursor.fetchall()

    def get_join_column(self, sibling):
        join_columns = [self.table_name, sibling]
        join_columns = sorted(join_columns)
        join_column = ('{0}'.format(column) for column in join_columns)
        join_column = '_'.join(join_column)
        return join_column

    def get_new_class(self, name):
        import models
        return getattr(models, name)

    def get_class_name(self, name):
        return name.title()[:-1]

    @classmethod
    def all(cls):
        import models
        class_name_db = cls.__name__.lower()
        statement = 'SELECT * FROM {0}'.format(class_name_db)
        connection = sqlite3.connect('my_sqlite.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(statement)
        list_rows = cursor.fetchall()
        list_classes = []

        for row in list_rows:
            new_class = getattr(models, cls.__name__)
            mapping_field = '{0}_id'.format(class_name_db)
            mapping_field = row[mapping_field]
            list_classes.append(new_class(mapping_field))
        return list_classes

    def get_all(self, class_name):
        statement = 'SELECT * FROM {0}'.format(class_name)
        self.cursor.execute(statement)
        return self.cursor.fetchall()

    def save(self):
        if self.entity_id is None:
            statement = self.get_query_to_insert()
            self.cursor.executemany(statement, (self.data_map.values(),))
            self.entity_id = self.cursor.lastrowid
        else:
            statement = self.get_query_to_update()
            values = (self.data_map.values())
            values.append(self.entity_id)
            self.cursor.executemany(statement, (values,))

    def get_list_classes(self, list_objects, class_name):
        list_classes = []

        for class_object in list_objects:
            new_class = self.get_new_class(class_name)
            mapping_field = class_object['article_id']
            list_classes.append(new_class(mapping_field))
        return list_classes

    def get_query_to_update(self):
        fields = ('{0}_{1} = ?'.format(self.table_name, column_name) 
            for column_name in self.data_map.keys())
        fields = ', '.join(fields)

        for key in self.data_map.keys():
            if key in self._parents:
                fields = ('{0}_id = ?'.format(column_name) 
                    for column_name in self.data_map.keys())
                fields = ', '.join(fields)

        statement = ('UPDATE \'{0}\' SET {1} WHERE {0}_id = ?'
            .format(self.table_name, fields))
        return statement

    def get_query_to_insert(self):
        columns = ('{0}_{1}'.format(self.table_name, column_name) 
            for column_name in self.data_map.keys())
        columns = ', '.join(columns)

        prepared_statement = self.get_prepared_statement_to_insert()
        statement = ('INSERT INTO \'{0}\' ({1}) VALUES ({2})'
            .format(self.table_name, columns, prepared_statement))
        return statement

    def get_prepared_statement_to_insert(self):
        prepared_statement = ('?' for i in self.data_map.items())
        prepared_statement  = ', '.join(prepared_statement)
        print prepared_statement
        return prepared_statement

    def delete(self):
        if self.entity_id is None:
            raise ValueError()
        statement = 'DELETE FROM \'{0}\' WHERE {0}_id = ?'.format(self.table_name)
        self.cursor.execute(statement, (self.entity_id,))

    def __del__(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        