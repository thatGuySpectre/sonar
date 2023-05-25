#!/bin/python3

import time
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


if __name__=="__main__":
    mics = [
        (0, 0, 2),
        (1, 0, 1),
        (0, 1, 5**0.5)
    ]

    x = optimize(mics)
    print(x)
