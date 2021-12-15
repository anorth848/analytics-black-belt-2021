#!/usr/bin/env bash
BUCKET=$1

sudo aws s3 cp s3://${BUCKET}/analytics-black-belt-2021/emr/jars/postgresql-42.3.1.jar /usr/lib/spark/jars/