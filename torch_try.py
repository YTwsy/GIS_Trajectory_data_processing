from geopy.distance import geodesic
from datetime import datetime, date
import shapefile
import json
import time
import os
import numpy as np
import torch as th

filePath = 'D:\GIS\GIS_轨迹数据处理\轨迹数据\周六深圳摩拜\周六深圳摩拜'
csv_flienames_list=list()
csv_flienames_list=os.listdir(filePath)

all_csv_np=np.zeros((0,4))

for one_csv_filename in csv_flienames_list:
    one_csv_np = np.loadtxt(filePath+"/"+one_csv_filename, delimiter=",", skiprows=1, unpack=False,
                           usecols=(1, 2, 3))
    if(len(one_csv_np)==0):  #文件为空
        continue

    time=np.zeros((len(one_csv_np),1))
    filename_str= one_csv_filename[8:16] + one_csv_filename[-10:]
    filename_str=filename_str.strip(".csv")
    time[:,0]=filename_str      #添加时间

    one_csv_np=np.hstack((one_csv_np,time))

    all_csv_np=np.vstack((all_csv_np, one_csv_np))

    print(len(all_csv_np))

#所有数据已经存入all_csv_np
all_csv_th=th.from_numpy(all_csv_np)
print(type(all_csv_th))
print(all_csv_th[:,2])
print(all_csv_th)

#按bikeid为每个线元素输出shp，点按时间排序：

all_bikeid=all_csv_th[:,2]
all_bikeid=th.unique(all_bikeid)

print(all_bikeid)
print(len(all_bikeid))

# %%
print(all_csv_th[5][3])
print(all_csv_th[5][3].long()+1)

print(int(all_csv_th[5][3].long()+1))
print(th.cuda.device_count())
# all_csv_th=all_csv_th.cuda()
# print(all_csv_th)
