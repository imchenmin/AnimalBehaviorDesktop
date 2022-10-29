from enum import IntEnum

class p_type(IntEnum):
    DOWNLOADING = 1
    ANALYSIS = 2

class p_status(IntEnum):
    WAITTING = 1
    PROCESSING = 2
    CANCELED = 3
    DONE = 4
    
class ProcessingObject:
    def __init__(self, _project_path, _ptype):
        self.ptype = _ptype
        self.project_path = _project_path
        self.progress = 0.0
        self.status = p_status.WAITTING
    def to_dict(self):
        return {
            'ptype' : self.ptype,
            'project_path' : self.project_path,
            'progress' : self.progress,
            'status' : self.status
        }

