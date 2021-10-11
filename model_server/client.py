import socket
import json

# 챗봇 엔진 서버 접속 정보
host = "127.0.0.1"  # 챗봇 엔진 서버 IP 주소
port = 5050  # 챗봇 엔진 서버 통신 포트

# 클라이언트 프로그램 시작
while True:
    print("질문 : ")
    query = input()  # 질문 입력
    if(query == "exit"):
        exit(0)
    print("-" * 40)

    # 챗봇 엔진 서버 연결
    mySocket = socket.socket()
    mySocket.connect((host, port))

    # 모델 엔진 질의 요청
    json_data = {
            "pid" : "qqq",
            "target" : "C:/JGBH/Dancer-Flow/model_server/module/sample_data/BTS-Dynamite1-3.mp4",
            "path" : "C:/JGBH/Dancer-Flow/model_server/module/sample_data/sample.mp4"
    }
    message = json.dumps(json_data)
    mySocket.send(message.encode())
    
    # 챗봇 엔진 답변 받기
    while True:
    
        data = mySocket.recv(2048)
        ret_data = json.loads(data.decode())
        if ret_data["ING"] == "finish":
            mySocket.close()
            break
        else:
            print("답변 : ")
            print(ret_data['TOTAL_SCORE'])

    
    # print(ret_data)
    # print(type(ret_data))
    # print("\n")

    # 챗봇 엔진 서버 연결 소켓 닫기
    mySocket.close()
