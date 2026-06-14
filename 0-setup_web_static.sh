#!/usr/bin/env bash
# Sets up the web servers for the deployment of web_static

apt-get -y update
apt-get -y install nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

printf '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>\n' > /data/web_static/releases/test/index.html

rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html index.htm;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }

    location / {
        try_files \$uri \$uri/ =404;
    }
}
" > /etc/nginx/sites-available/default

service nginx restart