import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase
from views.window import Window
from views.keyboard import Keyboard
from views.settings import Settings

# import threading
# import time

class Overview(Window):
    def __init__(self):
        print("Creating Overview Window...")
        Window.__init__(self, 'overview', OverviewHandler)

class OverviewHandler(Overview):
    def close(self, *args):
        # The following will always close the entire project.
        Gtk.main_quit()

    def click(self, *args):
        self.set_label(str("beaver"))

    def set_label(self, *args):
        Keyboard(self)

    def open_settings(self, *args):
        Settings()
