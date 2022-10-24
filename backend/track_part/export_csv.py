"""
从sleap的h5文件导出csv来。
"""
import h5py
import numpy as np
import csv
import sys

if __name__ == '__main__':
    filename = sys.argv[1]
    with h5py.File(filename, "r") as f:
        dset_names = list(f.keys())
        locations = f["tracks"][:].T
        node_names = [n.decode() for n in f["node_names"][:]]

    print("===filename===")
    print(filename)
    print()

    print("===HDF5 datasets===")
    print(dset_names)
    print()

    print("===locations data shape===")
    print(locations.shape)

    cls = ['frames'] 
    print("===nodes===")
    for i, name in enumerate(node_names):
        print(f"{i}: {name}")
        cls.append(name + '_x')
        cls.append(name + '_y')

    print()

    res = []
    for i in range(locations.shape[0]):
        temp = []
        temp.append(i)
        for j in range(locations.shape[1]):
            if str(locations[i][j][0][0]) == 'nan':
                temp.append(0)
                temp.append(0)
            else:
                temp.append(int(locations[i][j][0][0]))
                temp.append(int(locations[i][j][1][0]))
        res.append(temp)
        
    with open(filename + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([item for item in cls])
        for m in res:
            writer.writerow(m)
            i+=1
            
    