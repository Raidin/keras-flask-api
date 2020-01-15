#!/bin/bash
USER_NAME=$1
ENV_NAME=$2

if [ -z "$USER_NAME" ] || [ -z "$ENV_NAME" ]; then
    echo -e "[Error] Argument is not entered.\n Usage :: ./set_config [user name] [virtual env name]"
    exit
fi

echo " - USER_NAME : $USER_NAME"
echo " - ENV_NAME : $ENV_NAME"

# systemd unit setting
sed "s/\[user_name\]/$USER_NAME/g" flaskapp.service.ori > flaskapp.service

sed -i "s/\[path_to_project\]/\/home\/$USER_NAME\/keras-flask-api/g" flaskapp.service

sed -i "s/\[path_to_virtualenv]/\/home\/$USER_NAME\/$ENV_NAME/g" flaskapp.service

sudo cp flaskapp.service /etc/systemd/system/
rm flaskapp.service

sudo systemctl enable flaskapp
sudo systemctl start flaskapp

# nginx service setting
sudo cp custom_timeout.conf /etc/nginx/conf.d/

sed "s/\[path_to_project\]/\/home\/$USER_NAME\/keras-flask-api/g" nginx_server.ori > nginx_detection_server

sudo cp nginx_detection_server /etc/nginx/sites-available/
sudo rm /etc/nginx/sites-enabled/*
sudo ln -s /etc/nginx/sites-available/nginx_detection_server /etc/nginx/sites-enabled/nginx_detection_server

rm nginx_detection_server

echo "Completed Setting..."