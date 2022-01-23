import os
import numpy as np

filePath = 'D:\GIS\GIS_轨迹数据处理\轨迹数据\周六深圳摩拜\周六深圳摩拜'
filePath_1 = 'D:\GIS\GIS_轨迹数据处理\轨迹数据\周六深圳摩拜\周六深圳摩拜'

csv_flienames_list=list()
csv_flienames_list=os.listdir(filePath)
csv_flienames_list.extend(os.listdir(filePath_1))

print(csv_flienames_list)
for one_csv_filename in csv_flienames_list:
    str=one_csv_filename[8:16] + one_csv_filename[-10:]
    str=str.strip(".csv")
    print(str)