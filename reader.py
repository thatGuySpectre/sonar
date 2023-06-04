#!/bin/python3
import math

import scipy
import serial
import logging
import yaml
import numpy as np
import PySimpleGUI as sg

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def error_func(mics, vals):
    x, y, r = vals
    total = 0
    logger.debug(vals)
    logger.debug(mics)
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


def get_pos(t1, t2, t3, conf): 
    x0 = np.array((0, 0, 0))
    mics = conf["mics"]
    mics = [np.array((*m, float(t))) for (m, t) in zip(mics, (t1, t2, t3))]
    out = scipy.optimize.minimize(lambda x: error_func(mics, x), x0, method="BFGS", 
                                  jac = lambda x: grad_err_func(mics, x))
    return out.x


def get_radial(x0):
    x, y, r = x0
    phi = math.atan2(x, y) / math.pi * 180

    return r, phi


def update_view(window, distance, angle):
    graph = window["graph"]
    graph.erase()

    graph.draw_circle((200, 200), 160, line_color='black', fill_color='white')

    arrow_length = 120
    arrow_tip = (
        200 + arrow_length * math.sin(math.radians(angle)),
        200 + arrow_length * math.cos(math.radians(angle))
    )
    graph.draw_line((200, 200), arrow_tip, width=2)

    # Update the distance text
    window["dist"].update(f'{distance:.2f} units')


if __name__=="__main__":
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    layout = [
    [sg.Graph(canvas_size=(400, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 400), key='graph', background_color='white')],
    [sg.Text('Distance: ', justification='center')],
    [sg.Text('', size=(10, 1), key='dist', justification='center', font=("Arial", 20))]
]

    window = sg.Window("Sonar", layout=layout, finalize=True)

    serial_port = config["port"] # '/dev/ttyACM0'
    baud_rate = config["rate"]   # 54700

    ser = serial.Serial(serial_port, baud_rate)

    while True:
        line = ser.readline().decode().strip()
        logger.debug("serial message: " + line)

        l = line.split(",")
        if line[0] == "misfire":
            logging.info(line)
        else:
            t1, t2, t3 = l
            pos = get_pos(t1, t2, t3, config)
            r, phi = get_radial(pos)
            update_view(window, r, phi)
            window.read(timeout=0)
            logging.info(f"(x,y)={pos[0], pos[1]} - (r, phi)={r, phi}")


