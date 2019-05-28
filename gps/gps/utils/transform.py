"""
 Created by hanruida on 2019-03-23
"""
import math


class Transfrom:
    x_pi = 3.14159265358979324 * 3000.0 / 180.0

    @classmethod
    def bd09togcj02(cls, bd_lon, bd_lat):
        """
        百度坐标系(BD-09)转火星坐标系(GCJ-02)
        """
        x = float(bd_lon) - 0.0065
        y = float(bd_lat) - 0.006
        z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * cls.x_pi)
        theta = math.atan2(y, x) - 0.000003 * math.cos(x * cls.x_pi)
        gg_lng = z * math.cos(theta)
        gg_lat = z * math.sin(theta)

        return [gg_lng, gg_lat]
