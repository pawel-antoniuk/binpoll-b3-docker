FROM certbot/certbot
WORKDIR /app

COPY ./configure.sh /app/
COPY ./get-certificate.sh /app/

RUN chmod +x configure.sh
RUN chmod +x get-certificate.sh

ENTRYPOINT []
CMD ["/bin/sh", "/app/configure.sh"]