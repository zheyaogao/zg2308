import pymysql
import csv
import logging
import DataTableExceptions


class ColumnDefinition:
    """

    Represents a column definition in the CSV Catalog.
    """
    column_types = ("text", "number")
    # Allowed types for a column.
    def __init__(self, column_name, column_type="text", not_null=False):
        self.dic = {"column_name":column_name,
                    "column_type":column_type,
                    "not_null":not_null}
        """

        :param column_name: Cannot be None.
        :param column_type: Must be one of valid column_types.
        :param not_null: True or False
        """

class IndexDefinition:
    """
    Represents the definition of an index.
    """
    index_types = ("PRIMARY", "UNIQUE", "INDEX")

    def __init__(self, index_name, columns, index_type):
        self.dic = {"index_name":index_name,
                    "columns":columns,
                    "kind":index_type}
    """

    :param index_name: Name for index. Must be unique name for table.
    :param index_type: Valid index type.
    """

class TableDefinition:
    """
    Represents the definition of a table in the CSVCatalog.
    """

    def __init__(self, t_name=None, csv_f=None, column_definitions=None, index_definitions={}, cnx=None):


        """
        :param t_name: Name of the table.
        :param csv_f: Full path to a CSV file holding the data.
        :param column_definitions: List of column definitions to use from file. Cannot contain invalid column name.
            May be just a subset of the columns.
        :param index_definitions: List of index definitions. Column names must be valid.
        :param cnx: Database connection to use. If None, create a default connection.
        """
        self.t_name = t_name
        self.csv_f = csv_f
        self.column_definitions = column_definitions
        self.index_definitions = index_definitions
        self.cnx = cnx

    @classmethod
    def load_table_definition(cls, cnx, table_name):
        """

        :param cnx: Connection to use to load definition.
        :param table_name: Name of table to load.
        :return: Table and all sub-data. Read from the database tables holding catalog information.
        """
        cursor=self.cnx.cursor()
        q = "select * from tables where name='"+table_name+"'"
        cursor.execute(q)
        self.dic = cursor.fetchall()

    def add_column_definition(self, c):
        """
        Add a column definition.
        :param c: New column. Cannot be duplicate or column not in the file.
        :return: None
        """
        self.column_definitions+=c.dic

    def drop_column_definition(self, c):
        """
        Remove from definition and catalog tables.
        :param c: Column name (string)
        :return:
        """
        self.column_definitions.remove(c.dic)

    def to_json(self):
        """

        :return: A JSON representation of the table and it's elements.
        """
        pass

    def define_primary_key(self, columns):
        """
        Define (or replace) primary key definition.
        :param columns: List of column values in order.
        :return:
        """
        column_names = [c.dic['column_name'] for c in self.column_definitions]
        for col in columns:
            if col not in column_names:
                raise DataTableExceptions.DataTableException(code=-1000,message='Invalid key columns')

        self.index_definitions['PRIMARY']=IndexDefinition("PRIMARY",columns,"PRIMARY").dic

    def define_index(self, index_name, columns, kind="index"):
        """
        Define or replace and index definition.
        :param index_name: Index name, must be unique within a table.
        :param columns: Valid list of columns.
        :param kind: One of the valid index types.
        :return:
        """
        self.index_definitions[index_name]=IndexDefinition(index_name,columns,kind).dic

    def drop_index(self, index_name):
        """
        Remove an index.
        :param index_name: Name of index to remove.
        :return:
        """
        self.index_definitions.pop(index_name)


    def describe_table(self):
        """
        Simply wraps to_json()
        :return: JSON representation.
        """
        if self.column_definitions is None:
            col = []
        else:
            col = [col.dic for col in self.column_definitions]
        self.dic = {"definition":{"name":self.t_name,"path":self.csv_f},
                    "columns":col,
                    "indexes":self.index_definitions}
        return self.dic


class CSVCatalog:

    def __init__(self, dbhost="somedefault", dbport="somedefault",
                 dbname="somedefault", dbuser="somedefault", dbpw="somedefault"):
        """
        self.cnx=pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='lahman2018',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
         """
        self.tables = {}

    def create_table(self, table_name, file_name, column_definitions=None, primary_key_columns=None):
        if table_name in self.tables:
            message='Table name '+table_name+' is duplicate'
            raise DataTableExceptions.DataTableException(code=-101,message=message)

        if column_definitions is not None:
            column_names = [col.dic[column_name] for col in column_definitions]
            with open(file_name,'r') as csvfile:
                reader = csv.reader(csvfile)
                for rows in reader:
                        row = rows
                        break
            for c in column_names:
                if c not in row:
                    message = 'Column '+c+' definition is invalid'
                    raise DataTableExceptions.DataTableException(code=-100,message=message)

        t=TableDefinition(t_name=table_name, csv_f=file_name, column_definitions=column_definitions)
        self.tables[table_name] = t
        return t

    def drop_table(self, table_name):
        if table_name in self.tables:
            self.tables.pop(table_name)

    def get_table(self, table_name):
        """
        Returns a previously created table.
        :param table_name: Name of the table.
        :return:
        """
        return self.tables[table_name]
