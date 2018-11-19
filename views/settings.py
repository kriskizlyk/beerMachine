import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase
from views.window import Window
from views.keyboard import Keyboard

import time
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWS_DIR = os.path.join(BASE_DIR, 'views')

class Settings(Window):
    def __init__(self):
        Window.__init__(self, 'settings', SettingsHandler())
        print("Creating Settings Window...")
        self.y = 'piss'
        # self.x = self.builder.get_object("date_time")
        # x.set_label(str("holy hell"))
        # DataBase.set_value("date_time", time.strftime("%H:%M"))

class SettingsHandler(Settings):
    def close(self, *args):
        pass
        # x = self.builder.get_object('settings')
        # x.destroy()
        # DataBase.settings_widgets['settings'].destroy()
    def set_label(self, *args):
        x = self.builder.get_object("time_test")
        x.set_label(str("holy hell"))
