import time
import os
import sys
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord

sys.path.append(os.path.dirname(__file__))
from port_setup import setup

reset = [153.19, 137.81, -153.54, 156.79, 87.27, 13.62]

# Pick0 : coords:[-110, -200, 80,    85, 40, 0]

Pa = [ 240, -15, 50,    100, 40, 20  ] # approach
Pg = [ 240, -15,  0,    100, 40, 20  ] # grab
Pwp1=[ 210,  60, 100,   100, 45, 30  ] # waypnt 1
Pd = [ -70, 162,  120,   95, 38, 90  ] # drop

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


    sp = 20 

    set_grip(mycobot, False)
    time.sleep(1)

    #---- reset point
    mycobot.send_coords(Pwp1, sp, 0)
    time.sleep(3)


    #---- approach point
    mycobot.send_coords(Pa, sp, 0)
    time.sleep(5)


    #--- grab point
    mycobot.send_coords(Pg, sp, 0)
    time.sleep(5)

    #---- grab
    set_grip(mycobot, True)
    time.sleep(2)

    #---- lift up
    mycobot.send_coords(Pa, sp, 0)
    time.sleep(2)

    #----- reset place
    mycobot.send_coords(Pwp1, sp, 0)
    time.sleep(3)

    #---- drop point
    mycobot.send_coords(Pd, sp, 0)
    time.sleep(7)

    #---- drop
    set_grip(mycobot, False)
    time.sleep(1)

    #---- back to idle
    mycobot.send_coords(Pwp1, sp, 0)
    time.sleep(1)


    #mycobot.release_all_servos()

    print("=== test end ===\n")
    return


if __name__ == "__main__":

    time.sleep(3)

    mycobot = setup()
    test(mycobot)

