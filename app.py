from flask import Flask, request
import psycopg2

LEADERSERVER = ""
app = Flask(__name__)

DBNAME = 'template1'
USER = 'postgres'

@app.route('/')
def home_page():
    try:
        conn = psycopg2.connect(f"dbname='{DBNAME}' user='{USER}'")
        return f'<p>connected to database</p>'
    except Exception as e:
        return f'<p>Unable to connect to database:</p> <p style="color:red">{e}</p>'


@app.route('/customer/create')
def create_customer():
    customer = request.args.get('customer')
    pwd = request.args.get('pwd')
    region = request.args.get('region')
    if customer == None or pwd == None: 
        return f'<p>Incomplete customer data provided</p>'
    if region == None:
        region = 'null'
    else: region = f'{region}'
    try:
        conn = psycopg2.connect("dbname='template1' user='postgres'")
        cursor = conn.cursor()

        cursor.execute(f"""
insert into customer (customer_name, password, region)
values ('{customer}', '{pwd}', {region})
        """)
        conn.commit()
        return f'<p>creating customer: {customer}, password: {pwd}</p>'
    except Exception as e:
        return f'<p>Unable to complete action:</p> <p style="color:red">{e}</p>'


@app.route('/user/validate/<string:username>')
def validate_user(username):
    return f'<p>validating user {username}</p>'

