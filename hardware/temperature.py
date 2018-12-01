from database.admin import DataBase
from system.timer import TimerEvent

try:
    from w1thermsensor import W1ThermSensor
except:
    print("***WARNING*** w1thermsensor not loaded since this is not a RaspberryPi.")


class TemperatureSensor():

    def __init__(self):
        self.update_seconds = 1
        self.h_temperature = 'h_temperature'
        self.h_temp_decimal = 'h_temp_decimal'
        self.filtered = 0.0
        self.filtered_previous = 0.0
        self.new_output = 0.0
        self.filter_k = 0.3

        self.read_sensor_timer = TimerEvent(self.update_seconds, self.read_sensor)
        self.read_sensor_timer.start()
        self.busy = False

        print("Temperature Sensor created.")

    def is_busy(self):
        return self.busy

    def read_sensor(self):
        self.busy = True

        try:
            sensor = W1ThermSensor()
            self.new_input = sensor.get_temperature()
            self.filtered = ((1.0 - self.filter_k) * self.filtered_previous) + (self.filter_k * self.new_input)
            self.filtered_previous = self.filtered
        
            #temp = '{0:.' + str(self.h_temp_decimal) +'f}'.format(temp)
            temp = '{0:.1f}'.format(self.filtered)
        
            DataBase.set_value(self.h_temperature, temp)
            
        except:
            self.read_sensor_timer.error()
            print("Temperature Sensor reading failed.")

        self.busy = False

    def stop_timers(self):
        print("Stopping temperature sensor read event.")
        self.read_sensor_timer.cancel()

