import time

from pymycobot import MyCobotSocket

HOST="ubuntu.local"
PORT=9000

mc = MyCobotSocket(HOST, PORT)

print(mc.get_angles())
# mc.power_on()
# mc.power_off()
print("sync_send_angles")
mc.sync_send_angles([5, 0, -100, 10, -5 ,20], 100)

