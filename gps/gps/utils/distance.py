"""
 Created by hanruida on 2019-03-23
"""
import math


class Distance:
    NF_pi = 0.01745329251994329

    @classmethod
    def di(cls, start, end):
        start_longitude = float(start["longitude"])
        start_latitude = float(start["latitude"])
        end_longitude = float(end["longitude"])
        end_latitude = float(end["latitude"])

        d2 = start_longitude * cls.NF_pi
        d3 = start_latitude * cls.NF_pi
        d4 = end_longitude * cls.NF_pi
        d5 = end_latitude * cls.NF_pi
        d6 = math.sin(d2)
        d7 = math.sin(d3)
        d8 = math.cos(d2)
        d9 = math.cos(d3)
        d10 = math.sin(d4)
        d11 = math.sin(d5)
        d12 = math.cos(d4)
        d13 = math.cos(d5)
        array_of_double10 = (d9 * d8)
        array_of_double11 = (d9 * d6)
        array_of_double12 = d7
        array_of_double20 = (d13 * d12)
        array_of_double21 = (d13 * d10)
        array_of_double22 = d11
        d14 = math.sqrt((array_of_double10 - array_of_double20) * (array_of_double10 - array_of_double20)
                        + (array_of_double11 - array_of_double21) * (array_of_double11 - array_of_double21)
                        + (array_of_double12 - array_of_double22) * (array_of_double12 - array_of_double22))

        return math.asin(d14 / 2.0) * 12742001.579854401

# Distance.di({
#     "longitude": 116.5634764032,
#     "latitude": 39.7859361275
# }, {
#     "longitude": 116.5632200000,
#     "latitude": 39.7868200000
# })
