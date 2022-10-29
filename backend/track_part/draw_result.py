import cv2 as cv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
def draw_raw_img(namelist,polylist,width,height,videoname,resultpath):
    font = cv.FONT_HERSHEY_SIMPLEX
    newImg = np.zeros((height, width,3), np.uint8)
    newImg.fill(255)
    for i in range(0, len(polylist)):
        temp = np.array(polylist[i],np.int32)
        pts = temp.reshape((-1,1,2))
        cv.polylines(newImg,[pts],True,(0,0,0),thickness=4)
        midx = 0
        midy = 0
        for j in range(0, len(polylist[i])):
            midx+=polylist[i][j][0]
            midy+=polylist[i][j][1]
        midx/=len(polylist[i])
        midy/=len(polylist[i])
        cv.putText(newImg,namelist[i],(int(midx),int(midy)), font, 2,(0,0,0),4,cv.LINE_AA)
        #cv.putText(newImg,namelist[i],(int(midx),int(midy)), font, 0.5,( 0,0,0),1,cv.LINE_AA)
    cv.imwrite(resultpath+videoname+'_raw.png', newImg)

# def read_points(path):
#     df = pd.read_table(path,sep=',',header=None)
#     data = df.values
#     bodyx=np.hsplit(data,4)[0].flatten()
#     bodyy=np.hsplit(data,4)[1].flatten()
#     return bodyx, bodyy

# def draw_heat_map(img, bodyx, bodyy,width,height):
#     preImg = np.zeros((height,width), np.uint8)
#     radius = 5
#     for i in range(0,len(bodyx)):
#         low_x = bodyx[i]-radius
#         if (low_x<0):
#             low_x=0
#         low_y = bodyy[i]-radius
#         if (low_y<0):
#             low_y=0
#         high_x = bodyx[i]+radius
#         if (high_x>=width):
#             high_x=width-1
#         high_y = bodyy[i]+radius
#         if (high_y>=height):
#             high_y=height-1
#         for x in range(low_x,high_x+1):
#             for y in range(low_y,high_y+1):
#                 if ((x - bodyx[i]) ** 2 + (y - bodyy[i]) ** 2 < radius ** 2):
#                     preImg[y][x] = preImg[y][x]+1
#     heatmapshow = None
#     heatmapshow = cv.normalize(preImg, heatmapshow, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)
#     heatmapshow = cv.applyColorMap(heatmapshow, cv.COLORMAP_JET)
#     kernel = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]], np.float32)
#     dst = cv.filter2D(heatmapshow, -1, kernel=kernel)
#     cv.imshow("Heatmap", dst)
#     cv.waitKey(0)

