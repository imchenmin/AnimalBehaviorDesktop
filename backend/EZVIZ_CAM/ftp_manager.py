from ftplib import FTP            #加载ftp模块
import os
from EZVIZ_CAM.ezviz import EZVIZ
import time
class FTP_Manager:
    def __init__(self, ip, local_path):
        self.ip = ip
        self.root = "./DCIM/100EZVIZ/"
        self.local_path = local_path

    def openFTPFile(self):
        ftp = FTP()
        ftp.set_pasv(False)
        try:
            ftp.connect(self.ip)
        except:
            print('ERROR IN '+ self.ip)
        ftp.cwd(self.root)
        nlst = ftp.nlst()
        ezviz_list = self.rebuild(ftp, nlst)
        ftp.quit()
        return ezviz_list

    def rebuild(self, ftp, file_list):
        res = []
        for item in file_list:
            if item.endswith('.MP4'):
                timestamp = ftp.voidcmd("MDTM " + str(item))[4:].strip()
                server_path = os.path.join(self.root, item)
                path = self.local_path + '/' + item
                res.append(EZVIZ(path, server_path, item, timestamp))
        return res     

    def download_video(self, file_path, server_path, file_name, modify_time):
        ftp = FTP()
        ftp.connect(self.ip)
        ftp.set_pasv(False)
        ftp.cwd(self.root)               
        flag = 0
        bufsize = 1024
        
        if not os.path.exists(file_path[:-12]):
            os.mkdir(file_path[:-12])

        with open(file_path, 'wb') as fp:
            # try:
            ftp.retrbinary('RETR ' +  str(file_name), fp.write, bufsize)
            flag = 1
            time.sleep(10)
            if flag == 1:
                try:
                    ftp.delete(file_name)
                except Exception as ex:
                    flag = -1
                try:
                    ftp.delete(file_name[:-4]+'.THM')      
                except Exception as ex:
                    flag = -2
        # except:
            # return 0
        ftp.quit()
        return flag
        
        
