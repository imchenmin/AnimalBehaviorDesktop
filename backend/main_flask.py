from distutils.command.config import config
import sys
sys.path.insert(0, 'D:\\workspace\\AnimalBehaviorDesktop\\backend')
from camera_device import Camera
from wash_recognition import start_wash_recognition
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

@app.route('/api/wash_recognition', methods=['POST', 'GET'])
def wash_recognition():
    filename = json.loads(request.data)
    print('nmsl')
    print(filename['data'])
    start_wash_recognition(filename['data'])


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001)
