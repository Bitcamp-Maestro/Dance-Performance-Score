import os
import threading
from channels.generic.websocket import WebsocketConsumer
import json
import random
import base64

class PlayConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread = None
        self.module_dir = os.path.dirname(__file__)
        self.app_path = os.getcwd()
        self.stamp = 0

    def connect(self):
        self.accept()
        self.thread = self.set_interval(self.updateScore, 1.5, random.randint(10,421))
    
    def disconnect(self, code):
        self.thread.cancel()
        self.stamp = 0
        return super().disconnect(code)

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        # print(text_data)

        if bytes_data != None:
            self.stamp += 1
            # with open(os.path.join(self.app_path, f"..\\media\\chunks\\test7_{self.stamp}.mp4"), 'wb') as f:
            #     f.write(bytes_data)
            print(type(bytes_data))
            data = bytes_data.split(b';')
            # with open(os.path.join(self.app_path, f"..\\media\\chunks\\{data[0].decode('ascii')}.mp4"), 'wb') as f:
            #     f.write(data[1])
            return


        if text_data != None:
                
            json_data = json.loads(text_data)
            print(bytes_data)
            print(json_data['type'])
            if json_data['type'] =='close':
                self.disconnect(json_data['pid'])
            elif json_data['type'] == 'check':
                message = json_data['message']
                print(message)

                self.send(text_data=json.dumps({
                    'type' : 'check',
                    'message' : message,
                    'result' : '200',
                }))
            elif json_data['type'] == 'user_chunk':
                # print(json_data['message'])
                try:
                    # print(type(json_data['data']))
                    # print(len(json_data['data']))
                    print(json_data)
                    with open(os.path.join(self.app_path, f"..\\media\\chunks\\{json_data['stamp']}_2.webm"), 'wb') as f:
                        f.write(json_data['data'])
                    data = base64.b64decode(json_data['data'] + '=' * (-len(json_data['data']) % 4))
                    print(type(data))
                    with open(os.path.join(self.app_path, f"..\\media\\chunks\\{json_data['stamp']}.webm"), 'wb') as f:
                        f.write(data)
                except Exception as e:
                    print(e)
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