import time
import socketio
import datetime

SOCKET_URL = "http://127.0.0.1:5000"
CHANNEL = "event"


'''
A test script which emits 10 messages to the Websocket server
'''
if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect(SOCKET_URL)

    for i in range(10):
        now = datetime.datetime.now()
        msg = { "time": now.timestamp(), "msg": "Hello again!"}
        print("Sending message " + str(msg))
        sio.emit(CHANNEL, msg)
        time.sleep(5)

    sio.disconnect()