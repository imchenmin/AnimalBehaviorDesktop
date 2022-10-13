import sqlite3
from ezviz import EZVIZ_Status
from ezviz import EZVIZ
from utils import *
from ftp_manager import FTP_Manager
import schedule
import time
from sql import SQL_manager

class Transaction_Manager:
    def __init__(self, wifi_name, full_name) -> None:
        self.wifi_name = wifi_name
        self.full_name = full_name
        self.init_flag = True
        self.sql_mgr = SQL_manager(self.wifi_name, self.full_name)

        schedule.every(10).seconds.do(self.schedule_check)
        while True:
            schedule.run_pending()
            time.sleep(10)
    
    def duration_check(self):
        unfetch = self.sql_mgr.get_file_table(self.sql_mgr.check_record_status())
        mgr = FTP_Manager()
        for item in unfetch:
            if self.sql_mgr.check_status(item.id) == EZVIZ_Status.WAITINGFORDOWNLOADING.value:
                self.sql_mgr.update_status(item.id, EZVIZ_Status.DOWNLOADING.value)
                print('start download')
                flag = mgr.download_video(item.file_path, item.server_path, item.file_name, item.modify_time)
                if flag == 1:
                    self.sql_mgr.update_status(item.id, EZVIZ_Status.WAITINGFORRUNNING.value)
                else:
                    print('error in downloading', [flag, item.id, item.file_name, item.modify_time])

    def schedule_check(self):
        print('duration')
        self.duration_check()
    
