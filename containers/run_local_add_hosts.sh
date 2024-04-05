worker_ip=$(docker inspect app-worker | jq '.[0].NetworkSettings.Networks.bridge.IPAddress' | sed "s,\",,g")
worker2_ip=$(docker inspect app-worker2 | jq '.[0].NetworkSettings.Networks.bridge.IPAddress' | sed "s,\",,g")
coordinator_ip=$(docker inspect app-coordinator | jq '.[0].NetworkSettings.Networks.bridge.IPAddress' | sed "s,\",,g")

docker exec --user root app-worker sh -c "echo '$coordinator_ip neimhin' >> /etc/hosts"
docker exec --user root app-worker2 sh -c "echo '$coordinator_ip neimhin' >> /etc/hosts"
docker exec --user root app-coordinator sh -c "echo '$coordinator_ip neimhin' >> /etc/hosts"
