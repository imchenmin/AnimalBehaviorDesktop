
import cv2
import numpy as np

def getCrop(frame, x, y, width, height):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    w = 160
    h = 160
    ret = True
    if x > w and x + w < width:
        x1 = x - w
        x2 = x + w
    elif x < w:
        x1 = 0
        x2 = 2*w
    elif x + w > width:
        x1 = width - 2*w
        x2 = width
    else:
        ret = False
    if y > h and y + h < height:
        y1 = y - h
        y2 = y + h
    elif y < h:
        y1 = 0
        y2 = 2*h
    elif y + h > height:
        y1 = height - 2*h
        y2 = height
    else:
        ret = False
    return ret, frame[y1:y2,x1:x2]

def crop(filename):
    print('start crop', filename)
    cap = cv2.VideoCapture(filename)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vid_writer = cv2.VideoWriter(filename[:-4]+'_crop.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 60, (320, 320))
    ret, bg = cap.read()
    kernel = np.ones((3, 3), np.uint8)
    x=320
    y=320
    roi = [481, 2, 974, 988]
    bg = bg[roi[1]:roi[1] + roi[3],roi[0]:roi[0] + roi[2]]
    listx = []
    listy = []
    print(roi)
    while(True):
        ret, frame = cap.read()

        if ret==False:
            break
        else:    
            frame = frame[roi[1]:roi[1] + roi[3],roi[0]:roi[0] + roi[2]]
            mask = cv2.subtract(frame, bg)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            # cv2.imshow('real', mask)
            ret,mask = cv2.threshold(mask,30,255,cv2.THRESH_BINARY)
            
            mask = cv2.erode(mask, kernel, iterations=2)
            mask = cv2.dilate(mask, kernel, iterations=2)

            area = []              
            cnt, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            for j in range(len(cnt)):
                area.append(cv2.contourArea(cnt[j]))
                max_idx = np.argmax(area)
            try:
                (x,y), (a,b) ,angle = cv2.fitEllipse(cnt[max_idx])
            except:
                # print('error')
                pass
            flag, tcrop = getCrop(frame, int(x), int(y), roi[2], roi[3])
            if flag:
                crop = tcrop
                realx = x
                realy = y
            listx.append(roi[0] + realx)
            listy.append(roi[1] + realy)

            vid_writer.write(crop)
            # cv2.imshow('fgmk', mask)
            # cv2.imshow('origin', crop)
            if cv2.waitKey(1) & 0xff == 27:
                break
    with open(filename[:-4]+'_xy.csv', 'w') as f:
        for i in range(len(listx)):
            f.write(str(listx[i]) + ',' + str(listy[i]) + '\n')
    cap.release()
    cv2.destroyAllWindows()
    vid_writer.release()


# crop('D:\\top\\EZVZ0051.MP4')
# crop('C:\\Users\\Administrator\\Desktop\\videos\\EZVZ0052.MP4')
# crop('C:\\Users\\Administrator\\Desktop\\videos\\EZVZ0053.MP4')
