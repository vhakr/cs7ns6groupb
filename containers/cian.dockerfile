from cafe-app-base 

workdir /app/pgdata
user postgres
run initdb -D w1
copy confs/w1.pgsqlconf /app/pgdata/w1/postgresql.conf

copy mybin /app/bin

entrypoint /app/bin/app-entrypoint.sh

copy worker_init.sql /app/init.sql

run app-init-cian
