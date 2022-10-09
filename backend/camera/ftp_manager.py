from ftplib import FTP            #加载ftp模块
from dateutil import parser
from ezviz import EZVIZ,EZVIZS
import copy
import os
import time
class FTP_Manager:
    
    def __init__(self, log_server):
        self.log_server = log_server
        self.ip = "10.15.12.1"
        self.root = "./DCIM/100EZVIZ/"
        self.local_path = './backups/'

    def openFTPFile(self, wifi_name):
        ftp = FTP()
        ftp.connect(self.ip)   
        ftp.set_pasv(False)
        ftp.cwd(self.root)               
        ezviz_list = []
        name_list = []
        nlst = ftp.nlst()
        nlst.reverse()
        

    def check_record(self, item):
        ftp = FTP()
        ftp.connect(self.ip)                
        ftp.cwd(self.root)    

        try:            
            pre = ftp.voidcmd("MDTM " + str(item))[4:].strip()
            self.log_server.logger.info('Still recording ' + item)
            time.sleep(5)   
            timestamp = ftp.voidcmd("MDTM " + str(item))[4:].strip()
            if  pre == timestamp:
                self.log_server.logger.info('Finish recording ' + item)
                return True
            else:
                return False
        except Exception as ex:
            self.log_server.logger.warning('Something wrong in check_record MDTM.')
            return False

    def download_video(self, filename):
        ftp = FTP()
        ftp.connect(self.ip)
        ftp.set_pasv(False)
        ftp.cwd(self.root)               
        flag = True
        wifi_name = filename.split('_')[0]
        modify_time = filename.split('_')[1]
        filename = filename.split('_')[2]

        bufsize = 1024
        path = self.local_path + wifi_name + '/'
        if not os.path.exists(path):
            os.mkdir(path)
        self.log_server.logger.info('Start to download ' + filename +'...')
        
        timestamp = ftp.voidcmd("MDTM " + str(filename))[4:].strip()
        try:
            with open(path + str(timestamp) +'_'+ filename, 'wb') as fp:
                ftp.retrbinary('RETR ' +  str(filename), fp.write, bufsize)
            self.log_server.logger.info('Download '+ filename + ' successfully.')
            try:
                ftp.delete(filename)
                ftp.delete(filename[:-4]+'.THM')      
            except Exception as ex:
                self.log_server.logger.warning("Exception happens in download_video(delete)" + str(ex))
        finally:
            return flag, wifi_name + '_' + str(timestamp) + '_' + filename
    
