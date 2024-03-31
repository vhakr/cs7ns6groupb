mkdir -p tmp
echo "SELECT create_distributed_table('family',   'id');" > ./tmp/cmd.sql
psql -h localhost -U postgres -d postgres -f ./tmp/cmd.sql
