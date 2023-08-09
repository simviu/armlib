import time
import os
import sys
from pymycobot.mycobot import MyCobot
from pymycobot.genre import Angle, Coord

sys.path.append(os.path.dirname(__file__))
from port_setup import setup

reset = [153.19, 137.81, -153.54, 156.79, 87.27, 13.62]

# Pick0 : coords:[-110, -200, 80,    85, 40, 0]

Pa = [ 240 -30, 50,    80, 45, 70  ] # approach
Pg = [ 240 -30, 0,     80, 45, 70  ] # grab
Pwp1=[ 0,  100, 150,    80, 40, 0   ] # waypnt 1
Pd = [-120, 150, 100,  75, 40, -50 ] # drop

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


    sp = 10 

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
    time.sleep(3)

    #---- drop
    set_grip(mycobot, False)
    time.sleep(1)

    #---- back to idle
    mycobot.send_coords(Pwp1, sp, 0)
    time.sleep(1)


    #mycobot.release_all_servos()

    print("=== test end ===\n")


if __name__ == "__main__":

    time.sleep(3)

    mycobot = setup()
    test(mycobot)

