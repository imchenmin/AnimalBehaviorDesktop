# import sqlite3
from EZVIZ_CAM.ezviz import EZVIZ_Status
from EZVIZ_CAM.utils import *
from EZVIZ_CAM.ftp_manager import FTP_Manager
# import schedule
import time
from EZVIZ_CAM.sql import SQL_manager
from behavior_recognition import start_recognition
class Transaction_Manager:
    def __init__(self, device, path='') -> None:
        self.full_name = path
        self.device = device
        self.sql_mgr = SQL_manager(device, self.full_name)
        self.sql_mgr.update_record_status(1)
        while True:
            if self.sql_mgr.check_record_status() == 0:
                self.schedule_check()
                break
            self.schedule_check()
            time.sleep(60)

    def stop_record_event(self):
        self.sql_mgr.update_record_status(0)

    def duration_check(self):
        unfetch = self.sql_mgr.get_file_table(self.sql_mgr.check_record_status())
        mgr = FTP_Manager(self.device, self.full_name)
        for item in unfetch:
            if self.sql_mgr.check_status(item.id) == EZVIZ_Status.WAITINGFORDOWNLOADING.value:
                self.sql_mgr.update_status(item.id, EZVIZ_Status.DOWNLOADING.value)
                print('start download ' + item.file_name)
                flag = mgr.download_video(item.file_path, item.server_path, item.file_name, item.modify_time)
                print('finish download ' + item.file_name)
                if flag == 1:
                    self.sql_mgr.update_status(item.id, EZVIZ_Status.WAITINGFORRUNNING.value)
                else:
                    print('error in downloading', [flag, item.id, item.file_name, item.modify_time])
                time.sleep(10)
            if self.sql_mgr.check_status(item.id) == EZVIZ_Status.WAITINGFORRUNNING.value:
                start_recognition(item.file_path)

    def schedule_check(self):
        print('duration')
        self.duration_check()
    
