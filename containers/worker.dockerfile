from neimhin/cafe-app:base

workdir /app/pgdata
user postgres
run initdb -D w1
copy confs/w1.pgsqlconf /app/pgdata/w1/postgresql.conf
user root
run echo "host all all 0.0.0.0/0 trust" >> /app/pgdata/w1/pg_hba.conf
user postgres

copy mybin /app/bin

entrypoint /app/bin/app-entrypoint.sh

copy worker_init.sql /app/init.sql
copy app.py /app/app.py

run app-init-cian
