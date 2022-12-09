import time
import os
import sys
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord

sys.path.append(os.path.dirname(__file__))
from port_setup import setup

reset = [153.19, 137.81, -153.54, 156.79, 87.27, 13.62]


def set_grip(mc, on):
    if on:
        mc.set_encoder(7, 1300)
    else:
        mc.set_encoder(7, 2048)

def test(mycobot):
    print("\nStart check basic options\n")

    mycobot.set_color(255, 255, 0)
    print("::set_color() ==> color {}\n".format("255 255 0"))
    time.sleep(3)


    sp = 50

    set_grip(mycobot, False)
    time.sleep(1)
    mycobot.send_coords([160, -100, 100, -89.36, 42.82, -176.93], sp, 0)
    time.sleep(1)
    mycobot.send_coords([160, -100, 10, -89.36, 42.82, -176.93], sp, 0)
    time.sleep(1)
    set_grip(mycobot, True)
    time.sleep(1)
    mycobot.send_coords([-17.3, -190, 100, -91.3, 56.66, 173.02], sp, 0)
    time.sleep(1)

    mycobot.send_coords([-17.3, -190, 10, -91.3, 56.66, 173.02], sp, 0)
    time.sleep(1)
    set_grip(mycobot, False)
    time.sleep(1)

    mycobot.send_coords([80, -190, 100, -91.3, 56.66, 173.02], sp, 0)
    time.sleep(1)


    #mycobot.release_all_servos()

    print("=== test end ===\n")


if __name__ == "__main__":

    time.sleep(3)

    mycobot = setup()
    test(mycobot)

