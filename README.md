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
  
