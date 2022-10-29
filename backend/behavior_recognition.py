from yolov5.models.experimental import attempt_load
from yolov5.utils.general import check_img_size, non_max_suppression, scale_coords
from yolov5.utils.torch_utils import select_device
import pandas as pd
import cv2
import torch
import numpy as np
from yolov5.utils.datasets import letterbox
from multiprocessing import Process
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
    clsname = ['Wall', 'Stand', 'Normal', 'Wash', 'Groom']
    clsweight = [1,2,0,3,4]
    wall_counter = BehaviorCounter(fps=60, threshold=10, filter_frame=10, type='Wall')
    stand_counter = BehaviorCounter(fps=60, threshold=10, filter_frame=10, type='Stand')
    wash_counter = BehaviorCounter(fps=60, threshold=10, filter_frame=10, type='Wash')
    groom_counter = BehaviorCounter(fps=60, threshold=10, filter_frame=10, type='Groom')

    # Load model
    model = attempt_load(yolo_weights, device=device)  # load FP32 model
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

    vid_writer = cv2.VideoWriter(csv_path[:-4]+'.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frameps, (320, 320))
    #cv2.namedWindow('res',0)
    #cv2.resizeWindow('res',width=1280,height=360)
    while True:
        frame_idx+=1
        ret, frame = cap.read()
        if not ret:
            break
        frame_right = frame

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

        conf_max_right = 0
        conf_max_right_label = 0
        conf_max_right_box = [0,0,0,0]
        for i, det in enumerate(pred_right):  # detections per image
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img_right.shape[2:], det[:, :4], frame_right.shape).round()
                # Write results
                for *xyxy, conf, cls in reversed(det):
                    # to deep sort format
                    x_c, y_c, bbox_w, bbox_h = xyxy_to_xywh(*xyxy)
                    #### change here ####
                    if int(cls.item()) == 0:
                        if 2 * conf > conf_max_right:
                            conf_max_right_label = 0
                            conf_max_right = 1.2 * conf
                            conf_max_right_box = [x_c, y_c, bbox_w, bbox_h]
                    if int(cls.item()) == 1:
                        if conf > conf_max_right:
                            conf_max_right_label = 1
                            conf_max_right = 1 * conf
                            conf_max_right_box = [x_c, y_c, bbox_w, bbox_h]
                    if int(cls.item()) == 3:
                        if 3 * conf > conf_max_right:
                            conf_max_right_label = 3
                            conf_max_right = 1.5 * conf
                            conf_max_right_box = [x_c, y_c, bbox_w, bbox_h]
                    if int(cls.item()) == 4:
                        if 3 * conf > conf_max_right:
                            conf_max_right_label = 4
                            conf_max_right = 1.5 * conf
                            conf_max_right_box = [x_c, y_c, bbox_w, bbox_h]
    
        if conf_max_right > 0:
            cur_label = conf_max_right_label
            x_c, y_c, bbox_w, bbox_h = conf_max_right_box
            cv2.rectangle(frame_right, (int(x_c - bbox_w/2), int(y_c - bbox_h/2)), (int(x_c + bbox_w/2), int(y_c + bbox_h/2)), (0, 0, 255), 2)
            cv2.putText(frame_right, clsname[conf_max_right_label], (int(x_c - bbox_w/2), int(y_c - bbox_h/2 - 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        else:
            cur_label = -1

        if cur_label == -1:
            wall_counter.read()
            stand_counter.read()
            wash_counter.read()
            groom_counter.read()
        else:
            if cur_label != 0:
                wall_counter.read()
            else:
                wall_counter.read(0)

            if cur_label != 1:
                stand_counter.read()
            else:
                stand_counter.read(0)

            if cur_label != 3:
                wash_counter.read()
            else:
                wash_counter.read(0)

            if cur_label != 4:
                groom_counter.read()
            else:
                groom_counter.read(0)
        
        vid_writer.write(frame_right)
    cv2.destroyAllWindows()
    vid_writer.release()
    df_wall = pd.DataFrame(wall_counter.res)
    df_stand = pd.DataFrame(stand_counter.res)
    df_wash = pd.DataFrame(wash_counter.res)
    df_groom = pd.DataFrame(groom_counter.res)

    if df_wall.shape[0] != 0:
        df_wall['class'] = 1
        df_wall['type'] = 'Wall'
    if df_stand.shape[0] != 0:
        df_stand['class'] = 2
        df_wall['type'] = 'Stand'
    if df_groom.shape[0] != 0:
        df_groom['class'] = 0
        df_wall['type'] = 'Groom'
    if df_wash.shape[0] != 0:
        df_wash['class'] = 3
        df_wall['type'] = 'Wash'
    df_res = []
    df = []
    if len(df_groom) != 1:
        df_res.append(df_groom[1:]) 
    if len(df_wall) != 1:
        df_res.append(df_wall[1:]) 
    if len(df_stand) != 1:
        df_res.append(df_stand[1:]) 
    if len(df_wash) != 1:
        df_res.append(df_wash[1:])

    if len(df_res) != 0:
        df = pd.concat(df_res,axis=0)
        df[['class','start_time','end_time','type']].to_csv(csv_path)

def init(source,output_path):
    with torch.no_grad():
        detect(source, 'C:\\assets\\reserve.pt', 640, output_path)
    
def start_recognition(filepath):
    print('Recognition Start ' + filepath)
    init(filepath, filepath + "_detection_result.csv")
    print('Recognition FINISH ' + filepath)
    return 'done'
