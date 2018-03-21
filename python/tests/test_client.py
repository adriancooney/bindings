import uWebSockets

import threading
import time
import sys
import uuid
import json

"""
    A Test Client which sends random messages to wss://echo.websocket.org and verifies the replies
"""
class TestClient(uWebSockets.WebSocketClient):

    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self.expected = None
        self.sent_received = {}
        
    def on_message(self, message):
        print("Recv %s" % repr(message))
        assert(message == self.expected)
        assert(message in self.sent_received)
        assert(self.sent_received[message] == False)
        self.sent_received[message] = True
        self.expected = str(uuid.uuid4().hex).upper()[0:6]
        self.send(self.expected)
        
    def test(self):
        print("What")
        
    def send(self, message):
        print("Send %s" % repr(message))
        self.sent_received[message] = False
        return super(TestClient, self).send(message)
    
    def on_open(self):
        print("Open %s" % repr(self))
        self.expected = str(uuid.uuid4().hex).upper()[0:6]
        self.send(self.expected)
        
    def on_close(self, code, message):
        print("Closed %s %s" % (repr(code), repr(message)))
        
        
    def close(self):
        print("Overrode close here")
        return super(TestClient, self).close()
        
num_messages = 10
timeout = 20

ws = TestClient("wss://echo.websocket.org")
ws.run(True)
start_time = time.time()
time.sleep(3)

while (not ws.valid() or ws.connected()) \
  and (num_messages is None or len(ws.sent_received) < num_messages) \
  and (timeout is None or time.time() - start_time < timeout):
    time.sleep(1)

print(json.dumps(ws.sent_received, indent=4))
ws.close()
assert(len(ws.sent_received) >= num_messages)
## Required on Windoze
sys.exit(0)