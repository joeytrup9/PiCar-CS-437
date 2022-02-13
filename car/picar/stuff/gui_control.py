from tkinter import *
from tkinter import ttk
import picar_4wd as picar
from picar_4wd.pwm import PWM
from picar_4wd.adc import ADC
from picar_4wd.pin import Pin
from picar_4wd.motor import Motor
from picar_4wd.servo import Servo
from picar_4wd.ultrasonic import Ultrasonic 
from picar_4wd.speed import Speed
from picar_4wd.filedb import FileDB  
from picar_4wd.utils import *
from time import sleep
import random

left_rear_speed = Speed(25)
right_rear_speed = Speed(4)  




class App(object):
    def __init__(self):
        self.mode = 0 #0:key control, 1:avoid_mode, 2:line_follow_mode, 3:learn_room, 5:testing mode
        self.power = 50
        self.__r = False
        self.__l = False
        self.__f = False
        self.__b = False
        self.car = Car()
    def kill_connect(self):
        self.__r = False
        self.__l = False
        self.__f = False
        self.__b = False
        picar.stop()
        self.win.destroy()
    def key_pressed(self,event):
        if event.keysym == '1':
            self.car.mode = 0
        if event.keysym == '2':
            self.car.mode = 1
            self.car.avoid_mode()
        if event.keysym == '3':
            self.car.mode = 2
        if event.keysym == '4':
            self.car.mode = 3
        if event.keysym == '5':
            self.car.mode = 5
            self.car.ultrasonic_test()
            self.car.servo_test()
        if event.keysym == 'Escape':
            self.kill_connect()
        if event.keysym == 'Right':
            self.__r = True
            #picar.turn_right(power)
        if event.keysym == 'Left':
            self.__l = True
            #picar.turn_left(power)
        if event.keysym == 'Up':
            self.__f = True
            #picar.forward(power)
        if event.keysym == 'Down':
            #picar.backward(power)
            self.__b = True
        self.car.key_controller(self.__f,self.__b,self.__l,self.__r)
    def key_release(self,event):
        if event.keysym == 'Right':
            self.__r = False
            picar.stop()
        if event.keysym == 'Left':
            self.__l = False
            picar.stop()
        if event.keysym == 'Up':
            self.__f = False
            picar.stop()
        if event.keysym == 'Down':
            picar.stop()
            self.__b = False
        self.car.key_controller(self.__f,self.__b,self.__l,self.__r)
    def task(self):
        #if self.__r:
            #print ('right')
        #if self.__l:
            #print('left')
        #if self.__f:
            #print('forward')
        #if self.__b:
            #print('back')
        self.win.after(20,self.task)
    def runloop(self):
        self.win = Tk()
        self.win.geometry("750x750")
        self.frame = Frame(self.win, width=750, height=750)
        self.frame.pack()
        self.win.bind_all('<Key>', self.key_pressed)
        self.win.bind_all('<KeyRelease>', self.key_release)
        self.win.after(20,application.task)
        self.win.mainloop()

class Car():
    def __init__(self):
        self.left_front = Motor(PWM("P13"), Pin("D4"), is_reversed=True) # motor 1
        self.right_front = Motor(PWM("P12"), Pin("D5"), is_reversed=True) # motor 2
        self.left_rear = Motor(PWM("P8"), Pin("D11"), is_reversed=True) # motor 3
        self.right_rear = Motor(PWM("P9"), Pin("D15"), is_reversed=True) # motor 4
        self.servo = Servo(PWM("P0"), offset=0)
        self.ultrasonic = Ultrasonic(Pin('D8'), Pin('D9'))
        self.gs0 = ADC('A5')
        self.gs1 = ADC('A6')
        self.gs2 = ADC('A7')
        self.mode = 0
    def bidirectional_power(self, power_direction):
        self.left_front.set_power(power_direction[0])
        self.left_rear.set_power(power_direction[0])
        self.right_front.set_power(power_direction[1])
        self.right_rear.set_power(power_direction[1])
    def key_controller(self,f,b,l,r):
        power_direction = (0,0) #(left_power, right_power)
        #print("key command")
        if r:
            power_direction = (50,-50)
        if l:
            power_direction = (-50,50)
        if f:
            power_direction = (50,50)
        if b:
            power_direction = (-50,-50)
        if r and f:
            power_direction = (75,25)
        if r and b:
            power_direction = (-25, -75)
        if l and f:
            power_direction = (25,75)
        if l and b:
            power_direction = (-75,-25)
        self.bidirectional_power(power_direction)
    def servo_test(self):
        ang = input("type the angle you want the servo at:")
        self.servo.set_angle(int(ang))
    def ultrasonic_test(self):
        print(self.ultrasonic.get_distance() * .394)
        sleep(2)
        print(self.ultrasonic.get_distance() * .394)
    def key_control_mode():
        pass
    def avoid_mode(self):
        print(picar.power_read())
        self.bidirectional_power((50,50))
        while 1:
            scan_list = picar.scan_step(35)
            if scan_list != False and scan_list[3:7] != [2,2,2,2]:
                self.bidirectional_power((-50,-50))
                sleep(.5)
                turntime = random.randint(0,300)/100
                self.bidirectional_power((50, -50))
                sleep(turntime)
                self.bidirectional_power((50,50))
    def line_follow_mode():
        pass
    def learn_room_mode():
        pass
    def path_run_mode():
        pass

application = App()
application.runloop()
