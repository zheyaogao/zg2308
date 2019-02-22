# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy

import SimpleBO
from mpmath import limit
from bokeh.tests.test_driving import offset

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():
    fields = None
    in_args = None
    
    if request.args is not None:
        print('say: ',request.args)
        in_args = dict(copy.copy(request.args))
        #s = SimpleBO.args_to_str(in_args)
        #print("s: ",s)
        fields = copy.copy(in_args.get('fields',None))
        print('fields is : ',fields)
        offset = copy.copy(in_args.get('offset',None))
        limit = copy.copy(in_args.get('limit',None))
        if fields:
            del(in_args['fields'])
        if offset:
            del(in_args['offset'])
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




@app.route('/api/<resource_name>',methods = ['GET','POST'])
def get_resource(resource_name):
    
    in_args,fields,body,limit,offset = parse_and_print_args()
    print("in_args: ",in_args)
    args = SimpleBO.args_to_str(in_args)
    print("args: ",args)
    if request.method == 'GET':
        if limit is None and offset is None:
            limit_default = ['10']
            offset_default = ['0']
            if not in_args and fields is None:
                url = request.url+'?limit=10&offset=0'
            else:
                url = request.url+'&limit=10&offset=0'
            url_root = request.url_root
            result = SimpleBO.find_by_template(resource_name, in_args, fields,limit_default,offset_default)
            put_links=SimpleBO.generate_links(resource_name,result,args,url,url_root,limit_default,offset_default,fields)
            
            output=[{"data":result,
                       "links":put_links}]
            
            return json.dumps(output), 200, \
                {"content-type": "application/json; charset:utf-8"}
        elif limit is not None and offset is not None: 
            url = request.url
            url_root = request.url_root
            result = SimpleBO.find_by_template(resource_name, in_args, fields,limit,offset)
            links=SimpleBO.generate_links(resource_name,result,args,url,url_root,limit,offset,fields)
            print('result: ',len(result))
            output=[{"data":result,
                       "links":links}]
            
            return json.dumps(output), 200, \
                {"content-type": "application/json; charset:utf-8"}
    
    elif request.method == 'POST':
        print("table name: ", resource_name)
        print("the row here is: ", body)
        result1 = SimpleBO.insert(resource_name,body)
        return json.dumps(result1), 200, \
               {"content-type": "application/json; charset:utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource_name + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource_name>/<primary_key>',methods = ['GET','PUT','DELETE'])
def get_resource_primary_key(resource_name,primary_key):
    print("pk: ",primary_key)
    in_args,fields,body,limit,offset = parse_and_print_args()
    print("in_args:",in_args)
    limit_default=['10']
    offset_default=['0']
    args = SimpleBO.args_to_str(in_args)
    print("url: ",request.url)
    if request.method == 'GET':
        if limit is None and offset is None:
            result = SimpleBO.get_PK(resource_name,primary_key,fields)
            if not in_args and fields is None:
                url = request.url+'?limit=10&offset=0'
            else:
                url = request.url+'&limit=10&offset=0'
            url_root = request.url_root
            put_links=SimpleBO.generate_links(resource_name,result,args,url,url_root,limit_default,offset_default,fields)
            output=[{"data":result,
                           "links":put_links}]
            return json.dumps(output), 200, \
                   {"content-type": "application/json; charset:utf-8"}
        elif limit is not None and offset is not None:
            url = request.url
            url_root = request.url_root
            result = SimpleBO.get_PK(resource_name,primary_key, fields,limit,offset)
            links=SimpleBO.generate_links(resource_name,result,args,url,url_root,limit,offset,fields)
            print('result: ',len(result))
            output=[{"data":result,
                       "links":links}]
            
            return json.dumps(output), 200, \
                {"content-type": "application/json; charset:utf-8"}
    elif request.method == 'PUT':
        in_args,fields,body,limit,offset = parse_and_print_args()
        print("body is : ",body)
        print("table name: ", resource_name)
        print("the row here is: ", body)
        result1 = SimpleBO.Updating(resource_name,body,primary_key)
        return json.dumps(result1), 200, \
               {"content-type": "application/json; charset:utf-8"}
    elif request.method == 'DELETE':
        in_args,fields,body,limit,offset = parse_and_print_args()
        print("table name: ", resource_name)
        print("the row here is: ", body)
        result2 = SimpleBO.Delete(resource_name,body)
        return json.dumps(result2), 200, \
               {"content-type": "application/json; charset:utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource_name + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}

@app.route('/api/<resource_name>/<primary_key>/<related_resource>',methods = ['GET','POST'])
def get_resource_Related(resource_name,primary_key,related_resource):
    in_args,fields,body,limit,offset = parse_and_print_args()
    print("in_args: ",in_args)
    out_args = request.args.get('fields')
    limit_default=['10']
    offset_default=['0']
    args = SimpleBO.args_to_str(in_args)
    if request.method == 'GET':
        if limit is None and offset is None:
            result = SimpleBO.get_FK(resource_name,primary_key,related_resource,in_args,fields,limit,offset)
            if not in_args and fields is None:
                url = request.url+'?limit=10&offset=0'
            else:
                url = request.url+'&limit=10&offset=0'
            url_root = request.url_root
            resource_path = resource_name+"/"+primary_key+"/"+related_resource
            print('path: ',resource_path)
            put_links=SimpleBO.generate_links(resource_path,result,args,url,url_root,limit_default,offset_default,fields)
            output=[{"data":result,
                           "links":put_links}]
            return json.dumps(output), 200, \
                   {"content-type": "application/json; charset:utf-8"}
        elif limit is not None and offset is not None:
            url = request.url
            url_root = request.url_root
            resource_path = resource_name+"/"+primary_key+"/"+related_resource
            result = SimpleBO.get_FK(resource_name,primary_key,related_resource,in_args,fields,limit,offset)
            result1 = SimpleBO.find_by_template()
            links=SimpleBO.generate_links(resource_path,result,args,url,url_root,limit,offset,fields)
            print('result: ',len(result))
            output=[{"data":result,
                       "links":links}]
            
            return json.dumps(output), 200, \
                {"content-type": "application/json; charset:utf-8"}
        
    if request.method == 'POST':
        result = SimpleBO.insert(related_resource,body)
        return json.dumps(result), 200, \
               {"content-type": "application/json; charset:utf-8"}
    


if __name__ == '__main__':
    app.run()
