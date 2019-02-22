import csv  # Python package for reading and writing CSV files.

# You MAY have to modify to match your project's structure.
from src import DataTableExceptions
from src import CSVCatalog


import json

max_rows_to_print = 10


class CSVTable:
    # Table engine needs to load table definition information.
    __catalog__ = CSVCatalog.CSVCatalog()

    def __init__(self, t_name, load=True):
        """
        Constructor.
        :param t_name: Name for table.
        :param load: Load data from a CSV file. If load=False, this is a derived table and engine will
            add rows instead of loading from file.
        """

        self.__table_name__ = t_name

        # Holds loaded metadata from the catalog. You have to implement  the called methods below.
        self.__description__ = None
        if load:
            self.__load_info__()  # Load metadata
            self.__rows__ = None
            self.__load__()  # Load rows from the CSV file.

            # Build indexes defined in the metadata. We do not implement insert(), update() or delete().
            # So we can build indexes on load.
            self.__build_indexes__()
        else:
            self.__file_name__ = "DERIVED"

    def __load_info__(self):
        """
        Loads metadata from catalog and sets __description__ to hold the information.
        :return:
        """
        cat = CSVCatalog.CSVCatalog()
        t = cat.get_table(self.__table_name__)
        self.__description__ = t.describe_table()

    # Load from a file and creates the table and data.
    def __load__(self):

        try:
            fn = self.__get_file_name__()
            with open(fn, "r") as csvfile:
                # CSV files can be pretty complex. You can tell from all of the options on the various readers.
                # The two params here indicate that "," separates columns and anything in between " ... " should parse
                # as a single string, even if it has things like "," in it.
                reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')

                # Get the names of the columns defined for this table from the metadata.
                column_names = self.__get_column_names__()

                # Loop through each line (well dictionary) in the input file.
                for r in reader:
                    # Only add the defined columns into the in-memory table. The CSV file may contain columns
                    # that are not relevant to the definition.
                    projected_r = self.project([r], column_names)[0]
                    self.__add_row__(projected_r)

        except IOError as e:
            raise DataTableExceptions.DataTableException(
                code=DataTableExceptions.DataTableException.invalid_file,
                message="Could not read file = " + fn)

    def __get_column_names__(self):
        return [c["column_name"] for c in self.__description__["columns"]]

    def __get_file_name__(self):
        return self.__description__["definition"]["path"]

    def __add_row__(self,row):
        if self.__rows__:
            self.__rows__.append(row)
        else:
            self.__rows__ = [row]

    def __str__(self):
        """
        You can do something simple here. The details of the string returned depend on what properties you
        define on the class. So, I cannot provide a simple implementation.
        :return:
        """
    def get_indexed_columns(self):
        columns = {}
        for k,v in self.__description__["indexes"].items():
            if v['kind']=="INDEX":
                columns[k] = v["columns"]
        return columns

    def list_to_str(self,list):
        str = ""
        for i in list:
            str+=i+"_"
        return str[:-1]

    def __build_indexes__(self):
        if self.__description__["indexes"]:
            columns = self.get_indexed_columns()
            self.indexes = {}
            for k,v in columns.items():
                self.indexes[k] = {}
                id = 0
                for r in self.__rows__:
                    values = self.list_to_str([r[col] for col in v])
                    if values in self.indexes[k]:
                        self.indexes[k][values].append(id)
                    else:
                        self.indexes[k][values] = [id]
                    id+=1
        else:
            self.indexes = None

    def get_index_selectivity(self):
        return {k:len(self.__rows__)/len(v) for k,v in self.indexes.items()}


    def __get_access_path__(self, tmp):
        """
        Returns best index matching the set of keys in the template.

        Best is defined as the most selective index, i.e. the one with the most distinct index entries.

        An index name is of the form "colname1_colname2_coluname3" The index matches if the
        template references the columns in the index name. The template may have additional columns, but must contain
        all of the columns in the index definition.
        :param tmp: Query template.
        :return: Index or None
        """
        if not self.__description__["indexes"]:
            return None

        i_columns = self.get_indexed_columns()
        select = self.get_index_selectivity()
        for k,v in i_columns.items():
            for c in v:
                if c not in tmp:
                    select.pop(k)
                    break
        if select:
            return min(select, key = select.get)
        else:
            return None



    def matches_template(self, row, t):
        """

        :param row: A single dictionary representing a row in the table.
        :param t: A template
        :return: True if the row matches the template.
        """

        # Basically, this means there is no where clause.
        if t is None:
            return True

        try:
            c_names = list(t.keys())
            for n in c_names:
                if row[n] != t[n]:
                    return False
            else:
                return True
        except Exception as e:
            raise (e)

    def project(self, rows, fields):
        """
        Perform the project. Returns a new table with only the requested columns.
        :param fields: A list of column names.
        :return: A new table derived from this table by PROJECT on the specified column names.
        """
        try:
            if fields is None:  # If there is not project clause, return the base table
                return rows  # Should really return a new, identical table but am lazy.
            else:
                result = []
                for r in rows:  # For every row in the table.
                    tmp = {}  # Not sure why I am using range.
                    for j in range(0, len(fields)):  # Make a new row with just the requested columns/fields.
                        v = r[fields[j]]
                        tmp[fields[j]] = v
                    else:
                        result.append(tmp)  # Insert into new table when done.

                return result

        except KeyError as ke:
            # happens if the requested field not in rows.
            raise DataTableExceptions.DataTableException(-2, "Invalid field in project")

    def __find_by_template_scan__(self, t, fields=None, limit=None, offset=None):
        """
        Returns a new, derived table containing rows that match the template and the requested fields if any.
        Returns all row if template is None and all columns if fields is None.
        :param t: The template representing a select predicate.
        :param fields: The list of fields (project fields)
        :param limit: Max to return. Not implemented
        :param offset: Offset into the result. Not implemented.
        :return: New table containing the result of the select and project.
        """

        if limit is not None or offset is not None:
            raise DataTableExceptions.DataTableException(-101, "Limit/offset not supported for CSVTable")

        # If there are rows and the template is not None
        if self.__rows__ is not None:

            result = []

            # Add the rows that match the template to the newly created table.
            for r in self.__rows__:
                if self.matches_template(r, t):
                    result.append(r)

            result = self.project(result, fields)
        else:
            result = None

        return result

    def __find_by_template_index__(self, t, idx, fields=None, limit=None, offset=None):
        """
        Find using a selected index
        :param t: Template representing a where clause/
        :param idx: Name of index to use.
        :param fields: Fields to return.
        :param limit: Not implemented. Ignore.
        :param offset: Not implemented. Ignore
        :return: Matching tuples.
        """
        if self.__rows__ is not None:

            result = []

            v = []
            columns = self.get_indexed_columns()
            for c in columns[idx]:
                v.append(t[c])
                t.pop(c)
            values = self.list_to_str(v)
            ids = self.indexes[idx][values]

            for i in ids:
                if self.matches_template(self.__rows__[i], t):
                    result.append(self.__rows__[i])

            result = self.project(result, fields)
        else:
            result = None
        return result

    def find_by_template(self, t, fields=None, limit=None, offset=None):
        # 1. Validate the template values relative to the defined columns.
        # 2. Determine if there is an applicable index, and call __find_by_template_index__ if one exists.
        # 3. Call __find_by_template_scan__ if not applicable index.
        if t:
            df_columns = self.__get_column_names__()
            for k in t:
                if k not in df_columns:
                    raise DataTableExceptions.DataTableException(
                        code=-102,
                        message= "template values not relative to defined columns")

            r = self.__get_access_path__(t)
            if r:
                return self.__find_by_template_index__(t,r,fields)
            else:
                return self.__find_by_template_scan__(t,fields)
        else:
            return self.__rows__

    def insert(self, r):
        raise DataTableExceptions.DataTableException(
            code=DataTableExceptions.DataTableException.not_implemented,
            message="Insert not implemented"
        )

    def delete(self, t):
        raise DataTableExceptions.DataTableException(
            code=DataTableExceptions.DataTableException.not_implemented,
            message="Delete not implemented"
        )

    def update(self, t, change_values):
        raise DataTableExceptions.DataTableException(
            code=DataTableExceptions.DataTableException.not_implemented,
            message="Updated not implemented"
        )

    def join(self, right_r, on_fields, where_template=None, project_fields=None, optimize=False):
        """
        Implements a JOIN on two CSV Tables. Support equi-join only on a list of common
        columns names.
        :param left_r: The left table, or first input table
        :param right_r: The right table, or second input table.
        :param on_fields: A list of common fields used for the equi-join.
        :param where_template: Select template to apply to the result to determine what to return.
        :param project_fields: List of fields to return from the result.
        :return: List of dictionary elements, each representing a row.
        """
        if optimize:
            #select push down
            if where_template:
                l_template = {k:v for k,v in where_template.items() if k in self.__get_column_names__()}
                r_template = {k:v for k,v in where_template.items() if k in right_r.__get_column_names__()}
                l_rows = self.find_by_template(l_template)
                r_rows = right_r.find_by_template(r_template)
            else:
                l_rows = self.__rows__
                r_rows = right_r.__rows__

            final_result = []
            #decide which table can use index
            if self.__get_access_path__(on_fields):
                for r_r in r_rows:
                    on_template = {f:r_r[f] for f in on_fields}
                    l_r = self.find_by_template(on_template)
                    if l_r:
                        for r in l_r:
                            r_r.update(r)
                            final_result.append(r_r)

            elif right_r.__get_access_path__(on_fields):
                for l_r in l_rows:
                    on_template = {f:l_r[f] for f in on_fields}
                    r_r = self.find_by_template(on_template)
                    if r_r:
                        for r in r_r:
                            l_r.update(r)
                            final_result.append(l_r)

            else:
                self.__rows__ = l_rows
                for r_r in r_rows:
                    on_template = {f:r_r[f] for f in on_fields}
                    l_r = self.find_by_template(on_template)
                    if l_r:
                        for r in l_r:
                            r_r.update(r)
                            final_result.append(r_r)

            return self.project(final_result,project_fields)
        else:
            return self.nested_loop_join(right_r,on_fields,where_template,project_fields)


        # If not optimizations are possible, do a simple nested loop join and then apply where_clause and
        # project clause to result.
        #
        # At least two vastly different optimizations are be possible. You should figure out two different optimizations
        # and implement them.
        #
        pass
    def nested_loop_join(self, right_r, on_fields, where_template=None, project_fields=None):
        join_result = []
        for l_r in self.__rows__:
            on_template = {f:l_r[f] for f in on_fields}
            r_r = right_r.find_by_template(on_template)
            if r_r:
                for r in r_r:
                    l_r.update(r)
                    join_result.append(l_r)
        final_result = []
        for r in joint_result:
            if self.matches_template(r,where_template):
                row = self.project([r], fields=project_fields)
                final_result.append(row[0])
        return final_result
