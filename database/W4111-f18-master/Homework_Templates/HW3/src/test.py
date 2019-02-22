import json
import pymysql
import csv
"""
cnx = pymysql.connect(host='localhost',
                             user='dbuser',
                             password='dbuser',
                             db='hw3',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor=cnx.cursor()



class ColumnDefinition:

    column_types = ("text", "number")

    def __init__(self, column_name, column_type="text", not_null=False):
        self.dic = {"column_name":column_name,
                    "column_type":column_type,
                    "not_null":not_null}

    def to_json(self):
        return self.dic



class IndexDefinition:

    index_types = ("PRIMARY", "UNIQUE", "INDEX")

    def __init__(self, index_name, index_type):
        self.dic = {"index_name":index_name,
                    "index_type":index_type}

indexes = {"primary":IndexDefinition('abc','PRIMARY').dic}
columns = [ColumnDefinition('id','number').dic,ColumnDefinition('data','text').dic]
definition = {'name':'people','path':'123'}
dic = {"definition":definition,"columns":columns,"indexes":indexes}
a = ColumnDefinition('id','number').to_json()
"""

with open('PeopleSmall.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for rows in reader:
            row = rows
            break
print(row)
