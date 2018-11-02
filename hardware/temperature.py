from database.admin import DataBase
from system.timer import TimerEvent

class TemperatureSensor():

    def __init__(self):
        self.update_seconds = 1
        self.h_temperature = 'h_temperature'

        self.read_sensor_timer = TimerEvent(self.update_seconds, self.read_sensor)
        self.read_sensor_timer.start()

    def read_sensor(self):
        # x = float(DataBase.get_value(self.h_temperature))
        # x = x + 1
        # DataBase.set_value(self.h_temperature, x)
        pass

    def stop_timers(self):
        print("Stopping temperature sensor read event.")
        self.read_sensor_timer.cancel()
