from transcaction_manager import Transaction_Manager
from multiprocessing import Process, Queue
class Camera_Manager:
    def __init__(self) -> None:
        self.wifi_names = ['EZVIZ-7620']
        self.transaction_manager_queue = [Transaction_Manager(item) for item in self.wifi_names]
    
    def record(self):
        for item in self.transaction_manager_list:
            