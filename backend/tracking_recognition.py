from tkinter import CENTER
import cv2
import numpy as np
import math
import csv
import os

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

def crop_top(filename):
    print('start crop', filename)
    cap = cv2.VideoCapture(filename)
    vid_writer = cv2.VideoWriter(filename[:-4]+'_crop.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 60, (320, 320))
    bgcap = cv2.VideoCapture('C:\\Users\\Gianttek\\Desktop\\EZVZ0166.MP4')
    ret, bg = bgcap.read()
    kernel = np.ones((3, 3), np.uint8)
    roi = [481, 2, 974, 974]
    bg = bg[roi[1]:roi[1] + roi[3],roi[0]:roi[0] + roi[2]]
    listx = []
    listy = []
    print(roi)
    index = 0
    while(True):
        ret, frame = cap.read()
        index = index + 1
        if ret==False:
            break
        else:    
            frame = frame[roi[1]:roi[1] + roi[3],roi[0]:roi[0] + roi[2]]
            mask = cv2.subtract(frame, bg)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            ret,mask = cv2.threshold(mask,30,255,cv2.THRESH_BINARY)
            
            mask = cv2.erode(mask, kernel, iterations=2)
            mask = cv2.dilate(mask, kernel, iterations=2)
            mask = cv2.erode(mask, kernel, iterations=5)
            # cv2.imshow('real', mask)            

            area = []       
            cnt, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            areasize = []
            shouldcut = 0
            for j in range(len(cnt)):
                size = cv2.contourArea(cnt[j])
                if (size > 500):
                    area.append(cnt[j])
                    areasize.append(size)
                if (size > 4200):
                    shouldcut = 1
            if len(area)==3:
                xypluslist = []
                todrawlist = []
                tempxypluslist = []
                for anarea in area:
                    (x,y), (a,b) ,angle = cv2.fitEllipse(anarea)
                    x = int(x)
                    y = int(y)
                    a = int(a*2.2/3)
                    b = int(b*2.2/3)
                    xypluslist.append(x+y)
                    todrawlist.append([(x,y),(a,b),angle])
                    tempxypluslist.append(x+y)
                maxindex = tempxypluslist.index(max(tempxypluslist))
                del tempxypluslist[maxindex]
                maxindex = xypluslist.index(max(tempxypluslist))
                # for t in range(len(area)):
                #     if t!=maxindex:
                #         pass
                        # cv2.ellipse(frame, todrawlist[t][0], todrawlist[t][1], todrawlist[t][2], 0, 360, (0, 0, 0), -1)
                real = [todrawlist[maxindex][0], todrawlist[maxindex][1] ,todrawlist[maxindex][2]]
            elif len(area)==2:
                (x,y), (a,b) ,angle = cv2.fitEllipse(area[0])
                (x2,y2), (a2,b2) ,angle2 = cv2.fitEllipse(area[1])
                x = int(x)
                y = int(y)
                a = int(a)
                b = int(b)
                x2 = int(x2)
                y2 = int(y2)
                a2 = int(a2)
                b2 = int(b2)
                x_diff = abs(x-x2)
                y_diff = abs(y-y2)
                if (x_diff>y_diff):
                    if x<x2:
                        real = [(x2,y2), (a2,b2) ,angle2]
                        mirror = [(x,y), (a,b) ,angle]
                    else:
                        real = [(x,y), (a,b) ,angle]
                        mirror = [(x2,y2), (a2,b2) ,angle2]
                else:
                    if y<y2:
                        real = [(x,y), (a,b) ,angle]
                        mirror = [(x2,y2), (a2,b2) ,angle2]
                    else:
                        real = [(x2,y2), (a2,b2) ,angle2]
                        mirror = [(x,y), (a,b) ,angle]
                mirrorx, mirrory = mirror[1]
                mirrorx = int(mirrorx*2.2/3)    
                mirrory = int(mirrory*2.2/3)
                # cv2.ellipse(frame, mirror[0], (mirrorx,mirrory), mirror[2], 0, 360, (0, 0, 0), -1)
            else:
                if (len(area)==0):
                    real = [(320,320)]
                else:
                    (x,y), (a,b) ,angle = cv2.fitEllipse(area[0])
                    x = int(x)
                    y = int(y)
                    a = int(a)
                    b = int(b)          
                    real = [(x,y), (a,b) ,angle]
                   
            if shouldcut:
                if (real[1][0]>real[1][1]):

                    length = int(real[1][0])
                else:
                    length = int(real[1][1])
                length = length*0.25
                angle = real[2]
                if angle > 90:
                    angle = angle - 90
                else:
                    angle = angle + 90
                xtop = real[0][0] + math.cos(math.radians(angle))*length
                ytop = real[0][1] + math.sin(math.radians(angle))*length
                xbot = real[0][0] + math.cos(math.radians(angle+180))*length
                ybot = real[0][1] + math.sin(math.radians(angle+180))*length 
                apoint = (int(xtop),int(ytop))
                bpoint = (int(xbot),int(ybot))
                xdiff = abs(apoint[0]-bpoint[0])
                ydiff = abs(apoint[1]-bpoint[1])
                if (xdiff>ydiff):
                    if (apoint[0]>bpoint[0]):
                        realpoint = apoint
                    else:
                        realpoint = bpoint
                else:
                    if (apoint[1]<bpoint[1]):
                        realpoint = apoint
                    else:
                        realpoint = bpoint
            else:
                realpoint = real[0]
            # cv2.ellipse(frame, real[0], real[1], real[2], 0, 360, (0, 0, 255), 1)
            # cv2.circle(frame,(realpoint[0],realpoint[1]),2,(0,0,255),1)
            listx.append(realpoint[0] + roi[0])
            listy.append(realpoint[1] + roi[1])
            # cv2.imshow('crop',frame)
            # if cv2.waitKey(1) & 0xff == 27:
            #     break

    with open(filename[:-4]+'_part.csv', 'w') as f:
        for i in range(len(listx)):
            f.write(str(listx[i]) + ',' + str(listy[i]) + '\n')
    cap.release()
    cv2.destroyAllWindows()
    vid_writer.release()

def combine_csv(self):
    resultpath = self.full_name
    csvparts = os.listdir(self.full_name)
    csvcombined = os.path.join(resultpath + '/result/','video__all.csv')
    with open(csvcombined,"w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        for files in csvparts:
            if files.endswith('part.csv'):
                csvtoreadpath = os.path.join(resultpath,files)
                with open(csvtoreadpath,'r') as toread:
                    read = csv.reader(toread)
                    for row in read:
                        writer.writerow(row)

# crop('C:\\Users\\Gianttek\\Desktop\\EZVZ0131.MP4')