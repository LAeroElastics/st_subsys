# --- coding: utf-8 ---

import os
import math
import numpy as np


gauss = lambda n: math.floor(n)


def str2float(string):
    result = [float(s) for s in string]
    return result


def time2deg(time):
    result = time.hour + 100 * time.minute / 60.0 + time.second
    return result


def dms2deg(deg, min, sec):
    result = deg + min / 60 + sec / 3600
    return result


def deg2hms(deg):
    hour = int(deg)
    min = 60*(deg - int(deg))
    sec = 60*(min - int(min))
    return hour, min, sec


def right2deg(string):
    splitted = string.split()
    fsplitted = str2float(splitted)
    result = fsplitted[0] * 15.0 + fsplitted[1] * (15.0 / 60.0) + fsplitted[2] * (15.0 / (60.0 ** 2))
    return result


def right2rad(string):
    result = right2deg(string) * np.pi / 180.0
    return result


def dec2deg(string):
    splitted = string.split()
    fsplitted = str2float(splitted)
    if fsplitted[0] > 0:
        result = fsplitted[0] + fsplitted[1] / 60.0 + fsplitted[2] / (60.0 ** 2)
    else:
        result = fsplitted[0] - fsplitted[1] / 60.0 - fsplitted[2] / (60.0 ** 2)
    return result


def dec2rad(string):
    result = dec2deg(string) * np.pi / 180.0
    return result