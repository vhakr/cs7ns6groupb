set +e
docker kill app-coordinator
docker kill app-worker
docker kill app-worker2
docker rm app-coordinator
docker rm app-worker
docker rm app-worker2

set -e
docker run -td \
  --name app-coordinator \
  --network bridge \
  -p 80:5000 \
  -p 5432:5432 \
  neimhin/cafe-app:neimhin

docker run -td \
  --name app-worker \
  --network bridge \
  -p 81:5000 \
  -p 9701:5432 \
  neimhin/cafe-app:worker

docker run -td \
  --name app-worker2 \
  --network bridge \
  -p 82:5000 \
  -p 9702:5432 \
  neimhin/cafe-app:worker

worker_ip=$(docker inspect app-worker | jq '.[0].NetworkSettings.Networks.bridge.IPAddress' | sed "s,\",,g")
worker2_ip=$(docker inspect app-worker2 | jq '.[0].NetworkSettings.Networks.bridge.IPAddress' | sed "s,\",,g")
coordinator_ip=$(docker inspect app-coordinator | jq '.[0].NetworkSettings.Networks.bridge.IPAddress' | sed "s,\",,g")

docker exec --user root app-worker sh -c "echo '$coordinator_ip neimhin' >> /etc/hosts"
docker exec --user root app-worker2 sh -c "echo '$coordinator_ip neimhin' >> /etc/hosts"
docker exec --user root app-coordinator sh -c "echo '$coordinator_ip neimhin' >> /etc/hosts"
. test_api.sh
sleep 0.2
docker exec app-coordinator psql -c "select master_add_node('$worker_ip', 5432);"
docker exec app-coordinator psql -c "select master_add_node('$worker2_ip', 5432);"
docker exec app-coordinator psql -c "BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED; select rebalance_table_shards(); COMMIT;"
