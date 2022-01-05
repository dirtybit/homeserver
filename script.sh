#!/bin/bash

#arr+=("airsonic")
#arr+=("bookstack")
#arr+=("calibre-web")
#arr+=("clarkson")
#arr+=("cyberchef")
arr+=("diun")
#arr+=("dolibarr")
#arr+=("drone")
arr+=("etiketten")
#arr+=("filebrowser")
#arr+=("fireflyiii")
arr+=("fittrackee")
#arr+=("gauth")
#arr+=("gitlab")
arr+=("gogs")
arr+=("gotify")
#arr+=("grocy")
arr+=("guacamole")
arr+=("heimdall")
#arr+=("hoppscotch")
#arr+=("hrconvert2")
arr+=("jellyfin")
#arr+=("joplin")
#arr+=("keeweb")
arr+=("librespeed")
#arr+=("minecraft")
#arr+=("minetest")
#arr+=("monica")
#arr+=("motioneye")
arr+=("nextcloud")
#arr+=("notea")
#arr+=("odoo")
#arr+=("openproject")
#arr+=("paperless")
arr+=("photoprism")
#arr+=("pihole")
#arr+=("portainer")
arr+=("rainloop")
arr+=("registry")
arr+=("samba")
#arr+=("searx")
arr+=("sonarr")
#arr+=("syncserver") does not work
arr+=("syncthing")
arr+=("traefik")
#arr+=("traggo")
arr+=("transmission")
#arr+=("trilium")
#arr+=("uptimekuma")
arr+=("vpn") # disabled, so that backup script does not stop it, might cause problems when restarting
#arr+=("webtop")
#arr+=("wertpapierkredit")
#arr+=("wger")
arr+=("whoogle")
arr+=("wol")
#arr+=("xbrowsersync")
arr+=("youtube-dl")

for item in ${arr[*]}
do
    docker-compose -f ./$item/docker-compose.yml $1 $2 $3
done
