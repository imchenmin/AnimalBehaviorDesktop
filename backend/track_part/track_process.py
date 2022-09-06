import math
import re
import numpy as np
import cv2
import csv
import datetime
#import yolov5_main
# from bg_for_multi_user_click import multi_detect_handler
def calculatex(x,y,x_center,y_center,rotate):
    return int((x-x_center)*math.cos(rotate) - (y-y_center)*math.sin(rotate)+x_center)
def calculatey(x,y,x_center,y_center,rotate):
    return int((x-x_center)*math.sin(rotate) + (y-y_center)*math.cos(rotate)+y_center)
def rotateRec(rec_info):
    rec_info = rec_info.split(',') #left,top,height,width,rotate
    bias = 9 #index bias because of the pad in the page
    x1 = int(rec_info[0][:-2])
    y1 = int(rec_info[1][:-2])
    x2 = int(rec_info[0][:-2])+int(rec_info[3][:-2])
    y2 = int(rec_info[1][:-2])
    x3 = int(rec_info[0][:-2])
    y3 = int(rec_info[1][:-2])+int(rec_info[2][:-2])
    x4 = int(rec_info[0][:-2])+int(rec_info[3][:-2])
    y4 = int(rec_info[1][:-2])+int(rec_info[2][:-2])
    if (len(rec_info[4])!=0):
        rotate = float(rec_info[4][(rec_info[4].find('(')+1):(rec_info[4].find('rad'))])
        x_center = x1+(x2-x1)/2
        y_center = y1+(y3-y1)/2
        new_x1 = calculatex(x1,y1,x_center,y_center,rotate)
        new_y1 = calculatey(x1,y1,x_center,y_center,rotate)
        new_x2 = calculatex(x2,y2,x_center,y_center,rotate)
        new_y2 = calculatey(x2,y2,x_center,y_center,rotate)
        new_x3 = calculatex(x3,y3,x_center,y_center,rotate)
        new_y3 = calculatey(x3,y3,x_center,y_center,rotate)
        new_x4 = calculatex(x4,y4,x_center,y_center,rotate)
        new_y4 = calculatey(x4,y4,x_center,y_center,rotate)
        points=np.array([new_x1,new_y1,new_x2,new_y2,new_x4,new_y4,new_x3,new_y3])-bias
        points = points.reshape(4,2)
        return points
    '''
    n1  n2
    n3  n4
    return should be n1,n2,n4,n3
    '''
    points=np.array([x1,y1,x2,y2,x4,y4,x3,y3])-bias
    points = points.reshape(4,2)
    return points


def preProcessRecInfo(str):
    name = str[0:str.index(',')]
    info = str[str.index(',')+1:]
    return name,rotateRec(info)

def adjust_pts_order(pts_2ds):

    ''' sort rectangle points by clockwise '''

    cen_x, cen_y = np.mean(pts_2ds, axis=0)
    #refer_line = np.array([10,0])

    new_2ds = []
    for i in range(len(pts_2ds)):

        o_x = pts_2ds[i][0] - cen_x
        o_y = pts_2ds[i][1] - cen_y

        atan2 = np.arctan2(o_y, o_x)
        if atan2 < 0:
            atan2 += np.pi * 2
        new_2ds.append([pts_2ds[i], atan2])

    new_2ds = sorted(new_2ds, key=lambda x:x[1])

    order_2ds = np.array([x[0] for x in new_2ds])
    order_2ds = np.append(order_2ds,[order_2ds[0]],0)
    return order_2ds


def preProcessPolyInfo(str):
    new_str=re.split(',|;',str)
    name = new_str[0]
    points = []
    for i in range(1, len(new_str)-1,2):
        points.append([int(new_str[i]),int(new_str[i+1])])
        i=i+1

    #return name, adjust_pts_order(np.array(points))
    return name,points

def isRayIntersectsSegment(poi,s_poi,e_poi): #[x,y] [lng,lat]
    #输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    if s_poi[1]==e_poi[1]: #排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if s_poi[1]>poi[1] and e_poi[1]>poi[1]: #线段在射线上边
        return False
    if s_poi[1]<poi[1] and e_poi[1]<poi[1]: #线段在射线下边
        return False
    if s_poi[1]==poi[1] and e_poi[1]>poi[1]: #交点为下端点，对应spoint
        return False
    if e_poi[1]==poi[1] and s_poi[1]>poi[1]: #交点为下端点，对应epoint
        return False
    if s_poi[0]<poi[0] and e_poi[0]<poi[0]: #线段在射线左边
        return False

    xseg=e_poi[0]-(e_poi[0]-s_poi[0])*(e_poi[1]-poi[1])/(e_poi[1]-s_poi[1]) #求交
    if xseg<poi[0]: #交点在射线起点的左侧
        return False
    return True  #排除上述情况之后

#poly,namelist可作为全局变量在detect方法中存在，仅需将每一帧的坐标poi传入即可,嵌入了csv结果的输出
def isPoiWithinPoly(csv_path,poly,namelist,videoname,videopath,resultpath):
    cap = cv2.VideoCapture(videopath+"/"+videoname+".mp4")
    #print("!!!!!!!!!!!!!!!!!!!!")
    print(videopath)
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    cap.release()
    with open(csv_path) as f:
        reader = csv.reader(f)
        raw = list(reader)
        point_data = list(map(lambda q: (int(q[0]), int(q[1])), raw))
    pre = ""
    now = ""
    beginframe = 0
    flag = 0
    with open(resultpath+videoname+"_result.csv","w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        for frame_id in range(0, len(point_data)):
            #输入：点，多边形三维数组
            #poly=[[[x1,y1],[x2,y2],……,[xn,yn],[x1,y1]],[[w1,t1],……[wk,tk]]] 三维数组
            flag = 0
            for t in range(len(poly)): #循环每条边的曲线->each polygon 是二维数组[[x1,y1],…[xn,yn]]
                epoly = poly[t]
                sinsc=0
                for i in range(len(epoly)-1): #[0,len-1]
                    s_poi=epoly[i]
                    e_poi=epoly[i+1]
                    if isRayIntersectsSegment(point_data[frame_id],s_poi,e_poi):
                        sinsc+=1 #有交点就加1
                #此处判断是否在多边形内
                if isRayIntersectsSegment(point_data[frame_id],e_poi,epoly[0]):
                        sinsc+=1
                if sinsc%2==1:
                    now = namelist[t]
                    flag = 1
                    break
            if (pre!="" and flag==0):
                writer.writerow([beginframe,frame_id,pre])
                pre = ""
                continue
            if (pre=="" and flag==1):
                beginframe = frame_id
                pre = now
                continue
            if (pre!="" and flag==1):
                if pre==now:
                    continue
                if pre!=now:
                    writer.writerow([beginframe,frame_id,pre])
                    pre = now
                    beginframe = frame_id
                    continue
        #When loop end, check for last condition
        if(pre!=""):
            writer.writerow([beginframe,len(point_data),pre])
    cvt_time_result(resultpath+videoname+"_result.csv",videoname,FPS,resultpath)
    csvfile.close()
def cvt_time_result(csvpath,videoname,FPS,resultpath):
    with open(csvpath) as f:
        reader = csv.reader(f)
        raw = list(reader)
        data= list(map(lambda q: (int(q[0]), int(q[1]),q[2]), raw))
    f.close()
    with open(resultpath+videoname+"_timeresult.csv","w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        for begin,end,name in data:
            writer.writerow([datetime.timedelta(seconds=(begin/FPS)),datetime.timedelta(seconds=(end/FPS)),name])
    csvfile.close()