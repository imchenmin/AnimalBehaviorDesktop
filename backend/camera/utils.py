from netifaces import interfaces, ifaddresses, AF_INET, AF_INET6
import winreg
import platform

# 获取ipv4地址
def get_ipv4_address(key_name):
    if platform.system() == "Linux":
        try:
            return ifaddresses(key_name)[AF_INET][0]['addr']  # 返回ipv4地址信息
        except ValueError:
            return None
    elif platform.system() == "Windows":
        key = get_key(key_name)  # 获取网卡的键值
        if not key:
            return
        else:
            return ifaddresses(key)[AF_INET][0]['addr']  # 返回ipv4地址信息
    else:
        print('您的系统本程序暂时不支持')

# 获取ipv6地址
def get_ipv6_address(key_name):
    if platform.system() == "Linux":
        try:
            return ifaddresses(key_name)[AF_INET6][0]['addr']
        except ValueError:
            return None
    elif platform.system() == "Windows":
        key = get_key(key_name)
        if not key:
            return
        else:
            return ifaddresses(key)[AF_INET6][0]['addr']
    else:
        print('您的系统本程序暂时不支持')

# 获取Windows系统网卡接口在注册表的键值
def get_key(key_name):
    keys = interfaces()  # 获取所有网卡的键值
    key_name_dict = {}  # 存放网卡键值与键值名称的字典
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)  # 建立注册表链接
        reg_key = winreg.OpenKey(reg , r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
    except Exception as e:
        return '路径出错或者其他问题，请仔细检查'

    for key in keys:
        try:
            reg_subkey = winreg.OpenKey(reg_key , key + r'\Connection')  # 读取网卡键值的Name
            key_name_dict[winreg.QueryValueEx(reg_subkey , 'Name')[0]] = key  # 写入key_name字典
        except FileNotFoundError:
            pass
    # print('所有接口信息字典列表： ' + str(key_name_dict))
    return key_name_dict[key_name]

