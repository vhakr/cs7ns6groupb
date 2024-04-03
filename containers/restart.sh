docker rm app
docker build -t cafe-app-neimhin -f neimhin.dockerfile .  && docker run --name app -it --network host cafe-app-neimhin
