from datetime import timedelta

class BehaviorCounter:
    def __init__(self, fps=117.093896,threshold=20, filter_frame=30, type=''):
        self.fps = fps
        # continue 
        self.threshold =threshold
        self.filter_frame = filter_frame
        self.ans = {}
        self.res =  [{}]
        self.frame_count = 0
        self.count = 0
        self.df = ""
        self.scount = 0
        self.type = type
    
    # 计算当前处在第几次抓搔中
    def read(self, label = -1):
        self.frame_count += 1

        if label == 0:
            # print("\n")
            # print(self.res)
            # print(self.ans)
            if 'end' in self.ans.keys() and self.frame_count - self.ans['end'] < self.threshold:
                self.ans['end'] = self.frame_count
            elif 'end' in self.ans.keys() and self.frame_count - self.ans['end'] >= self.threshold:
                self.ans['start_time'] = str(round(self.ans['st'] / self.fps, 2))
                self.ans['end_time'] = str(round(self.ans['end'] / self.fps, 2))
                self.ans['type'] = self.type
                if self.ans['end'] - self.ans['st'] >= self.filter_frame:
                    self.res.append(self.ans)
                    self.count += 1 
                # res.append(ans)
                self.ans = {}
                self.ans['st'] = self.frame_count
                self.ans['end'] = self.frame_count
            else:
                self.ans['st'] = self.frame_count
                self.ans['end'] = self.frame_count

    def batch_read(self, df):
        ans = {}
        seq = df['frame']
        count = 0
        for i in seq:
            if 'end' in ans.keys() and i - ans['end'] < self.threshold:
                if i - ans['end'] > 1:
                    count += 1
                ans['end'] = i
            elif 'end' in ans.keys() and i - ans['end'] >= self.threshold:
                ans['start_time'] = str(timedelta(seconds=(ans['st'] / self.fps)))
                ans['end_time'] = str(timedelta(seconds=(ans['end'] / self.fps)))
                ans['count'] = count + 1
                if ans['end'] - ans['st'] >= self.filter_frame:
                    self.res.append(ans)
                # res.append(ans)
                ans = {}
                ans['st'] = i
                ans['end'] = i
                count = 0
            else:
                ans['st'] = i
                ans['end'] = i
                count = 0
                
    def batch_read_fake(self, df):
        self.df = df
    
    def fake_read(self,frame_id):
        # ans = {}
        df = self.df
        seq = df['frame']
        i = frame_id
        if i in df.frame.values:
            print(i)
            if 'end' in self.res[-1].keys() and i - self.res[-1]['end'] < self.threshold:
                if i - self.res[-1]['end'] > 1:
                    self.scount += 1
                    self.res[-1]['count'] = self.scount
                self.res[-1]['end'] = i
                self.res[-1]['start_time'] = str(timedelta(seconds=(self.res[-1]['st'] / self.fps)))
                self.res[-1]['end_time'] = str(timedelta(seconds=(self.res[-1]['end'] / self.fps)))
                self.res[-1]['duration'] = str(timedelta(seconds=((self.res[-1]['end']-self.res[-1]['st'])  / self.fps)))
            elif 'end' in self.res[-1].keys() and i - self.res[-1]['end'] >= self.threshold:
                self.res[-1]['start_time'] = str(timedelta(seconds=(self.res[-1]['st'] / self.fps)))
                self.res[-1]['end_time'] = str(timedelta(seconds=(self.res[-1]['end'] / self.fps)))
                self.res[-1]['duration'] = str(timedelta(seconds=((self.res[-1]['end']-self.res[-1]['st'])  / self.fps)))
                self.res[-1]['count'] = self.scount + 1
                if self.res[-1]['end'] - self.res[-1]['st'] >= self.filter_frame:
                    self.res.append({})
                # res.append(ans)
                self.res[-1] = {}
                self.res[-1]['st'] = i
                self.res[-1]['end'] = i
                self.res[-1]['duration'] = str(timedelta(seconds=((self.res[-1]['end']-self.res[-1]['st'])  / self.fps)))
                self.scount = 0
            else:
                self.res[-1]['st'] = i
                self.res[-1]['end'] = i
                self.res[-1]['duration'] = str(timedelta(seconds=((self.res[-1]['end']-self.res[-1]['st'])  / self.fps)))
                self.scount = 0
        


        

 
