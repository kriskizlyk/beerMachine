from database.admin import DataBase
from system.timer import TimerEvent
from smbus2 import SMBusWrapper, i2c_msg
from struct import pack, unpack
from time import sleep
from decimal import Decimal

class Scale():

    def __init__(self, scale_number, address):
        self.address = str(address)
        self.scale_number = str(scale_number)

        self.h_scale_address = 'h_scale_' + self.scale_number + '_address'
        DataBase.set_value(self.h_scale_address, address)
        self.h_scale_name = 'h_scale_' + self.scale_number + '_name'
        self.h_scale_actual = 'h_scale_' + self.scale_number + '_actual'
        self.h_scale_dec = 'h_scale_' + self.scale_number + '_decimal'
        self.h_scale_grads = 'h_scale_' + self.scale_number + '_grads'
        self.h_scale_max = 'h_scale_' + self.scale_number + '_max'
        self.h_scale_max = 'h_scale_' + self.scale_number + '_zero'
        self.h_scale_max = 'h_scale_' + self.scale_number + '_tare'
        self.h_scale_style = 'h_scale_' + self.scale_number + '_style'
        self.h_scale_style = 'h_scale_' + self.scale_number + '_brewdate'
        self.h_scale_style = 'h_scale_' + self.scale_number + '_brewstyle'

        self.busy = False
        self.update_seconds = 0.1
        self.start_timers()

        print("Scale " + str(self.scale_number) + " created.")

    def is_busy(self):
        return self.busy

    def set_value(self, tagname, value):
        if (self.is_busy() == False):
            if (tagname == 'zero'):
                _send_command(100, int(value))
            elif (tagname == 'span'):
                _send_command(101, int(value))
            elif (tagname == 'tare'):
                _send_command(102, int(value))
            elif (tagname == self.h_scale_dec):
                _send_command(103, int(value))
            elif (tagname == self.h_scale_grads):
                _send_command(104, int(value))
            else:
                print('Command Write: Scale ' + str(self.scale_number) + tagname + ' command failed. Action not found.')
        else:
            print('Command Write: Scale ' + str(self.scale_number) + tagname + ' command failed. Busy.')

    def start_timers(self):
        self.read_scale_timer = TimerEvent(self.update_seconds, self._update_weight)
        self.read_scale_timer.start()

    def stop_timers(self):
        print('Stopping scale ' + self.scale_number + ' read event.')
        self.read_scale_timer.cancel()

    def _send_command(self, cmd, value):
        self.busy = True
        bytes_to_read = 1
        command = [pack('>B', cmd), pack('>I', value)]

        try:
            with SMBusWrapper(1) as bus:
                write = i2c_msg.write(self.address, command)
                    # Have to get rid of the last byte on...smbus2 messes with the last word, not am sure why.
                read = i2c_msg.read(self.address, bytes_to_read + 1)
                bus.i2c_rdwr(write, read)
                data = list(read)
                data.pop()
                data = bytes(data)
                result = unpack('>I', data)[0]
                if (result == 10):
                    print('Command Read: ' + str(cmd) + ' successful.')
                else:
                    print('Command Read: ' + str(cmd) + ' failed.')

        except:
            self.read_scale_timer.error()
            print('Command Read: Scale ' + str(self.scale_number) + ' command ' + str(cmd) + ' timed out.')

        self.busy = False

    def _get_command(self, cmd):
        self.busy = True
        bytes_to_read = 4
        command = pack('>B', cmd)

        try:
            with SMBusWrapper(1) as bus:
                write = i2c_msg.write(self.address, command)
                    # Have to get rid of the last on...smbus2 messes with the last word, not am sure why.
                read = i2c_msg.read(self.address, bytes_to_read + 1)
                bus.i2c_rdwr(write, read)
                data = list(read)
                data.pop()
                data = bytes(data)
                result = unpack('>I', data)[0]

        except:
            self.read_scale_timer.error()
            print('Command Read: Scale ' + str(self.scale_number) + ' command ' + str(cmd) + ' timed out.')
            result = False

        self.busy = False
        return result

    def _update_weight(self):
        data = self._get_command(10)
        if (data == False):
            pass

        else:
            if (data < 0):
                data = 0.0
                DataBase.set_value(self.h_tap_capacity, result)

            elif (result > 100000):
                print('Scale ' + self.scale_number + ' update out of bounding.')

            else:
                decimal = DataBase.get_value(self.h_scale_dec)
                result = '{0:.3f}'.format(result / pow(10, decimal))
                DataBase.set_value(self.h_scale_actual, result)

        if (self.read_scale_timer.get_status() == False):
            print('Scale ' + self.scale_number + ' has timed out, manually reconnect.')

    # def read_scale(self):
    #     self.busy = True
    #     address = 0x08
    #     command = pack('>B', 10)
    #     data = 0
    #     result = 0
    #
    #     try:
    #         with SMBusWrapper(1) as bus:
    #             write = i2c_msg.write(address, command)
    #             read = i2c_msg.read(address, 5)
    #             bus.i2c_rdwr(write, read)
    #             data = list(read)
    #             data.pop() # Have to get rid of the last on...smbus2 messes with the last word, not am sure why.
    #             data = bytes(data)
    #             result = unpack('>I', data)[0]
    #             if (result < 0):
    #                 result = 0.0
    #                 DataBase.set_value(self.h_tap_capacity, result)
    #             elif (result > 100000):
    #                 pass
    #             else:
    #                 result = '{0:.3f}'.format(result / 1000.0)
    #                 DataBase.set_value(self.h_tap_capacity, result)
    #             #print('Scale reading success.  ' + str(result))
    #
    #     except:
    #         pass
    #         # print('Scale reading Failed.')
    #
    #     self.busy = False
    #     # x = float(DataBase.get_value(self.h_tap_capacity))
    #     # x = x + 1
    #     # DataBase.set_value(self.h_tap_capacity, x)
