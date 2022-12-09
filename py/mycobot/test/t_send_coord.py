import sys
import os
sys.path.append(os.path.dirname(__file__))
from port_setup import setup

if __name__ == "__main__":
    mc = setup()
    _sp = input('Please input speed(0-100):')
    try:
        sp = int(_sp)
    except Exception:
        print('Error: invalid speed, speed is default: 80')
        sp = 80

    while not False:
        sinp = input('Please input coord(euler,xyz), like ("0,0,0,0,0,0"):')
        try:
            slist = sinp.split(',')
            if len(slist) != 6:
                raise Exception('')
            coord = [float(i) for i in slist]
        except Exception:
            print('Error: invalid angles string.')
            continue

        mc.send_coords(coord, sp, 0)

