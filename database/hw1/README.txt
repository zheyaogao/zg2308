Design choices:
file type: .ipynb
CSVTable: A Class include load(), load_header(), save(), primary_key_error(), invalid_keys_error(template), insert_error(template), find_by_primary_key(strings(), fields), find_by_template(template, fields), insert(template), delete(template) functions and file_name, primary_key, reader, writer, header variables in __init__ function.
RDBTable: No  load(), load_header(), save() functions and file_name, reader, writer, header variables. The others are the same.


Running the code:
CSV_implementation and testCSV can be run directly using Jupyter notebook
For RDB_implementation and testRDB, connect information should be changed the to a database with the tables before running it.
For top ten hitters, CSV implementation can only be run using a small subset of the table

Correctness rules:
Return errors when:
Find by primary keys and the primary keys are not a subset of the columns in the underlying file/table
find by template with invalid keys
insert with invalid keys
insert without primary keys
insert duplicate primary keys
delete with invalid keys