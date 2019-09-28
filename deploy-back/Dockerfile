FROM home.antoniuk.pl:5000/binpoll-dev-back
WORKDIR /app
COPY ./src/binpoll-back           ${BINPOLL_BACK_SRC}
CMD ["./wait-for-it.sh", "database:3306", "-t", "30", "--", "bash", "/app/configure.sh"]
EXPOSE 80
