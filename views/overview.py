import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase
from views.window import Window
from views.keyboard import Keyboard
from views.settings import Settings

class OverviewHandler():
    def close(self, *args):
        Gtk.main_quit()

    def click(self, *args):
        print("clicked")
        # DataBase.set_value(self.h_tap_capacity, 1)

    def set_name(self, label, button):
        Keyboard(label)

    def open_settings(self, label, button):
        Settings()

class Overview(Window):
    def __init__(self):
        Window.__init__(self, 'overview', OverviewHandler())
        print("Creating Overview Window...")
