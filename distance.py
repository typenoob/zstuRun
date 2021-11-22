import math
from math import radians, cos, sin, asin, sqrt


def get_distance_wgs84(lon1, lat1, lon2, lat2):
    """
    根据https://github.com/googollee/eviltransform，里面的算法：WGS - 84
    :param lon1: 经度1
    :param lat1: 纬度1
    :param lon2: 经度2
    :param lat2: 纬度2
    :return: 距离，单位为 米
    """
    earthR = 6378137.0

    pi180 = math.pi / 180
    arcLatA = lat1 * pi180
    arcLatB = lat2 * pi180
    x = (math.cos(arcLatA) * math.cos(arcLatB) *
         math.cos((lon1 - lon2) * pi180))
    y = math.sin(arcLatA) * math.sin(arcLatB)
    s = x + y
    if s > 1:
        s = 1
    if s < -1:
        s = -1
    alpha = math.acos(s)
    distance = alpha * earthR
    return distance
