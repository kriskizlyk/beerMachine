from hardware.scale import Scale
from hardware.temperature import TemperatureSensor
from hardware.doorswitch import DoorSwitch

class Hardware():
    def __init__(self):
        self.scale_co2 = Scale('co2', 0x08)
        self.scale_1 = Scale('1', 0x09)
        self.temp_sensor = TemperatureSensor()
        self.door_switch = DoorSwitch(5, 'i'),

        self.hardware = [
            self.scale_co2,
            self.scale_1,
            self.temp_sensor,
            self.door_switch,
        ]

    def stop_services(self):
        print('Stopping Hardware Read Services...')
        # If the system is told to shut down but durring a read these
        # services may not shut off in between reads.  Should use a proper
        # scheduler to see if the hanlder is busy or not.
        print(len(self.hardware))
        while len(self.hardware) >= 1:
            for each_service in self.hardware:
                print(each_service)
                if (each_service.is_busy() == False):
                    each_service.stop_timers()
                    self.hardware.remove(each_service)
                    # print(dir(self.hardware[0]))
