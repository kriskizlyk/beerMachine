from database.admin import DataBase
from system.timer import TimerEvent

class DoorSwitch:

    def __init__(self, pin_number, io_typetype):
        try:
            import RPi.GPIO as GPIO
        except:
            print("***WARNING*** GPIO not loaded since this is not a RaspberryPi.")

        self.door_switch_temp = 'h_door_switch_2'
        self.pin_number = pin_number
        self.pin_state = 0

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin_number, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        except:
            print("Error settings compressor output.")# Code will only work with a RaspberryPi            

        self.update_seconds = 1.0
        self.read_switch_timer = TimerEvent(self.update_seconds, self.read_switch)
        self.read_switch_timer.start()
        self.busy = False

        print("Door Switch created.")

    def is_busy(self):
        return self.busy

    def read_switch(self):
        self.busy = True
        try:
            self.pin_state = GPIO.input(self.pin_number)
            #print(GPIO.input(self.pin_number))
        except:
            self.pin_state = 1

        if (self.pin_state == 0):
            DataBase.set_value(self.door_switch_temp, 'open')
        else:
            DataBase.set_value(self.door_switch_temp, 'closed')

        self.busy = False

    def stop_timers(self):
        print("Stopping door switch read event.")
        self.read_switch_timer.cancel()
