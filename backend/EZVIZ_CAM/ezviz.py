from enum import IntEnum

class EZVIZ_Status(IntEnum):
    FINISH = 6
    RUNNING = 5
    WAITINGFORRUNNING = 4
    DOWNLOADING = 3
    WAITINGFORDOWNLOADING = 2
    UNFETCHING = 1

class EZVIZ:
    def __init__(self, file_path, server_path, file_name, modify_time) -> None:
        self.file_name = file_name
        self.status = EZVIZ_Status.UNFETCHING
        self.modify_time = modify_time
        self.file_path = file_path
        self.server_path = server_path
        self.id = 0
        self.full_name = ''
        # self.fid = self.file_path + self.file_name[:-4] + '_' + str(self.sid) + '.MP4'
        
class Complete_EZVIZ:
    def __init__(self, file_path, file_name, ) -> None:
        self.max_id = 0