# import sqlite3
from asyncore import write
from unittest import result
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
import csv
from EZVIZ_CAM.cropImg_white import crop
import cv2

class Transaction_Manager:
    def __init__(self, device, path='', w=1) -> None:
        self.full_name = path
        self.device = device
        self.sql_mgr = SQL_manager(device, self.full_name)
        self.sql_mgr.update_record_status(1)
        self.process_queue = Queue()
        self.download_queue = Queue()
        self.w = w
        self.sql_mgr.create_progress()

        while True:
            if self.sql_mgr.check_record_status() == 0:
                print('last check')
                time.sleep(10)
                while self.sql_mgr.check_downloading_status(self.full_name):
                    time.sleep(20)
                    self.last_check()
                while self.sql_mgr.check_running_status(self.full_name):
                    time.sleep(20)
                    self.last_check()
                time.sleep(20)
                self.last_check()
                if self.full_name.endswith('top'):
                    self.combine_csv() # 拼接视频
                else:
                    try:
                        self.concater() # 拼接识别csv
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

    def combine_csv(self):
        resultpath = self.full_name
        csvparts = os.listdir(self.full_name)
        csvcombined = os.path.join(resultpath + '/result/','video__all.csv')
        with open(csvcombined,"w",newline='') as csvfile:
            writer = csv.writer(csvfile)
            for files in csvparts:
                if files.endswith('part.csv'):
                    csvtoreadpath = os.path.join(resultpath,files)
                    with open(csvtoreadpath,'r') as toread:
                        read = csv.reader(toread)
                        for row in read:
                            writer.writerow(row)

    def stop_record_event(self):
        self.sql_mgr.update_record_status(0)

    def convert_dlc_to_simple_csv(self,originalcsvpath,simplecsvpath,BODY_PART_NUM):
        raw_data = pd.read_csv(originalcsvpath,skiprows=3,header=None)
        output = []

        for i in range(BODY_PART_NUM):
            output.append([(0,0)])
        
        for idx,row in raw_data.iterrows():
            partindex = 0
            for i in range (1,3*BODY_PART_NUM,3):
                if pd.isnull(row[i]):
                    #bodypartlist[(pointer%BODY_PART_NUM)].append((-1,-1))
                    output[partindex].append(output[partindex][-1])
                else:
                    #use threthold 
                    if row[i+2]<=0.8:
                        output[partindex].append(output[partindex][-1])    
                    else:
                        output[partindex].append((row[i],row[i+1]))
                partindex = partindex + 1
                        
        with open(simplecsvpath,"w",newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i in range (len(output[0])):
                towrite = []
                for partindex in output:
                    towrite.append(str(int(partindex[i][0])))
                    towrite.append(str(int(partindex[i][1])))
                    #towrite = towrite+","+str(int(partindex[i][0]))+","+str(int(partindex[i][1]))              
                    #writer.writerow([index[0],index[1]])
                #towrite = towrite[1:]
                writer.writerow(towrite)        

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
        final_clip.to_videofile(self.full_name + '/topvideotoshow.MP4', fps=60, remove_temp=True)

    def concater(self):
        csv_files = os.listdir(self.full_name)
        timer = 0
        dfs = []
        for csv_file in csv_files:
            if csv_file.endswith('_crop.csv'):
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
        time.sleep(5)
        Process(target=self.check_recog, args=()).start()

    def last_check(self):
        self.check_download()
        time.sleep(5)
        self.check_recog()

    def check_download(self):
        unfetch = self.sql_mgr.get_file_table(self.sql_mgr.check_record_status())
        mgr = FTP_Manager(self.device, self.full_name)
        for item in unfetch:
            if self.sql_mgr.check_status(item.id) == EZVIZ_Status.WAITINGFORDOWNLOADING.value and self.download_queue.qsize() == 0:
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
    
    def check_recog(self):
        waitingrunning = self.sql_mgr.get_waitingruning()
        for item in waitingrunning:
            while self.sql_mgr.check_nv_status():
                print('wait 1')
                time.sleep(10)
            if self.process_queue.qsize() == 0:
                self.process_queue.put(1)
                print('start reco')
                crop(item.file_path)
                self.sql_mgr.add_nv_status()
                self.sql_mgr.update_status(item.id, EZVIZ_Status.RUNNING)
                try:
                    if self.full_name.endswith('top'):
                        video_path = item.file_path[:-4] + '_crop.mp4'
                        video_name = item.file_name[:-4] + '_crop.mp4'
                        resultpath = self.full_name+'/result/'
                        print(['video_path:',video_path,'video_name:',video_name,'resultpath:',resultpath,])
                        if not os.path.exists(resultpath):
                            os.mkdir(resultpath)
                        print(['top', self.full_name])
                        deeplabcut.analyze_videos(config="C:/Users/Administrator/Desktop/whitemouse1024-sbx-2022-10-24/config.yaml",videos=[video_path],destfolder=self.full_name,save_as_csv=True,n_tracks=1)
                        # deeplabcut.analyze_videos_converth5_to_csv(self.full_name)  
                        originalcsv = os.path.join(self.full_name,video_name[:-4]+"DLC_resnet50_whitemouse1024Oct24shuffle1_60000.csv")
                        csv_path = os.path.join(self.full_name,video_name[:-4] + "_partbeforeplus.csv")
                        xycsvpath = os.path.join(self.full_name,item.file_name[:-4] + "_xy.csv")
                        print("convert")
                        self.convert_dlc_to_simple_csv(originalcsv, csv_path,4)
                        print("convertover")
                        cap = cv2.VideoCapture(video_path)
                        len_frames = int(cap.get(7))
                        contentinxycsv = []
                        contentindlccsv = []
                        with open (xycsvpath) as xycsv:
                            read1 = csv.reader(xycsv)
                            for line in read1:
                                contentinxycsv.append(line)
                        with open (csv_path) as dlcsimplecsv:
                            read2 = csv.reader(dlcsimplecsv)
                            for line in read2:
                                contentindlccsv.append(line)
                        contentindlccsv = contentindlccsv[1:]
                        with open(os.path.join(self.full_name,video_name[:-4] + "_part.csv"),'w',newline='') as csvfile:
                            writer = csv.writer(csvfile)    
                            for i in range(len(contentinxycsv)):
                                towrite = []
                                for j in range(0,8,2):
                                    towrite.append(int(float(contentindlccsv[i][j])+float(contentinxycsv[i][0])))
                                    towrite.append(int(float(contentindlccsv[i][j+1])+float(contentinxycsv[i][1])))
                                writer.writerow(towrite)
                    else:
                        start_recognition(item.file_path[:-4] + '_crop.mp4')
                except:
                    print('ERROR in recognition')
                finally:
                    self.sql_mgr.update_status(item.id, EZVIZ_Status.FINISH)

                self.sql_mgr.delete_nv_status()
                self.process_queue.get()
                print('finish reco')    