# Flask_Practice
Object Detection REST full API Using Keras + Flask + uWSGI + nginx 

---
### Environments
* Ubuntu 16.04
* python 3.7
* virtualenv

---
### Requirements
* Flask==1.1.1
* h5py==2.10.0
* Keras==2.3.1
* matplotlib==3.1.1
* numpy==1.16.5
* opencv-python==4.1.1.26
* opencv-contrib-python==4.1.1.26
* pandas==0.25.1
* Pillow==6.2.0
* tensorflow-gpu==2.0.0
* tqdm==4.37.0
* uWSGI==2.0.18

---
### How to Use
* Install Flask, uWSGI, nginx 
  ```shell
  $ virtualenv [env_name] --python=python3.7
  $ source [env_name]/bin/activate
  $ pip install Flask
  $ pip install uWSGI
  $ sudo apt install nginx

  # nginx status check
  $ sudo service nginx status
  ```
  
* Setting Config
  * Manually
  ```shell
  $ cd setting_files
  
  # systemd uwsgi service setting
  sed "s/\[user_name\]/$USER_NAME/g" flaskapp.service.ori > flaskapp.service
  sed -i "s/\[path_to_project\]/\/home\/$USER_NAME\/keras-flask-api/g" flaskapp.service
  sed -i "s/\[path_to_virtualenv]/\/home\/$USER_NAME\/$ENV_NAME/g" flaskapp.service

  sudo cp flaskapp.service /etc/systemd/system/
  rm flaskapp.service

  sudo systemctl enable flaskapp
  sudo systemctl start flaskap
  
  # nginx service setting
  sudo cp custom_timeout.conf /etc/nginx/conf.d/

  sed "s/\[path_to_project\]/\/home\/$USER_NAME\/keras-flask-api/g" nginx_server.ori > nginx_detection_server

  sudo cp nginx_detection_server /etc/nginx/sites-available/
  sudo rm /etc/nginx/sites-enabled/*
  sudo ln -s /etc/nginx/sites-available/nginx_detection_server /etc/nginx/sites-enabled/nginx_detection_server

  rm nginx_detection_server
  ```
  
  * Using script
  ```shell
  $ cd setting_files
  $ ./set_config.sh [user name] [virtualenv name]
  ```

* Server Operation
  * Manually
  ```shell
  # server start
  $ sudo service nginx start
  $ sudo service flaskapp start
  
  # server stop
  $ sudo service nginx stop
  $ sudo service flaskapp stop
  
  # server restart
  $ sudo service nginx restart
  $ sudo service flaskapp restart
  
  ```
  
  * Using script
  ```shell
  $ cd [path to proejct]
  $ ./server_restart.sh
  ```
