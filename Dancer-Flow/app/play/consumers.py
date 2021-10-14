import os
import threading
from channels.generic.websocket import WebsocketConsumer
import json
import random
import base64
from urllib.parse import urlparse
import cv2
import numpy
import base64
import socket
import json

class PlayConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.thread = None
        self.module_dir = os.path.dirname(__file__)
        self.app_path = os.getcwd()
        self.stamp = 0
        self.pid = None
        self.model = None
        self.thread = None
        self.score = 0

    def connect(self):
        self.accept()
        print(self.scope)
        self.pid = self.scope['url_route']['kwargs']['play_id']
        self.model_init()
        self.set_model_thread(self.model_listen, 2.5)
    
    def disconnect(self, code):
        self.thread.cancel()
        self.stamp = 0
        self.model.close()
        return super().disconnect(code)

    def model_init(self):
            host = "127.0.0.1"  # 모델 엔진 서버 IP 주소
            port = 5050  # 모델 엔진 서버 통신 포트
            self.model = socket.socket()
            self.model.connect((host, port))

    def model_send(self, data_path):
        json_data = {
            "pid" : self.pid,
            "chunk" : data_path,
        }
        message = json.dumps(json_data)
        self.model.send(message.encode())

    def model_listen(self):
        while True:
            data = self.model.recv(2048)
            ret_data = json.loads(data.decode())
            self.stamp += 1
            if ret_data["ING"] == "finish":
                self.model.close()
                break
            else:
                print("답변 : ")
                print(ret_data['total_score'])
                self.score += ret_data['total_score']
            # length = self.recvall(self.model, 64)
            # length1 = length.decode('utf-8')
            # stringData = self.recvall(self.model, int(length1))
            # data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
            # decimg = cv2.imdecode(data,1)

            self.updateScore(self.score)

        #     text = "Score : {}".format(str(ret_data['total_score']))
        #     org=(50,100)
        #     font = cv2.FONT_HERSHEY_SIMPLEX
        #     cv2.putText(decimg, text,org, font,1,(255,0,0),2 )
            
        #     cv2.imshow("image", decimg)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break
                
        # cv2.destroyAllWindows()
        # self.model.close()

    def recvall(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
        
    def set_model_thread(self, func, sec, *args):
        def func_wrapper():
            func(*args)
        self.thread = threading.Timer(sec, func_wrapper)
        self.thread.start()


    def receive(self, text_data=None, bytes_data=None, **kwargs):
        if bytes_data != None:
            data_path = os.path.join(self.app_path, f"..\\media\\chunks\\test7_{self.stamp}.mp4")
            with open(data_path, 'wb') as f:
                f.write(bytes_data)
                self.model_send(data_path=data_path)
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
        
    def updateScore(self, score):
        self.send(text_data=json.dumps({
            'type' : 'update_score',
            'score' : score,
            'result' : 200, 
        }))
