1.How to run the code?
Run application_function.py then URLs based on localhost can be parsed and data will be sent back or changes to database will be executed

note: When there primary keys in URL. The order should be written as follow:
batting: playerID_yearID_stint_teamID
appearances: yearID_teamID_playerID
fielding: playerID_yearID_stint_team_POS_InnOuts
teams: yearID_teamID
managers: playerID_yearID_teamID_inseason

2.Deign choices
application_function.py which is the main function can parse the URL request, input parameters to functions in SimpleBO and return data or queries.
Any operation directly related with database is done in SimpleBO.py. it inclueds find_by_template, find_by_primary_key, find_by_foreign_key, find_teammates, find_career_stats, find_roster, generate_links, insert, delete, update functions. 

When using specific source, there will be no link below the data, while there will be at least current link below the data for the other get functions.
When using put, post, delete, the output will be queries that update, insert to specific table or delete from the table.  

3.files included
application_function.py: main function
SimpleBO.py: subfunction called by application_function.py
modify schema.sql: sql file that modifies the database schema
test screenshots: inclueds all screenshots of all output when using Postman to test