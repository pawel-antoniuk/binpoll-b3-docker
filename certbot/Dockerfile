FROM certbot/certbot
WORKDIR /app

COPY ./configure.sh /app/
COPY ./get-certificate.sh /app/

ENTRYPOINT []
CMD ["/bin/sh", "/app/configure.sh"]