from database.admin import DataBase
from system.timer import TimerEvent
from smbus2 import SMBusWrapper, i2c_msg
from struct import pack, unpack
from time import sleep
from decimal import Decimal

class Scale():

    def __init__(self, scale_number):
        self.scale_number = scale_number
        self.update_seconds = 0.1
        self.h_tap_capacity = 'h_tap_' + self.scale_number + '_capacity'

        self.read_scale_timer = TimerEvent(self.update_seconds, self.read_scale)
        self.read_scale_timer.start()
        self.busy = False
    
    def is_busy(self):
        return self.busy

    def read_scale(self):
        self.busy = True
        address = 0x08
        command = pack('>B', 10)
        data = 0        
        result = 0
        
        try:
            with SMBusWrapper(1) as bus:
                write = i2c_msg.write(address, command)
                read = i2c_msg.read(address, 5) 
                bus.i2c_rdwr(write, read)
                data = list(read)
                data.pop() # Have to get rid of the last on...smbus does something I am not sure why.
                data = bytes(data)
                result = unpack(">I", data)[0]
                if (result < 0):
                    result = 0.0
                    DataBase.set_value(self.h_tap_capacity, result)
                elif (result > 100000):
                    pass
                else:
                    result = '{0:.3f}'.format(result / 1000.0)
                    DataBase.set_value(self.h_tap_capacity, result)                    
                #print("Scale reading success.  " + str(result))      
            
        except:
            print("Scale reading Failed.")        
        
        self.busy = False
        # x = float(DataBase.get_value(self.h_tap_capacity))
        # x = x + 1
        # DataBase.set_value(self.h_tap_capacity, x)

    def stop_timers(self):
        print("Stopping scale " + self.scale_number + " read event.")
        self.read_scale_timer.cancel()
