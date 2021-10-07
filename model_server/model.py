import threading
from pymongo import MongoClient
import json


from utils.Server import Server
from module.det_pose_video import Play
from module.data_preprocessing import video__init__




def to_client(conn, addr, params):
    # db = params['db']
    play = params['play']
    try:

        read = conn.recv(2048)  # 수신 데이터가 있을 때 까지 블로킹
        print('===========================')
        print('Connection from: %s' % str(addr))
        if read is None or not read:
            # 클라이언트 연결이 끊어지거나, 오류가 있는 경우
            print('클라이언트 연결 끊어짐')
            exit(0)
        print(read)
        # json 데이터로 변환
        try:
            recv_json_data = json.loads(read.decode())
            # recv_json_data = json.loads(read.encode())
            print("데이터 수신 : ", recv_json_data)
            path = recv_json_data['path']
            pid = recv_json_data['pid']
            target = recv_json_data["target"]
        except:
            path = read["path"]
        print("시작전")
        print("path : ", path)
        
        video__init__(user_video=path, target_video=target, output="result")
        
        message = play.det_Pose_Video(user_video="media/result.mp4", play_id=pid)
        conn.send(message)
        print("끝남")
    except Exception as ex:
        print(ex)

    finally:
        # if db is not None: # db 연결 끊기
            # db.close()
        conn.close()
    pass




if __name__ == "__main__":
    # Detction 설정
    DET_CONFIG_FASTER_R_CNN_R50_FPN_COCO = "module/configs/detection/faster_rcnn_r50_fpn_coco.py"                                                                                                        # Detection config 파일
    DET_CHECKPOINT_FASTER_R_CNN_R50_FPN_COCO = "checkpoints/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth"        # Detection 훈련 모델 파일

    # Pose 설정
    POSE_CONFIG_HRNET_W48_COCO_256X192 = "module/configs/pose/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py"                                                               # Pose config 파일
    # POSE_CHECKPOINT_HRNET_W48_COCO_256X192 = "https://download.openmmlab.com/mmpose/checkpoints/pose/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth"                                             # Pose 훈련 모델 파일
    POSE_CHECKPOINT_HRNET_W48_COCO_256X192 = "checkpoints/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth"                                             # Pose 훈련 모델 파일
    
    play= Play()
    play.det__init__(DET_CONFIG_FASTER_R_CNN_R50_FPN_COCO, DET_CHECKPOINT_FASTER_R_CNN_R50_FPN_COCO, device="cuda:0")
    play.pose__init__(POSE_CONFIG_HRNET_W48_COCO_256X192, POSE_CHECKPOINT_HRNET_W48_COCO_256X192, device="cuda:0")
    

    # Server port number
    port = 5050
    listen = 100

    bot = Server(port, listen)
    bot.create_sock()
    print("bot start")
    
    while True:
        conn, addr = bot.ready_for_client()
        params = {
            # "db" : db,
            "play" : play
        }

        client = threading.Thread(target= to_client, args=(
            conn,
            addr,
            params
        ))

        client.start()

    
