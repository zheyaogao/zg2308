import pymysql
import csv
import logging
from src import DataTableExceptions


class ColumnDefinition:
    """

    Represents a column definition in the CSV Catalog.
    """
    column_types = ("text", "number")
    # Allowed types for a column.
    def __init__(self, column_name, column_type="text", not_null=False):
        self.column_name = column_name
        self.column_type = column_type
        self.not_null = not_null
        """

        :param column_name: Cannot be None.
        :param column_type: Must be one of valid column_types.
        :param not_null: True or False
        """
    def to_json(self):
        dic = {"column_name":self.column_name,
               "column_type":self.column_type,
               "not_null":self.not_null}
        return dic

class IndexDefinition:
    """
    Represents the definition of an index.
    """
    index_types = ("PRIMARY", "UNIQUE", "INDEX")

    def __init__(self, index_name, columns, index_type):
        self.index_name = index_name
        self.columns = columns
        self.index_type = index_type
        self.dic = {"index_name":self.index_name,
                    "columns":self.columns,
                    "kind":self.index_type}

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
        cursor=cnx.cursor()
        q = "select * from table_definitions where name='"+table_name+"'"
        cursor.execute(q)
        td = cursor.fetchall()
        csv_f = td[0]['file']

        q = "select * from column_definitions where table_name='"+table_name+"'"
        cursor.execute(q)
        r= cursor.fetchall()
        column_definitions = [ColumnDefinition(row['column_name'],row['column_type'],row['not_null']) for row in r]

        q = "select * from index_definitions where table_name='"+table_name+"'"
        cursor.execute(q)
        r= cursor.fetchall()
        index_definitions = {}
        for row in r:
            if row['index_name'] in index_definitions.keys():
                index_definitions[row['index_name']]['columns'].append(row['column'])
            else:
                index_definitions[row['index_name']] = IndexDefinition(row['index_name'],[row['column']],row['index_type']).dic

        return cls(table_name,csv_f,column_definitions,index_definitions,cnx)

    def add_column_definition(self, c):
        """
        Add a column definition.
        :param c: New column. Cannot be duplicate or column not in the file.
        :return: None
        """
        cursor=self.cnx.cursor()
        q = "insert into column_definitions values('" \
        +c.column_name+"','" \
        +c.column_type+"','" \
        +str(c.not_null)+"','" \
        +self.t_name+"')"
        r = cursor.execute(q)
        self.cnx.commit()

        self.column_definitions+=[c]

    def drop_column_definition(self, c):
        """
        Remove from definition and catalog tables.
        :param c: Column name (string)
        :return:
        """
        cursor=self.cnx.cursor()
        q = "delete from column_definitions where column_name="+c.column_name+" and table_name="+self.t_name
        r = cursor.execute(q)
        self.column_definitions.remove(c)

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
        column_names = [c.column_name for c in self.column_definitions]
        for col in columns:
            if col not in column_names:
                raise DataTableExceptions.DataTableException(code=-1000,message='Invalid key columns')

        for col in columns:
            cursor=self.cnx.cursor()
            q = "insert into index_definitions values('PRIMARY','PRIMARY','" \
            +col+"','" \
            +self.t_name+"')"
            r = cursor.execute(q)
            self.cnx.commit()

        self.index_definitions['PRIMARY']=IndexDefinition("PRIMARY",columns,"PRIMARY").dic

    def define_index(self, index_name, columns, kind="index"):
        """
        Define or replace and index definition.
        :param index_name: Index name, must be unique within a table.
        :param columns: Valid list of columns.
        :param kind: One of the valid index types.
        :return:
        """
        for col in columns:
            cursor=self.cnx.cursor()
            q = "insert into index_definitions values('"+index_name+"','" \
            +kind+"','" \
            +col+"','" \
            +self.t_name+"')"
            r = cursor.execute(q)
            self.cnx.commit()

        self.index_definitions[index_name]=IndexDefinition(index_name,columns,kind).dic

    def drop_index(self, index_name):
        """
        Remove an index.
        :param index_name: Name of index to remove.
        :return:
        """
        cursor=self.cnx.cursor()
        q = "delete from index_definitions where index_name="+index_name+" and table_name="+self.t_name
        r = cursor.execute(q)

        self.index_definitions.pop(index_name)


    def describe_table(self):
        """
        Simply wraps to_json()
        :return: JSON representation.
        """
        dic = {"definition":{"name":self.t_name,"path":self.csv_f},
               "columns":[col.to_json() for col in self.column_definitions],
               "indexes":self.index_definitions}
        return dic


class CSVCatalog:

    def __init__(self, dbhost="somedefault", dbport="somedefault",
                 dbname="somedefault", dbuser="somedefault", dbpw="somedefault"):
        self.cnx=pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='hw3',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def create_table(self, table_name, file_name, column_definitions=None, primary_key_columns=None):
        r = self.run_q("select * from table_definitions where name='"+table_name+"'")
        if r:
            message='Table name '+table_name+' is duplicate'
            raise DataTableExceptions.DataTableException(code=-101,message=message)

        if column_definitions:
            column_names = [col.column_name for col in column_definitions]
            with open("../data/"+file_name,'r') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)
            for c in column_names:
                if c not in headers:
                    message = 'Column '+c+' definition is invalid'
                    raise DataTableExceptions.DataTableException(code=-100,message=message)

            for c in column_definitions:
                q = "insert into column_definitions values('" \
                +c.column_name+"','" \
                +c.column_type+"','" \
                +str(c.not_null)+"','" \
                +table_name+"')"
                r = self.run_q(q)
        else:
            column_definitions = []

        q = "insert into table_definitions values('"+table_name+"','"+file_name+"')"
        r = self.run_q(q)

        t=TableDefinition(t_name=table_name, csv_f=file_name, column_definitions=column_definitions,cnx=self.cnx)
        return t

    def drop_table(self, table_name):
        q = "delete from table_definitions where name='"+table_name+"'"
        r = self.run_q(q)
        q = "delete from column_definitions where table_name='"+table_name+"'"
        r = self.run_q(q)
        q = "delete from index_definitions where table_name='"+table_name+"'"
        r = self.run_q(q)

    def get_table(self, table_name):
        """
        Returns a previously created table.
        :param table_name: Name of the table.
        :return:
        """
        t = TableDefinition.load_table_definition(self.cnx,table_name)
        return t

    def run_q(self,q):
        cursor = self.cnx.cursor()
        cursor.execute(q)
        result = cursor.fetchall()
        self.cnx.commit()
        return result
