import socketio
from flask import Flask

CHANNEL = "event"
REDIS_URL = "redis://127.0.0.1:6379"

'''
Create Websocket server

If queue_enabled is False, then the server will be started without Redis being used as the message queue.

Regarding 'python-socket.io' the reason why you would like to use a message queue with your server is to scale your
Websocket service because multiple servers can listen to the same messages being emitted to the queue. 
Using a queue implementation such as Redis for the Websocket server is not mandatory as long as we have only a small 
amount of clients.
'''
def create_server(queue_enabled=False, debug_enabled=False):

    client_manager = None
    if queue_enabled:
        client_manager = socketio.RedisManager(url=REDIS_URL, channel=CHANNEL)

    return socketio.Server(client_manager=client_manager, logger=debug_enabled, engineio_logger=debug_enabled)

# The Websocket server instance
sio = create_server(True, False)

'''
Listen on events that are sent by clients to the server, the function name needs to match the event name/type/channel
'''
@sio.event
def event(sid, data):
    # Re-emit the data to others to ensure that consumers get it, this will also cause that the message ends up in the
    # message queue if you created the server with queue_enabled=True
    sio.emit(CHANNEL, data)
    print(str(data))

'''
Serve the Websocket server via Flask
'''
wsgi_app = socketio.WSGIApp(sio)
app = Flask(__name__)
app.wsgi_app = wsgi_app

if __name__ == '__main__':
    print("Starting Websocket server ...")
    # This emits a message to all clients that are listening and to all servers that use the same message queue.
    sio.emit(CHANNEL, "Hello there!")
    app.run()
