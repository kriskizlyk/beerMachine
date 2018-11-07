from database.admin import DataBase
from system.timer import TimerEvent

try:
    import RPi.GPIO as GPIO
except:
    print("***WARNING*** GPIO not loaded since this is not a RaspberryPi.")

class DoorSwitch:
    def __init__(self, pin_number, type):
        self.door_switch = 'h_door_switch'
        self.pin_number = pin_number
        self.pin_state = 0

        try:
            GPIO.setmode(GPIO.BCM)
            if (type == 'i'):
                GPIO.setup(self.pin_number, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
            elif (type == 'o'):
                pass
        except:
            # Code will only work with a RaspberryPi
            pass

        self.update_seconds = 1.0
        self.read_switch_timer = TimerEvent(self.update_seconds, self.read_switch)
        self.read_switch_timer.start()
        self.busy = False

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
            DataBase.set_value(self.door_switch, 'open')
        else:
            DataBase.set_value(self.door_switch, 'closed')

        self.busy = False

    def stop_timers(self):
        print("Stopping door switch read event.")
        self.read_switch_timer.cancel()
