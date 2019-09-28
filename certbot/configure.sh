#!/bin/sh

echo "looking for a certificate..."
if [[ ! -f "/extern/letsencrypt/live/${BINPOLL_SERVER_NAME}/fullchain.pem" \
        && ! -f  "/extern/letsencrypt/live/${BINPOLL_SERVER_NAME}/privkey.pem" ]]
then
    echo "certificate nod found"
    echo "creating new certificate"
    . /app/get-certificate.sh
fi

/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait ${!}; done;'
