import cv2
import csv
from collections import deque
import numpy as np
def output_video(videopath,videoname,polylist,namelist,resultpath):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    result_data = []
    position_data=[]
    posititon_to_draw=deque()
    csv_path = resultpath+videoname+".csv"
    result_path = resultpath+videoname+"_result.csv"
    with open(result_path) as f:
        reader = csv.reader(f)
        raw = list(reader)
        result_data = list(map(lambda q: (int(q[0]), int(q[1]),q[2]), raw))
    f.close()
    with open(csv_path) as f:
        reader = csv.reader(f)
        raw = list(reader)
        position_data = list(map(lambda q: (int(q[0]), int(q[1])), raw))
    f.close()
    result_iter = iter(result_data)
    cap = cv2.VideoCapture(videopath+"/"+videoname+".mp4")
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    FPS = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(resultpath+videoname+'_result.mp4',fourcc, FPS, (frame_width,frame_height),True)
    frameid=0
    lb = 0
    ub = 0
    name = ""
    try:
        lb,ub,name = next(result_iter)
    except StopIteration:
        lb = -1
        ub = -1
        name =""
    
    while(True):
        ret, frame = cap.read()
        if ret==False:
            break
        if (frameid>ub):
            try:
                lb,ub,name = next(result_iter)
            except StopIteration:
                lb = -1
                ub = -1
                name =""
        for i in range(0,len(namelist)):
            font = cv2.FONT_HERSHEY_SIMPLEX
            temp = np.array(polylist[i],np.int32)
            pts = temp.reshape((-1,1,2))
            #draw poly
            cv2.polylines(frame,[pts],True,(0,0,0),thickness=4)
            midx = 0
            midy = 0
            for j in range(0, len(polylist[i])):
                midx+=polylist[i][j][0]
                midy+=polylist[i][j][1]
            midx/=len(polylist[i])
            midy/=len(polylist[i])
            #draw text
            if (frameid>=lb) and (frameid<=ub) and (namelist[i]==name):
                cv2.putText(frame,namelist[i],(int(midx),int(midy)), font, 2,(0,0,255),4,cv2.LINE_AA)
            else:
                #draw common picture
                cv2.putText(frame,namelist[i],(int(midx),int(midy)), font, 2,(0,0,0),4,cv2.LINE_AA)
        (x,y) = position_data[frameid]
        if len(posititon_to_draw)>=5*FPS:
            posititon_to_draw.pop()
            posititon_to_draw.appendleft((x,y))
        else:
            posititon_to_draw.appendleft((x,y))
        (s_x,s_y)=posititon_to_draw[0]
        cv2.circle(frame,(s_x,s_y),15,(255,0,0),1)
        last_x = s_x
        last_y = s_y
        for index in range(1,len(posititon_to_draw)):
            #draw track
            cv2.line(frame,(last_x,last_y),posititon_to_draw[index],(0,255,0),2)
            (last_x,last_y) = posititon_to_draw[index]
        out.write(frame)
        frameid = frameid+1
        #print(frameid)
    cap.release()
    out.release()

# namelist = ['close', 'open-1', 'open-2']
# polylist = [[[544, 463], [1451, 463], [1451, 550], [544, 550]], [[961, 45], [1036, 45], [1036, 456], [961, 456]], [[958, 557], [1027, 557], [1027, 960], [958, 960]]]
# output_video("C:\\Users\\Sun\\Desktop\\maze\\eight_maze_short_demo.mp4","eight_maze_short_demo",[],[])
