# import sqlite3
from EZVIZ_CAM.ezviz import EZVIZ_Status
from EZVIZ_CAM.utils import *
from EZVIZ_CAM.ftp_manager import FTP_Manager
import time
from EZVIZ_CAM.sql import SQL_manager
from behavior_recognition import start_recognition
from multiprocessing import Process,Queue
from EZVIZ_CAM.cropImg_white import crop
from EZVIZ_CAM.utils import concat_video, concat_behavior_csv, combine_csv
from tracking_recognition import crop_top
class Transaction_Manager:
    def __init__(self, device, path='') -> None:
        self.full_name = path
        self.device = device
        self.sql_mgr = SQL_manager(device, self.full_name)
        self.sql_mgr.update_record_status(1)
        self.process_queue = Queue()
        self.download_queue = Queue()

        while True:
            if self.sql_mgr.check_record_status() == 0:
                print('last check')
                while self.sql_mgr.check_downloading_status(self.full_name):
                    self.last_check()
                    time.sleep(20)
                while self.sql_mgr.check_running_status(self.full_name):
                    self.last_check()
                    time.sleep(20)
                time.sleep(5)
                if self.full_name.endswith('top'):
                    combine_csv() # 拼接topcsv
                    pass
                else:
                    try:
                        concat_behavior_csv() # 拼接识别csv
                    except:
                        print('Error in concat csv left back')
                try:
                    self.concat_video()
                except:
                    print('Error in concat video')
                fake_filename = self.full_name
                if self.full_name.endswith('top'):
                    fake_filename = fake_filename[:-3]
                else:
                    fake_filename = fake_filename[:-4]
                with open(fake_filename + 'video.mkv', 'w') as f:
                    f.write('fake')
                break
            self.schedule_check()
            time.sleep(30)

    def stop_record_event(self):
        self.sql_mgr.update_record_status(0)

    def schedule_check(self):
        Process(target=self.check_download, args=(False,)).start()
        time.sleep(5)
        Process(target=self.check_recog, args=(False,)).start()

    def last_check(self):
        self.check_download(True)
        time.sleep(5)
        self.check_recog(True)

    def check_download(self, last=False):
        unfetch = self.sql_mgr.get_file_table(self.sql_mgr.check_record_status())
        mgr = FTP_Manager(self.device, self.full_name)
        for item in unfetch:
            if not last:
                if self.download_queue.qsize() > 0:
                    print('download full')
                    return
            else:
                while self.download_queue.qsize() > 0:
                    print('loop wait download full')
                    time.sleep(10)
            if self.sql_mgr.check_status(item.id) == EZVIZ_Status.WAITINGFORDOWNLOADING.value:
                self.sql_mgr.update_status(item.id, EZVIZ_Status.DOWNLOADING.value)
                print('start download ' + item.file_name)
                self.download_queue.put(1)
                self.sql_mgr.update_progress()
                flag = mgr.download_video(item.file_path, item.server_path, item.file_name, item.modify_time)
                self.download_queue.get()
                if flag == 1:
                    print('finish download ' + item.file_name)
                    self.sql_mgr.update_status(item.id, EZVIZ_Status.WAITINGFORRUNNING.value)
                else:
                    print('error in downloading', [flag, item.id, item.file_name, item.modify_time])
    
    def check_recog(self, last):
        waitingrunning = self.sql_mgr.get_waitingruning()
        for item in waitingrunning:
            if not last:
                if self.process_queue.qsize() != 0:
                    print('process full')
                    return
            else:
                while self.process_queue.qsize() != 0:
                    print('loop wait process full')
                    time.sleep(10)

            self.process_queue.put(1)
            print('start reco')
            self.sql_mgr.update_status(item.id, EZVIZ_Status.RUNNING)
            try:
                if item.full_name.endswith('top'):
                    crop_top(item.file_path)
                else:
                    crop(item.file_path)
                    start_recognition(item.file_path[:-4] + '_crop.mp4')
            except Exception as e:
                print('ERROR in recognition', e)
            finally:
                self.sql_mgr.update_status(item.id, EZVIZ_Status.FINISH)

            self.process_queue.get()
            print('finish reco')