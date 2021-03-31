#!/bin/bash

docker-compose -f /mnt/docker up -d

arr+=("airsonic")
arr+=("bookstack")
arr+=("calibre-web")
arr+=("clarkson")
#arr+=("cyberchef")
#arr+=("drone")
arr+=("etiketten")
#arr+=("fireflyiii")
#arr+=("ftp")
#arr+=("gitlab")
arr+=("gogs")
#arr+=("guacamole")
#arr+=("hoppscotch")
#arr+=("hrconvert2")
arr+=("librespeed")
#arr+=("minecraft")
#arr+=("minetest")
#arr+=("monica")
arr+=("nextcloud")
#arr+=("odoo")
#arr+=("openproject")
#arr+=("paperless")
#arr+=("portainer")
arr+=("rainloop")
arr+=("registry")
#arr+=("searx")
arr+=("syncthing")
#arr+=("traggo")
#arr+=("wertpapierkredit")
#arr+=("wger")
arr+=("wireguard")
#arr+=("youtube-dl")

for item in ${arr[*]}
do
    docker-compose -f /mnt/docker/$item up -d
done
