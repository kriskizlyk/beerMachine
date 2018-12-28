from hardware.scale import Scale
from hardware.temperature import TemperatureSensor
from hardware.doorswitch import DoorSwitch
from hardware.compressor import Compressor
try:
    import RPi.GPIO as GPIO
except:
    print("***WARNING*** Raspberry GPIO not loaded since this is not a RaspberryPi.")

class Hardware():
    def __init__(self):
        self.scale_co2 = Scale('co2', 8)
        self.scale_1 = Scale('1', 9)
        self.scale_2 = Scale('2', 10)        
        self.temp_sensor = TemperatureSensor()
        self.door_switch = DoorSwitch(5, 'i')
        self.compressor = Compressor(27, 'o')

        self.hardware = [
            self.scale_co2,
            self.scale_1,
            self.scale_2,
            self.temp_sensor,
            self.door_switch,
            self.compressor,
        ]

    def stop_services(self):
        print('Stopping Hardware Read Services...')
        # If the system is told to shut down but durring a read these
        # services may not shut off in between reads.  Should use a proper
        # scheduler to see if the hanlder is busy or not.

        try:
            GPIO.cleanup()
        except:
            print("***WARNING*** Raspberry GPIO not cleaned since this is not a RaspberryPi.")

        while len(self.hardware) >= 1:
            for each_service in self.hardware:
                if (each_service.is_busy() == False):
                    each_service.stop_timers()
                    self.hardware.remove(each_service)
                    # print(dir(self.hardware[0]))
