import socketio


SOCKET_URL = "http://127.0.0.1:5000"
CHANNEL = "event"

'''
Consuming client that listens on event messages
'''
if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect(SOCKET_URL)

    '''
    Listen on events, the function name needs to match the event name/type/channel
    '''
    @sio.event
    def event(data):
        print(str(data))