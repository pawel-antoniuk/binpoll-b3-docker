FROM ubuntu:18.04
WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive
ENV BINPOLL_BACK_TARGET /var/www/binpoll-back
ENV BINPOLL_BACK_SRC /app/binpoll-back

# prepare environment
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get install -y apache2 python3 python3-pip libapache2-mod-wsgi-py3 libmysqlclient-dev

# configure python
RUN ln -sfn /usr/bin/python3.6 /usr/bin/python \
    && ln -sfn /usr/bin/pip3 /usr/bin/pip \
    && pip install virtualenv
COPY requirements.txt /app/
RUN virtualenv /app/venv \ 
    && . /app/venv/bin/activate \
    && pip install -r /app/requirements.txt

# configure apache2
COPY binpoll-back.conf      /etc/apache2/sites-available/
RUN a2enmod -q headers ratelimit expires\
    && a2dissite -q 000-default \
    && a2ensite -q binpoll-back

# copy config and data files
COPY wait-for-it.sh         /app/
COPY configure.sh           /app/
#COPY binpoll-back           ${BINPOLL_BACK_SRC}
COPY manage.sh              /app/
RUN chmod +x wait-for-it.sh  
RUN chmod +x configure.sh
RUN chmod +x manage.sh 
RUN mkdir                   ${BINPOLL_BACK_SRC}
COPY populate_db.py         /app/

EXPOSE 80
