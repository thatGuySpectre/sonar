import os

import numpy as np
from matplotlib import pyplot as plt

for file in os.listdir("measurements"):
    with open(file) as f:
        lines = [l.strip("[]\n").split(" ") for l in f.readlines()]
        lines = [[float(x) for x in i if x != ""] for i in lines]

    xs = sorted([i[0] for i in lines])[3:-3]
    ys = sorted([i[1] for i in lines])[3:-3]

    xavg = np.average(xs)
    yavg = np.average(ys)

    xdev = np.std(xs)
    ydev = np.std(ys)

    fig, ax = plt.subplots()

    ax.plot(xs, ys, ".")

    # set the x-spine (see below for more info on `set_position`)
    ax.spines['left'].set_position('zero')

    # turn off the right spine/ticks
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()

    # set the y-spine
    ax.spines['bottom'].set_position('zero')

    # turn off the top spine/ticks
    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()

    if "buzz" in file:
        scale = 0.3
    else:
        scale = 3
    ax.set_xlim([-scale, scale])
    ax.set_ylim([-scale, scale])

    fig.savefig(file + ".png")
    # plt.show()

    print(f"{file}: {xavg:.3f} +- {xdev:.3f} : {yavg:.3f} +- {ydev:.3f}")