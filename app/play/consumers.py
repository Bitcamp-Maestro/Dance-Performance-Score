
from os import set_inheritable
import threading
from channels.generic.websocket import WebsocketConsumer
import json
import random

class PlayConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = None


    def connect(self):
        self.accept()
        self.thread = self.set_interval(self.updateScore, 1.5, random.randint(10,421))
    
    def disconnect(self, code):
        self.thread.cancel()
        return super().disconnect(code)

    def receive(self, text_data):
        json_data = json.loads(text_data)
        print(json_data)
        if json_data['type'] =='close':
            self.disconnect(json_data['pid'])
        message = json_data['message']
        print(message)

        self.send(text_data=json.dumps({
            'type' : 'check',
            'message' : message,
            'result' : '200',
        }))
        # return super().receive(text_data=text_data, bytes_data=bytes_data)
    def set_interval(self, func, sec, *args):
        def func_wrapper():
            func(*args)
            self.set_interval(func, sec, *args)
        self.thread = threading.Timer(sec, func_wrapper)
        self.thread.start()
        
    def updateScore(self, score):
        score = random.randint(10,421)
        print(score)
        self.send(text_data=json.dumps({
            'type' : 'update_score',
            'score' : score,
            'result' : 200, 
        }))
