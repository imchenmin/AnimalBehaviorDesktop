import cv2
import numpy as np
def getCrop(frame, x, y, width, height):

    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    w = 160
    h = 160

    if x > w and x + w < width:
        x1 = x - w
        x2 = x + w
    elif x < w:
        x1 = 0
        x2 = 2*w
    elif x + w >= width:
        x1 = width - 2*w
        x2 = width

    if y > h and y + h < height:
        y1 = y - h
        y2 = y + h
    elif y < h:
        y1 = 0
        y2 = 2*h
    elif y + h >= height:
        y1 = height - 2*h
        y2 = height
    
    return frame[y1:y2,x1:x2], x1, y1, x2, y2

def crop_file(filename):
    output_filename = filename[:-4] + '_crop.mp4'
    cap = cv2.VideoCapture(filename)
    ret, frame0 = cap.read()
    frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((3,3),np.uint8)
    if not ret:
        print('No frames')
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
        mask = cv2.subtract(frame, frame0)
        
        ret, mask = cv2.threshold(mask,30,255,cv2.THRESH_BINARY)
        mask = cv2.bitwise_not(src=mask)

        #开操作，去除白噪声。先erode
        #闭操作：消除黑色的小块，填充闭合区域
        mask = cv2.erode(mask, kernel, iterations=3)#前景物体变小，整幅图像的白色区域会减少,断连
        mask = cv2.dilate(mask, kernel, iterations=2)
        
        getCrop()
    return output_filename