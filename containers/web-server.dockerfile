from debian:latest

run apt-get update
run apt-get install -y python3
run apt-get install -y python3-pip
run apt-get install -y postgresql-server-dev-all
run apt-get install -y python3-flask
run apt-get install -y python3-psycopg2

run mkdir -p /app
copy app.py /app/app.py
copy web-server-entrypoint.sh /app/

entrypoint /app/web-server-entrypoint.sh
