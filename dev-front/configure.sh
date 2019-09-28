#!/bin/bash

ln -fs ${BINPOLL_FRONT_SRC}/dist/binpoll-front ${BINPOLL_FRONT_TARGET}
. /app/update-front-config.sh && echo "front config.js file update"
apache2ctl start
if [ "$BINPOLL_ENABLE_SSL" = 1 ]
then
  a2ensite -q binpoll-front-ssl-80
  echo "waiting for SSL certificate and key"
  while [[ ! -f "/extern/letsencrypt/live/${BINPOLL_SERVER_NAME}/fullchain.pem" \
          && ! -f  "/extern/letsencrypt/live/${BINPOLL_SERVER_NAME}/privkey.pem" ]]
  do
    sleep 1
  done
  echo "certificate and key arrived"
  a2ensite -q binpoll-front-ssl-443
  apache2ctl restart
else
  a2ensite -q binpoll-front-nossl-80 
  apache2ctl restart
fi
echo "configuration end" 
tail -f /dev/null
#     && source /app/update-front-config.sh && apachectl -D FOREGROUND \
#    && npm install \
#    && npm run ng build \
#    && ln -s ${BINPOLL_FRONT_SRC}/dist/binpoll-front ${BINPOLL_FRONT_TARGET} \
#    && echo "configuration end" \