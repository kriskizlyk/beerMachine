import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from views.admin import RunViewServer
from database.admin import DataBase
from hardware.admin import Hardware

if __name__ == '__main__':
    hardware = Hardware()
    RunViewServer()
    hardware.stop_services()
