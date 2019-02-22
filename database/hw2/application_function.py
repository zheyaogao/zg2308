# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy

import SimpleBO

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():
    fields = None
    in_args = None
    if request.args is not None:
        in_args = dict(copy.copy(request.args))
        fields = copy.copy(in_args.get('fields',None))
        if fields:
            del(in_args['fields'])
        offset = copy.copy(in_args.get('offset',None))
        if offset:
            del(in_args['offset'])
        limit = copy.copy(in_args.get('limit',None))
        if limit:
            del(in_args['limit'])
    try:
        if request.data:
            body = json.loads(request.data)
        else:
            body = None
    except Exception as e:
        print("exception here is: ", e)
        body = None



    print("Request.args : ", json.dumps(in_args))
    return in_args,fields,body,limit,offset





@app.route('/api/<resource>',methods = ['GET','POST'])
def Basic_resource(resource):

    in_args,fields,body,offset,limit = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_by_template(resource,in_args,fields,limit,offset)
        url = request.url
        url_root = request.url_root
        links = SimpleBO.generate_links(url,url_root,resource,in_args,fields,offset,limit,result)
        output=[{"data":result,
                   "links":links}]
        return json.dumps(output), 200, \
            {"content-type": "application/json; charset:utf-8"}

    elif request.method == 'POST':
        result = SimpleBO.Insert(resource,body)
        return result

    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/<resource>/<primary_key>',methods = ['GET','PUT','DELETE'])
def Specific_resource(resource,primary_key):

    in_args,fields,body,offset,limit = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_by_primary_key(resource,primary_key,fields)
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset:utf-8"}

    elif request.method == 'PUT':
        result = SimpleBO.Update(resource,body,primary_key)
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset:utf-8"}

    elif request.method == 'DELETE':
        result = SimpleBO.Delete(resource,primary_key)
        return result

    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/<resource>/<primary_key>/<related_resource>',methods = ['GET','POST'])
def related_resource(resource,primary_key,related_resource):

    in_args,fields,body,offset,limit = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_by_fk(resource,primary_key,related_resource,in_args,fields,limit,offset)
        url = request.url
        url_root = request.url_root
        all_resource = resource+"/"+primary_key+"/"+related_resource
        links=SimpleBO.generate_links(url,url_root,all_resource,in_args,fields,offset,limit,result)
        output=[{"data":result,
                       "links":links}]
        return json.dumps(output), 200, \
               {"content-type": "application/json; charset:utf-8"}

    elif request.method == 'POST':
        result = SimpleBO.Insert(related_resource,body)
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset:utf-8"}

    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/teammates/<playerid>', methods=['GET'])
def get_teammates(playerid):

    in_args,fields,body,offset,limit = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_teammates(playerid,limit,offset)
        url = request.url
        url_root = request.url_root
        resource = 'teammates/'+playerid
        links=SimpleBO.generate_links(url,url_root,resource,in_args,fields,offset,limit,result)
        output=[{"data":result,
                   "links":links}]
        return json.dumps(output), 200, \
            {"content-type": "application/json; charset:utf-8"}

@app.route('/api/people/<playerid>/career_stats', methods=['GET'])
def get_career_stats(playerid):

    in_args,fields,body,offset,limit = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_career_stats(playerid,limit,offset)
        url = request.url
        url_root = request.url_root
        resource = 'people/'+playerid+'/career_stats'
        links=SimpleBO.generate_links(url,url_root,resource,in_args,fields,offset,limit,result)
        output=[{"data":result,
                   "links":links}]
        return json.dumps(output), 200, \
            {"content-type": "application/json; charset:utf-8"}

    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/roster', methods=['GET'])
def get_roster():

    in_args,fields,body,offset,limit = parse_and_print_args()
    if request.method == 'GET':
        result = SimpleBO.find_roster(in_args,limit,offset)
        url = request.url
        url_root = request.url_root
        resource = 'roster'
        links=SimpleBO.generate_links(url,url_root,resource,in_args,fields,offset,limit,result)
        output=[{"data":result,
                   "links":links}]
        return json.dumps(output), 200, \
            {"content-type": "application/json; charset:utf-8"}

    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

if __name__ == '__main__':
    app.run()
