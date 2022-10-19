import cv2
import os

def merge_video(to_merge):
    first = to_merge[0]
    cap = cv2.VideoCapture(first)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    vid_writer = cv2.VideoWriter(first[:-4]+'res.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    for item in to_merge:
        cap = cv2.VideoCapture(item)
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret or i > 1000:
                break
            vid_writer.write(frame)
            i += 1
    vid_writer.close()

if __name__ == '__main__':
    l = os.listdir('./')
    to_merge = []
    for item in l:
        if item.endswith('.MP4'):
            to_merge.append(item)
    merge_video(to_merge)