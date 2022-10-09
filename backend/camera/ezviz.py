from enum import Enum


class EZVIZ_Status(Enum):
    RUNNING = 0
    WAITING_RUNNING = 1
    DOWNLOADING = 2
    WAITING_DOWNLOAD = 3
    UNFETCHING = 4

class EZVIZ:
    def __init__(self, file_path, file_name, sid, modify_time) -> None:
        self.file_name = file_name
        self.status = EZVIZ_Status.UNFETCHING
        self.modify_time = modify_time
        self.sid = sid
        self.file_path = file_path
        self.fid = self.file_path + self.file_name[:-4] + '_' + str(self.sid) + '.MP4'
        
class Complete_EZVIZ:
    def __init__(self, file_path, file_name, ) -> None:
        self.max_id = 0