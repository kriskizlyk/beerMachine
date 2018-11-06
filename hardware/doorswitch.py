from database.admin import DataBase
from system.timer import TimerEvent
import RPi.GPIO as GPIO

class DoorSwitch:
    def __init__(self, pin_number, type):
        self.door_switch = 'h_door_switch'
        self.pin_number = pin_number
        self.pin_state = 0
        GPIO.setmode(GPIO.BCM)
        if (type == 'i'):
            GPIO.setup(self.pin_number, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        elif (type == 'o'):
            pass
        
        self.update_seconds = 1.0
        self.read_switch_timer = TimerEvent(self.update_seconds, self.read_switch)
        self.read_switch_timer.start()
        self.busy = False
        
    def is_busy(self):
        return self.busy  
    
    def read_switch(self):
        self.busy = True
        self.pin_state = GPIO.input(self.pin_number)
        #print(GPIO.input(self.pin_number))
        if (self.pin_state == 0):
            print("Door switch open.")
            DataBase.set_value(self.door_switch, 'open')
        else:
            print("Door switch closed.")
            DataBase.set_value(self.door_switch, 'closed')
        
        self.busy = False
        
    def stop_timers(self):
        print("Stopping door switch read event.")
        self.read_switch_timer.cancel()