from database.admin import DataBase
from system.timer import TimerEvent
from smbus2 import SMBusWrapper, i2c_msg
from struct import pack, unpack
from time import sleep

class Scale():

    def __init__(self, scale_number):
        self.scale_number = scale_number
        self.update_seconds = 1.0
        self.h_tap_capacity = 'h_tap_' + self.scale_number + '_capacity'

        self.read_scale_timer = TimerEvent(self.update_seconds, self.read_scale)
        self.read_scale_timer.start()

    def read_scale(self):
        address = 0x08
        command = pack('>B', 10)
        data = 0        
        result = 0
        
        try:
            write = i2c_msg.write(address, command)
            read = i2c_msg.read(address, 4)
            with SMBusWrapper(1) as bus:
                bus.i2c_rdwr(write, read)
            data = bytes(list(read))
            #print(bytes(data))
            print(data)
            result = unpack(">I", data)[0]
            DataBase.set_value(self.h_tap_capacity, result)
            print("Scale reading success.  " + str(result))        
            
        except:
            print("Scale reading Failed.")        
        
        # x = float(DataBase.get_value(self.h_tap_capacity))
        # x = x + 1
        # DataBase.set_value(self.h_tap_capacity, x)
        pass

    def stop_timers(self):
        print("Stopping scale " + self.scale_number + " read event.")
        self.read_scale_timer.cancel()
