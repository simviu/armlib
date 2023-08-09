import time
import os
import sys
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord

sys.path.append(os.path.dirname(__file__))
from port_setup import setup

reset = [153.19, 137.81, -153.54, 156.79, 87.27, 13.62]

# Pick0 : coords:[-110, -200, 80,    85, 40, 0]



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
    mycobot.send_coords([-110, -200, 160,  85, 40, 0  ], sp, 0)
    time.sleep(3)
    mycobot.send_coords([-170, -200, 140,  85, 40, -10], sp, 0)
    time.sleep(5)
    mycobot.send_coords([-173, -190, 80,  70, 43, -17], sp, 0)
    time.sleep(5)
    set_grip(mycobot, True)
    time.sleep(2)
    mycobot.send_coords([-110, -200, 160,  85, 40, 0], sp, 0)
    time.sleep(2)
    mycobot.send_coords([ 110, -200, 160,  85, 40, 0  ], sp, 0)
    time.sleep(3)

    mycobot.send_coords([ 120, -220, 60,  170, -5, -110  ], sp, 0)

    time.sleep(3)
    set_grip(mycobot, False)
    time.sleep(1)

    mycobot.send_coords([ 110, -160, 160,  85, 40, 0   ], sp, 0)
    time.sleep(1)


    #mycobot.release_all_servos()

    print("=== test end ===\n")


if __name__ == "__main__":

    time.sleep(3)

    mycobot = setup()
    test(mycobot)

