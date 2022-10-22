from behavior_recognition import start_recognition
import sys
sys.path.insert(0, 'D:\\workspace\\AnimalBehaviorDesktop\\backend')
sys.path.insert(0, 'D:\\zjh\AnimalBehaviorDesktop\\backend\\yolov5')
sys.path.insert(0, 'D:\\zjh\AnimalBehaviorDesktop\\backend')

# start_recognition('C:\\Users\\Gianttek\\Desktop\\test2206')
import pywifi,time
from behavior_recognition import init
def main():
    start_recognition('C:\\Users\\Gianttek\\1312\\top\\EZVZ0051.MP4')
 
if __name__ == "__main__":
    main()