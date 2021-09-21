import json
import re

from cv2 import pointPolygonTest


class Form():
    def data_form(dict, i , keypoint):
        
        if i == 0:
            dict["nose"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 1:
            dict["left_eye"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 2:
            dict["right_eye"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 3:
            dict["left_ear"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 4:
            dict["right_ear"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 5:
            dict["left_shoulder"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 6:
            dict["right_shoulder"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 7:
            dict["left_elbow"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 8:
            dict["right_elbow"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 9:
            dict["left_wrist"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 10:
            dict["right_wrist"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 11:
            dict["left_hip"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 12:
            dict["right_hip"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 13:
            dict["left_knee"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 14:
            dict["right_knee"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 15:
            dict["left_ankle"] = [str(keypoint[0]),str(keypoint[1])]
        elif i == 16:
            dict["right_ankle"] = [str(keypoint[0]),str(keypoint[1])]
        return dict

    def make_dic(frame, bbox, keypoint_dic):
        

        data = dict()
        data["frame"] = frame
        data["bbox"] = [str(bbox[0]), str(bbox[1])]
        data["keypoints"] = keypoint_dic
        
        
        return data

