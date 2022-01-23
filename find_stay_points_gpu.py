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


filePath_1 = 'D:\GIS\GIS_轨迹数据处理\轨迹数据\周一深圳摩拜\周一深圳摩拜'
csv_flienames_list_1=list()
csv_flienames_list_1=os.listdir(filePath_1)


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


all_csv_np_1=np.zeros((0,4))

for one_csv_filename in csv_flienames_list_1:
    one_csv_np = np.loadtxt(filePath_1+"/"+one_csv_filename, delimiter=",", skiprows=1, unpack=False,
                           usecols=(1, 2, 3))

    if(len(one_csv_np)==0):  #文件为空
        continue

    time=np.zeros((len(one_csv_np),1))
    filename_str= one_csv_filename[8:16] + one_csv_filename[-10:]
    filename_str=filename_str.strip(".csv")
    time[:,0]=filename_str      #添加时间

    one_csv_np=np.hstack((one_csv_np,time))

    all_csv_np_1=np.vstack((all_csv_np_1, one_csv_np))

    print(len(all_csv_np_1))

all_csv_np=np.vstack((all_csv_np, all_csv_np_1))
#所有数据已经存入all_csv_np
all_csv_th=th.from_numpy(all_csv_np_1).cuda(0)

print(type(all_csv_th))
print(all_csv_th[:,2])
print(all_csv_th)

#按bikeid为每个线元素输出shp，点按时间排序：

all_bikeid=all_csv_th[:,2]
all_bikeid=th.unique(all_bikeid)

print(all_bikeid)
print(len(all_bikeid))

#开始识别停驻点：

# 标记停留点的到达时间和离开时间。
# 算法思路：从第一个轨迹点开始以此作为锚点 [公式]，向后找到距离未超出距离阈值 [公式] 的所有点，
# 如果这些点的总时长大于时间阈值 [公式] ，则归为停留点，并以停留点集的下一个点作为新的锚点；
# 否则将锚点后移一位，重新召回和判断。
# https://zhuanlan.zhihu.com/p/382037032

i = 0
dist_threh = 1000  # m
time_threh = 1200  # s
all_stay_points = th.zeros((0, 4)).cuda()

for one_bike_id in all_bikeid:   # len(all_bikeid) == 285446
    one_bike_id_np=all_csv_th[all_csv_th[:,2] == one_bike_id]  #每个id的车的np
    one_bike_id_np=one_bike_id_np[th.argsort(one_bike_id_np[:,3])]  #按时间进行排序
    print(one_bike_id)

    while(i < len(one_bike_id_np)):
        j=i+1

        while(j<len(one_bike_id_np)):
            dist=geodesic((one_bike_id_np[i][1], one_bike_id_np[i][0]),
                         (one_bike_id_np[j][1], one_bike_id_np[j][0])).m

            if (dist > dist_threh):
                time_j_1=int(one_bike_id_np[j][3].long())
                time_j = str(time_j_1)
                # time_1 = '2020-03-02 16:00:00'
                time_j = time_j[0:4] + '-' + time_j[4:6] + '-' + time_j[6:8] + ' ' +\
                         time_j[8:10] + ':' + time_j[10:12] + ':' + time_j[12:14]

                time_i_1=int(one_bike_id_np[i][3].long())
                time_i = str(time_i_1)
                # time_1 = '2020-03-02 16:00:00'
                time_i = time_i[0:4] + '-' + time_i[4:6] + '-' + time_i[6:8] + ' ' +\
                         time_i[8:10] + ':' + time_i[10:12] + ':' + time_i[12:14]

                time_i_struct = datetime.strptime(time_i, "%Y-%m-%d %H:%M:%S")
                time_j_struct = datetime.strptime(time_j, "%Y-%m-%d %H:%M:%S")
                change_time = (time_j_struct - time_i_struct).seconds

                if (change_time > time_threh):
                    one_stay_points = one_bike_id_np[i:j + 1]
                    all_stay_points = th.vstack((all_stay_points, one_stay_points))

                    i=j
                else:
                    i+=1
                break

            j+=1
        if(j == len(one_bike_id_np)):
            break

print(len(all_stay_points))

# %%
#开始输出停驻点：
wpoint = shapefile.Writer('预处理后的数据/'+'周一停驻点1000m_1200s')  # 添加所有点至one_bike_id+'_with_all_sorted_time'

wpoint.field('x', 'N', decimal=30)
wpoint.field('y', 'N', decimal=30)
wpoint.field('bike_id', 'C')
wpoint.field('time', 'C')

for one_bike_id_np_count in range(len(all_stay_points)):
    # print(one_bike_id_np[:, 0])

    wpoint.point(all_stay_points[:, 0][one_bike_id_np_count],all_stay_points[:,1][one_bike_id_np_count])

    wpoint.record(x=all_stay_points[:, 0][one_bike_id_np_count],
                 y=all_stay_points[:,1][one_bike_id_np_count],
                 bike_id=all_stay_points[:,2][one_bike_id_np_count],
                 time=all_stay_points[:,3][one_bike_id_np_count])

wpoint.close()




























