# Homeserver
A robust and extensible homeserver setup without any magic.

It is designed to be hosted and used only on your local network. Even though being only used on your local network it uses ```https``` via a wildcard certificate for everything to avoid browser security warnings and because some services do not work properly without TLS. You can still access from all around the world via a VPN e.g. Tailscale.

## Structure
Each service is fully contained in a directory. Usually there are at least a ```docker-compose.yml``` and an ```.env.example``` file. All data is persistet in the service's ```data/``` direcrtory.
Traefik is the reverse proxy for all the services. To start a service simply ```cp .env.example .env``` edit it to your likes, add the service name to the ```SERVICES``` variable in the root ```.env``` file and run ```./script.sh up -d```. This script simply applies all passed parameters to ```docker compose``` executed in each service`s directory specified in the ```.env``` file.

## Initial Setup

### Prerequisites
- server running docker
- domain (get a free one at https://www.freenom.com/)
- DNS A-record wildcard pointing to your servers IP (e.g. 192.168.1.2)

Not all DNS providers support wildcard A-records, https://www.digitalocean.com/ does. Sign up and point your domain's NS-records to digitalocean's nameservers. It is free.

### Setup Traefik
```
cp .env.example .env
cd services/traefik
cp .env.example .env
```
Change the ```DOMAIN``` in ```.env``` and edit ```DOMAIN```, ```ACME_EMAIL``` and ```DO_AUTH_TOKEN``` in ```services/traefik/.env```. You can get a ```DO_AUTH_TOKEN``` here https://cloud.digitalocean.com/account/api/tokens

To test if you can get a certificate from letsencrypt uncomment the line about the staging server in ```services/traefik/docker-compose.yml``` by removing the ```#``` sign.

Run
```
docker network create dirtybit
./script.sh up -d
```
wait till all images are pulled, build and a certificate retrieved. Then you can access nextcloud and gogs via your browser. If your browser warns you about an unknown certificate authority accept the risk because you know it is a staging certificate or maybe a self signed certificate from traefik. In the latter case you still need to wait a minute till your letsencrypt certificate is issued or you have an error somewhere. Check ```docker compose logs -f traefik``` to view the logs of traefik. If everything worked alright, just comment out the one line in traefik's docker-compose.yml and run the script again to get a valid certificate.

## Customization

You have several options to customize the services without effecting the state of this git repository.
1. Change or add variables in the corrosponding ```.env``` file
2. Change a deployment by adding your own ```docker-compose.override.yml``` file
3. Add your own service

## Add your own services

If you have you a own website or you want to host a service which is not listed under ```./services``` then you can add it under ```./custom_services```. Everything here is not traced by git. Follow the same pattern by creating a subfolder and ```docker-compose.yml``` file for each service e.g. ```./custom_service/my_website/docker-compose.yml```. To automatically start and stop it via the script, just add the subfolder`s name to the ```CUSTOM_SERVICES``` variable in the ```.env``` file.

## Backup

Because all user data is mounted to the filesystem you can backup everything simply by backing up this folder. You can use your own solution or use the ```./backup.sh``` script. It assumes that this homeserver-folder lives under ```/mnt/data``` and you want to back it up to ```/mnt/backup```.

## docker-compose.yml template

```
version: "3.6"
services:
  app123:
    container_name: app123
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    networks:
      - traefik
    labels:
      my.zone: dirtybit
      traefik.enable: true
      traefik.http.routers.app123.rule: Host(`${SUBDOMAIN}.${DOMAIN}`)
      traefik.http.routers.app123.entrypoints: websecure
      traefik.http.services.app123.loadbalancer.server.port: 3000

networks:
  traefik:
    name: dirtybit

```
