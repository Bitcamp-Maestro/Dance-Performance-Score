import os
import warnings
import cv2

from mmpose.apis.inference import (inference_top_down_pose_model, 
                                    init_pose_model, 
                                    process_mmdet_results, 
                                    vis_pose_result)

from mmdet.apis.inference import (inference_detector, 
                                    init_detector)


class Play():
    def __init__(self):
        """
        Input file:
            Model Input
                deet__init__() : config, checkpoint, device \n
                pose__init__() : config, checkpoint, device \n

            User Input
                Video() : file, .mp4,
                Output_phat : 저장될 위치 경로
        """
        pass


    def det__init__(self, det_config, det_checkpoint, device="cuda:0"):
        """
        Input:
            Detction -> config, checkpoint, device
            객체 인식 : config파일, checkpoint파일, 디바이스 종류
        """
        self.det_config = det_config
        self.det_checkpoint = det_checkpoint
        self.det_device = device

    def pose__init__(self, pose_config, pose_checkpoint, device="cuda:0"):
        """
        Input:
            Pose -> config, checkpoint, device
            포즈 인식 : config파일, checkpoint파일, 디바이스 종류
        """
        self.pose_config = pose_config
        self.pose_checkpoint = pose_checkpoint
        self.pose_device = device

    def det_Pose_Video(self, video, outpath="result"):
        SHOW = True                                 # 보여줄건지 선택 변수
        DET_CAT_ID = 1      # Category id for bounding box detection model

        # 1. build the detection moedl from a fonfig file and a checkpoint file
        det_model = init_detector(self.det_config, self.det_checkpoint, device=self.det_device)
        
        # 2. build the pose model from a config file and a checkpoint file
        pose_model = init_pose_model(self.pose_config, self.pose_checkpoint, device=self.pose_device)

        # test dataset 설정
        # dataset = pose_model.cfg.data['test']['type']
        
        # 3. 영상 파일을 불러오기
        cap = cv2.VideoCapture(video)
        # assert cap.isOpened(), f'Faild to load video file {VIDEO_PATH}'

        # 만약 out 루트가 있는지 없는지 확인
        if outpath == '':
            save_out_video = False
        else:
            os.makedirs(outpath, exist_ok=True)
            save_out_video = True

        if save_out_video:
            fps = cap.get(cv2.CAP_PROP_FPS)
            size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            videoWriter = cv2.VideoWriter(
                os.path.join(outpath,
                            f'DancerFlow_{os.path.basename(video)}'), fourcc,
                fps, size)

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
                bbox_thr=0.5,
                format='xyxy',
                # dataset=dataset,
                return_heatmap=return_heatmap,
                outputs=output_layer_names)

            # show the results
            vis_img = vis_pose_result(
                pose_model,
                img,
                pose_results,
                # dataset=dataset,
                kpt_score_thr=0.5,
                radius=4,               # 원 크기
                thickness=2,            # 관절 두께
                show=False)

            if SHOW == True:
                cv2.imshow('Image', vis_img)

            if save_out_video:
                videoWriter.write(vis_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        if save_out_video:
            videoWriter.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    
    DET_CONFIG = "configs/detection/faster_rcnn_r50_fpn_coco.py"                                                # Detection config 파일
    DET_CHECKPOINT = "https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/faster_rcnn_r50_fpn_1x_coco/faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth"                  # Detection 훈련 모델 파일
    POSE_CONFIG = "configs/pose/body/2d_kpt_sview_rgb_img/topdown_heatmap/coco/hrnet_w48_coco_256x192.py"       # Pose config 파일
    POSE_CHECKPOINT = "https://download.openmmlab.com/mmpose/checkpoints/pose/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth"                           # Pose 훈련 모델 파일
    VIDEO = "./sample_data/target.mp4"
    
    play= Play()
    play.det__init__(DET_CONFIG, DET_CHECKPOINT, device="cpu")
    play.pose__init__(POSE_CONFIG, POSE_CHECKPOINT, device="cpu")
    play.det_Pose_Video(VIDEO)