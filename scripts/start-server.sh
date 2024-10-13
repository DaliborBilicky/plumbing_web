#!/bin/bash

PORT=8000
DIR="."

if [ ! -z "$1" ]; then
	PORT=$1
fi

if [ ! -z "$2" ]; then
	DIR=$2
fi

echo "Starting Python http server. Port: $PORT, Files: $DIR"

python3 -m http.server $PORT --directory $DIR
