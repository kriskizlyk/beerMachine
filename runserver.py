import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from views.admin import Window
from database.admin import DataBase
from hardware.scale import Scale
from hardware.temperature import TemperatureSensor
from hardware.doorswitch import DoorSwitch

if __name__ == '__main__':

    win = Window()
    DataBase.create_tag_database()

    print('Starting Hardware Services...')

    scale_co2 = Scale('co2', 0x08)
    scale_1 = Scale('1', 0x09)
    temp_sensor = TemperatureSensor()
    door_switch = DoorSwitch(5, 'i')

    Gtk.main()

    # If the system is told to shut down but durring a read these
    # services may not shut off in between reads.  Should use a proper
    # scheduler to see if the hanlder is busy or not.

    print('Stopping Hardware Services...')

    while True:
        if (door_switch.is_busy() == False):
            door_switch.stop_timers()
            break

    while True:
        if (scale_co2.is_busy() == False):
            scale_co2.stop_timers()
            break

    while True:
        if (scale_1.is_busy() == False):
            scale_1.stop_timers()
            break

    while True:
        if (temp_sensor.is_busy() == False):
            temp_sensor.stop_timers()
            break
