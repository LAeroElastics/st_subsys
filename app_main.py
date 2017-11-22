#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime, time
import matplotlib.pyplot as plt
from greenwich import *
from file_io import *

plt.rcParams['agg.path.chunksize'] = 100000

MIN_VMAG_THRESHOLD = 3.0


def main(filepath):
    _date = datetime(2000,1,1)
    _time = time(12,0,0)
    lambd = (145,45,45)
    gw = GreenWich(_date, _time, lambd)
    print(gw.__repr__())
    print(gw.theta)

    catalog = Hipprcos(filepath)

    direction, altitude = [], []
    mapped = catalog.generate_mapped_catalog()
    for star in mapped:
        star.transformation_to_horizontal_system(util.dms2deg(*lambd)*d2r, gw.theta*d2r)
        if star.vmag < MIN_VMAG_THRESHOLD:
            direction.append(star.lambda_*r2d)
            altitude.append(star.phi*r2d)

    for star in mapped:
        star.__repr__()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(direction, altitude, c="k", marker=".", s=1)
    ax.set_title("")
    ax.set_xlabel("Direction[deg]")
    ax.set_ylabel("Altitude[deg]")
    plt.minorticks_on()
    plt.xlim([-90, 270])
    plt.tick_params(axis="both", which="both", direction="in")
    plt.grid(which="major", color="k", linestyle="--")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Hipparcus catalog path")
    args = parser.parse_args()
    main(args.path)
