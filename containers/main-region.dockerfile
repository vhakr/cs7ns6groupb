from cafe-app-base 

workdir /app/pgdata
user postgres
run initdb -D c1

copy mybin /app/bin

entrypoint /app/bin/app-entrypoint.sh

copy init.sql /app/init.sql

run app-start-node c1 && psql -f /app/init.sql && app-stop-node c1
