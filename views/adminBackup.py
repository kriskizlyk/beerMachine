import os, gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from database.admin import DataBase

from views.overview import OverviewHandler
# from views.settings import SettingsHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWS_DIR = os.path.join(BASE_DIR, 'views')

def create_window():
    new_window('overview')
    DataBase.create_tag_database()
    Gtk.main()

def new_window(window):

    window_name = window
    path = os.path.join(VIEWS_DIR, 'glade')
    # self.gladefile = self.path + '/' + self.window_name + '.glade'
    gladefile = path + '/' + 'overview.glade'

    # Create a GTK Window Object
    builder = Gtk.Builder()

    # Link all the GTK objects to a glade file.
    builder.add_from_file(gladefile)

    # Create a database of all the glade widgets.
    DataBase.create_widget_database(builder.get_objects())

    # Link window to the windows handler
    builder.connect_signals(eval('OverviewHandler()'))

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

    # self.button = self.builder.get_object("nav_button")
    # self.button.connect("clicked", NavigationHandler.nav_click)

    # def start_window():

# class GladeWindow:
#     '''
#     class GladeWindow(window_name as Str)
#     Creates a glade window with the assocated handlers.
#     '''
#
#     def create_window(self, window):
#         self.window_name = window
#         self.path = os.path.join(VIEWS_DIR, 'glade')
#         # self.gladefile = self.path + '/' + self.window_name + '.glade'
#         self.gladefile = self.path + '/' + 'overview.glade'
#
#         # Create a GTK Window Object
#         self.builder = Gtk.Builder()
#
#         # Link all the GTK objects to a glade file.
#         self.builder.add_from_file(self.gladefile)
#
#         # Link window to the windows handler
#         self.builder.connect_signals(eval(window.capitalize() + 'Handler()'))
#
#         # Get the GTKWindow ID from the glade file and show window.
#         self.window = self.builder.get_object(self.window_name)
#
#         self.window.show_all()
#
#         # self.button = self.builder.get_object("nav_button")
#         # self.button.connect("clicked", NavigationHandler.nav_click)
#
#     # def start_window():
