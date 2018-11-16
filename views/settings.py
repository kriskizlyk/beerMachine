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

class SettingsHandler():
    def close(self, *args):
        DataBase.settings_widgets['settings'].destroy()

    def set_label(self, label, button):
        Keyboard(label)

class Settings(Window):
    def __init__(self):
        Window.__init__(self, 'settings', SettingsHandler())
        print("Creating Settings Window...")

        # Add a Label Update using the built in GObject Thread.
        GObject.timeout_add(100, self.label_refresh)

    def label_refresh(self):
        DataBase.set_value("date_time", time.strftime("%H:%M"))
        DataBase.refresh_tag_database()
        return True
