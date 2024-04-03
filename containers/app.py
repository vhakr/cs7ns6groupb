#!/usr/bin/env python3
from flask import Flask, request
import psycopg2

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
    customer = request.args.get('customer')
    password = request.args.get('pwd')
    tenant_id = request.args.get('tenant_id')
    print(customer, password, tenant_id)
    if customer == None or password == None: 
        return f'<p>Incomplete customer data provided</p>'
    tenant_id = f'{tenant_id}' if tenant_id is not None else '0'
    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(f"""
insert into customer (name, password, tenant_id)
values ('{customer}', '{password}', {tenant_id})
        """)
        conn.commit()
        return f'<p>creating customer: {customer}, password: {password}</p>'
    except Exception as e:
        if conn:
            conn.rollback()
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'

@app.route("/family/create")
def family_create():
    customer = request.args.get('customer')
    password = request.args.get('password')
    # print(password)
    # if password is None:
    #     return "<p>Authentication failed</p>"

    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()
        
        cursor.execute(f"select tenant_id from customer where name = '{customer}' AND password = 'pwd'");
        row = cursor.fetchone()
        tenant_id = None
        if row is not None and len(row) == 1:
            tenant_id = row[0]

        if row is None:
            return "<p> Failed to authenticate </p>"

        if len(row) > 1:
            return "<p> Failed because too many users </p>"

        if tenant_id is None:
            return "<p> Failed because customer tenant_id is None </p>"

        q = f"""
        SELECT * FROM family WHERE
            member1_id = '{customer}' OR
            member2_id = '{customer}' OR
            member3_id = '{customer}' OR
            member4_id = '{customer}';
        """
        print(q);
        cursor.execute(q)
        row = cursor.fetchone()
        print("family row", row)
        if row is None:
            q = f"""
                INSERT INTO family (tenant_id, member1_id) VALUES ({tenant_id}, '{customer}') RETURNING *; 
            """
            cursor.execute(q)

            family = cursor.fetchone()
            print("inserted family:", family, type(family))
            print(family[0], family[1])
            family_id = family[1]
            q = f"""
                UPDATE customer 
                SET family_id = {family_id} 
                WHERE name = '{customer}' AND password = '{password}';
            """
            cursor.execute(q)
        else:
           conn.rollback()
           return f"<p> Failed: {row} </p>"

        conn.commit()
        return f"<p> Created family: {family} </p>"

    except Exception as e:
        if conn:
            conn.rollback()
        print(e)
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'


@app.route('/family/join')
def family_join():
    customer = request.args.get('customer')
    password = request.args.get('password')
    family_tenant_id = request.args.get('family_tenant_id')
    family_id = request.args.get('family_id')

    conn = None
    try:
        conn = connect()
        cursor = conn.cursor()
    except Exception as e:
        if conn:
            conn.rollback()
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'


@app.route('/user/validate/<string:username>')
def validate_user(username):
    return f'<p>validating user {username}</p>'

