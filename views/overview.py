import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase
from views.window import Window
from views.keyboard import Keyboard
from views.settings import Settings
import time

class Overview(Window):
    def __init__(self):
        Window.__init__(self, 'overview', OverviewHandler())
        print("Creating Overview Window...")
        x = self.builder.get_object("time_test")
        x.set_label(str("holy hell"))

class OverviewHandler():
    def close(self, *args):
        Gtk.main_quit()

    def click(self, *args):
        print("clicked")
        x = self.builder.get_object("time_test")
        # x.set_label(str("holy hell"))

    def set_name(self, *args):
        Keyboard(label)

    def open_settings(self, *args):
        Settings()
