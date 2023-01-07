#!/usr/bin/env bash

echo "Downloading nvm"
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

source ~/.bashrc

echo "==> Checking for versions"
nvm --version
node --version
npm --version

echo "==> Print binary paths"
which npm
which node
which yarn

sudo apt-get update -y
sudo apt-get upgrade -y

nvm install 16
sudo apt-get install nodejs -y
sudo apt-get install npm -y
npm install
npm install create-react-app
npm install react
npm install react-dom
npm install react-scripts
npm install web-vitals
npm i --save @devexpress/dx-react-core @devexpress/dx-react-scheduler
npm i --save @devexpress/dx-react-scheduler-material-ui
npm install @material-ui/core
npm install babel-plugin-inline-react-svg --save-dev

echo "At bottom of downloads"
########################################

echo "==> installing pip"
sudo apt-get install python3-pip

echo "==> adding react bootstrap"
npm install react-bootstrap bootstrap

echo "==> installing yarn"
corepack enable
yarn init -2

echo "==> setting up flask env"
cd /home/ubuntu/cis-3760/cis3760-website

sudo python3 -m venv venv
source venv/bin/activate

sudo apt-get install python3-venv
sudo apt-get install nginx -y

sudo apt install python3-flask
sudo apt install gunicorn
sudo apt install pre-commit -y
sudo npm install -g install-peerdeps
sudo install-peerdeps --dev eslint-config-airbnb -n
sudo install-peerdeps --dev eslint-config-airbnb-base -n

npm run build

sudo cp -r /home/ubuntu/cis-3760/cis3760-website/build /var/www/html/

sudo systemctl enable nginx

sudo cp -r /home/ubuntu/cis-3760/cis3760-website/build /var/www/html
sudo cp -a /home/ubuntu/cis-3760/cis3760-website/api/nginx.conf /etc/nginx/nginx.conf

sudo useradd -r nginx
sudo nginx -t

sudo systemctl restart nginx
#Run React Project at ec2 IPv4 (Public) Custom Address
#sudo systemctl enable nginx
