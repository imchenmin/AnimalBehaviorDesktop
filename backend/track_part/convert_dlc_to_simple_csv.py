import pandas as pd
import csv
BODY_PART_NUM = 5
def convert_dlc_to_simple_csv(originalcsvpath,simplecsvpath):
    #csvpath = str(videoname)+"_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv"
    raw_data = pd.read_csv(originalcsvpath,skiprows=3)
    output = []
    
    for i in range(BODY_PART_NUM):
        output.append([])
    
    for idx,row in raw_data.iterrows():
        partindex = 0
        for i in range (1,len(row),3):
            if pd.isnull(row[i]):
                #bodypartlist[(pointer%BODY_PART_NUM)].append((-1,-1))
                output[partindex].append(output[partindex][-1])
            else:
                #use threthold 
                if row[i+2]<=0.8:
                    output[partindex].append(output[partindex][-1])    
                else:
                    output[partindex].append((row[i],row[i+1]))
            partindex = partindex + 1
                    
    with open(simplecsvpath,"w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range (len(output[0])):
            towrite = []
            for partindex in output:
                towrite.append(str(int(partindex[i][0])))
                towrite.append(str(int(partindex[i][1])))
                #towrite = towrite+","+str(int(partindex[i][0]))+","+str(int(partindex[i][1]))              
                #writer.writerow([index[0],index[1]])
            #towrite = towrite[1:]
            writer.writerow(towrite)
#convert_dlc_to_simple_csv("D:/workspace/AnimalBehaviorDesktop/backend/track_part/Testfor1shortDLC_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv","testfor1_result.csv")
            