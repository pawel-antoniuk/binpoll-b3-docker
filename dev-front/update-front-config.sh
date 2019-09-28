#!/bin/bash

config_data="{\"apiUrl\":\"$BINPOLL_API_URL\", \"pollSoundsUrl\":\"$BINPOLL_API_URL/static/poll_sounds/\", \"exampleVideoAssetUrl\": \"/assets/example-movie/\"}"
echo "$config_data" > "$BINPOLL_FRONT_SRC/dist/binpoll-front/assets/config.json"
