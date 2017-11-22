# --- coding: utf-8 ---

import os
import numpy as np
import utils as util

make_path = lambda f: os.path.join(os.path.dirname(__file__), ""+f)

HIPP_CATALOG_HEADER_SIZE = 5
MAPPED_CATALOG_HEADER = ["ID", "VMAG", "RIGHT", "DEC"]

d2r = np.pi/180.0
r2d = 180.0/np.pi


class Hipprcos(object):
    def __init__(self, fp):
        self._path = make_path(fp)

        def fetch(self):
            result = []
            with open(self._path, mode="r") as f:
                result = [row.split("|") for row in f]
            return result

        self._fetched = fetch(self)

    def generate_mapped_catalog(self):
        (_, _hipID, _right, _dec, _stype, _vmag, _raDeg, _decDeg) = range(8)
        _stars = self._fetched[HIPP_CATALOG_HEADER_SIZE:]
        _starEnlisted = []
        for star in _stars:
            _, id = star[_hipID].split()
            right = util.right2rad(star[_right])
            dec = util.dec2rad(star[_dec])
            vmag = float(star[_vmag])
            _starEnlisted.append(SingleStar(id=id, vmag=vmag, right=right, declination=dec))

        matrix_mapped_catalog = np.empty((len(_starEnlisted)), dtype=SingleStar)
        for i, _row in enumerate(_starEnlisted):
            matrix_mapped_catalog[i] = _row

        return matrix_mapped_catalog


class SingleStar(object):
    def __init__(self, id, vmag, right, declination):
        self.id = id
        self.vmag = vmag
        self.lambda_ = right
        self.phi = declination
        self.isHorizontal = False

    def __repr__(self):
        system_str = "Equator"
        if self.isHorizontal:
            system_str = "Horizontal"
        return "ID:{0}. VMAG:{1}, RIGHT_ASCENTION:{2}, DECLINATION:{3}, SYSTEM: {4}"\
            .format(self.id, self.vmag, self.lambda_*r2d, self.phi*r2d, system_str)

    def __str__(self):
        system_str = "Equator"
        if self.isHorizontal:
            system_str = "Horizontal"

        return "{}".format(self.id, self.vmag, self.lambda_ * r2d, self.phi * r2d, system_str)

    def direction_cosine(self):
        cd, ca = np.cos(self.phi), np.cos(self.lambda_)
        sd, sa = np.sin(self.phi), np.sin(self.lambda_)
        dcm = np.matrix([cd * ca, cd * sa, sd])
        return np.transpose(dcm)

    def to_horizontal_system(self, lam, theta):
        lmatrix = np.matrix([[np.sin(lam), 0, -np.cos(lam)], [0, 1, 0], [np.cos(lam), 0, np.sin(lam)]])
        rmatrix = np.matrix([[np.cos(theta), np.sin(theta), 0], [-np.sin(theta), np.cos(theta), 0], [0, 0, 1]])
        return lmatrix * rmatrix

    def transformation_matrix_product(self, lam, theta):
        return self.to_horizontal_system(lam, theta) * self.direction_cosine()

    def transformation_to_horizontal_system(self, lam, theta):
        left = self.transformation_matrix_product(lam, theta)[:, 0]
        if left[0] >= 0.0:
            self.lambda_ = np.arctan(-left[1] / left[0])
        else:
            self.lambda_ = np.arctan(-left[1] / left[0]) + np.pi

        self.phi = np.arcsin(left[2])
        self.isHorizontal = True
        return np.hstack((self.lambda_, self.phi))