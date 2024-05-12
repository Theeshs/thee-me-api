#!/bin/bash
echo "deleting old deployment"
sudo rm -rf /var/www/thee-protfolio

echo "creating app folder again"
sudo mkdir /var/www/thee-protfolio

echo "moving files to app folder"
sudo mv * /var/www/thee-protfolio

cd var/www/thee-protfolio/
sudo mv env .env

echo "removing old deployment docker"
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

echo "removing old docker image"
docker rmi $(docker images -q)

echo "pruning docker system"
docker system prune -a -y

echo "starting service"
sudo docker compose up

#if ! command -v nginx > /dev/null; then
#  echo "nginx is not installed"
#  echo "installing nginx"
#  sudo apt-get update
#  sudo apt-get install nginx
#fi
#
#if [ ! -f /etc/nginx/sites-enabled/default ]; then
#  echo "removing default nginx configuration"
#  sudo rm /etc/nginx/sites-enabled/default
#  sudo bash -c 'cat > /etc/nginx/sites-available/thee-protfolio <<EOF
#  server {
#    listen 80;
#    server_name _;
#
#    location / {
#      include proxy_params;
#      proxy_pass http://unix:/var/www/thee-protfolio/thee-protfolio.sock;
#    }
#
#  }
#  EOF'
#
#fi

