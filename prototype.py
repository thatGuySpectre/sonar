#!/bin/python3

import random


def circle_intersect(c1, c2, r1, r2):
    x1, y1 = c1
    x2, y2 = c2 

    r = ((x1 - x2)**2 + (y1 - y2)**2)**.5

    #if not (abs(r1-r2) <= r <= abs(r1+r2)):
    #    return ()

    a = 0.5*(x1+x2) + (r1**2 - r2**2)/2/r**2 * (x2-x1)
    apm = 0.5*(2*(r1**2+r2**2)/r**2 - (r1**2-r2**2)**2/r**4 - 1)**.5 * (y2 - y1)
    
    b = 0.5*(y1+y2) + (r1**2 - r2**2)/2/r**2 * (y2-y1)
    bpm = 0.5*(2*(r1**2+r2**2)/r**2 - (r1**2-r2**2)**2/r**4 - 1)**.5 * (x1 - x2)

    return ((a+apm, b+bpm), (a-apm, b-bpm))


def get_random_pos(d=5):
    x = (random.random()-0.5) * 2*d
    y = (random.random()-0.5) * 2*d

    return x, y


def get_times(x1, x2, x3, x, y):
    t1 = ((x-x1[0])**2 + (y-x1[1])**2)**0.5 / 343
    t2 = ((x-x2[0])**2 + (y-x2[1])**2)**0.5 / 343
    t3 = ((x-x3[0])**2 + (y-x3[1])**2)**0.5 / 343

    return t1, t2, t3


def get_actual(p1, p2, p3):
    best = float("inf")
    best_i = 0, 0, 0

    for i in range(2):
        for j in range(2):
            for k in range(2):
                err = 0
                err += diff(p1[i], p2[j])
                err += diff(p1[i], p3[k])
                err += diff(p2[j], p3[k])

                if abs(err) < best:
                    best = abs(err)
                    best_i = i, j, k

    i, j, k = best_i
    best_x = (p1[i][0] + p2[j][0] + p3[k][0])/3
    best_y = (p1[i][1] + p2[j][1] + p3[k][1])/3
    
    return best_x, best_y


def diff(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)**.5


def noise(t1, t2, t3, n=0.5/343):
    return (
            t1 + (random.random() - 0.5) * n,
            t2 + (random.random() - 0.5) * n,
            t3 + (random.random() - 0.5) * n,
            )


if __name__=="__main__":
    x1, x2, x3 = (0, 0), (1, 0), (0, 1)
    x, y = get_random_pos()

    t1, t2, t3 = noise(*get_times(x1, x2, x3, x, y)) 

    c = 343

    p1 = (circle_intersect(x1, x2, t1*c, t2*c))
    p2 = (circle_intersect(x1, x3, t1*c, t3*c))
    p3 = (circle_intersect(x2, x3, t2*c, t3*c))

    print("actual:")
    print(x, y)
    print("measured:")
    print(get_actual(p1, p2, p3))
