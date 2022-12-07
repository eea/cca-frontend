#!/bin/bash

site=cca-prod
serverip=10.50.5.50
serverport=5554
date=$(date '+%Y-%m-%d')
backups=./data/
echo "--------------------------------------------------------"
echo " BACKUP $site"
echo "--------------------------------------------------------"
echo "Today: "$date

destination=$backups$site-$date

mkdir -p $destination
echo "Created folder: "$destination
rsync -avz -e 'ssh -p '$serverport' -i ~/.ssh/key' root@$serverip:/data-production/filestorage/Data.fs $destination
rsync -avz -e 'ssh -p '$serverport' -i ~/.ssh/key' root@$serverip:/data-production/blobstorage $destination
