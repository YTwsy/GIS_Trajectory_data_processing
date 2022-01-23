# coding=utf-8
import shapefile

shpfile_list = ["停驻点300m_500s", '停驻点500m_750s', '停驻点1000m_1200s'
    , '停驻点1500m_3600s', '停驻点2000m_5000s', '停驻点5000m_8000s'
    , '周一停驻点300m_500s', '周一停驻点500m_750s', '周一停驻点1000m_1200s'
    , '周一停驻点300m_500s', '2天停驻点500m_750s', '2天停驻点5000m_8000s']

for shpfile in shpfile_list:
    reader = shapefile.Reader("预处理后的数据/" + shpfile)
    # shapes= reader.shape()
    print(reader.fields)

    points_xy_list = list()

    for i in range(len(reader.records())):
        print(reader.shape(i).points)
        points_xy_fields_list = list()
        points_xy_fields_list.append(reader.shape(i).points[0])
        points_xy_list.append(points_xy_fields_list)

    print(points_xy_list)

    w = open("D:\GIS\GIS_轨迹数据处理\轨迹点的聚类\pre_cluster_points" + shpfile + ".txt", "w")
    for i in range(len(points_xy_list)):
        w.writelines(str(points_xy_list[i][0][0]) + "," + str(points_xy_list[i][0][1])+ "\n")
    w.close()

print('全部完成')