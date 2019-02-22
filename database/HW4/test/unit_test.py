import sys
sys.path.append('../')

from redis_cache import data_cache
from utils import utils as ut

ut.set_debug_mode(True)

t = [{"playerID": "willite01", "nameLast": "Williams", "bats": "R"}]
r = [{'nameLast':'Williams',"birthCity":'San Diego'}]


def test1():
    '''
    test check cache
    '''

    r = data_cache.check_query_cache("people", {"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
                               ['nameLast', "birthCity"])
    if r:
        print('check_query_cache:\ncache hit, result=',r)
    else:
        print('check_query_cache:\ncache miss')



def test2():
    '''
    test add to query cache
    '''

    result = data_cache.add_to_query_cache("people",{"playerID": "willite01", "nameLast": "Williams", "bats": "R"}, \
    ['nameLast', "birthCity"],[{'nameLast':'Williams',"birthCity":'San Diego'}])
    print('cache insert', result)

test1()
test2()
test1()
