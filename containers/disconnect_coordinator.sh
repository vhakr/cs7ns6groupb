netns_id=$(docker inspect -f '{{.NetworkSettings.SandboxKey}}' app-coordinator)
echo $netns_id
sudo ip netns exec $netns_id ip link set eth0 down

docker inspect app-coordinator | jq '.[0].NetworkSettings.Networks'
