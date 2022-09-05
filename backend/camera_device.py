import cv2
from multiprocessing import Process, Queue

class Camera:
    def __init__(self):
        self.record_flag = Queue()
        self.filename = Queue()
        self.side_name = Queue()
        self.open_flag = Queue()

    def open(self):
        self.open_flag.put(1)
        p_top = Process(target=self.play, args=(0, 1280, 720, 120, 'top'))
        p_side = Process(target=self.play, args=(1, 2560, 720, 60, 'side'))
        p_top.start()
        p_side.start()

    def start(self, filename):
        self.filename.put(filename)
        self.record_flag.put(1)

    def play(self, num, w, h, fps, name):
        cam = cv2.VideoCapture(num)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        cam.set(cv2.CAP_PROP_FPS, fps)
        cam_record = None
        while True:
            ret, frame = cam.read()
            if not ret or self.open_flag.qsize() == 0:
                break
                                
            cv2.imshow(name, frame)
            cv2.waitKey(1)

            if self.record_flag.qsize() == 1:
                cam_record = cv2.VideoWriter(self.filename.get() + '_' + name +'.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 120, (1280, 720))
                cam_record.write(frame)
                self.record_flag.put(1)
            elif self.record_flag.qsize() == 2:
                cam_record.write(frame)
            elif self.record_flag.qsize() == 0:
                try:
                    if cam_record != None:
                        cam_record.release()
                except:
                    print('err')

    def close(self):
        self.open_flag.get(1)

    def stop(self):
        while self.record_flag.qsize() > 0:
            self.record_flag.get()

