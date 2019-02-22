import CSVCatalog
import CSVTable

import time
import json

def cleanup():
    """
    Deletes previously created information to enable re-running tests.
    :return: None
    """
    cat = CSVCatalog.CSVCatalog()
    cat.drop_table("people")
    cat.drop_table("batting")
    cat.drop_table("teams")

    cat.drop_table("teams")

def print_test_separator(msg):
    print("\n")
    lot_of_stars = 20*'*'
    print(lot_of_stars, '  ', msg, '  ', lot_of_stars)
    print("\n")

def test_find_by_template_scan():

    print_test_separator("Starting test_find by_template_scan")
    cleanup()

    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", column_type="text", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("H", column_type="number", not_null=False))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number", not_null=False))

    t = cat.create_table("batting",
                         "Batting.csv",
                         cds)
    t.define_index("team_year_idx", ['teamID', 'yearID','H'], "INDEX")
    batting_tbl = CSVTable.CSVTable("batting")

    start_time = time.time()

    tmp = {'playerID':'willite01','yearID':'1939','stint': '1','teamID':'BOS'}
    fields = ['playerID','yearID','stint','teamID']

    find_result = batting_tbl.find_by_template(tmp,fields)

    end_time = time.time()
    print("Result = \n",json.dumps(find_result,indent=2))
    elapsed_time = end_time - start_time
    print("\nElapsed time to execute queries = ",elapsed_time)
    print_test_separator("Complete test_find_by_template_scan")

def test_find_by_template_indexed():

    print_test_separator("Starting test_find by_template_indexed")
    cleanup()

    cat = CSVCatalog.CSVCatalog()

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", column_type="text", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))
    cds.append(CSVCatalog.ColumnDefinition("H", column_type="number", not_null=False))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number", not_null=False))

    t = cat.create_table("batting",
                         "Batting.csv",
                         cds)
    t.define_index("team_year_idx", ['teamID', 'yearID'], "INDEX")
    batting_tbl = CSVTable.CSVTable("batting")

    start_time = time.time()

    tmp = {'playerID':'willite01','yearID':'1939','stint': '1','teamID':'BOS'}
    fields = ['playerID','yearID','stint','teamID']

    find_result = batting_tbl.find_by_template(tmp,fields)
    print("Result = \n",json.dumps(find_result,indent=2))
    end_time = time.time()

    elapsed_time = end_time - start_time
    print("\nElapsed time to execute queries = ",elapsed_time)
    print_test_separator("Complete test_find_by_template_indexed")

def test_join_not_optimized(optimize=False):
    """

    :return:
    """

    print_test_separator("Starting test_optimizable_1, optimize = " + str(optimize))
    print("\n\nDude. This takes 30 minutes. Trust me.\n\n")
    return

    cleanup()
    print_test_separator("Starting test_optimizable_1, optimize = " + str(optimize))

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    start_time = time.time()

    tmp = { "playerID": "willite01"}
    join_result = people_tbl.join(batting_tbl,['playerID'], tmp, optimize=optimize)

    end_time = time.time()

    print("Result = \n", json.dumps(join_result,indent=2))
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable")


def test_join_optimizable_2(optimize=False):
    """
    Calling this with optimize=True turns on optimizations in the JOIN code.
    :return:
    """
    cleanup()
    print_test_separator("Starting test_optimizable_2, optimize = " + str(optimize))

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))
    t.define_index("pid_idx", ['playerID'], "INDEX")

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    start_time = time.time()

    join_result = people_tbl.join(batting_tbl,['playerID'], None, optimize=optimize)

    end_time = time.time()

    print("Result = \n", json.dumps(join_result,indent=2))
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable_2")


def test_join_optimizable_3(optimize=False):
    """

    :return:
    """
    cleanup()
    print_test_separator("Starting test_optimizable_3, optimize = " + str(optimize))

    cat = CSVCatalog.CSVCatalog()
    cds = []

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameLast", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("nameFirst", column_type="text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCity", "text"))
    cds.append(CSVCatalog.ColumnDefinition("birthCountry", "text"))
    cds.append(CSVCatalog.ColumnDefinition("throws", column_type="text"))

    t = cat.create_table(
        "people",
        data_dir + "People.csv",
        cds)
    t.define_index("pid_idx", ['playerID'], "INDEX")
    print("People table metadata = \n", json.dumps(t.describe_table(), indent=2))

    cds = []
    cds.append(CSVCatalog.ColumnDefinition("playerID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("H", "number", True))
    cds.append(CSVCatalog.ColumnDefinition("AB", column_type="number"))
    cds.append(CSVCatalog.ColumnDefinition("teamID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("yearID", "text", True))
    cds.append(CSVCatalog.ColumnDefinition("stint", column_type="number", not_null=True))

    t = cat.create_table(
        "batting",
        data_dir + "Batting.csv",
        cds)
    print("Batting table metadata = \n", json.dumps(t.describe_table(), indent=2))
    t.define_index("pid_idx", ['playerID'], "INDEX")

    people_tbl = CSVTable.CSVTable("people")
    batting_tbl = CSVTable.CSVTable("batting")

    start_time = time.time()

    tmp = {"playerID": "willite01"}
    join_result = people_tbl.join(batting_tbl,['playerID'], tmp, optimize=optimize)

    end_time = time.time()

    print("Result = \n", json.dumps(join_result,indent=2))
    elapsed_time = end_time - start_time
    print("\n\nElapsed time = ", elapsed_time)

    print_test_separator("Complete test_join_optimizable_3")


test_find_by_template_scan()
test_find_by_template_indexed()

test_join_not_optimized(optimize=False)
test_join_optimizable_2(optimize=True)
test_join_optimizable_3(optimize=True)
