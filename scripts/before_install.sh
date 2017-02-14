#!/bin/bash

# Make project directory if it doesn't exist. This is mainly to ensure that these scripts work on a bare server

rm -Rf /home/datamade/la-metro-councilmatic
mkdir -p /home/datamade/la-metro-councilmatic

if [ "$DEPLOYMENT_GROUP_NAME" == "staging" ]
then
    rm -Rf /home/datamade/lametro-staging
    mkdir -p /home/datamade/lametro-staging
fi
if [ "$DEPLOYMENT_GROUP_NAME" == "production" ]
then
    rm -Rf /home/datamade/lametro
    mkdir -p /home/datamade/lametro
fi

# Decrypt files encrypted with blackbox
cd /opt/codedeploy-agent/deployment-root/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/deployment-archive/ && chown -R datamade.datamade . && sudo -H -u datamade blackbox_postdeploy
