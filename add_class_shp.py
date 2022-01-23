import shapefile
import numpy as np

points_txt_list = ["停驻点300m_500s", '停驻点500m_750s', '停驻点1000m_1200s'
    , '停驻点1500m_3600s', '停驻点2000m_5000s', '停驻点5000m_8000s'
    , "周一停驻点300m_500s", '周一停驻点500m_750s', '周一停驻点1000m_1200s'
    , '周一停驻点300m_500s', '2天停驻点500m_750s', '2天停驻点5000m_8000s']

for shpname in points_txt_list:
    one_csv_np = np.loadtxt("D:\GIS\GIS_轨迹数据处理\轨迹点的聚类\pre_cluster_points" + shpname +
                            ".txtk-means_point.txt", delimiter=",", skiprows=0, unpack=False,
                            usecols=(0, 1))
    C = one_csv_np[:, 1]

    reader = shapefile.Reader("D:/GIS/GIS_轨迹数据处理/轨迹点的聚类/" + shpname + ".shp")

    writer = shapefile.Writer("D:/GIS/GIS_轨迹数据处理/轨迹点的聚类/" + shpname+"k-mean" + ".shp", shapeType=1)
    writer.field(u'class', u'N', 9, 0)

    for i in range(len(reader.records())):
        writer.point(reader.shape(i).points[0][0], reader.shape(i).points[0][1])
        writer.record(C[i])

    print("完成"+shpname)

print("全部完成")
