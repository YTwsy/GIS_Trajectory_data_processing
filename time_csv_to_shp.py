import shapefile
import json
import time
import os
import numpy as np

# %%
filePath = 'D:\GIS\GIS_轨迹数据处理\轨迹数据\周一深圳摩拜\周一深圳摩拜'
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

# %%
#按bikeid为每个线元素输出shp，点按时间排序：

all_bikeid=all_csv_np[:,2]
all_bikeid=np.unique(all_bikeid)

print(all_bikeid)
print(len(all_bikeid))

# %%
from geopy.distance import geodesic
from datetime import datetime, date

wline = shapefile.Writer('预处理后的数据/周一all_lines_with_id_sorted_by_time')

wline.field('bike_id', 'C')
# wline.field('time', 'C')

for one_bike_id in all_bikeid:   # len(all_bikeid) == 285446
    one_bike_id_np=all_csv_np[all_csv_np[:,2] == one_bike_id]  #每个id的车的np
    one_bike_id_np=one_bike_id_np[np.argsort(one_bike_id_np[:,3])]  #按时间进行排序
    print(one_bike_id)
    # print(one_bike_id_np)

    if(len(one_bike_id_np) < 2):   #少于两个点，不处理
        continue

    #去除异常值
    max_v=14   #m/s ~= 50 km/h 基本为市区不可达到的极限

    #异常点定义规则：到两侧的速度均大于50km/h
    #初始点：到第二个点的速度大于50km/h，且第二个点不为异常点，才定义为异常点
    #末点：到之前的点的速度大于50km/h，且之前的点不为异常点，才定义为异常点

    will_delete_index=list()

    #开始处理中间点：
    for i in range(1,len(one_bike_id_np)-1,1):
        pre_s=geodesic((one_bike_id_np[i-1][1], one_bike_id_np[i-1][0]),
                    (one_bike_id_np[i][1], one_bike_id_np[i][0])).m

        time_1 = str(one_bike_id_np[i-1][3])
        # time_1 = '2020-03-02 16:00:00'

        time_1 = time_1[0:4] + '-' + time_1[4:6] + '-' + time_1[6:8] + \
                 ' ' + time_1[8:10] + ':' + time_1[10:12] + ':' + time_1[12:14]

        time_2 = str(one_bike_id_np[i][3])

        # time_1 = '2020-03-02 16:00:00'
        time_2 = time_2[0:4] + '-' + time_2[4:6] + '-' + time_2[6:8] + \
                 ' ' + time_2[8:10] + ':' + time_2[10:12] + ':' + time_2[12:14]

        time_1_struct = datetime.strptime(time_1, "%Y-%m-%d %H:%M:%S")
        time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S")
        pre_t = (time_2_struct - time_1_struct).seconds

        pre_v=pre_s / pre_t

        bef_s = geodesic((one_bike_id_np[i][1], one_bike_id_np[i][0]),
                         (one_bike_id_np[i+1][1], one_bike_id_np[i+1][0])).m

        time_1 = str(one_bike_id_np[i - 1][3])
        # time_1 = '2020-03-02 16:00:00'

        time_1 = time_1[0:4] + '-' + time_1[4:6] + '-' + time_1[6:8] + \
                 ' ' + time_1[8:10] + ':' + time_1[10:12] + ':' + time_1[12:14]

        time_2 = str(one_bike_id_np[i][3])
        # time_1 = '2020-03-02 16:00:00'

        time_2 = time_2[0:4] + '-' + time_2[4:6] + '-' + time_2[6:8] + \
                 ' ' + time_2[8:10] + ':' + time_2[10:12] + ':' + time_2[12:14]

        time_1_struct = datetime.strptime(time_1, "%Y-%m-%d %H:%M:%S")
        time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S")
        bef_t = (time_2_struct - time_1_struct).seconds

        bef_v = bef_s / bef_t

        if(pre_v > max_v and bef_v > max_v):
            will_delete_index.append(i)  #加入异常列表


    #轨迹点 == 2:

    if(len(one_bike_id_np) == 2):
        pre_s = geodesic((one_bike_id_np[0][1], one_bike_id_np[0][0]),
                         (one_bike_id_np[1][1], one_bike_id_np[1][0])).m

        time_1 = str(one_bike_id_np[0][3])
        # time_1 = '2020-03-02 16:00:00'

        time_1 = time_1[0:4] + '-' + time_1[4:6] + '-' + time_1[6:8] + \
                 ' ' + time_1[8:10] + ':' + time_1[10:12] + ':' + time_1[12:14]

        time_2 = str(one_bike_id_np[1][3])

        # time_1 = '2020-03-02 16:00:00'
        time_2 = time_2[0:4] + '-' + time_2[4:6] + '-' + time_2[6:8] + \
                 ' ' + time_2[8:10] + ':' + time_2[10:12] + ':' + time_2[12:14]

        time_1_struct = datetime.strptime(time_1, "%Y-%m-%d %H:%M:%S")
        time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S")
        pre_t = (time_2_struct - time_1_struct).seconds

        pre_v = pre_s / pre_t

        if (pre_v > max_v):
            continue   #不保留这一轨迹 ！

    #轨迹点 > 2:
    #开始处理两端：
    #处理首端：

    pre_s = geodesic((one_bike_id_np[0][1], one_bike_id_np[0][0]),
                     (one_bike_id_np[1][1], one_bike_id_np[1][0])).m

    time_1 = str(one_bike_id_np[0][3])
    # time_1 = '2020-03-02 16:00:00'

    time_1 = time_1[0:4] + '-' + time_1[4:6] + '-' + time_1[6:8] + \
             ' ' + time_1[8:10] + ':' + time_1[10:12] + ':' + time_1[12:14]

    time_2 = str(one_bike_id_np[1][3])

    # time_1 = '2020-03-02 16:00:00'
    time_2 = time_2[0:4] + '-' + time_2[4:6] + '-' + time_2[6:8] + \
             ' ' + time_2[8:10] + ':' + time_2[10:12] + ':' + time_2[12:14]

    time_1_struct = datetime.strptime(time_1, "%Y-%m-%d %H:%M:%S")
    time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S")
    pre_t = (time_2_struct - time_1_struct).seconds

    pre_v = pre_s / pre_t

    if(pre_v > max_v):
        will_delete_index.append(0)  #处理首端


    #处理末端:
    pre_s = geodesic((one_bike_id_np[-1][1], one_bike_id_np[-1][0]),
                     (one_bike_id_np[-2][1], one_bike_id_np[-2][0])).m

    time_1 = str(one_bike_id_np[-2][3])
    # time_1 = '2020-03-02 16:00:00'

    time_1 = time_1[0:4] + '-' + time_1[4:6] + '-' + time_1[6:8] + \
             ' ' + time_1[8:10] + ':' + time_1[10:12] + ':' + time_1[12:14]

    time_2 = str(one_bike_id_np[-1][3])

    # time_1 = '2020-03-02 16:00:00'
    time_2 = time_2[0:4] + '-' + time_2[4:6] + '-' + time_2[6:8] + \
             ' ' + time_2[8:10] + ':' + time_2[10:12] + ':' + time_2[12:14]

    time_1_struct = datetime.strptime(time_1, "%Y-%m-%d %H:%M:%S")
    time_2_struct = datetime.strptime(time_2, "%Y-%m-%d %H:%M:%S")
    pre_t = (time_2_struct - time_1_struct).seconds

    pre_v = pre_s / pre_t

    if (pre_v > max_v):
        will_delete_index.append(-1)  # 处理末端

    one_bike_id_np = np.delete(one_bike_id_np, will_delete_index ,axis=0)

    #取出xy
    one_bike_id_np_xy=one_bike_id_np[:, [0, 1]]
    # print(one_bike_id_np_xy)
    # print(one_bike_id_np_xy.tolist())

    #所有符合的元素tolist
    wline_list=list()
    wline_list.append(one_bike_id_np_xy.tolist())
    wline.line(wline_list)           #添加单个线轨迹至all_lines_with_id_sorted_by_time.shp
    wline.record(
                 bike_id=one_bike_id
                 # time=one_bike_id_np[:,3][one_bike_id_np_count]
                )


    # #开始处理点：
    # wpoint = shapefile.Writer('处理后的数据/'+
    #     str(one_bike_id).strip(".0") + '_with_all_sorted_time')  # 添加所有点至one_bike_id+'_with_all_sorted_time'
    # print(str(one_bike_id).strip(".0"))
    #
    # wpoint.field('x', 'N', decimal=30)
    # wpoint.field('y', 'N', decimal=30)
    # wpoint.field('bike_id', 'C')
    # wpoint.field('time', 'C')
    #
    # for one_bike_id_np_count in range(len(one_bike_id_np)):
    #     # print(one_bike_id_np[:, 0])
    #
    #     wpoint.point(one_bike_id_np[:, 0][one_bike_id_np_count],one_bike_id_np[:,1][one_bike_id_np_count])
    #
    #     wpoint.record(x=one_bike_id_np[:, 0][one_bike_id_np_count],
    #                  y=one_bike_id_np[:,1][one_bike_id_np_count],
    #                  bike_id=one_bike_id_np[:,2][one_bike_id_np_count],
    #                  time=one_bike_id_np[:,3][one_bike_id_np_count])
    #
    # wpoint.close()

wline.close()



