import ast
import numpy as np
from matplotlib import pyplot as plt

with open(input()) as f:
    lines = [l.strip("[]\n").split(" ") for l in f.readlines()]
    lines = [[float(x) for x in i if x != ""] for i in lines]

xs = sorted([i[0] for i in lines])[3:-3]
ys = sorted([i[1] for i in lines])[3:-3]

xavg = np.average(xs)
yavg = np.average(ys)

xdev = np.std(xs)
ydev = np.std(ys)

plt.plot(xs, ys, ".")
# plt.xlim(-1, 1)
# plt.ylim(-1, 1)
plt.show()

print(f"{xavg:.3f} +- {xdev:.3f} : {yavg:.3f} +- {ydev:.3f}")