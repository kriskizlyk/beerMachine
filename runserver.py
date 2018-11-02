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

    scale_1 = Scale('1')
    scale_2 = Scale('2')
    temp_sensor = TemperatureSensor()

    Gtk.main()

    scale_1.stop_timers()
    scale_2.stop_timers()
    temp_sensor.stop_timers()
