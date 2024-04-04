from neimhin/cafe-app:base

workdir /app/pgdata
user postgres
run initdb -D c1
run echo "host all all 0.0.0.0/0 trust" >> c1/pg_hba.conf
copy confs/main_coordinator.pgsqlconf /app/pgdata/c1/postgresql.conf

copy mybin /app/bin

entrypoint /app/bin/app-entrypoint.sh

copy main_coordinator_init.sql /app/init.sql

run app-init-main-coordinator

copy app.py /app/app.py
