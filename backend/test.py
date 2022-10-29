# from behavior_recognition import start_recognition
import sys
sys.path.insert(0, 'D:\\workspace\\AnimalBehaviorDesktop\\backend\\yolov5')
sys.path.insert(0, 'D:\\workspace\\AnimalBehaviorDesktop\\backend')
import os
import pandas as pd
from moviepy.editor import concatenate_videoclips,VideoFileClip
# start_recognition('C:\\Users\\Gianttek\\Desktop\\test2206')
# from behavior_recognition import init
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
    final_clip.to_videofile(full_name + 'combine.mp4', fps=60, remove_temp=False)


def concater(full_name):
    csv_files = os.listdir(full_name)
    timer = 0
    dfs = []
    for csv_file in csv_files:
        if csv_file.endswith('.csv'):
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
    print(df)
    df[['class','start_time','end_time','type']].to_csv(full_name[:-3] + '/detection_result.csv')

def main():
    root = 'C:\\Users\\Administrator\\test7\\top'
    concat_video(root)
 
if __name__ == "__main__":
    main()