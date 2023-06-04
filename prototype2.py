#!/bin/python3
import math
import random
import time

import numpy
import scipy.optimize

def error_func(mics, vals):
    x, y, r = vals
    total = 0
    for mic in mics:
        xm, ym, c = mic
        total += (
           (x-xm)**2 + (y-ym)**2 - (r + c)**2
        ) ** 2
    
    return total

def grad_err_func(mics, vals):
    x, y, r = vals
    dx, dy, dr = 0, 0, 0
    for mic in mics:
        xm, ym, c = mic

        dx += (
            4 * (x - xm) * (
                (x-xm)**2 + (y-ym)**2 - (r + c)**2
            )
        )
        dy += (
            4 * (y - ym) * (
                (x-xm)**2 + (y-ym)**2 - (r + c)**2
            )
        )
        dr += (
            -4 * (r + c) * (
                (x-xm)**2 + (y-ym)**2 - (r + c)**2
            )
        )

    return dx, dy, dr

def ooptimize(mics, d = 0.1):
    x, y, r = 0, 0, 0
    err_change = float("inf")
    err = error_func(mics, x, y, r)

    while abs(err_change) > 0.01:
        dx, dy, dr = grad_err_func(mics, x, y, r)
        nx = x - d * dx
        ny = y - d * dy
        nr = r - d * dr

        if err < error_func(mics, nx, ny, nr):
            d = d/2
            continue

        x = nx
        y = ny
        r = nr

        print(x, y, r, " -> ", dx, dy, dr)

        time.sleep(0.1)

    return x, y, r

def optimize(mics):
    x0 = 0, 0, 0
    out = scipy.optimize.minimize(lambda x: error_func(mics, x), x0, method="BFGS", 
                                  jac = lambda x: grad_err_func(mics, x))
    return out.x


def noise_mics(mics, n=0.1):
    mics = [(i, j, k * (1 + (-0.5 + random.random()) * n)) for (i, j, k) in mics]
    min_r = min(mic[2] for mic in mics)
    mics = [(i, j, k - min_r) for (i, j, k) in mics]
    return mics


def get_r_phi(x, y, r):
    r = (x**2 + y**2)**0.5
    phi = math.atan2(x, y) / math.pi * 180

    return r, phi


if __name__=="__main__":
    mics = [
        (0, -1, 2**0.5),
        (1, 0, 2),
        (0, 1, 2**0.5)
    ]

    rs, phis = [], []

    for noise in range(10):

        for i in range(100):

            n_mics = noise_mics(mics, 0.02 * noise)
    #        print(n_mics)

            xs = optimize(n_mics)
    #        print(xs)
    #        print("r={:2f} phi={:2f}°".format(*get_r_phi(*xs)))
            r, phi = get_r_phi(*xs)
            rs.append(r)
            phis.append(phi)

        print(f"noise = {noise * 0.05} \nr = ({numpy.mean(rs):.2f}+-{numpy.std(rs):.2f}) \nphi = ({numpy.mean(phis):.2f}+-{numpy.std(phis):.2f})°\n")