# --- coding: utf-8 ---

import numpy as np
import utils as util

d2r = np.pi/180.0
r2d = 180.0/np.pi

def calc_julian_day(udate, modified=False):
    """
    Calculate Julian Day
    :param udate:Date(Arbitrary)
    :param modified:Modified Julian Day
    :return: Julian Day
    """
    _y = udate.year + util.gauss((udate.month - 3) / 12)
    _m = (udate.month - 3) % 12
    _d = udate.day - 1
    _n = _d + util.gauss((153 * _m + 2) / 5) + 365 * _y + util.gauss(_y / 4) - util.gauss(_y / 100) + util.gauss(_y / 400)
    Tu = _n - 678881 - 0.5

    if not modified:
        Tu += 2400001
    return Tu


def calc_sideral_time_greenwich(Tu):
    """
    Calculate Sideral Time
    :param Tu: Julian Day
    :return:Sideral Time
    """
    _2000_1_1 = 2451545.0
    _TeeU = (Tu - _2000_1_1) / 36525.0
    _TeeG = (24110.54841 + 8640184.812866 * _TeeU + 0.093104 * _TeeU ** 2 - 0.0000062 * _TeeU ** 3) / 86400
    theta0 = 24 * (_TeeG - util.gauss(_TeeG))
    return theta0


def calc_sideral_time(lambda_, theta0, utime):
    """
    Calculate Local Sideral Time
    :param lambda_: Longitude of observation
    :param theta0: Sideral Time
    :param utime: Time
    :return: Sideral Time(Local)
    """
    _lambda = util.dms2deg(*lambda_) / 15  # [deg]
    theta = theta0 + 1.00273791 * util.time2deg(utime) + _lambda
    if theta > 24.0:
        theta -= 24.0
    return theta


class GreenWich(object):
    def __init__(self, udate, utime, lambda_):
        self._udate = udate
        self._utime = utime
        self._lambda_ = lambda_
        self.Tu = calc_julian_day(self._udate)
        self.theta0 = calc_sideral_time_greenwich(self.Tu)
        self.theta = calc_sideral_time(self._lambda_, self.theta0, self._utime)

    def __repr__(self):
        return "{0[0]}h {0[1]:.5f}' {0[2]:.5f}''".format(util.deg2hms(self.theta))

    def __str__(self):
        return "{}.format(util.deg2rad(self.theta))"
