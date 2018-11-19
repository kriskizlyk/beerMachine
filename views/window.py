import os, gi
import time
import threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWS_DIR = os.path.join(BASE_DIR, 'views')

class Window(Gtk.Window, GObject.GObject):
    def __init__(self, name, handler):
        self.window_name = str(name)
        path = os.path.join(VIEWS_DIR, 'glade')
        gladefile = path + '/' + self.window_name + '.glade'

        # Create a GTK Window Object
        self.builder = Gtk.Builder()

        # Link all the GTK objects to a glade file.
        self.builder.add_from_file(gladefile)

        # Add tags from the current window to the RAM database
        DataBase.create_tag_database(self.builder.get_objects(), self.window_name)

        # Link window to the windows handler.  Requires a function name only.
        # Note that the handler is not fucntion call!
        self.builder.connect_signals(handler)

        # Add css styling from my custom file.
        css = Gtk.CssProvider()
        css.load_from_path(VIEWS_DIR + '/glade/css/custom.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Get the GTKWindow ID from the glade file and show window.
        self.window = self.builder.get_object(self.window_name)

        # Immediatly updates all the labels from the Tag Database.
        self.update_widget_label()

        # Add a Label Update using the built in GObject Thread.
        GObject.timeout_add(1000, self.update_widget_label)

        # Show the window.make
        self.window.show_all()

    def update_widget_label(self):
        ''' Function takes the RAM database and push it out to file.'''
        ''' All label widgets are updated on the screen. '''

        # Get the process time it takes to update the tags.
        self.start_time = time.clock()

        # Send all current tags to database to be saved.
        DataBase.refresh_tag_database()

        # Update all Widget Labels on the HMI.
        for each_tag in DataBase.tags:
            try:
                widget = self.builder.get_object(each_tag)
                tag = DataBase.get_value(str(each_tag))
                widget.set_label(str(tag))
            except:
                # pass
                print(each_tag + str(" not found durring window refresh."))

        # print(self.window_name + " Tags updated: {:.3f} ms.".format((time.clock() - self.start_time)*1000))
        return True
