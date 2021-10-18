from channels.generic.websocket import WebsocketConsumer
import os
import threading
import json
from urllib.parse import urlparse
import cv2
import numpy
import base64
import socket
import json
import time
import asyncio
from queue import Queue

class PlayConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module_dir = os.path.dirname(__file__)
        self.app_path = os.getcwd()
        self.stamp = 0
        self.pid = None
        self.model_thread : threading.Thread = None
        self.model_socket = None
        self.total_score = 0
        self.parts_score = {
            'face_body' : 0,
            'left_arm' : 0,
            'right_arm' : 0,
            'left_leg' : 0,
            'right_leg' : 0,
        }
        
        self.chunk_path_queue = Queue()

    def connect(self):
        self.accept()
        print(self.scope)
        self.pid = self.scope['url_route']['kwargs']['play_id']    
        self.model_socket = self.create_model_socket()
    
    def create_model_socket(self):
        host = "127.0.0.1"  # 모델 엔진 서버 IP 주소
        port = 5050  # 모델 엔진 서버 통신 포트
        model_socket = socket.socket()
        model_socket.connect((host, port))
        print('model server connected')
        return model_socket
            
    def model_task(self, model_socket):
        
        json_data = {
            "pid" : self.pid,
            "chunk_path" : self.chunk_path_queue.get(),
        }
        message = json.dumps(json_data)
        self.model_socket.send(message.encode()) 

        while True:
            try:
                data = self.model_socket.recv(2048)
                ret_data = json.loads(data.decode())
            except Exception as e:
                print('model_task() : socket error', e)
                self.model_socket.close()
                self.model_socket = self.create_model_socket()
                break

            if ret_data["ING"] == "finish":
                # cv2.destroyAllWindows()
                break

            print("답변 : ")
            print(ret_data['total_score'])
        
            self.total_score += int(ret_data['total_score'])
            print(self.total_score)
            self.updateScore(int(ret_data['total_score']), ret_data['parts_score'])

            # length = self.recvall(self.model_socket, 64)
            # length1 = length.decode('utf-8')
            # stringData = self.recvall(self.model_socket, int(length1))
            # data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
            # decimg = cv2.imdecode(data,1)
            
            # text = "Score : {}".format(str(ret_data['total_score']))
            # org=(50,100)
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(decimg, text,org, font,1,(255,0,0),2 )
            
            # cv2.imshow("image", decimg)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
                    
        #     cv2.destroyAllWindows()
        # cv2.destroyAllWindows()

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf
        

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        if bytes_data != None:
            self.stamp += 1
            data_path = os.path.join(self.app_path, f"..\\media\\chunks\\{self.pid}_{self.stamp}.mp4")
            with open(data_path, 'wb') as f:
                f.write(bytes_data)
                self.chunk_path_queue.put(data_path)
                try:
                    asyncio.create_task(self.model_task(self.model_socket))
                except Exception as e:
                    print('model socket error', e)
                return

        if text_data != None:                
            json_data = json.loads(text_data)
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
        
    def updateScore(self, score, parts_score):
        self.send(text_data=json.dumps({
            'type' : 'update_score',
            'score' : score,
            'parts_score' : parts_score, 
            'result' : 200, 
        }))


    def disconnect(self, code):
        self.stamp = 0
        return super().disconnect(code)
