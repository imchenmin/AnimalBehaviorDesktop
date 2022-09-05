import cv2
import csv
def draw_track(csv_path,video_name):
    with open(csv_path) as f:
        reader = csv.reader(f)
        raw = list(reader)
        gaze_data = list(map(lambda q: (int(q[0]), int(q[1])), raw))
        bg = cv2.imread("../result/"+video_name+"_raw.png")
        (s_x,s_y)=gaze_data[0]
        cv2.circle(bg,(s_x,s_y),7,(0,255,0),1)
        last_x = s_x
        last_y = s_y
        for index in range(1,len(gaze_data)):
            cv2.line(bg,(last_x,last_y),gaze_data[index],(255,0,0))
            (last_x,last_y) = gaze_data[index]
        cv2.circle(bg,(last_x,last_y),7,(0,0,255),1)
        
        f.close()
        cv2.imwrite("../result/"+video_name+"_track.png",bg)