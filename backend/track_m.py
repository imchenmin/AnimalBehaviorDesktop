from stand_or_wall import init
import os

if __name__ == '__main__':
    rootdir = 'D:/workspace/'
    list_file = os.listdir(rootdir)
    for i in range(0,len(list_file)):
        if list_file[i].endswith('.mp4') or list_file[i].endswith('.MP4'):
            input_p = os.path.join(rootdir,list_file[i])
            output_p = os.path.join(rootdir,'inference',list_file[i][:-4]+'.csv')
            if not os.path.exists(output_p):
                init(input_p, output_p)
