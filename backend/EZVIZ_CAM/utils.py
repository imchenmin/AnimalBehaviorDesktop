import os
from moviepy.editor import concatenate_videoclips,VideoFileClip
import pandas as pd
import csv
def combine_csv(full_name):
    resultpath = full_name
    csvparts = os.listdir(full_name)
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

def concat_video(full_name):
    mp4_file = []
    # 访问 video 文件夹 (假设视频都放在这里面)
    for root, dirs, files in os.walk(full_name):
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
    final_clip.to_videofile(full_name + '/topvideotoshow.MP4', fps=60, remove_temp=True)

def concat_behavior_csv(full_name):
    csv_files = os.listdir(full_name)
    timer = 0
    dfs = []
    for csv_file in csv_files:
        if csv_file.endswith('_detection_result.csv'):
            file_path = os.path.join(full_name, csv_file)
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
    df[['class','start_time','end_time','type']].to_csv(full_name[:-5] + '/detection_result.csv')