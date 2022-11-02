"""
对大鼠抓挠进行分析，输入是csv文件
"""
from behavior.BasicBehavior import BasicBehavior
import pandas as pd
import sleap
from matplotlib import pyplot as plt
class RatScratching(BasicBehavior):


    _behavior_type = "RatScratching"
    csv_df = None

    def __init__(self,model_path=None):
        self.model_path = model_path
        if model_path != None:
            self.predictor = sleap.load_model(model_path)


    def read_csv(self, csv_filepath):
        self.csv_df = pd.read_csv(csv_filepath)
        return self.csv_df

    def inference(self, video_filepath):
        video = sleap.load_video(video_filepath)
        self.labels = self.predictor.predict(video)
        return self.labels
    
    def plot_hind_seq(self):
        pass

        
        

