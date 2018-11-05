import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from views.admin import Window
from database.admin import DataBase
from hardware.scale import Scale
from hardware.temperature import TemperatureSensor

if __name__ == '__main__':

    win = Window()
    DataBase.create_tag_database()

    print('Starting Hardware Services...')
    scale_1 = Scale('1')
    #scale_2 = Scale('2')
    temp_sensor = TemperatureSensor()

    Gtk.main()

    # If the system is told to shut down but durring a read these
    # services may not shut off in between reads.  Should use a proper
    # scheduler to see if the hanlder is busy or not.
    
    print('Stopping Hardware Services...')
    
    while True:
        if (scale_1.is_busy() == False):
            scale_1.stop_timers()
            break

    #scale_2.stop_timers()
    
    while True:
        if (temp_sensor.is_busy() == False):
            temp_sensor.stop_timers()
            break
