#!/usr/bin/env python3
from flask import Flask, request, Response, jsonify
import psycopg2

def r_bad_request(obj, status=400, mimetype="application/json"):
    print(obj)
    return Response(obj, status=status, mimetype=mimetype)

def r_internal_server_error(obj, status=500, mimetype="application/json"):
    return Response(obj, status=statu, mimetype=mimetype)

def r_nyi(status=500, mimetype='application/json'):
    return Response({"message": "Not Yet Implemented"}, status=status, mimetype=mimetype)

def r_ok(obj, status=200, mimetype="application/json"):
    o = "ok" if obj is None else obj
    return Response(o, status=status, mimetype=mimetype)

def require_args(*args):
    argv = {}
    for arg in args:
        argv[arg] = request.args.get(arg)
        if not argv[arg]:
            return None, r_bad_request({
                "message": f"{arg} param required"
                })
    return argv, None

LEADERSERVER = ""
app = Flask(__name__)

DBNAME = 'postgres'
USER = 'postgres'

def connect():
    return psycopg2.connect(f"dbname='{DBNAME}' user='{USER}' host='localhost'")

@app.route('/')
def home_page():
    try:
        conn = connect()
        return f'<p>connected to database</p>'
    except Exception as e:
        return f'<p>Unable to connect to database:</p> <p style="color:red">{e}</p>'


@app.route('/customer/create')
def create_customer():
    # customer = request.args.get('customer')
    # password = request.args.get('pwd')
    # tenant_id = request.args.get('tenant_id')
    args, argerr = require_args('customer', 'pwd', 'tenant_id')
    if argerr:
        return argerr
    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(f"""
insert into customer (name, password, tenant_id)
values ('{args['customer']}', '{args['pwd']}', {args['tenant_id']}) returning *;
        """)
        conn.commit()
        return r_ok({"customer": cursor.fetchone()})

        if conn:
            conn.rollback()
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'
    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'

@app.route("/family/create")
def family_create():
    args, argerr = require_args('customer', 'pwd')
    if argerr:
        return argerr
    args['family_id'] = request.args.get('family_id')

    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()
        
        cursor.execute(f"select tenant_id from customer where name = '{args['customer']}' AND password = '{args['pwd']}'");
        row = cursor.fetchone()
        tenant_id = None

        if row is None:
            return r_bad_request({"message": "could not find customer tenant_id"})

        tenant_id = row[0]

        if tenant_id is None:
            return "<p> Failed because customer tenant_id is None </p>"

        q = f"""
        SELECT * FROM family WHERE
            member1_id = '{args['customer']}' OR
            member2_id = '{args['customer']}' OR
            member3_id = '{args['customer']}' OR
            member4_id = '{args['customer']}';
        """
        print(q);
        cursor.execute(q)
        row = cursor.fetchone()
        print("family row", row)
        if row is not None:
            conn.rollback()
            return r_bad_request({
                "message": "user is already part of family"})
        q = f"""
            INSERT INTO family (
                tenant_id, 
                member1_id 
                {', id' if args['family_id'] else ''})
            VALUES (
                {tenant_id},
                '{args['customer']}'
                {',' + args['family_id'] if args['family_id'] else ''}
                ) RETURNING *; 
        """
        cursor.execute(q)

        family = cursor.fetchone()
        print("inserted family:", family, type(family))
        family_id = family[1]
        q = f"""
            UPDATE customer 
            SET family_id = {family_id} 
            WHERE name = '{args['customer']}' AND password = '{args['pwd']}';
        """
        cursor.execute(q)
        conn.commit()
        return r_ok({"family": family})

    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'


@app.route('/family/join')
def family_join():
    args, argerr = require_args('customer', 'pwd', 'family_tenant_id', 'family_id')
    if argerr:
        return argerr
    customer = args['customer']
    pwd = args['pwd']
    family_tenant_id = args['family_tenant_id']
    family_id = args['family_id']
    try:
        with connect() as conn:
            cursor = conn.cursor()

            q = f"""
            SELECT * FROM family WHERE
                member1_id = '{customer}' OR
                member2_id = '{customer}' OR
                member3_id = '{customer}' OR
                member4_id = '{customer}';
            """
            print(q);
            cursor.execute(q)
            family = cursor.fetchone()
            if family is not None:
                return r_bad_request({
                    "message": f"{customer} is already in a family"
                    })

            q = f"""
            SELECT member1_id, member2_id, member3_id, member4_id FROM family WHERE
                tenant_id = {family_tenant_id} AND
                id = {family_id};
            """
            print(q)
            cursor.execute(q)
            insert_family = cursor.fetchone()
            print('insert_family', insert_family)
            if insert_family is None:
                print("bad request")
                return r_bad_request({'message': 'family does not exist'})
            i = 1
            while i <= 4 and insert_family[i-1] is not None:
                i += 1
                print(i)

            if i > 4:
                return r_bad_request({
                    "message": "family is full"
                    })
            q = f"""
                UPDATE customer 
                SET family_id = {family_id}
                WHERE 
                    name = '{customer}' AND
                    password = '{pwd}'
                RETURNING *;
            """
            print(q)
            cursor.execute(q)
            if cursor.fetchone() is None:
                return r_bad_request({
                    'message': 'failed to update user family_id'})
            q = f"""
                UPDATE family
                SET member{i}_id = '{args['customer']}'
                WHERE 
                    tenant_id = {family_tenant_id} AND
                    id = {family_id} 
                RETURNING *;
            """
            print(q)
            cursor.execute(q)

            f = cursor.fetchone()
            conn.commit()
            return r_ok({'family': f})

    except Exception as e:
        print(e)
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'


@app.route('/user/validate/<string:username>')
def validate_user(username):
    return f'<p>validating user {username}</p>'

