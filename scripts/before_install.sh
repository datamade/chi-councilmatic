#!/bin/bash

# Make project directory if it doesn't exist. This is mainly to ensure that these scripts work on a bare server

rm -Rf /home/datamade/chi-councilmatic
mkdir -p /home/datamade/chi-councilmatic

if [ "$DEPLOYMENT_GROUP_NAME" == "staging" ]
then
    rm -Rf /home/datamade/chicago-staging
    mkdir -p /home/datamade/chicago-staging
fi
if [ "$DEPLOYMENT_GROUP_NAME" == "production" ]
then
    rm -Rf /home/datamade/chicago
    mkdir -p /home/datamade/chicago
fi

# Decrypt files encrypted with blackbox
cd /opt/codedeploy-agent/deployment-root/$DEPLOYMENT_GROUP_ID/$DEPLOYMENT_ID/deployment-archive/ && chown -R datamade.datamade . && sudo -H -u datamade blackbox_postdeploy
