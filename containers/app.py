#!/usr/bin/env python3
from flask import Flask, request, Response
import psycopg2
import json
import datetime
import math

def r_bad_request(obj, status=400, mimetype="application/json", format=json.dumps):
    print(obj)
    return Response(format(obj), status=status, mimetype=mimetype)

def r_internal_server_error(obj, status=500, mimetype="application/json", format=json.dumps):
    return Response(format(obj), status=status, mimetype=mimetype)

def r_nyi(status=500, mimetype='application/json', format=json.dumps):
    return Response(format({"message": "Not Yet Implemented"}), status=status, mimetype=mimetype)

def r_ok(obj, status=200, mimetype="application/json", format=json.dumps):
    o = "ok" if obj is None else obj
    return Response(format(o), status=status, mimetype=mimetype)

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
values ('{args['customer']}', '{args['pwd']}', '{args['tenant_id']}') returning *;
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
                '{tenant_id}',
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
                tenant_id = '{family_tenant_id}' AND
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
                    tenant_id = '{family_tenant_id}' AND
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

@app.route('/family/purchase')
def family_purchase():
    args, argerr = require_args('till', 'till_pwd', 'customer', 'pwd', 'amount_euro_equivalent')
    if argerr:
        return argerr
    conn = None
    try:
        with connect() as conn:
            cursor = conn.cursor()

            # TODO authenticate till

            # TODO authenticate customer

            q = f"""
                SELECT tenant_id, name FROM customer WHERE
                    name = '{args['customer']}' AND
                    password = '{args['pwd']}';
            """
            cursor.execute(q)
            c = cursor.fetchone()
            print("customer", c)
            if c is None:
                return r_bad_request({
                    'message': 'failed to authenticate customer'
                })
            ctenant_id, cname = c


            q = f"""
                SELECT tenant_id, id FROM family WHERE
                    member1_id = '{args['customer']}' OR
                    member2_id = '{args['customer']}' OR
                    member3_id = '{args['customer']}' OR
                    member4_id = '{args['customer']}';
            """
            cursor.execute(q)
            f = cursor.fetchone()
            if f is None:
                return r_bad_request({
                    'message': 'customer is not in a family'})
            print("family", f)
            ftenant_id, fid = f
            # CREATE TABLE purchase (
            #     tenant_id INT, id INT,
            #     family_id INT,
            #     customer_tenant_id INT, customer_name VARCHAR(255),
            #     amount_euro_equivalent DECIMAL,
            #     PRIMARY KEY (tenant_id, id)
            # );
            amount = args['amount_euro_equivalent']
            q = f"""
                INSERT INTO purchase ( tenant_id,   family_id, customer_tenant_id, customer_name, amount_euro_equivalent) VALUES
                                     ('{ftenant_id}',{fid     },'{ctenant_id       }','{cname       }',{amount})
                RETURNING amount_euro_equivalent;
            """
            print(q)
            cursor.execute(q)
            p = cursor.fetchone()
            conn.commit()
            print(p)
            p = float(p[0])
            return r_ok({'purchase_amount': p})

    except Exception as e:
        print(e)
        if conn:
            conn.rollback()
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'

def timestamp_n_seconds_ago(n):
    current_time = datetime.datetime.now()
    time_delta = datetime.timedelta(seconds=n)
    timestamp = current_time - time_delta
    return timestamp.timestamp()

print(timestamp_n_seconds_ago(1))

# /family/voucher
# requires authentication of user (via loyalty card)
# requires authentication of till (outside of scope of project - we’ll just assume the request came from a till)
# returns the total reduction in payment the till is authorised to issue, this payload is signed cryptographically
# the till can validate this payload cryptographically before reducing the balance due by the customer for the purchase
@app.route('/family/voucher')
def family_voucher():
    args, argerr = require_args('till', 'till_pwd', 'customer', 'pwd', 'subtotal')
    if argerr:
        return argerr

    subtotal = None
    try:
        subtotal = float(args['subtotal'])
    except Exception:
        return r_bad_request({'message': 'could not parse subtotal as float'})

    conn = None
    from datetime import datetime, timedelta

    try:
        with connect() as conn:
            cursor = conn.cursor()

            # TODO authenticate till

            q = f"""
                SELECT tenant_id, name, family_id FROM customer WHERE
                    name = '{args['customer']}' AND
                    password = '{args['pwd']}';
            """
            cursor.execute(q)
            c = cursor.fetchone()
            print("customer", c)
            if c is None:
                return r_bad_request({
                    'message': 'failed to authenticate customer'
                })
            ctenant_id, cname, family_id = c
            since = timestamp_n_seconds_ago(6) # TODO: in production use 60*60*24*21 (21 days)
            q = f"""
                SELECT amount_euro_equivalent, timestamp FROM purchase WHERE
                    tenant_id = '{ctenant_id}' AND
                    family_id = {family_id} AND
                    timestamp > {since};
            """
            cursor.execute(q)
            purchases = cursor.fetchall()
            if purchases is None:
                return r_ok({
                    'order_total': subtotal,
                    'discount_percent': 0,
                    'subtotal': subtotal,
                })
            conn.commit()
            print(purchases)
            purchases = map(lambda x: x[0], purchases)
            discount_percent = min(50, int(math.floor(sum(map(float, purchases)))))
            discount_decimal = discount_percent / 100
            if discount_percent < 0:
                return r_internal_server_error({
                    'message': 'total purchases negative'
                })
            return r_ok({
                'order_total': subtotal - (discount_decimal * subtotal),
                'discount_percent': discount_percent,
                'subtotal': subtotal,
            })

    except Exception as e:
        print(e)
        if conn:
            conn.rollback()
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'
