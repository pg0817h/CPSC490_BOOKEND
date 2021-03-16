#!/usr/bin/env bash

set -e

PROJECT_BASE_PATH='/Users/Abby/Desktop/cpsc490_project/project/first_project'
#/Users/Abby/Desktop/cpsc490_project/project/first_project
git pull
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput
supervisorctl restart bookend

echo "DONE! :)"
