from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute
import redis
import socketio
import json

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 16379
SOCKET_URL = "http://127.0.0.1:5000"
CHANNEL = "event"

# Deps needed by the Gear
DEPS = ["requests", "python-socketio"]


print("Connecting to Redis ...")
conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def process(y):
    try:
        print("Processing change ...)")
        key = str(y['value']['key'])
        str_value = str(y['value']['value'])
        msg = json.loads(str_value.replace("'", "\""))
        msg['_key'] = key
        print("msg = {}".format(str(msg)))
        print("Sending to Socket.io server ...")
        sio = socketio.Client()
        sio.connect(SOCKET_URL)
        sio.emit(CHANNEL, msg)
        sio.disconnect()
    except Exception as e:
        print(str(e))

# Capture a change event
print("Registering keys reader ...")
cap = GearsBuilder('KeysReader', r=conn, addClientToRequirements=True)
cap.foreach(lambda x:
            execute('XADD', f'changed', '*', 'key', x['key'], 'value', x['value']))
cap.register(prefix='*',
             mode='sync',
             eventTypes=['hset'],
             readValue=True)

# Buffer the changes in a stream and process them
print("Registering stream reader ...")
proc = GearsBuilder('StreamReader', r=conn, addClientToRequirements=True, requirements=DEPS)
proc.foreach(process)
proc.register(prefix='changed')