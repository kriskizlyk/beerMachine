import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase
from views.window import Window

# import threading
# import time

class Keyboard(Window):
    buffer_label = 0

    def __init__(self, tagname):
        print("Creating Keyboard Window...")
        Window.__init__(self, 'keyboard', KeyboardHandler)

        # Create a global variable...not sure handlers can't inherit builder.
        global buffer_label
        buffer_label = self.builder.get_object('l_buffer')

        # Create the local buffer but, leave it blank.
        DataBase.set_local_value('keyboard_buffer', '')

        # Set the label to show the current tag value.
        buffer_label.set_label(DataBase.get_value(tagname.get_name()))

        DataBase.set_local_value('keyboard_shift_pointer', 1)
        DataBase.set_local_value('keyboard_variable', tagname.get_name())

class KeyboardHandler(Keyboard):
    def close(self, *args):
        # The following will only destroy the current window.
        # The glade object must pass the window as User data to destroy.
        print("Closing Keyboard Window...")
        self.destroy()

    def push_enter(self, *args):
        DataBase.set_value(DataBase.get_local_value('keyboard_variable'),
            DataBase.get_local_value('keyboard_buffer'))
        # Have to find a way to auto close the window.

    def enable_shift(self, *args):
        DataBase.set_local_value('keyboard_shift_pointer', 1)

    def push_letter(self, *args):
        letter = str(self.get_name())

        if letter == "apostorphe":
            letter = "'"
        elif letter == "period":
            letter = "."

        if (DataBase.get_local_value('keyboard_shift_pointer')) == 1:
            letter = letter.capitalize()
            DataBase.set_local_value('keyboard_shift_pointer', 0)
        value = DataBase.get_local_value('keyboard_buffer') + letter
        DataBase.set_local_value('keyboard_buffer', value)

        if letter == "space":
            print('space')
            DataBase.set_local_value('keyboard_shift_pointer', 1)
        buffer_label.set_label(DataBase.get_local_value('keyboard_buffer'))

    def push_space(self, *args):
        value = DataBase.get_local_value('keyboard_buffer') + " "
        DataBase.set_local_value('keyboard_buffer', value)
        DataBase.set_local_value('keyboard_shift_pointer', 1)
        buffer_label.set_label(DataBase.get_local_value('keyboard_buffer'))

    def push_clear(self, *args):
        DataBase.set_local_value('keyboard_buffer', "")
        DataBase.set_local_value('keyboard_shift_pointer', 1)
        buffer_label.set_label(DataBase.get_local_value('keyboard_buffer'))

    def delete_letter(self, *args):
        value = DataBase.get_local_value('keyboard_buffer')
        if len(value) >= 1:
            value = value[:-1]
            DataBase.set_local_value('keyboard_buffer', value)
        buffer_label.set_label(DataBase.get_local_value('keyboard_buffer'))
