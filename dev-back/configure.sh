#!/bin/bash

cd "$BINPOLL_BACK_SRC" \
    && . /app/venv/bin/activate \
    && python manage.py collectstatic --noinput \
    && python manage.py makemigrations data_collector \
    && python manage.py migrate \
    && cd /app && python populate_db.py \
    && ln -sf "$BINPOLL_BACK_SRC" "$BINPOLL_BACK_TARGET" \
    && ln -sf /app/poll_sounds "$BINPOLL_BACK_SRC"/static \
    && apache2ctl start \
    && echo "configuration end" \
    && tail -f /dev/null