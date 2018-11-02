import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from database.admin import DataBase
from views.keyboard import Keyboard

class OverviewHandler():
    def close(self, *args):
        Gtk.main_quit()

    def click(self, button):
        DataBase.set_value(self.h_tap_capacity, 1)

    def set_name(self, label, button):
        Keyboard(label)
