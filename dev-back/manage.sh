#!/bin/bash

(source venv/bin/activate \
    && python binpoll-back/manage.py "$@")


#user_name="pawel"
#user_pass="pawel"
#(source /app/venv/bin/activate; \
#     echo "from django.contrib.auth import get_user_model;User = get_user_model(); User.objects.create_superuser('$user_name', '', '$user_pass')" 
#     | python manage.py shell)