#!/bin/python3
import math

import scipy
import serial
import logging
import yaml
import numpy as np
import PySimpleGUI as sg

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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
    return np.array((dx, dy, dr))


def get_pos(r1, r2, r3, conf):
    x0 = np.array((0, 0, 0))
    mics = conf["mics"]
    mics = [np.array((*m, float(t))) for (m, t) in zip(mics, (r1, r2, r3))]
    logger.info(mics)
    out = scipy.optimize.minimize(
        fun=lambda x: error_func(mics, x),
        x0=x0,
        method="BFGS",
        jac=lambda x: grad_err_func(mics, x)
    )
    return out.x


def get_radial(x0):
    x, y, _ = x0
    r = (x**2 + y**2)**0.5
    phi = math.atan2(y, x) / math.pi * 180

    return r, phi


def update_view(window, distance, angle):
    graph = window["graph"]
    graph.erase()

    graph.draw_circle((200, 200), 160, line_color='black', fill_color='white')

    arrow_length = 120
    arrow_tip = (
        200 + arrow_length * - math.cos(math.radians(angle)),
        200 + arrow_length * - math.sin(math.radians(angle))
    )
    graph.draw_line((200, 200), arrow_tip, width=2)

    # Update the distance text
    window["dist"].update(f'{distance:.2f} meters')
    window["angle"].update(f"{angle:.2f} degrees from x")


if __name__=="__main__":
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    layout = [
    [sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), key='graph', background_color='white')],
    [sg.Text('Distance: ', justification='center')],
    [sg.Text('', size=(40, 1), key='dist', justification='center', font=("Arial", 20))],
    [sg.Text('', size=(40, 1), key='angle', justification='center', font=("Arial", 20))]
]

    window = sg.Window("Sonar", layout=layout, finalize=True)

    serial_port = config["port"] # '/dev/ttyACM0'
    baud_rate = config["rate"]   # 54700

    ser = serial.Serial(serial_port, baud_rate)

    while True:
        line = ser.readline().decode().strip()
        logger.debug("serial message: " + line)

        l = line.split(",")
        if len(l) != 3:
            logging.info(line)
        else:
            t1, t2, t3 = l
            logger.info((t1, ":", t2, ":", t3))
            m1 = int(t1) / config["scale_factor"]
            m2 = int(t2) / config["scale_factor"]
            m3 = int(t3) / config["scale_factor"]
            pos = get_pos(m1, m2, m3, config)
            logger.info(pos)
            with open("buzz_-3_10.txt", "a") as f:
                f.write(f"{pos}\n")
            r, phi = get_radial(pos)
            update_view(window, r, phi)
            window.read(timeout=0)
            logging.info(f"(x,y)={pos[0], pos[1]} - (r, phi)={r, phi}")


