# Monolithic application with balanced and distributed data (DB and files)


## Course Details


| Information  |                   |
|--------------|      :-----:      |
| Name    | Sebastian Guerra - Juan David Prieto - Juan David Echeverri - Jacobo Rave Londoño |
| Email   | jsguerrah@eafit.edu.co - jdprietom@eafit.edu.co - jdecheverv@eafit.edu.co - jravel@eafit.edu.co |
| Teacher | Edwin Montoya          |
| Course  | ST0263                 |

## Description

The project was created to practice the deployment of a Monolithic application with balanced and distributed data, for this case a CMS was deployed using container technology, with its own domain.

The information and parameters of the project criteria are in the teacher's domain. In view of this situation, it remains to say that in this project all the considerations required by the teacher are completely fulfilled.

## Development
### DB Config
The following codeblock is the one used to configurate the docker instance in the db machine. 
```yml
version: '3.8'
services:
db:
image: postgres:14.1-alpine
restart: always
environment:
- POSTGRES_USER=postgres
- POSTGRES_PASSWORD=postgres
ports:
- '5432:5432'
volumes:
- db:/var/lib/postgresql/data
volumes:
db:
driver: local
```
And then run 
```cmd
docker-compose up -d
```

Then, we need to access the docker instance with 
```cmd
docker exec -it ID_DE_TU_CONTENEDOR /bin/bash
```
So we can run the following commands needed to setup the DB:
```
apk update
apk add postgresql-contrib
psql -U postgres -d mi_basedatos -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"
```
Finally, we just run `exit`and save the id of the instance for later

### NFS Config

In this step, we just followed the instruction in the [NFS tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04#step-7-mounting-the-remote-nfs-directories-at-boot)

### Drupal resources extraction
Given that we already have a file system ready to save, in the same instance where you set up the client, we will start saving all the necessary configuration files for Drupal. We are going to host this on the NFS Server so that, even if the containers die, the service metadata remains available and allows for the construction of CMS mirrors (that is, setting up more instances with distant containers but with the same information to improve its fault tolerance).
For this, we will start building the most basic Drupal container. Below is the docker-compose.yml used.

```yml
version: '3'
services:
drupal:
image: drupal:latest
ports:
- "80:80"
```
Once we created this, we save and raise the container.

The next step is to continue with the creation of the site. You can do this by accessing it from the web browser with the public IP of your VM (where you have the Drupal container). Throughout this form, you will be asked for the private IP of your database and some additional settings, manage and wait for the site to be created successfully.
After this, what we will do is migrate that information to our NFS Server. We will do this by creating a copy on the path where all this data is stored inside the container, and exporting it on the path you defined in the NFS Client. And since this is already set up, what will happen is that all this data will end up on our server

```cmd
cd /nfs/home
docker cp TU_CONTENEDOR_DRUPAL:/opt/drupal ./
```

The intention of the first command is for you to navigate to the path where you did the mount, that is, the point where the NFS client is located. Then, referring to the name or ID of your container, all files under that path inside the container will be copied to the folder where you are currently located in your VM

### Add another drupal instance
For this part, it corresponds to the entire initial procedure of our second machine in Drupal. That is, having Docker and other tools installed. To continue with this part, you must reconfigure the NFS Client and associate it with the server. Here, it becomes important to have configured the wildcard so that it accepts the connection without having to modify the server. Once you have it ready, we can move on to a v2.0 of our docker-compose.yml, which will use the bind mounts strategy to complement the container's information based on what is defined on your machine. However, that information is not actually on your current machine, but on the NFS server! Heres the updated compose

```cmd
version: '3.8'
services:
drupal:
image: drupal:latest
ports:
- 80:80
volumes:
- /nfs/home/drupal/web:/var/www/html
restart: always
```

At this point, both instances should be connected, so you should be able to see that the changes in one of them also happen in the other instance

###NGINE X Configuration
With two instances having the same information, we need to set up a reverse proxy that redirects traffic to these two machines.
To do this, you will create an NGINX configuration file named nginx.conf.
Inside it, you will put the following
```yml
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;
events {
worker_connections 1024;
}
http {
upstream backend {
server my.dummy.ip.1; #Aquí va la IP privada donde tienes el container 1
server my.dummy.ip.2; #Aquí va la IP privada donde tienes el container 2
}
server {
listen 80;
listen [::]:80;
server_name _;
location / {
proxy_pass http://backend;
proxy_redirect off;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Host $host;
proxy_set_header X-Forwarded-Server $host;
proxy_set_header X-Forwarded-Proto $scheme;
}
}
}
```
With this done, we will proceed with the instantiation of an NGINX container. Remember that for this step you must have Docker and its tools installed. Here is the docker-compose.yml.
```
version: '3.1'
services:
nginx:
container_name: nginx
image: nginx
volumes:
- /home/ubuntu/nginx.conf:/etc/nginx/nginx.conf:ro
ports:
- 80:80
```

In this file, you are defining a bind mount again, in which you state that the container should use the file you previously created as the reverse proxy configuration.
Once this is done, you bring up your container and go to AWS to create an Elastic IP. You will link this IP to the machine where you created the NGINX container.
As a final test, what you need to do is take that Elastic IP and enter it into your web browser. The expected result is that you can successfully view your Drupal page. Internally, the container is already forwarding traffic to your Drupal instances as it sees fit.
