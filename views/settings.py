import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase
from views.window import Window
from views.keyboard import Keyboard

# import threading
# import time

class Settings(Window):
    def __init__(self):
        print("Creating Settings Window...")
        Window.__init__(self, 'settings', SettingsHandler)

class SettingsHandler(Settings):
    def destroy(self, *args):
        print("Closing Settings Window...")
        self.destroy()

    def close(self, *args):
        # The following will only destroy the current window.
        # The glade object must pass the window as User data to destroy.
        self.destroy()

    def set_label(self, *args):
        Keyboard(self)
