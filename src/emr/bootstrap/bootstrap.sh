#!/usr/bin/env bash
set -e

JAR_BUCKET=$1
RUNTIME_CONFIGS=$2

sudo aws s3 sync s3://${JAR_BUCKET}/artifacts/emr/jars/ /usr/lib/spark/jars/

is_master=$(cat /mnt/var/lib/info/instance.json | jq .isMaster)
if [ $is_master = true ]
then
    sudo aws s3 sync ${RUNTIME_CONFIGS} /mnt/var/lib/instance-controller/public/runtime_configs/ && sudo chmod -R 755 $_
fi
