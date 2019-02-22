
# Database engine implemention  

## Part 1: CSVCatalog  
### 1.create.sql
In this file, I created three tables called table_definitions, column_definitions, index_definitions in workbench to store metadata.  
### 2.CSVCatalog.py
Four classed are defined in this file:  

**TableDefinition**: hold all catalog information a table has, and have methods to modify and load the metadata in workbench.  
**ColumnDefinition**: hold column information.  
**IndexDefinition**: hold index information  
**CSVCatalog**: have methods to create, drop and get catalog tables in workbench. Output is TableDefinition object.  
### 3.unit_test_catalog.py
Five successful and three failed test cases are inplemented in this file:  

**test_create_table_1**: Simple create of table definition. No columns or indexes.  
**test_create_table_2_fail**: Creates a table, and then attempts to create a table with the same name. Second create should fail.  
**test_create_table_3**: Creates a table that includes several column definitions.  
**test_create_table_3_fail**: This test should fail because one of the defined columns is not in the underlying CSV file.  
**test_create_table_4**: Creates a table that includes several column definitions and a primary key.  
**test_create_table_4_fail**: The primary key references an undefined column, which is an error.  
**test_create_table_5_prep**: Creates a table that includes several column definitions and a primary key.  
**test_create_table_5**: Modifies a preexisting/precreated table definition.  

## Part 2: CSVDataTable Engine  
### 1.CSVTable.py  
Defined a class has methods as follow:  

**___load__**: load the csv file when initialized.   
**__load_info__**: load metadata from workbench when initialized.  
**__build_indexes__**: build indexes when initialized.  
**__find_by_template_scan__**: a basic find method.  
**__find_by_template_index__**: use built indexes to find.  
**__get_access_path__**: decide which find method to use and what index to use.  
**join(optimize=True)**: implement two optimization on join: select pushdown; swapping probe.  
**nested_loop_join**: a basic join method.  
### 2.unit_test_csv_table.py  
Two cases to test find_by_template and three cases to test join:  

**test_find_by_template_scan**: test find without using an index.  
**test_find_by_template_indexed**: test find using an index. (about 60 times faster)  
**test_join_not_optimized**: this takes too long to test.  
**test_join_optimizable_2**: define an index on people table and join without where template.  
**test_join_optimizable_3**: join with template and index on people table.
