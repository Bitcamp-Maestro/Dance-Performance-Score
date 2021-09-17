import os
import cv2

# mmpose, mmdet 함수 호출
from mmpose.apis import inference_top_down_pose_model, init_pose_model, process_mmdet_results, vis_pose_result
from mmdet.apis import inference_detector, init_detector

# 유사도 측정 라이브러리
from sklearn.metrics.pairwise import cosine_similarity

# 비디오 mix 라이브러리
from video_mix import Video_Mix

def det_Pose_Video():
    """
    video1 : 유저가 업로드하고자 하는 비디오
    video2 : 비교할 영상
    output : 파일을 저장할 풀더 이름

    """
    ALL = 0
    # Video_Mix(video1, video2, name="sample")
    ############################################# 변수 ##################################################################################
    SHOW = True                                # WINDOW에 보여줄건지 선택 변수
    # SAVE = True                               # 저장할건지 선택 변수
    DEVICE = "cuda:0"                           # DEVICE 선택 변수 cpu, cuda, ---


    VIDEO_PATH = "./final_clips.mp4"

    # Detection config 파일
    DET_CONFIG = "configs/detection/faster_rcnn_r50_fpn_coco.py" 
    # Detection 훈련 모델 파일
    DET_CHECKPOINT = "checkpoints/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth" 
    
    # Pose config 파일
    POSE_CONFIG = "configs/pose/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py" 
    # Pose 훈련 모델 파일
    POSE_CHECKPOINT = "checkpoints/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth" 
    
    
    OUT_VIDEO_ROOT = "ss" # 저장 파일 위치 설정

    DET_CAT_ID = 1      # Category id for bounding box detection model
    BBOX_THR = 0.3      # Bounding box score threshold
    KPT_THR = 0.3       # Keypoint score threshold
    RADIUS = 4          # Keypoint radius for visualization
    THICKNESS = 1       # Link thickness for visualization
    #######################################################################################################################################
    # 1. build the detection moedl from a fonfig file and a checkpoint file
    det_model = init_detector(DET_CONFIG, DET_CHECKPOINT, device=DEVICE)
    
    # 2. build the pose model from a config file and a checkpoint file
    pose_model = init_pose_model(POSE_CONFIG, POSE_CHECKPOINT, device=DEVICE)

    dataset = pose_model.cfg.data['test']['type']
    
    # 3. 영상 파일을 불러오기
    cap = cv2.VideoCapture(VIDEO_PATH)
    # assert cap.isOpened(), f'Faild to load video file {VIDEO_PATH}'

    # 만약 out 루트가 있는지 없는지 확인
    if OUT_VIDEO_ROOT == '':
        save_out_video = False
    else:
        os.makedirs(OUT_VIDEO_ROOT, exist_ok=True)
        save_out_video = True

    if save_out_video:
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        videoWriter = cv2.VideoWriter(
            os.path.join(OUT_VIDEO_ROOT,
                        f'vis_{os.path.basename(VIDEO_PATH)}'), fourcc,
            fps, size)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(size)
    # optional
    return_heatmap = False

    # e.g. use ('backbone', ) to return backbone feature
    output_layer_names = None
    while cap.isOpened():


        flag, img = cap.read()
        
        if not flag:
            break
        
        # test a single image, the resulting box is (x1, y1, x2, y2)
        mmdet_results = inference_detector(det_model, img)

        # keep the person class bounding boxes.
        person_results = process_mmdet_results(mmdet_results, DET_CAT_ID)

        # test a single image, with a list of bboxes.
        pose_results, returned_outputs = inference_top_down_pose_model(
            pose_model,
            img,
            person_results,
            bbox_thr=BBOX_THR,
            format='xyxy',
            dataset=dataset,
            return_heatmap=return_heatmap,
            outputs=output_layer_names)
        # print(pose_results[0]["bbox"])
        ############################################################ 유사도 측정 ##################################################################################
        try:
            b1_point = pose_results[0]["bbox"] # 첫번째 사람 
            b2_point = pose_results[1]["bbox"] # 오른쪽 사람

            for i, p_point in enumerate(pose_results[0]["keypoints"]):
                if i == 0:
                    nose_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 1:    
                    head_bottom_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 2:    
                    head_top_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 3:    
                    left_ear_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 4:    
                    right_ear_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 5:    
                    left_shoulder_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 6:    
                    right_shoulder_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 7:    
                    left_elbow_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 8:    
                    right_elbow_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 9:            
                    left_wrist_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 10:    
                    right_wrist_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 11:    
                    left_hip_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 12:    
                    right_hip_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 13:    
                    left_knee_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 14:    
                    right_knee_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]    
                elif i == 15:    
                    left_ankle_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]
                elif i == 16:    
                    right_ankle_1 = [[(p_point[0]-b1_point[0])/(b1_point[2]-b1_point[0]), (p_point[1]-b1_point[1])/(b1_point[3]-b1_point[1])]]

            for i, p_point in enumerate(pose_results[1]["keypoints"]):
                if i == 0:
                    nose_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 1:    
                    head_bottom_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 2:    
                    head_top_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 3:    
                    left_ear_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 4:    
                    right_ear_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 5:    
                    left_shoulder_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 6:    
                    right_shoulder_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 7:    
                    left_elbow_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 8:    
                    right_elbow_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 9:
                    left_wrist_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 10:    
                    right_wrist_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 11:    
                    left_hip_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 12:    
                    right_hip_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 13:    
                    left_knee_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 14:    
                    right_knee_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 15:    
                    left_ankle_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]
                elif i == 16:    
                    right_ankle_2 = [[(p_point[0]-b2_point[0])/(b2_point[2]-b2_point[0]), (p_point[1]-b2_point[1])/(b2_point[3]-b2_point[1])]]

            # 머리부분
            nose_score = cosine_similarity(nose_1, nose_2)
            head_bottom_score = cosine_similarity(head_bottom_1, head_bottom_2)
            head_top_score = cosine_similarity(head_top_1, head_top_2)
            left_ear_score = cosine_similarity(left_ear_1, left_ear_2)
            right_ear_score = cosine_similarity(right_ear_1, right_ear_2)

            # 몸 부분
            left_shoulder_score = cosine_similarity(left_shoulder_1, left_shoulder_2)
            right_shoulder_score = cosine_similarity(right_shoulder_1, right_shoulder_2)
            left_hip_score = cosine_similarity(left_hip_1, left_hip_2)
            right_hip_score = cosine_similarity(right_hip_1, right_hip_2)


            left_elbow_score = cosine_similarity(left_elbow_1, left_elbow_2)
            right_elbow_score = cosine_similarity(right_elbow_1, right_elbow_2)
            left_wrist_score = cosine_similarity(left_wrist_1, left_wrist_2)
            right_wrist_score = cosine_similarity(right_wrist_1, right_wrist_2)
            left_knee_score = cosine_similarity(left_knee_1, left_knee_2)
            right_knee_score = cosine_similarity(right_knee_1, right_knee_2)
            left_ankle_score = cosine_similarity(left_ankle_1, left_ankle_2)
            right_ankle_score = cosine_similarity(right_ankle_1, right_ankle_2)
            
            # 
            all_score = ((nose_score + head_bottom_score + head_top_score + left_ear_score + right_ear_score)/5
                            + (left_shoulder_score + right_shoulder_score + left_elbow_score + right_elbow_score)/4 
                            + left_wrist_score + right_wrist_score + left_hip_score + right_hip_score 
                            + left_knee_score + right_knee_score + left_ankle_score + right_ankle_score)/10
            
            # 점수 산출 
            if all_score >= 0.998:
                ALL += 5
                score = 5
                print("현재 당신의 정확도는 {}% | + 5점".format(all_score*100))
                print("현재 당신의 점수 : {}".format(ALL))
            elif all_score >= 0.95:
                ALL += 4
                score = 4
                print("현재 당신의 정확도는 {}% | + 4점".format(all_score*100))
                print("현재 당신의 점수 : {}".format(ALL))
            elif all_score >= 0.90:
                ALL += 3
                score = 3
                print("현재 당신의 정확도는 {}% | + 3점".format(all_score*100))
                print("현재 당신의 점수 : {}".format(ALL))
            elif all_score >= 0.85:
                ALL += 2
                score = 2
                print("현재 당신의 정확도는 {}% | + 2점".format(all_score*100))
                print("현재 당신의 점수 : {}".format(ALL))
            elif all_score >= 0.80:
                ALL += 1
                score = 1
                print("현재 당신의 정확도는 {}% | + 1점".format(all_score*100))
                print("현재 당신의 점수 : {}".format(ALL))
       
        except:
            pass
        #############################################################################################################################################################
        
        
        # show the results
        vis_img = vis_pose_result(
            pose_model,
            img,
            pose_results,
            dataset=dataset,
            kpt_score_thr=KPT_THR,
            radius=RADIUS,
            thickness=THICKNESS,
            show=False)

        text = "+ {} | Your current score : {}".format(score, ALL)
        if SHOW == True:
            cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Image', 1920,540)
            cv2.putText(vis_img,text, (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2,cv2.LINE_AA)
            cv2.imshow('Image', vis_img)

        if save_out_video:
            videoWriter.write(vis_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        


    cap.release()
    if save_out_video:
        videoWriter.release()
    cv2.destroyAllWindows()

    print("전체 스코어 점수 : {}".format(ALL))
   

if __name__ == '__main__':
    det_Pose_Video()
