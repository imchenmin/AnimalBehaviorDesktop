import sys,os
#track part
sys.path.insert(0, "F:\\workspace\\AnimalBehaviorDesktop\\backend\\track_part")
from track_process import *
from draw_result import draw_raw_img
from ouput_video import output_video
from convert_dlc_to_simple_csv import convert_dlc_to_simple_csv
import gazeheatplot
from deeplabcut import analyze_videos
###
from distutils.command.config import config
from camera_device import Camera
from flask import Flask
app = Flask(__name__)
from flask import request
from flask import json
from flask_cors import CORS
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

config_json = None
cam = Camera()
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

@app.route('/api/open_camera',methods=['POST','GET'])
def open_camera():
    cam.open()

@app.route('/api/start_record',methods=['POST','GET'])
def start_record():
    cam.start('D://test')

@app.route('/api/close_camera',methods=['POST','GET'])
def close_camera():
    cam.close()

@app.route('/api/stop_record',methods=['POST','GET'])
def stop_record():
    cam.stop()

@app.route('/api/runtrack', methods=['GET', 'POST'])
def execute():
    data = json.loads(request.data)
    argvs = data['argvs']
    #print(argvs)
    namelist = []
    polylist = []
    video_width = argvs[0]
    video_height = argvs[1]
    video_path = argvs[-2]
    video_name = argvs[-1]
    rect_num = int(argvs[2])
    resize = 2.4 #尺寸映射
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
    csv_path = "result/"+video_name+".csv"
    #video_path = "C:\\Users\\Sun\\Desktop\\maze\\eight_maze_short_demo.mp4"
    if not os.path.exists(csv_path):
        #deeplabcut.analyze_videos(config="C:/Users/Sun/Desktop/MOT_NEW-sbx-2022-07-27/config.yaml",videos=["C:/Users/Sun/Desktop/testfor1crop.mp4"],destfolder="result/",save_as_csv=True)
        originalcsv = "result/"+video_name+"DLC_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv"
        convert_dlc_to_simple_csv(originalcsv,csv_path)
    draw_raw_img(namelist,polylist,video_width,video_height,video_name)
    gazeheatplot.draw_heat_main(csv_path,video_height,video_width,video_name)
    isPoiWithinPoly(csv_path,polylist,namelist,video_name,video_path)
    output_video(video_path,video_name,polylist,namelist)
    return ('done')


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001)
