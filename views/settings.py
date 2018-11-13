import os, gi
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase
from views.keyboard import Keyboard

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWS_DIR = os.path.join(BASE_DIR, 'views')

class SettingsHandler():
    def close(self, *args):
        DataBase.settings_widgets['settings'].destroy()

    def set_label(self, label, button):
        Keyboard(label)

class Settings(Gtk.Window, GObject.GObject):
    def __init__(self):
        window_name = 'settings'
        path = os.path.join(VIEWS_DIR, 'glade')
        gladefile = path + '/' + 'settings.glade'

        # Create a GTK Window Object
        builder = Gtk.Builder()

        # Link all the GTK objects to a glade file.
        builder.add_from_file(gladefile)

        # Create a database of all the glade widgets.
        DataBase.create_widget_database(builder.get_objects())

        # Link window to the windows handler
        builder.connect_signals(eval('SettingsHandler()'))

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

        window.show_all()

    def label_refresh(self):
        DataBase.refresh_tag_database()
        return True
