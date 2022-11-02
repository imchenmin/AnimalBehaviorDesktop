import sys,os
from serial_manager import btn_record
import re
#track part
#sys.path.insert(0, "F:\\workspace\\AnimalBehaviorDesktop\\backend\\track_part")
# sys.path.insert(0, 'D:\\workspace\\AnimalBehaviorDesktop\\backend')



#from deeplabcut import analyze_videos
###
from flask import Flask
app = Flask(__name__)
from flask_socketio import SocketIO
from flask import request
from flask import json
from flask_cors import CORS
CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api
# EZVIZ_CAM PACKAGE
# from behavior_recognition import start_recognition
from EZVIZ_CAM.transcaction_manager import Transaction_Manager
from multiprocessing import Process
from EZVIZ_CAM.sql import SQL_manager
from dao.ProcessingObject import ProcessingObject, p_status, p_type
import time
# EZVIZ_CAM PACKAGE END
config_json = None
socketio = SocketIO(app)

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
    btn_record()
    data = json.loads(request.data)
    filename = data['video_filename']
    rtsplist = data['rtsp_list']
    filename = filename.replace('\\', '/')
    camera_process_list = []
    for rtsp_item in rtsplist:
        try:
            os.makedirs(filename + rtsp_item['name'])
        except:
            print(f"Error in making dir in {rtsp_item['name']}" + filename)
        ip_addr = re.search("\d+\.\d+\.\d+\.\d+", rtsp_item['alternativeName']).group()
        camera_process_list.append(Process(target=Transaction_Manager, args=(ip_addr, filename + rtsp_item['name'], 9)))
        camera_process_list[-1].start()

    return 'Done'
    
@app.route('/api/stop_record',methods=['POST','GET'])
def stop_record():
    btn_record()
    data = json.loads(request.data)
    filename = data['video_filename']
    rtsplist = data['rtsp_list']
    filename = filename.replace('\\', '/')
    
    for rtsp_item in rtsplist:
        try:
            os.makedirs(filename + rtsp_item['name'])
        except:
            print(f"Error in making dir in {rtsp_item['name']}" + filename)
        ip_addr = re.search("\d+\.\d+\.\d+\.\d+", rtsp_item['alternativeName']).group()
        sql_mgr = SQL_manager(ip_addr)
        sql_mgr.update_record_status(0)

    return 'Done'



@app.route('/api/rat_sleap', methods=['GET', 'POST'])
def rat_sleap():
    """
    调用sleap-track推理，然后调用sleap-convert转换成h5，再生成csv文件。
    """
    # TODO: 添加进度显示
    import subprocess
    from behavior.export_csv import export_csv
    data = json.loads(request.data)
    video_name = data['video_filename']
    pose_worker = subprocess.Popen(f"conda activate sleap && sleap-track {video_name} -m D://221024_104102.single_instance.n=353", shell=True)
    # for line in iter(pose_worker.stdout.readline, b''):
    #     print(line)
    #     pose_worker.stdout.close()
    pose_worker.wait()
    slp_file = video_name + '.predictions.slp'
    h5_file = video_name + '.predictions.h5'
    csv_file = video_name + '.predictions.csv'
    convert_worker = subprocess.Popen(f"conda activate sleap && sleap-convert {slp_file} --format analysis -o {h5_file}", shell=True)
    convert_worker.wait()
    export_csv(h5_file,csv_file)
    # TODO: envoke distance checking algorithm
    return ('done')
    	

@app.route('/api/get_status', methods=['POST', 'GET'])
def get_status():
    filename = json.loads(request.data)
    filename = filename['video_filename']
    print(filename)

@socketio.on('connection')
def test_connect():
    print('get connection')

@socketio.on('disconnection')
def test_disconnect():
    print('get disconnection')



@socketio.on('require_project_status',namespace='/')
def require_project_status(data):
    print('received message: ' , data['project_list'])
    rtsplist = data['rtsp_list']
    filename = filename.replace('\\', '/')
    progressList = []
    p = 0
    while True:
        for item in data['project_list']:
            cur = time.time()
            item = item[:-13]
            for rtsp_item in rtsplist:
                ip_addr = re.search("\d+\.\d+\.\d+\.\d+", rtsp_item['alternativeName']).group()
                sql_mgr = SQL_manager(ip_addr, only_query=True)
                p += sql_mgr.get_progress(item, cur)
            p/=3
            temp = ProcessingObject(item, p_type.ANALYSIS)
            temp.progress = p
            progressList.append(temp.to_dict())

        socketio.emit("project_status",{
            'msg': progressList,
            'code': 200
        })
        time.sleep(60)


if __name__ == '__main__':
    # app.run(host='127.0.0.1',port=5001)
    socketio.run(app, host='127.0.0.1', port=5001)
