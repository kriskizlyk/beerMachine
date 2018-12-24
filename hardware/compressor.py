from database.admin import DataBase
from system.timer import TimerEvent

try:
    import RPi.GPIO as GPIO
except:
    print("***WARNING*** compressor not loaded since this is not a RaspberryPi.")

class Compressor:

    def __init__(self, pin_number, io_type):
        #try:
        #    import RPi.GPIO as GPIO
        #except:
        #    print("***WARNING*** GPIO not loaded since this is not a RaspberryPi.")

        self.door_switch = 'h_compressor_switch'
        self.pin_number = pin_number
        self.pin_state = 0

        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin_number, GPIO.OUT)

        except:
            print("Error settings compressor output.")# Code will only work with a RaspberryPi

        self.update_seconds = 1.0
        self.run_compressor_timer = TimerEvent(self.update_seconds, self.run_compressor)
        self.run_compressor_timer.start()
        self.busy = False
        self.state = 0
        self.last_state = 0
        self.run = 0

        print("Compressor Motor switch created.")

    def is_busy(self):
        return self.busy

    def run_compressor(self):
        self.busy = True
        temp = DataBase.get_value('h_temperature')
        temp = float(temp)

        #try:
        if (temp > 8.0):
            DataBase.set_value('h_door_switch', 'RUNNING')
            GPIO.output(self.pin_number, 1)


        elif (temp < 6.0):
            DataBase.set_value('h_door_switch', 'STOPPED')
            GPIO.output(self.pin_number, 0)

        else:
            pass

        self.busy = False

    def stop_timers(self):
        print("Stopping compressor run read event.")
        self.run_compressor_timer.cancel()
