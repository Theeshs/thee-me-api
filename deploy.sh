#!/bin/bash
echo "removing old deployment docker"
sudo docker stop TheeMeAPI

echo "pruning docker system"
yes | sudo docker system prune -a

echo "deleting old deployment"
sudo rm -rf ./thee-portfolio

echo "creating app folder again"
sudo mkdir ./thee-protfolio

echo "moving files to app folder"
sudo mv * ./thee-portfolio

echo "moving env file"
cd ./thee-portfolio
sudo mv env .env

echo "starting service"
sudo docker compose up
exit 0

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

