# coding=utf-8
# ---------------------------------------------------------------------------
# Author: wsy
# Created on: 2022/1/8
# Reference:
"""
Description:Python2.7
Usage:

"""
# ---------------------------------------------------------------------------

import arcpy
import numpy as np
# encoding=utf8
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')

points_txt_list = ["停驻点300m_500s", '停驻点500m_750s', '停驻点1000m_1200s'
    , '停驻点1500m_3600s', '停驻点2000m_5000s', '停驻点5000m_8000s'
    , "周一停驻点300m_500s", '周一停驻点500m_750s', '周一停驻点1000m_1200s'
    , '周一停驻点300m_500s', '2天停驻点500m_750s', '2天停驻点5000m_8000s']

for shpname in points_txt_list:
    filename = "D:/GIS/GIS_轨迹数据处理/轨迹点的聚类/pre_cluster_points" + shpname + ".txtk-means_point.txt"

    one_csv_np = np.loadtxt(filename, delimiter=",", skiprows=0, unpack=False,
                            usecols=(0, 1))
    C = one_csv_np[:, 1]

    arcpy.AddField_management(shpname, "my_class", "TEXT", field_length=5)
    with  arcpy.da.UpdateCursor("D:/GIS/GIS_轨迹数据处理/轨迹点的聚类/" + shpname, ["my_class"]) as cursor:
        class_i = 0
        for row in cursor:
            row[0] = C[class_i]
            # print "更改完成"
            cursor.updateRow(row)
            class_i += 1

    del cursor
    print "完成" + shpname

print "全部完成"
