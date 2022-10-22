# from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6
# import winreg
# import platform
# import pywifi,time
# from pywifi import const

# class WIFI_DEVICE:
#     def __init__(self, wlan_name, wifi_name, ind) -> None:
#         self.wlan_name = wlan_name
#         self.wifi_name = wifi_name
#         self.index = ind
#         key = get_key(self.wlan_name)  # 获取网卡的键值
#         print(key)
#         print(ifaddresses(key)[AF_INET])

#     def connect_wifi(self):
#         wifi = pywifi.PyWiFi()
#         ifaces = wifi.interfaces()[self.index]
#         print(ifaces.name())               #输出无线网卡名称
#         ifaces.disconnect()
#         time.sleep(3)
    
#         profile = pywifi.Profile()                          #配置文件
#         profile.ssid = self.wifi_name                       #wifi名称
#         profile.auth = const.AUTH_ALG_OPEN                  #需要密码
#         profile.akm.append(const.AKM_TYPE_WPA2PSK)          #加密类型
#         profile.cipher = const.CIPHER_TYPE_CCMP             #加密单元
#         profile.key = "1234567890"                          #wifi密码
    
#         ifaces.remove_all_network_profiles()                #删除其它配置文件
#         tmp_profile = ifaces.add_network_profile(profile)   #加载配置文件
#         ifaces.connect(tmp_profile)
#         time.sleep(5)
#         isok = True
    
#         if ifaces.status() == const.IFACE_CONNECTED:
#             print("connect successfully!")
#         else:
#             print("connect failed!")
    
#         time.sleep(1)
#         return isok


# # 获取ipv4地址
# def get_ipv4_address(key_name):
#     if platform.system() == "Linux":
#         try:
#             return ifaddresses(key_name)[AF_INET][0]['addr']  # 返回ipv4地址信息
#         except ValueError:
#             return None
#     elif platform.system() == "Windows":
#         key = get_key(key_name)  # 获取网卡的键值
#         if not key:
#             return
#         else:
#             return ifaddresses(key)[AF_INET][0]['addr']  # 返回ipv4地址信息
#     else:
#         print('您的系统本程序暂时不支持')

# # 获取ipv6地址
# def get_ipv6_address(key_name):
#     if platform.system() == "Linux":
#         try:
#             return ifaddresses(key_name)[AF_INET6][0]['addr']
#         except ValueError:
#             return None
#     elif platform.system() == "Windows":
#         key = get_key(key_name)
#         if not key:
#             return
#         else:
#             return ifaddresses(key)[AF_INET6][0]['addr']
#     else:
#         print('您的系统本程序暂时不支持')

# # 获取Windows系统网卡接口在注册表的键值
# def get_key(key_name):
#     keys = interfaces()  # 获取所有网卡的键值
#     print(keys)
#     key_name_dict = {}  # 存放网卡键值与键值名称的字典
#     try:
#         reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)  # 建立注册表链接
#         reg_key = winreg.OpenKey(reg , r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
#     except Exception as e:
#         return '路径出错或者其他问题，请仔细检查'

#     for key in keys:
#         try:
#             reg_subkey = winreg.OpenKey(reg_key , key + r'\Connection')  # 读取网卡键值的Name
#             key_name_dict[winreg.QueryValueEx(reg_subkey , 'Name')[0]] = key  # 写入key_name字典
#         except FileNotFoundError:
#             pass
#     print('所有接口信息字典列表： ' + str(key_name_dict))
#     return key_name_dict[key_name]
 
# def wifi_connect_status():
#     wifi = pywifi.PyWiFi()
#     iface = wifi.interfaces()[0] #acquire the first Wlan card,maybe not
 
#     if iface.status() in [const.IFACE_CONNECTED,const.IFACE_INACTIVE]:
#         print("wifi connected!")
#         return 1
#     else:
#         print("wifi not connected!")
    
#     return 0
 
# def scan_wifi():
#     wifi = pywifi.PyWiFi()
#     iface = wifi.interfaces()[0]
 
#     iface.scan()
#     time.sleep(1)
#     basewifi = iface.scan_results()
 
#     for i in basewifi:
#         print("wifi scan result:{}".format(i.ssid))
#         print("wifi device MAC address:{}".format(i.bssid))
        
#     return basewifi
