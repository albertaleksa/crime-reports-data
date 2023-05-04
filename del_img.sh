docker stop my-crime-trends-container
docker rm my-crime-trends-container
docker rmi $(docker images crime-trends -q)