import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)


def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

def template_to_where_clause(t):
    s = ""
    if t is None:
        return s
    for (key,value) in t.items():
        if s != "":
            s += "AND "
        if type(value) == list:
            s += key + "='" + value[0] + "'"
        else:
            s += key + "='" + value + "'"

    if s != "":
        s = "WHERE " + s;

    return s
def template_to_set_clause(t):
    s = ""
    if t is None:
        return s
    for (key,value) in t.items():
        if s != "":
            s += ","
        s += key + "='" + value + "'"

    if s != "":
        s = "SET " + s;
    return s

def pk_to_template(table,pk):
    pk_value = pk.split('_')
    value_list = []
    for v in pk_value:
        value_list.append([v])
    q = "select COLUMN_NAME from (select * from INFORMATION_SCHEMA.KEY_COLUMN_USAGE  \
        where TABLE_NAME = "+"'"+table+"'"+" ) as a \
        where a.CONSTRAINT_SCHEMA = 'lahman2017raw' and CONSTRAINT_NAME = 'PRIMARY'"
    print(q)
    pk = run_q(q,None,True)
    pk_list = []
    for k in pk:
        pk_list.append(k.get('COLUMN_NAME'))
    dic = dict(zip(pk_list,value_list))
    return dic

def find_by_template(table,t,fields=None,limit=None,offset=None):
    WC = template_to_where_clause(t)
    if offset is None:
        offset = '0'
    else:
        offset = offset[0]
    if limit is None:
        limit = '10'
    else:
        limit = limit[0]

    if fields is not None:
        q = "select " + fields[0] + " from "+table + " " +WC+" limit "+limit+" offset "+offset
    else:
        q = "select * from "+table + " " +WC+" limit "+limit+" offset "+offset
    print(q)
    result = run_q(q, None, True)
    return result

def find_by_primary_key(table, primary_key,fields=None):
    template = pk_to_template(table,primary_key)
    result = find_by_template(table,template,fields)
    return result

def Insert(table,t):
    body = template_to_set_clause(t)
    q = "INSERT INTO " + table +" "+ body
    run_q(q, None, True)
    return q

def Update(table,t,primary_key):
    body = template_to_set_clause(t)
    template = pk_to_template(table,primary_key)
    WC = template_to_where_clause(template)
    q = "UPDATE " + table +" "+ body + " " + WC
    run_q(q, None, True)
    return q

def Delete(table,primary_key):
    t = pk_to_template(table,primary_key)
    WC = template_to_where_clause(t)
    q = "DELETE FROM " + table +" "+ WC
    run_q(q, None, True)
    return q

def find_by_fk(table,primary_key,related_table,template,fields,limit,offset):
    fk_list = []
    q = "select column_name from (select * from INFORMATION_SCHEMA.KEY_COLUMN_USAGE  \
        where TABLE_NAME =" +"'" + table + "'" +") as a \
        where a.CONSTRAINT_SCHEMA = 'lahman2017raw' and REFERENCED_TABLE_NAME =" + "'" +related_table+ "'"
    foreign_key = run_q(q,None,True)
    for k in foreign_key:
        fk_list.append(k.get('COLUMN_NAME'))
    pk_template = pk_to_template(table, primary_key)

    if foreign_key == ():
        if template is not None:
            pk_template.update(template)
        result = find_by_template(related_table,pk_template,fields,limit,offset)
        return result
    else:
        template = {key:value for key,value in pk_template.items() if key in fk_list}
        result = find_by_template(related_table,template,fields,limit,offset)
        return result

def find_teammates(playerid,limit,offset):
    if offset is None:
        offset = '0'
    else:
        offset = offset[0]
    if limit is None:
        limit = '10'
    else:
        limit = limit[0]
    q = "select e.playerID,e.teammate,e.first_year,e.last_year,count(*) as times from \
            (select c.playerID,c.teammate,c.yearID,c.teamID,d.first_year,d.last_year from \
                (select a.playerID,b.playerID as teammate,a.yearID,a.teamID from \
                    (select * from batting where playerID = " + " '" + playerid +"'" +" ) as a \
                    join batting as b \
                    on a.teamID = b.teamID and a.yearID = b.yearID) as c \
                join \
                (select playerid,min(yearID) as first_year,max(yearID) as last_year from batting group by playerid) as d \
                on c.teammate = d.playerID) as e \
        group by e.playerID,e.teammate,e.first_year,e.last_year limit "+limit+" offset "+offset
    result = run_q(q,None,True)
    return result

def find_career_stats(playerid,limit,offset):
    if offset is None:
        offset = '0'
    else:
        offset = offset[0]
    if limit is None:
        limit = '10'
    else:
        limit = limit[0]
    q = "select c.playerID,teamID,yearID,g_all,d.hits,d.ABs,d.A,d.E from appearances as c \
        join \
        (select a.playerID,A,E,b.H as hits,b.AB as ABs from \
            (select playerID,A,E from Fielding) as a \
            join batting as b \
            on a.playerID = b.playerID) as d \
        on c.playerID = d.playerID \
        WHERE c.playerID = '"+ playerid +"' limit "+limit+' offset '+offset
    result = run_q(q,None,True)
    return result

def find_roster(t,limit,offset):
    if offset is None:
        offset = '0'
    else:
        offset = offset[0]
    if limit is None:
        limit = '10'
    else:
        limit = limit[0]
    WC = template_to_where_clause(t)
    q = "select c.playerid, d.nameLast, d.nameFirst,c.teamid,c.yearid,c.G_all,c.H,c.AB from \
            (select distinct a.playerid,a.teamid,a.yearid,a.G_all,b.H,b.AB from \
                (select playerid,teamid,yearid,G_all from appearances "+ WC + ") as a \
                join \
                (select playerid,teamid,yearid,H,AB from batting " + WC + ") as b \
                on a.playerid = b.playerid) as c \
            join people as d \
            on d.playerid = c.playerid" + " limit "+limit+' offset '+offset

    print(q)
    result = run_q(q, None, True)
    return result

def dic_to_str(in_args):
    args = "?"
    if in_args is None:
        return args
    for k,v in in_args.items():
        args += k+"="+v[0]+"&"
    return args

def list_to_str(in_fields):
    if in_fields is None:
        return ''
    fields = 'fields='
    for i in in_fields:
        fields += i+','
    return fields[:-1]+'&'

def generate_links(url,url_root,resource,in_args,in_fields,offset,limit,result):
    args = dic_to_str(in_args)
    fields = list_to_str(in_fields)
    if offset is None:
        offset = 0
    else:
        offset = int(offset[0])
    if limit is None:
        limit = 10
    else:
        limit = int(limit[0])

    previous_link = {"rel":"previous","href":url_root+'api/'+resource+args+fields+'offset='+str(offset-limit)+'&limit='+str(limit)}
    current_link = {"rel":"current","href":url}
    next_link = {"rel":"next","href":url_root+'api/'+resource+args+fields+'offset='+str(offset+limit)+'&limit='+str(limit)}

    if len(result) < 10:
        if offset == 0:
            return [current_link]
        else:
            return [previous_link,current_link]
    elif len(result) == 10:
        if offset == 0:
            return [current_link,next_link]
        else:
            return [previous_link,current_link,next_link]
