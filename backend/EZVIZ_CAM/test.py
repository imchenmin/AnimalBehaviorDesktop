from ftplib import FTP            #加载ftp模块
ftp = FTP()
ip = '10.15.12.103'
ftp.connect(ip)
ftp.set_pasv(False)
ftp.cwd("./DCIM/100EZVIZ/")               
flag = 0
bufsize = 1024
nlst = ftp.nlst()
for item in nlst:
    ftp.delete(item)      
# with open('./test', 'wb') as fp:
#     # try:
#     ftp.retrbinary('RETR ' +  str('EZVZ0010.MP4'), fp.write, bufsize)