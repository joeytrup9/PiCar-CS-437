from evdev import InputDevice,categorize,ecodes,KeyEvent
from gui_control import Car
dev = InputDevice('/dev/input/event0')
print(dev)
car = Car()
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        print(event.value, event.code)
        if event.value == 1:
            if event.code == ecodes.KEY_RIGHT:
                car.key_controller(False,False,False,True)
            if event.code == ecodes.KEY_UP:
                car.key_controller(True,False,False,False)
            if event.code == ecodes.KEY_LEFT:
                car.key_controller(False,False,True,False)
            if event.code == ecodes.KEY_DOWN:
                car.key_controller(False,True,False,False)
        if event.value == 0:
            if event.code == ecodes.KEY_RIGHT:
                car.key_controller(False,False,False,False)
            if event.code == ecodes.KEY_UP:
                car.key_controller(False,False,False,False)
            if event.code == ecodes.KEY_LEFT:
                car.key_controller(False,False,False,False)
            if event.code == ecodes.KEY_DOWN:
                car.key_controller(False,False,False,False)