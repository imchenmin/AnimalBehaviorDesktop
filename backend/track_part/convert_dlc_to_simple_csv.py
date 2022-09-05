import pandas as pd
import csv
def convert_dlc_to_simple_csv(originalcsvpath,simplecsvpath):
    #csvpath = str(videoname)+"_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv"
    raw_data = pd.read_csv(originalcsvpath,skiprows=3)
    output = []
    for idx,row in raw_data.iterrows():
        if pd.isnull(row[1]):
            output.append(output[-1])
        else:

            if row[3]<=0.8:
                output.append(output[-1])
            else:
                output.append((int(row[1]),int(row[2])))
    with open(simplecsvpath,"w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        for index in output:
            writer.writerow([index[0],index[1]])
#convert_dlc_to_simple_csv("testfor1DLC_dlcrnetms5_MOT_NEWJul27shuffle1_50000_el.csv","testfor1_result.csv")
            