#!/bin/bash
# Ensure that all requirements of that Gear are present before deploying
python3.7 -m pip install git+https://github.com/RedisGears/redisgears-py.git
python3.7 -m pip install -r requirements.txt

# Use the Redis Gears client to send the Gears
python3.7 rg_socketio-client.py