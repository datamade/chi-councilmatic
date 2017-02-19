#! /bin/bash

cd /home/datamade/chicago
/home/datamade/.virtualenvs/chi-councilmatic/bin/python manage.py import_data >> /tmp/chicago-loaddata.log 2>&1 
