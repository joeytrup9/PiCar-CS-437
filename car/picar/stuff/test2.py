from gui_control import Car
import picar_4wd as picar
import signal
from sys import exit
car = Car()
def handler(sig,frame):
    picar.stop()
    exit()

signal.signal(signal.SIGINT, handler)

car.avoid_mode()
