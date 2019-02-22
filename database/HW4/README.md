
# NoSQL databases  
---  
## Part 1 neo4j  
In this part, I implemented and tested 4 methods:  
**Create_comment**：create a comment node and relationship comment_on, comment_by, if player_id and taem_id is not none.  
**Create_sub_comment**: create a comment node and relationship response_to, response_by.  
**get_player_comment**: get a player node and comments on it, sub_comments, commenters and relationship between them; return them in json.  
**get_team_comment**: get a team node and other nodes, relationships similar to get_player_comment.  
  
Test cases are all in unit_test_local.py, they are:  
**test_create_comment**: created one comment node and all necessary relationships by using Create_comment method.  
**test_create_comment_fail**: failed to create a comment using Create_comment method beacause the comment message is an empty string.  
**test_create_sub_comment**: created one sub_comment responds to the comment created above and all necessary relationships.  
**test_create_sub_comment_fail**: failed to create a sub_comment because the original comment_id is invalid.  
**test_get_player_comments**: use get_player_comments method to find comments related to player 'pedrodu01'.  
**test_get_team_comments**: use get_team_comments method to find comments related to team 'BOS'.  
  
## Part 2 redis  
In this part, I implemented and tested 3 functions:  
**check_query_cahe**: check redis if there exists a record. Rreturn the result or none.  
**add_to_query_cache**: add the result get from mysql database to redis.  
**retrieve_by_template**: get record from database or cache according to the template. If there exists a match record in redis, return it and print cache hit; if not, print cache miss, get it from database, save it to redis, print the insert key and return the result.  
  
Test cases are in unit_test.py and unit_test_ds.py:  
**unit_test.py**: test check_query_cahe and add_to_query_cache by first check, the add and check again.  
**unit_test_ds.py**: test retrieve_by_template by retrieving using the same template for three times. The outcome should be miss hit hit.  
