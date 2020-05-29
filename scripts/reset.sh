docker-compose down
docker rm $(docker ps -a -q)
docker volume rm $(docker volume ls -qf dangling=true)
rm -rf vol/*
