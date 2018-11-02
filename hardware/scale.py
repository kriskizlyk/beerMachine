from database.admin import DataBase
from system.timer import TimerEvent

class Scale():

    def __init__(self, scale_number):
        self.scale_number = scale_number
        self.update_seconds = 0.1
        self.h_tap_capacity = 'h_tap_' + self.scale_number + '_capacity'

        self.read_scale_timer = TimerEvent(self.update_seconds, self.read_scale)
        self.read_scale_timer.start()

    def read_scale(self):
        # x = float(DataBase.get_value(self.h_tap_capacity))
        # x = x + 1
        # DataBase.set_value(self.h_tap_capacity, x)
        pass

    def stop_timers(self):
        print("Stopping scale " + self.scale_number + " read event.")
        self.read_scale_timer.cancel()
