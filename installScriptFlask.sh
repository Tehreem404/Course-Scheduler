#!/usr/bin/env bash

cd cis3760-website/api

python3 -m venv venv
source venv/bin/activate

pip install boto3
pip install requests
pip install wheel
pip install gunicorn flask
pip install pylint
pip install pre-commmit
pre-commit install

deactivate

pre-commit install
sudo apt install pre-commit -y
sudo npm install -g install-peerdeps
sudo install-peerdeps --dev eslint-config-airbnb -n
sudo install-peerdeps --dev eslint-config-airbnb-base -n

sudo cp /home/ubuntu/cis-3760/cis3760-website/api/flask.service /etc/systemd/system/ 

chown -R ubuntu:www-data /home/ubuntu/cis-3760/cis3760-website/api
chmod -R 775 /home/ubuntu/cis-3760/cis3760-website/api

sudo systemctl daemon-reload
sudo systemctl start flask
sudo systemctl enable flask

systemctl status flask

sudo nginx -t
sudo systemctl restart nginx
