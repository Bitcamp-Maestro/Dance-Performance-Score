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
        self.score = 0
        self.chunk_path_queue = Queue()

    def connect(self):
        self.accept()
        print(self.scope)
        self.pid = self.scope['url_route']['kwargs']['play_id']    
        self.model_thread = threading.Thread(target=self.model_loop)
        self.model_thread.start()
    
    def model_loop(self):
        while True:
            if self.chunk_path_queue.get():
                # time.wait(1)
                continue

            host = "127.0.0.1"  # 모델 엔진 서버 IP 주소
            port = 5050  # 모델 엔진 서버 통신 포트
            model_socket = socket.socket()
            model_socket.connect((host, port))

            json_data = {
                "pid" : self.pid,
                "chunk_path" : self.chunk_path_queue.get(),
            }
            message = json.dumps(json_data)
            self.model.send(message.encode())            

            try:
                asyncio.create_task(self.model_task(model_socket))
            except Exception as e:
                print('model socket error', e)
                continue
            
    def model_task(self, model_socket):
        while True:
            try:
                data = model_socket.recv(2048)
                ret_data = json.loads(data.decode())
            except Exception as e:
                print('model_task() : socket error', e)
                break

            if ret_data["ING"] == "finish":
                cv2.destroyAllWindows()
                break

            print("답변 : ")
            print(ret_data['total_score'])
                
            self.score += ret_data['total_score']
            self.updateScore(self.score)

            length = self.recvall(self.model, 64)
            length1 = length.decode('utf-8')
            stringData = self.recvall(self.model, int(length1))
            data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
            decimg = cv2.imdecode(data,1)


            
            text = "Score : {}".format(str(ret_data['total_score']))
            org=(50,100)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(decimg, text,org, font,1,(255,0,0),2 )
            
            cv2.imshow("image", decimg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                    
            cv2.destroyAllWindows()
        cv2.destroyAllWindows()

    def recvall(sock, count):
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
            data_path = os.path.join(self.app_path, f"..\\media\\chunks\\test7_{self.stamp}.mp4")
            with open(data_path, 'wb') as f:
                f.write(bytes_data)
                self.chunk_path_queue.put(data_path)
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
        
    def updateScore(self, score):
        self.send(text_data=json.dumps({
            'type' : 'update_score',
            'score' : score,
            'result' : 200, 
        }))


    def disconnect(self, code):
        self.stamp = 0
        return super().disconnect(code)
