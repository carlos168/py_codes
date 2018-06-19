#!/usr/bin/env bash

nohup python manage.py runserver > ./logs/web.log 2>&1&

#ps aux |grep runserver |grep -v grep |awk '{print $2}'|xargs kill -9


