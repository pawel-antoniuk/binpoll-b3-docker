FROM ubuntu:18.04
WORKDIR /app

COPY node_setup_10.sh .
RUN chmod +x node_setup_10.sh

ENV DEBIAN_FRONTEND noninteractive
ENV BINPOLL_FRONT_TARGET /var/www/binpoll-front
ENV BINPOLL_FRONT_SRC /app/binpoll-front
ENV BINPOLL_API_URL http://localhost:8000/

# prepare environment
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && ./node_setup_10.sh \
    && apt-get install -y apache2 nodejs 
    #&& curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    #&& echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    #&& npm install -g npm-cache
    #&& apt-get install -y yarn

# configure apache2
COPY binpoll-front-ssl-80.conf         /etc/apache2/sites-available/
COPY binpoll-front-ssl-443.conf        /etc/apache2/sites-available/
COPY binpoll-front-nossl-80.conf       /etc/apache2/sites-available/
RUN a2enmod -q rewrite headers expires proxy proxy_http ssl\
    && a2dissite -q 000-default

# copy installation scripts and config files
COPY update-front-config.sh /app/
COPY configure.sh           /app/
RUN chmod +x update-front-config.sh
RUN chmod +x configure.sh
#COPY binpoll-front          ${BINPOLL_FRONT_SRC}
RUN mkdir                   ${BINPOLL_FRONT_SRC}

CMD ["bash", "/app/configure.sh"]

EXPOSE 80
