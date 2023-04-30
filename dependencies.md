# Stack
nginx
pyenv
gunicorn
uvicorn
ufw
rabbitmq
python 3.11.3
	- Django
	- Django-Rest-Framework
	- gunicorn
	- uvicorn
	- celery








### Nginx Set Up

Install 
```
sudo apt-get install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```




```
sudo vim /etc/nginx/sites-available/project
server {
	listen 80;
	server_name IP_ADDRESS;

	location = /favicon.ico { access_log off; log_not_found off;}
	location /static/ {
		PATH_TO_STATIC_DIR;
	}

	location / {
		include proxy_params;
		proxy_pass http://unix:/run/gunicorn.sock;
	}
}
```
- Link file to sites enabled
```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```


- Test config
```
sudo nginx -t
```

- Allow nginx through ufw
```
sudo ufw allow 'Nginx Full'
```


### Gunicorn Socket and Service set up

- Socket
```
sudo vim /etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

- Service

```
sudo vim /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target



[Service]
User=mrrobot
Group=www-data
WorkingDirectory=/home/mrrobot/websites/rpiserver
ExecStart=gunicorn \
	--access-logfile - \
	-k uvicorn.workers.UvicornWorker \
	--workers 3 \
	--bind unix:/run/gunicorn.sock \
	rpiserver.asgi:application

[Install]
WantedBy=multi-user.target
```

- Start command
```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

- View service
```
sudo systemctl status gunicorn.socket
```

- Check Gunicorn logs
```
sudo journalctl -u gunicorn.socket
```

- Restart
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

### RabbitMQ server
```
sudo apt-get install rabbitmq-server
```

add user

```
sudo rabbitmqctl add_user <user> <password>
```

create virtualhost
```
sudo rabbitmqctl add_vhost <vhostname>
```

set permissions
```
sudo rabbitmqctl set_permissions -p <vhost> <user> <".*" ".*" ".*">
```

 "broker_url = 'amqp://myuser:mypassword@localhost:5672/myvhost'


