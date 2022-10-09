import sqlite3
import queue
import requests
from requests_toolbelt.adapters.source import SourceAddressAdapter
from utils import *
import re
from multiprocessing import Process

class Transaction:
    def __init__(self, wifi_name, ) -> None:
        self.wifi_name = wifi_name
        self.conn = sqlite3.connect(self.wifi_name + '.db')
        self.select_sql = ''

    def get_from_server(self, name):
        session = requests.Session()
        # 使用以太网的网卡访问 
        yitai_ip = get_ipv4_address(name)
        session.mount('http://', SourceAddressAdapter(yitai_ip))
        data = session.get(url="http://10.15.12.1/DCIM/100EZVIZ/")
        data=re.findall(r'class="link" href="([^\<]+.MP4)"', data.text)
        return data        
    
    def check(self):
        print(self.get_from_server(self.wifi_name))



        

