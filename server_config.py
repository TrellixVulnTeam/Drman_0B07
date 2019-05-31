# ---------------------------- 1.Edit hosts & hostname ---------------------------------
#  sudo nano /etc/hosts :
# 193.176.242.97 roposha.com
# 193.176.242.97 ubuntu

# sudo nano /etc/hostname
# roposha.com
# ubuntu

# sudo service hostname restart

# ---------------------------- 2.apache config ---------------------------------
# sudo nano /etc/apache2/sites-available/mysite.conf
# <VirtualHost *:80>
#     ServerName roposha.com
#     ServerAlias www.roposha.com
#
#     ErrorLog ${APACHE_LOG_DIR}/mysite-error-test.log
#     CustomLog ${APACHE_LOG_DIR}/mysite-access-test.log combined
#
#     WSGIDaemonProcess mysite processes=2 threads=25 python-path=/var/www/mysite
#     WSGIProcessGroup mysite
#     WSGIScriptAlias / /var/www/mysite/mysite/wsgi.py
#     Alias /robots.txt /var/www/mysite/static/robots.txt
#     Alias /favicon.ico /var/www/mysite/static/favicon.ico
#     Alias /static/ /var/www/mysite/static/
#     Alias /static/ /var/www/mysite/media/

#    <Directory /var/www/mysite/mysite>
#    <Directory /var/www/mysite/mysite>
#        <Files wsgi.py>
#            Require all granted
#        </Files>
#    </Directory>
#
#    <Directory /var/www/mysite/static>


# a2ensite mysite
# sudo systemctl reload apache2

# tail -f /var/log/apache2/mysite-error.log

# ---------------------------- 3.hostname server ---------------------------------
# sudo hostname roposha.com
# hostname

# login with root to server
# sudo su

# ---------------------------- 3.resolv.conf ---------------------------------
# sudo nano /etc/resolvconf/resolv.conf.d/tail
# domain roposha.com
# nameserver 193.176.242.97
# sudo resolvconf -u

# then /etc/resolv.conf generate like this :
# nameserver 8.8.8.8
# search openstacklocal
# domain echoteb.ir
# nameserver 193.176.242.97

# ---------------------------- 4.nginx.conf ---------------------------------
# /etc/nginx/sites-available/nginx.conf
# sudo nano /etc/nginx/conf.d/nginx.conf
# upstream hello_django {
#     server 193.176.242.97:8000;
# }
#
# server {
#
#     listen 80;
#     root /var/www/Drman/Doctors/templates/;
#     index index.html index.htm;
#     server_name roposha.com www.roposha.com;
#
#     location / {
#         proxy_pass http://hello_django;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header Host $host;
#         proxy_redirect off;
#     }
#
#     location /static/ {
#         alias /var/www/Drman/static/;
#         autoindex on;
#     }
#
# }


# sudo service nginx restart

# ---------------------------- 4. Change DNS to pull docker image ---------------------------------
# sudo nano /etc/resolvconf/resolv.conf.d/tail
# nameserver 94.232.174.194
# nameserver 178.22.122.100
# nameserver 8.8.8.8
# nameserver 8.8.8.4
# nameserver 193.176.242.97


# then /etc/resolv.conf generate like this :
# notice: order of nameserver is important
# search openstacklocal
# nameserver 94.232.174.194
# nameserver 178.22.122.100
# nameserver 8.8.8.8
# nameserver 8.8.8.4
# nameserver 193.176.242.97


# emaple pf docker pull :
# sudo docker-compose up -d --build
# sudo docker pull elastic/elasticsearch:6.4.1
# sudo docker pull kibana:6.4.1

# ---------------------------- 5.kibana conf ---------------------------------

# for start kibana to work greate we should :
# 1. make mapping with code in kibana
# 2. create index maually

# 1. sudo docker-compose up -d --build
# 2. sudo docker-compose up

# ---------------------------- 5.go to Psql shell ---------------------------------
# psql
# psql -U postgres
# \dt
# SELECT * FROM auth_user;

# ---------------------------- 5.Configure SSL ---------------------------------

# https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html
# sudo ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled
# sudo /etc/init.d/nginx restart

# https://www.digitalocean.com/community/tutorials/how-to-set-up-let-s-encrypt-with-nginx-server-blocks-on-ubuntu-16-04
# https://geekflare.com/setup-nginx-with-lets-encrypt-cert/

# see the sudo nano /etc/nginx/sites-enabled/nginx.conf and upload following files to arvancloud :
#     ssl_certificate /etc/letsencrypt/live/echoteb.ir/fullchain.pem; # managed by Certbot
#     ssl_certificate_key /etc/letsencrypt/live/echoteb.ir/privkey.pem; # managed by Certbot

# sudo certbot renew --dry-run

# ---------------------------- 5.Configure SSL (work like a charm) ---------------------------------

# 1. follow these giudelines :
# 2. https://sigmoidal.io/setting-up-ssl-with-nginx-and-letsencrypt-for-your-website/
# 3. https://www.sslforfree.com

# 4. first configure your nano /etc/nginx/sites-enabled/nginx.conf like this (important part is add location /.well-known)
# upstream hello_django {
#     server 193.176.242.97:8000;
# }
#
# server {
#
#     listen 80 ;
#     root /var/www/Drman/Doctors/templates/;
#     index index.html index.htm;
#     server_name  echoteb.ir;
#
#     location / {
#         proxy_pass http://hello_django;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header Host $host;
#         proxy_redirect off;
#     }
#
#     location /static/ {
#         alias /var/www/Drman/static/;
#         autoindex on;
#     }
#
#     location /.well-known {
#         alias /var/www/Drman/.well-known/;
#     }
# }

# 5. follow guidelines site step
# 6. finally /etc/nginx/sites-enabled/nginx.conf should be like :

# upstream hello_django {
#     server 193.176.242.97:8000;
# }
#
# server {
#     listen 80 default_server;
#     return 444;
# }
#
# server {
#
#     listen 80;
#     server_name echoteb.ir;
#     root /var/www/Drman/Doctors/templates/;
#     index index.html index.htm;
#     return         301 https://echoteb.ir$request_uri;
#
# }
#
# server {
#
#     listen 443 ssl;
#     server_name echoteb.ir;
#     root /var/www/Drman/Doctors/templates/;
#     index index.html index.htm;
#     return         301 https://echoteb.ir$request_uri;
#
# }
#
# server {
#
#     listen 443 ssl;
#     server_name echoteb.ir;
#
#     # location of key and certificate files
#     ssl_certificate /etc/nginx/ssl/certificate.crt;
#     ssl_certificate_key /etc/nginx/ssl/privkey.key;
#
#     # cache ssl sessions
#     ssl_session_cache  builtin:1000  shared:SSL:10m;
#
#     # prefer server ciphers (safer)
#     ssl_prefer_server_ciphers on;
#
#     # important! protects your website against MITM attacks.
#     add_header Strict-Transport-Security "max-age=604800";
#     location / {
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header Host $http_host;
#         proxy_pass http://hello_django;
#     }
#
#     location /static/ {
#         alias /var/www/Drman/static/;
#         autoindex on;
#     }
#
#     location /.well-known {
#        alias /var/www/Drman/.well-known/;
#    }
# }


# 7. go to arvancloud and use "customized and manuall user for domain" and add (.key , .crt)