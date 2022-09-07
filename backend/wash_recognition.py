import sys
sys.path.insert(0, 'D:\\workspace\\AnimalBehaviorDesktop\\backend\\yolov5')
sys.path.insert(0, 'D:\\workspace\\AnimalBehaviorDesktop\\backend\\assets')
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

def detect(source, yolo_weights, imgsz, csv_path):
 
    half=False  # use FP16 half-precision inference
    init = 0
    from BehaviorCounter import BehaviorCounter
    bcounter = BehaviorCounter(fps=60, threshold=10, filter_frame=10)

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
    ret, frame = cap.read()

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    frame_idx = 0

    vid_writer = cv2.VideoWriter(csv_path[:-4]+'.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frameps, (840, 720))
    label_wash =[]

    while True:
        frame_idx+=1
      
        t1 = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        # frame = frame[375:375+375, 135:135 + 1700]
        frame = frame[:, 1280+160:1280+1000]
        img = letterbox(frame)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device)
        if half:
            img = img.half()  # uint8 to fp16/32
        else:
            img = img.float()
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.2, 0.5, None, False)
        conf_norm = [0]
        conf_wash = [0]
        flag = 0
        first = True
        for i, det in enumerate(pred):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if first:
                        bcounter.read(int(cls.item()))
                        first = False
                    # to deep sort format
                    x_c, y_c, bbox_w, bbox_h = xyxy_to_xywh(*xyxy)
                    #### change here ####
                    if int(cls.item()) == 0:
                        if conf > 0.5:
                            cv2.rectangle(frame, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
                            cv2.putText(frame, 'Wash', (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                            flag += 1

                    if int(cls.item()) == 1:
                        conf_norm.append(conf)
            else:
                bcounter.read()
        if flag == 1:
            label_wash.append(1)
        else:
            label_wash.append(0)

        vid_writer.write(frame)
        cv2.imshow('res', frame)
        cv2.waitKey(1)
    df = pd.DataFrame(bcounter.res)
    df['class'] = 0
    df[['class','st','end']].to_csv(csv_path, header=None,index=None)

def init(source,output_path):
    with torch.no_grad():
        detect(source, 'D:\\workspace\\AnimalBehaviorDesktop\\backend\\assets\\best.pt', 640, output_path)

def start_wash_recognition(filepath):
    init(filepath, filepath + "/detection_result.csv")