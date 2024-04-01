from cafe-app-base 

workdir /app/pgdata
user postgres
run initdb -D c1
copy confs/main_coordinator.pgsqlconf /app/pgdata/c1/postgresql.conf

copy mybin /app/bin

entrypoint /app/bin/app-entrypoint.sh

copy main_coordinator_init.sql /app/init.sql

run app-init-main-coordinator
