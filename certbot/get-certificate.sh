#!/bin/sh

#  add flag --dry-run for debug
certbot certonly -n --webroot -w /extern/webroot --preferred-challenges http \
    -d ${BINPOLL_SERVER_NAME} -m ${BINPOLL_SERVER_EMAIL} --agree-tos