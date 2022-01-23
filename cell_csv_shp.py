import shapefile
import json
import time
import os
import numpy as np

for i in range(1, 1, 1):
    print(i)

# %%
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
print(type(all_csv_np))
print(all_csv_np[:,2])
print(all_csv_np)

#按bikeid为每个线元素输出shp，点按时间排序：

all_bikeid=all_csv_np[:,2]
all_bikeid=np.unique(all_bikeid)

print(all_bikeid)
print(len(all_bikeid))


# %%
one_try_id=all_csv_np[all_csv_np[:,2]==8621832450.0
]
print(one_try_id)
import matplotlib.pyplot as plt

plt.plot(one_try_id[:, 0], one_try_id[:, 1], label='one_try_id', color='g', linewidth=1, linestyle=':')  # 添加linewidth设置线条大小
plt.show()

time_1 = str(one_try_id[2][3])
print(time_1)
print(time_1[0:4])
print(time_1[4:6])
print(time_1[6:8])
print(time_1[8:10])
print(time_1[10:12])
print(time_1[12:14])

# time_2 = '2020-03-02 16:00:00'
time_2=time_1[0:4]+'-'+time_1[4:6]+'-'+time_1[6:8]+' '+time_1[8:10]+':'+time_1[10:12]+':'+time_1[12:14]
print(time_2)

# %%
from numpy import ma
from pykalman import KalmanFilter

one_try_id=one_try_id[:,[0,1]]
km_data = ma.asarray(one_try_id)
# print(km_data)
# km_data[15]=ma.masked
# print(km_data)


init_mean = np.mean(one_try_id,axis=0)

kf = KalmanFilter(initial_state_mean=init_mean, n_dim_obs=2)

result,_ = kf.em(km_data).smooth(km_data)
print(result)

plt.scatter(one_try_id[:,0],one_try_id[:,1],label='true')
plt.legend()
plt.show()

plt.scatter(result[:,0],result[:,1],label='klm')

plt.legend()
plt.show()

plt.scatter(one_try_id[:,0],one_try_id[:,1],label='true')
plt.scatter(result[:,0],result[:,1],label='klm')
plt.legend()
plt.show()

plt.plot(one_try_id[:, 0], one_try_id[:, 1], label='one_try_id', color='r', linewidth=2, linestyle=':')  # 添加linewidth设置线条大小
plt.plot(result[:, 0], result[:, 1], label='one_try_id', color='g', linewidth=1, linestyle='-')  # 添加linewidth设置线条大小
plt.show()





