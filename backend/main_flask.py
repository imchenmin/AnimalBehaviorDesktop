import sys,os
import deeplabcut
#track part
#sys.path.insert(0, "F:\\workspace\\AnimalBehaviorDesktop\\backend\\track_part")
# sys.path.insert(0, 'D:\\workspace\\AnimalBehaviorDesktop\\backend')
sys.path.insert(0, 'D:\\zjh\AnimalBehaviorDesktop\\backend\\yolov5')
sys.path.insert(0, 'D:\\zjh\AnimalBehaviorDesktop\\backend')

from track_part.track_process import *
from track_part.draw_result import draw_raw_img
from track_part.output_video_part import output_video_part
from track_part.convert_dlc_to_simple_csv import convert_dlc_to_simple_csv
from track_part.gazeheatplot import draw_heat_main
#from deeplabcut import analyze_videos
###
from flask import Flask
app = Flask(__name__)
from flask import request
from flask import json
from flask_cors import CORS
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api
# EZVIZ_CAM PACKAGE
from behavior_recognition import start_recognition
from EZVIZ_CAM.transcaction_manager import Transaction_Manager
from multiprocessing import Process
from EZVIZ_CAM.sql import SQL_manager
# EZVIZ_CAM PACKAGE END
config_json = None

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/api/config',methods=['POST','GET'])
def load_config():
    if request.method == 'POST':
        print(request)
        filename = request.values.get('config_filename',0)
        if filename == 0:
            return app.response_class(
                status=404,
                mimetype='application/json'
            )
        with open(filename, 'r') as f:
            global config_json
            config_json = json.load(f)
            return config_json
    if request.method == 'GET':
        if config_json is not None:
            return config_json
        else:
            return app.response_class(
                response=json.dumps("{}"),
                status=204,
                mimetype='application/json'
            )

@app.route('/api/start_record',methods=['POST','GET'])
def start_record():
    filename = json.loads(request.data)
    filename = filename['video_filename']
    filename = filename.replace('\\', '/')

    try:
        os.makedirs(filename + '/back')
    except:
        print('Error in making dir in back' + filename)
    
    try:
        os.makedirs(filename + '/left')
    except:
        print('Error in making dir in left' + filename)
    
    try:
        os.makedirs(filename + '/top')
    except:
        print('Error in making dir in top' + filename)
    p0 = Process(target=Transaction_Manager, args=('10.15.12.102', filename + '/back'))
    p1 = Process(target=Transaction_Manager, args=('10.15.12.103', filename + '/left'))
    p2 = Process(target=Transaction_Manager, args=('10.15.12.101', filename + '/top'))

    p0.start()
    p1.start()
    p2.start()

    return 'Done'
    
@app.route('/api/stop_record',methods=['POST','GET'])
def stop_record():
    sql_mgr = SQL_manager('10.15.12.102')
    sql_mgr.update_record_status(0)
    sql_mgr = SQL_manager('10.15.12.103')
    sql_mgr.update_record_status(0)
    sql_mgr = SQL_manager('10.15.12.101')
    sql_mgr.update_record_status(0)
    return 'Done'

@app.route('/api/runtrack', methods=['GET', 'POST'])
def execute():
    data = json.loads(request.data)
    argvs = data['argvs']
    #print(argvs)
    namelist = []
    polylist = []
    video_width = argvs[0]
    video_height = argvs[1]
    video_path = argvs[-3]
    video_name = argvs[-2]
    check_out_list = argvs[-1]
    rect_num = int(argvs[2])
    resize = 1.6 #尺寸映射
    video_width = int(video_width*resize)
    video_height = int(video_height*resize)
    for i in range (3,3+rect_num):
        name, poly = preProcessRecInfo(argvs[i])
        namelist.append(name)
        poly = poly.tolist()
        for points in poly:
            for i in range(2):
                points[i] =int(points[i]*resize)
        polylist.append(poly)
    poly_num = int(argvs[3+rect_num])
    
    for i in range (4+rect_num,4+rect_num+poly_num):
        name, poly = preProcessPolyInfo(argvs[i])
        for points in poly:
            for i in range(2):
                points[i] =int(points[i]*resize)
        namelist.append(name)
        polylist.append(poly)
    print(namelist)
    print(polylist)
    resultpath = video_path+"/result/"
    csv_path = resultpath+video_name+".csv"
    #videopath = video.mp4's path
    #videoname = video
    #video_path = "C:\\Users\\Sun\\Desktop\\maze\\eight_maze_short_demo.mp4"
    if not os.path.exists(resultpath):
        os.mkdir(resultpath)
    if not os.path.exists(csv_path):
        originalvideopath = video_path+"/"+video_name+".mkv"
        deeplabcut.analyze_videos(config="D:/workspace/DLC/config.yaml",videos=[originalvideopath],destfolder=video_path,save_as_csv=True,n_tracks=1)
        deeplabcut.analyze_videos_converth5_to_csv(video_path,'.mkv')  
        originalcsv = video_path+"/"+video_name+"DLC_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv"
        convert_dlc_to_simple_csv(originalcsv,csv_path)
    draw_raw_img(namelist,polylist,video_width,video_height,video_name,resultpath)
    draw_heat_main(csv_path,video_height,video_width,video_name,resultpath)
    isPoiWithinPoly(csv_path,polylist,namelist,video_name,video_path,resultpath)
    output_video_part(video_path,video_name,polylist,namelist,resultpath,check_out_list)
    #output_video(video_path,video_name,polylist,namelist,resultpath)
    return ('done')
	
@app.route('/api/wash_recognition', methods=['POST', 'GET'])
def wash_recognition():
    filename = json.loads(request.data)
    filename = filename['video_filename']
    print(filename)
    return start_recognition(filename)
    
@app.route('/api/get_status', methods=['POST', 'GET'])
def get_status():
    filename = json.loads(request.data)
    filename = filename['video_filename']
    print(filename)

# @app.route('/api/run_tracker', methods=['POST', 'GET'])
# def run_tracker():
#     resultpath = video_path+"/result/"
#     csv_path = resultpath+video_name+".csv"
#     if not os.path.exists(resultpath):
#         os.mkdir(resultpath)
#     if not os.path.exists(csv_path):
#         originalvideopath = video_path+"/"+video_name+".mkv"
#         deeplabcut.analyze_videos(config="D:/workspace/DLC/config.yaml",videos=[originalvideopath],destfolder=video_path,save_as_csv=True,n_tracks=1)
#         deeplabcut.analyze_videos_converth5_to_csv(video_path,'.mkv')  
#         originalcsv = video_path+"/"+video_name+"DLC_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv"
#         convert_dlc_to_simple_csv(originalcsv,csv_path)
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001)
