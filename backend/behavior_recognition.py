import sys
import os
from yolov5.models.experimental import attempt_load
from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords
from yolov5.utils.torch_utils import select_device
import pandas as pd
import time
import cv2
import torch
import numpy as np
import csv
from yolov5.utils.datasets import letterbox

def xyxy_to_xywh(*xyxy):
    """" Calculates the relative bounding box from absolute pixel values. """
    bbox_left = min([xyxy[0].item(), xyxy[2].item()])
    bbox_top = min([xyxy[1].item(), xyxy[3].item()])
    bbox_w = abs(xyxy[0].item() - xyxy[2].item())
    bbox_h = abs(xyxy[1].item() - xyxy[3].item())
    x_c = (bbox_left + bbox_w / 2)
    y_c = (bbox_top + bbox_h / 2)
    w = bbox_w
    h = bbox_h
    return x_c, y_c, w, h

def getEach(data, fps):

    res = []
    for i in range(len(data) - 1):
        if data[i] == 0 and data[i + 1] != 0:
            if len(res) == 0:
                res.append(i + 2)
            elif i + 2 - res[-1] > fps * 5:
                res.append(i + 2)
    return res

def detect(source, yolo_weights, imgsz, csv_path, behavior='wash'):
 
    half=False  # use FP16 half-precision inference
    init = 0
    from BehaviorCounter import BehaviorCounter
    if behavior == "wash":
        bcounter = BehaviorCounter(fps=60, threshold=10, filter_frame=10)
    elif behavior == "stand":
        bcounter1 = BehaviorCounter(fps=60, threshold=10, filter_frame=10)
        bcounter2 = BehaviorCounter(fps=60, threshold=10, filter_frame=10)
    device = select_device('0')
    half &= device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(yolo_weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    if half:
        model.half()  # to FP16
    else:
        model.float()

    # Set Dataloader
    cap = cv2.VideoCapture(source)
    frameps = int(cap.get(cv2.CAP_PROP_FPS))
    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    frame_idx = 0

    vid_writer = cv2.VideoWriter(csv_path[:-4]+'.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frameps, (2560, 720))
    cv2.namedWindow('res',0)
    cv2.resizeWindow('res',width=1280,height=360)
    while True:
        frame_idx+=1
        flag_left = -1
        flag_right = -1
        
        t1 = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        frame_right = frame[:, 1280:]
        frame_left = frame[:, :1280]

        img_right = letterbox(frame_right)[0]
        # Convert
        img_right = img_right[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img_right = np.ascontiguousarray(img_right)
        img_right = torch.from_numpy(img_right).to(device)
        if half:
            img_right = img_right.half()  # uint8 to fp16/32
        else:
            img_right = img_right.float()
        img_right /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img_right.ndimension() == 3:
            img_right = img_right.unsqueeze(0)

        pred_right = model(img_right, augment=False)[0]
        pred_right = non_max_suppression(pred_right, 0.2, 0.5, None, False)

        # flag = 0
        first = True

        for i, det in enumerate(pred_right):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img_right.shape[2:], det[:, :4], frame_right.shape).round()
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if first:
                        if behavior == "wash":
                            # bcounter.read(int(int(cls.item()) != 0))
                            flag_right = [int(int(cls.item()) != 0)]
                        elif behavior == "stand":
                            # bcounter1.read(int(int(cls.item()) != 0))
                            # bcounter2.read(int(int(cls.item()) != 1))
                            flag_right = [int(int(cls.item()) != 0), int(int(cls.item()) != 1)]

                        first = False
                    # to deep sort format
                    x_c, y_c, bbox_w, bbox_h = xyxy_to_xywh(*xyxy)
                    #### change here ####
                    if behavior == "wash":
                        if int(cls.item()) == 0:
                            if conf > 0.5:
                                cv2.rectangle(frame_right, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                                cv2.putText(frame_right, 'Wash', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    else:
                        if int(cls.item()) == 0:
                            cv2.rectangle(frame_right, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                            cv2.putText(frame_right, 'Wall', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                        if int(cls.item()) == 1:
                            cv2.rectangle(frame_right, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                            cv2.putText(frame_right, 'Stand', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                        if int(cls.item()) == 2:
                            cv2.rectangle(frame_right, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                            cv2.putText(frame_right, 'Norm', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        img_left = letterbox(frame_left)[0]
        # Convert
        img_left = img_left[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img_left = np.ascontiguousarray(img_left)
        img_left = torch.from_numpy(img_left).to(device)
        if half:
            img_left = img_left.half()  # uint8 to fp16/32
        else:
            img_left = img_left.float()
        img_left /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img_left.ndimension() == 3:
            img_left = img_left.unsqueeze(0)

        pred_right = model(img_left, augment=False)[0]
        pred_right = non_max_suppression(pred_right, 0.2, 0.5, None, False)
 
        # flag = 0
        first = True
        for i, det in enumerate(pred_right):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img_left.shape[2:], det[:, :4], frame_left.shape).round()
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if first:
                        if behavior == "wash":
                            flag_left = [int(int(cls.item()) != 0)]
                        elif behavior == "stand":
                            flag_left = [int(int(cls.item()) != 0), int(int(cls.item()) != 1)]
                        first = False
                    # to deep sort format
                    x_c, y_c, bbox_w, bbox_h = xyxy_to_xywh(*xyxy)
                    #### change here ####
                    if behavior == "wash":
                        if int(cls.item()) == 0:
                            if conf > 0.5:
                                cv2.rectangle(frame_left, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                                cv2.putText(frame_left, 'Wash', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                    else:
                        if int(cls.item()) == 0:
                            cv2.rectangle(frame_left, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                            cv2.putText(frame_left, 'Wall', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                        if int(cls.item()) == 1:
                            cv2.rectangle(frame_left, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                            cv2.putText(frame_left, 'Stand', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                        if int(cls.item()) == 2:
                            cv2.rectangle(frame_left, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                            cv2.putText(frame_left, 'Normal', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        
        
        if behavior == "wash":
            if flag_left != -1 and flag_right != -1:
                bcounter.read(flag_left[0] or flag_right[0])
            elif flag_left != -1:
                bcounter.read(flag_left[0])
            elif flag_right != -1:
                bcounter.read(flag_right[0])
            else:
                bcounter.read()

        elif behavior == "stand":
            if flag_left != -1 and flag_right != -1:
                bcounter1.read(flag_left[0] or flag_right[0])
                bcounter2.read(flag_left[1] or flag_right[1])

            elif flag_left != -1:
                bcounter1.read(flag_left[0])
                bcounter2.read(flag_left[1])
            elif flag_right != -1:
                bcounter1.read(flag_right[0])
                bcounter2.read(flag_right[1])
            else:
                bcounter1.read()
                bcounter2.read()
       
        whole_frame = cv2.hconcat([frame_left, frame_right])#垂直拼接

        vid_writer.write(whole_frame)
        cv2.imshow('res', whole_frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    vid_writer.release()
    if behavior == "wash":
        df = pd.DataFrame(bcounter.res)
        if df.shape[0] != 0:
            df['class'] = 0
        print(df)

    elif behavior == "stand":
        df1 = pd.DataFrame(bcounter1.res)
        df2 = pd.DataFrame(bcounter2.res)
        if df1.shape[0] != 0:
            df1['class'] = 1
        if df2.shape[0] != 0:
            df2['class'] = 2
        df = pd.concat([df1,df2],axis=0)
    return df

def init(source,output_path):
    df_list = [pd.DataFrame.from_dict({"class": [0], "st":[1], 'end':[1]})]
    with torch.no_grad():
        df_list.append(detect(source, 'D:\\assets\\wash.pt', 640, output_path,'wash'))
    with torch.no_grad():
        df_list.append(detect(source, 'D:\\assets\\stand.pt', 640, output_path,'stand'))
    df = pd.concat(df_list,axis=0)
    df[['class','st','end']].to_csv(output_path, header=None,index=None)

def start_recognition(filepath):
    print('Recognition Start')
    init(filepath + '/video1.mp4', filepath + "/detection_result.csv")