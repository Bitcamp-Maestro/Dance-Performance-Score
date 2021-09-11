
from channels.generic.websocket import WebsocketConsumer
import json

class PlayConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    
    def disconnect(self, code):
        pass
    def receive(self, text_data):
        json_data = json.loads(text_data)
        message = json_data['message']
        print(message)
        self.send(text_data=json.dumps({
            'message' : message,
            'result' : '200',
        }))
        # return super().receive(text_data=text_data, bytes_data=bytes_data)
