class Generator(object):
    def __init__(self):
        self.tables = []
        self.alters = []
        self.triggers = []

    def write_to_file(self, output_file):
        with open(output_file, 'w') as sql_file:
            sql_file.write('{0}{1}'.format('\n'.join(table for table in self.tables), '\n'))
            sql_file.write('{0}{1}'.format('\n'.join(alter for alter in self.alters), '\n'))
            sql_file.write('{0}{1}'.format('\n'.join(trigger for trigger in self.triggers), '\n'))

    def read_from_file(self, input_file):
        import yaml
        with open(input_file, 'r') as stream:
            return yaml.safe_load(stream)

    def get_fields(self, table, structure):
        fields = ("\'{0}_{1}\' {2}".format(table, column_name, column_type) 
            for column_name, column_type in structure['fields'].items())
        fields = ', '.join(fields)
        return fields

    def create_table(self, name, fields):
        create_table = ('CREATE TABLE \'{0}\' (\n\t\'{0}_id\' SERIAL PRIMARY KEY,\n\t{1}\n\t\'{0}_created\''
            'INTEGER NOT NULL DEFAULT cast(extract(epoch from now()) AS INTEGER),\n\t\'{0}_updated\''
            'INTEGER NOT NULL DEFAULT 0\n\t);\n'
            .format(name, fields))
        return create_table

    def alter_table(self, table, related_table):
        alter_table = ('ALTER TABLE \'{0}\' ADD \'{1}_id\' INTEGER NOT NULL,\n\t'
            'ADD CONSTRAINT \'fk_{0}_{1}_id\' FOREIGN KEY (\'{1}_id\')'
            'REFERENCES \'{1}\' (\'{1}_id\');\n'
            .format(table, related_table))
        return alter_table

    def join_table(self, table, related_table):
        join_table = ('CREATE TABLE \'{0}__{1}\' (\n\t\'{0}_id\' INTEGER NOT NULL,\n\t\'{1}_id\''
            'INTEGER NOT NULL,\n\tPRIMARY KEY (\'{0}_{1}\', \'{1}_id\')\n);\n'
            .format(table, related_table))
        return join_table

    def get_function(self, table):
        function = ('CREATE OR REPLACE FUNCTION update_{0}_timestamp()\nRETURNS TRIGGER AS '
            '$$\nBEGIN\n\tNEW.{0}_updated = cast(extract(epoch from now()) as integer);\n\t'
            'RETURN NEW;\nEND;\n$$ language \'plpgsql\';\n'
            .format(table))
        return function

    def get_trigger(self, table):
        trigger = ('CREATE TRIGGER \'tr_{0}_updated\' BEFORE UPDATE ON \'{0}\''
            'FOR EACH ROW EXECUTE PROCEDURE\n\t update_{0}_timestamp();\n'
            .format(table))
        return trigger

    def set_tables(self, statements):
        self.tables.append(statements)
    
    def set_alters(self, statements):
        self.alters.append(statements)
    
    def set_triggers(self, statements):
        self.triggers.append(statements)

    def create_statements(self, input_file, output_file):
        data_map = self.read_from_file(input_file)
        statements = []

        for table, structure in data_map.items():
            table = table.lower()
            fields = self.get_fields(table, structure)

            for related_table, relations_type in structure['relations'].items():
                self.set_tables(self.create_table(table, fields))
                relations_status = data_map[related_table]['relations'].values()[0];
                related_table = related_table.lower()

                if relations_type == 'one' and relations_status == 'many':
                    self.set_alters(self.alter_table(table, related_table))

                if relations_type == relations_status:
                    self.set_tables(self.join_table(table, related_table))
                    join_table = '{0}__{1}'.format(table, related_table)
                    self.set_alters(self.alter_table(join_table, table))
                    self.set_alters(self.alter_table(join_table, related_table))
            
            self.set_triggers(self.get_function(table))
            self.set_triggers(self.get_trigger(table))
        self.write_to_file(output_file)

if __name__ == '__main__':
    Generator().create_statements('many_to_many.yaml', 'schema.sql')
