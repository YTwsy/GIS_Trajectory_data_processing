# coding=utf-8
import subprocess
import os

k=5
max=20

points_txt_list = ["停驻点300m_500s", '停驻点500m_750s', '停驻点1000m_1200s'
    , '停驻点1500m_3600s', '停驻点2000m_5000s', '停驻点5000m_8000s'
    , '周一停驻点300m_500s', '周一停驻点500m_750s', '周一停驻点1000m_1200s'
    , '周一停驻点300m_500s', '2天停驻点500m_750s', '2天停驻点5000m_8000s']

for one_txt in points_txt_list:
    one_txt_name="D:\GIS\GIS_轨迹数据处理\轨迹点的聚类\pre_cluster_points"+one_txt+'.txt'
    points_count=len(open(one_txt_name, 'rU').readlines())
    os.system("D:\GIS\GIS_轨迹数据处理\K-means_k_max_count_filename.exe"+" "+str(k)+" "
              +str(max)+" "+str(points_count)+" "+one_txt_name)
    print("完成"+one_txt)

print('全部完成')



