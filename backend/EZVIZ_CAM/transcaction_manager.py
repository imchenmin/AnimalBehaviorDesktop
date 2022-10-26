# import sqlite3
from certifi import where
from EZVIZ_CAM.ezviz import EZVIZ_Status
from EZVIZ_CAM.utils import *
from EZVIZ_CAM.ftp_manager import FTP_Manager
# import schedule
import time
from EZVIZ_CAM.sql import SQL_manager
from behavior_recognition import start_recognition
import os
from multiprocessing import Process,Queue
import pandas as pd
from moviepy.editor import concatenate_videoclips,VideoFileClip
import deeplabcut
from track_part.convert_dlc_to_simple_csv import convert_dlc_to_simple_csv
from EZVIZ_CAM.cropImg_white import crop
class Transaction_Manager:
    def __init__(self, device, path='', w=1) -> None:
        self.full_name = path
        self.device = device
        self.sql_mgr = SQL_manager(device, self.full_name)
        self.sql_mgr.update_record_status(1)
        self.process_queue = Queue()
        self.download_queue = Queue()
        self.w = w

        while True:
            if self.sql_mgr.check_record_status() == 0:
                print('last check')
                while self.sql_mgr.check_downloading_status(self.full_name):
                    time.sleep(10)
                    self.last_check()
                while self.sql_mgr.check_running_status(self.full_name):
                    time.sleep(10)
                    self.last_check()
                time.sleep(10)
                self.last_check()
                # self.concat_video() # 拼接视频
                # self.concater() # 拼接识别csv
                break
            self.schedule_check()
            time.sleep(30)

    def stop_record_event(self):
        self.sql_mgr.update_record_status(0)

    # def duration_check(self):
    #     unfetch = self.sql_mgr.get_file_table(self.sql_mgr.check_record_status())
    #     mgr = FTP_Manager(self.device, self.full_name)
    #     for item in unfetch:
    #         print(item.file_name, item.status)
    #         if self.sql_mgr.check_status(item.id) == EZVIZ_Status.WAITINGFORDOWNLOADING.value and self.download_queue.qsize() == 0:
    #             self.sql_mgr.update_status(item.id, EZVIZ_Status.DOWNLOADING.value)
    #             print('start download ' + item.file_name)
    #             self.download_queue.put(1)
    #             flag = mgr.download_video(item.file_path, item.server_path, item.file_name, item.modify_time)
    #             self.download_queue.get()
    #             if flag == 1:
    #                 print('finish download ' + item.file_name)
    #                 self.sql_mgr.update_status(item.id, EZVIZ_Status.WAITINGFORRUNNING.value)
    #             else:
    #                 print('error in downloading', [flag, item.id, item.file_name, item.modify_time])
    #             time.sleep(5)
    #         if self.sql_mgr.check_status(item.id) == EZVIZ_Status.WAITINGFORRUNNING.value and self.process_queue.qsize() == 0 and self.sql_mgr.check_nv_status(self.w):
    #             self.process_queue.put(1)
    #             print('start reco')
    #             self.sql_mgr.update_nv_status(self.w)
    #             self.sql_mgr.update_status(item.id, EZVIZ_Status.RUNNING)
    #             try:
    #                 if self.full_name.endswith('top'):
    #                     video_path = item.file_path
    #                     video_name = item.file_name
    #                     resultpath = video_path+"/result/"
    #                     csv_path = resultpath + video_name + ".csv"
    #                     print(['top', self.full_name])
    #                     originalvideopath = item.file_path
    #                     deeplabcut.analyze_videos(config="D:/workspace/DLC/config.yaml",videos=[originalvideopath],destfolder=self.full_name,save_as_csv=True,n_tracks=1)
    #                     deeplabcut.analyze_videos_converth5_to_csv(video_path)  
    #                     originalcsv = video_path+"/"+video_name+"DLC_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv"
    #                     convert_dlc_to_simple_csv(originalcsv, csv_path)
    #                 else:
    #                     start_recognition(item.file_path)
    #                 self.sql_mgr.update_status(item.id, EZVIZ_Status.FINISH)
    #             except:
    #                 print('ERROR in recognition')
    #             finally:
    #                 self.sql_mgr.update_nv_status(-self.w)
    #                 self.process_queue.get()
    #             print('finish reco')    
            
    # def recognition_check(self):
    #     print('here')
    #     unfetch = self.sql_mgr.get_downloaded_file_table()
    #     for item in unfetch:
    #         print([item.id, item.file_name])
            

    def concat_video(self):
        mp4_file = []
        # 访问 video 文件夹 (假设视频都放在这里面)
        for root, dirs, files in os.walk(self.full_name):
            # 按文件名排序
            files.sort()
            # 遍历所有文件
            for file in files:
                # 如果后缀名为 .mp4
                if os.path.splitext(file)[1] == '.MP4':
                    # 拼接成完整路径
                    filePath = os.path.join(root, file)
                    # 载入视频
                    video = VideoFileClip(filePath)
                    # 添加到数组
                    mp4_file.append(video)

        final_clip = concatenate_videoclips(mp4_file)
        final_clip.to_videofile(self.full_name + '/combine.mp4', fps=60, remove_temp=False)

    def concater(self):
        csv_files = os.listdir(self.full_name)
        timer = 0
        dfs = []
        for csv_file in csv_files:
            if csv_file.endswith('.csv'):
                file_path = os.path.join(self.full_name, csv_file)
                print(file_path + 'reader concat.')
                df = pd.read_csv(file_path)
                df['start_time'] = df['start_time'] + timer
                df['end_time'] = df['end_time'] + timer
                timer += 300
                dfs.append(df)

        df = pd.concat(dfs, axis=0)
        gp = df.groupby('type')
        df_res = []
        for name, group in gp:
            group = group.reset_index(drop=True)
            df_res.append(group)
        df = pd.concat(df_res,axis=0)
        df[['class','start_time','end_time','type']].to_csv(self.full_name[:-3] + '/detection_result.csv')

    def schedule_check(self):
        Process(target=self.check_download, args=()).start()
        time.sleap(5)
        Process(target=self.check_recog, args=()).start()

    def last_check(self):
        self.check_download()
        time.sleap(5)
        self.check_recog()
    def check_download(self):
        unfetch = self.sql_mgr.get_file_table(self.sql_mgr.check_record_status())
        mgr = FTP_Manager(self.device, self.full_name)
        for item in unfetch:
            if self.sql_mgr.check_status(item.id) == EZVIZ_Status.WAITINGFORDOWNLOADING.value and self.download_queue.qsize() == 0:
                self.sql_mgr.update_status(item.id, EZVIZ_Status.DOWNLOADING.value)
                print('start download ' + item.file_name)
                self.download_queue.put(1)
                flag = mgr.download_video(item.file_path, item.server_path, item.file_name, item.modify_time)
                self.download_queue.get()
                if flag == 1:
                    print('finish download ' + item.file_name)
                    self.sql_mgr.update_status(item.id, EZVIZ_Status.WAITINGFORRUNNING.value)
                else:
                    print('error in downloading', [flag, item.id, item.file_name, item.modify_time])
    
    def check_recog(self):
        waitingrunning = self.sql_mgr.get_waitingruning()
        for item in waitingrunning:
            if self.process_queue.qsize() == 0 and self.sql_mgr.check_nv_status(self.w):
                self.process_queue.put(1)
                print('start reco')
                crop(item.file_path)
                self.sql_mgr.update_nv_status(self.w)
                self.sql_mgr.update_status(item.id, EZVIZ_Status.RUNNING)
                try:
                    if self.full_name.endswith('top'):
                        video_path = item.file_path[:-4] + '_crop.mp4'
                        video_name = item.file_name[:-4] + '_crop.mp4'
                        resultpath = self.full_name+'/result'
                        print(['video_path:',video_path,'video_name:',video_name,'resultpath:',resultpath,])
                        if not os.path.exists(resultpath):
                            os.mkdir(resultpath)
                        print(['top', self.full_name])
                        deeplabcut.analyze_videos(config="C:/Users/Administrator/Desktop/whitemouse1024-sbx-2022-10-24/config.yaml",videos=[video_path],destfolder=self.full_name,save_as_csv=True,n_tracks=1)
                        deeplabcut.analyze_videos_converth5_to_csv(self.full_name)  
                        originalcsv = self.full_name+video_name[-4]+"DLC_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv"
                        csv_path = os.path.join(self.full_name,resultpath,video_name[:-4] + "_part.csv")
                        convert_dlc_to_simple_csv(originalcsv, csv_path)
                    else:
                        start_recognition(item.file_path[:-4] + '_crop.mp4')
                    self.sql_mgr.update_status(item.id, EZVIZ_Status.FINISH)
                except:
                    print('ERROR in recognition')
                finally:
                    self.sql_mgr.update_nv_status(-self.w)
                self.process_queue.get()
                print('finish reco')    