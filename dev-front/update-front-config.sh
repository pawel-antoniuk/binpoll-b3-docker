#!/bin/bash

config_data="{\"apiUrl\":\"$BINPOLL_API_URL\", \"pollSoundsUrl\":\"$BINPOLL_API_URL/static/poll_sounds/\", \"exampleVideoAssetUrl\": \"/assets/example-movie/\"}"
mkdir -p "$BINPOLL_FRONT_SRC/src/assets/"
mkdir -p "$BINPOLL_FRONT_SRC/dist/binpoll-front/assets/"
echo "$config_data" > "$BINPOLL_FRONT_SRC/src/assets/config.json"
echo "$config_data" > "$BINPOLL_FRONT_SRC/dist/binpoll-front/assets/config.json"
