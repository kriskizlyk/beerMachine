import os, gi
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWS_DIR = os.path.join(BASE_DIR, 'views')

class KeyboardHandler():
    def close(self, *args):
        DataBase.keyboard_widgets['window'].destroy()

    def push_enter(self, *args):
        DataBase.set_value(DataBase.get_local_value('keyboard_variable'),
            DataBase.get_local_value('keyboard_buffer'))
        DataBase.keyboard_widgets['window'].destroy()

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
        DataBase.keyboard_widgets['buffer'].set_label(DataBase.get_local_value('keyboard_buffer'))

        if letter == "space":
            print('space')
            DataBase.set_local_value('keyboard_shift_pointer', 1)

    def push_space(self, *args):
        value = DataBase.get_local_value('keyboard_buffer') + " "
        DataBase.set_local_value('keyboard_buffer', value)
        DataBase.set_local_value('keyboard_shift_pointer', 1)
        DataBase.keyboard_widgets['buffer'].set_label(DataBase.get_local_value('keyboard_buffer'))

    def push_clear(self, *args):
        DataBase.set_local_value('keyboard_buffer', "")
        DataBase.set_local_value('keyboard_shift_pointer', 1)
        DataBase.keyboard_widgets['buffer'].set_label(DataBase.get_local_value('keyboard_buffer'))

    def delete_letter(self, *args):
        value = DataBase.get_local_value('keyboard_buffer')
        if len(value) >= 1:
            value = value[:-1]
            DataBase.set_local_value('keyboard_buffer', value)
            print(DataBase.get_local_value('keyboard_buffer'))
            DataBase.keyboard_widgets['buffer'].set_label(DataBase.get_local_value('keyboard_buffer'))

class Keyboard(Gtk.Window, GObject.GObject):
    def __init__(self, tagname):
        window_name = 'keyboard'
        path = os.path.join(VIEWS_DIR, 'glade')
        gladefile = path + '/' + 'keyboard.glade'

        # Create a GTK Window Object
        builder = Gtk.Builder()

        # Link all the GTK objects to a glade file.
        builder.add_from_file(gladefile)

        # Create a database of all the glade widgets.
        DataBase.create_widget_database2(builder.get_objects())

        # Link window to the windows handler
        builder.connect_signals(KeyboardHandler)

        # Add css styling from my custom file.
        css = Gtk.CssProvider()
        css.load_from_path(VIEWS_DIR + '/glade/css/custom.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Get the GTKWindow ID from the glade file and show window.
        window = builder.get_object(window_name)

        # Create the local tags.
        DataBase.set_local_value('keyboard_buffer', DataBase.get_value(tagname.get_name()))
        DataBase.keyboard_widgets['buffer'].set_label(DataBase.get_local_value('keyboard_buffer'))
        DataBase.set_local_value('keyboard_shift_pointer', 1)
        DataBase.set_local_value('keyboard_variable', tagname.get_name())

        window.show_all()
