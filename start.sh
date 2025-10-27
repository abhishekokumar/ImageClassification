#!/bin/bash
# Start Flask in background
python server/main.py &

# give Flask a few seconds to start
sleep 2

# Start nginx in foreground
nginx -g "daemon off;"