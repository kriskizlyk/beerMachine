from gi.repository import Gtk
from database.cache import Cache

class DataBase:
    local_data = {}

    tags = {} # Tag Database in RAM
    __tag_database = Cache('tags') # Tag Database object.

    glade_widgets = {} # Window Widgets in RAM
    keyboard_widgets = {}
    settings_widgets = {}

    def create_widget_database(builder):
        ''' Creates a RAM library of widgets for local access. '''
        for each_widget in builder:
            if (type(each_widget) == Gtk.Label):

                # Do not add the widget if it does not have a empty Widget Name
                if each_widget.get_name() != "GtkLabel":
                    DataBase.glade_widgets[str(each_widget.get_name())] = each_widget

    def create_widget_database2(builder):
        ''' Creates a RAM library of widgets for local access. '''
        for each_widget in builder:
            if (type(each_widget) == Gtk.Button or
                type(each_widget) == Gtk.Label or
                type(each_widget) == Gtk.Window):
                DataBase.keyboard_widgets[str(each_widget.get_name())] = each_widget

    def create_widget_database3(builder):
        ''' Creates a RAM library of widgets for local access. '''
        for each_widget in builder:
            if (type(each_widget) == Gtk.Button or
                type(each_widget) == Gtk.Label or
                type(each_widget) == Gtk.Window):
                DataBase.settings_widgets[str(each_widget.get_name())] = each_widget

    def create_tag_database():
        ''' Creates RAM dictonary of TAGS from Widgets on the glade screen. '''
        widget_type = ''
        for each_widget in (DataBase.glade_widgets):
            if type(DataBase.glade_widgets[each_widget]) == Gtk.Button:
                widget_type = 'button'
            elif type(DataBase.glade_widgets[each_widget]) == Gtk.Label:
                widget_type = 'label'
            else: pass

            DataBase.tags[each_widget] = {'value': '####', '__type': widget_type, '__redraw': False, '__read': 0, '__write': 0}

        ''' If the RAM widget DNE and not Local, remove it. '''
        file_data = DataBase.__tag_database.get_data()
        remove_keys = []
        for each_key in file_data.keys():
            if each_key not in DataBase.tags.keys() and widget_type != 'local':
                remove_keys.append(each_key)
        DataBase.__tag_database.remove(remove_keys)

        ''' From the RAM dictonary update values from file. '''
        DataBase.tags.update(DataBase.__tag_database.get_data())

    def set_local_value(tagname, value):
        try:
            DataBase.local_data[str(tagname)] = value
        except:
            # DataBase.local_data['keyboard_buffer'] = value
            print("DataBase.set_value(" + tagname + ") does not exist in the database.")

    def get_local_value(tagname):
        ''' Returns the value stored in RAM '''
        value = DataBase.local_data.get(tagname)
        if value is None:
            value = ''
        return value

    def set_value(tagname, value):
        ''' Sets the value stored in RAM '''
        # old_value = DataBase.get_value(tagname)
        try:
            DataBase.tags[str(tagname)]['value'] = value
        except:
            print("DataBase.set_value(" + tagname + ") does not exist in the database.")
        # print(tagname + ": " + old_value + " changed to: " + value)

    def get_value(tagname):
        ''' Returns the value stored in RAM '''
        try:
            value = DataBase.tags.get(tagname).get('value')
        except:
            print("DataBase.set_value(" + tagname + ") does not exist in the database.")
            value = '_invalid_'
        return value

    def refresh_tag_database():
        ''' Refreshes RAM database '''
        ''' Refresh all widgets at once, or only if the redraw says to?!?'''
        # print('DataBase refresh.')
        DataBase.__tag_database.refresh(DataBase.tags)

        ''' Reload all widgets values from RAM. '''
        DataBase.__update_glade_label_widgets()

    def __update_glade_label_widgets():
        ''' Label widgets are set to the RAM value. '''
        for each_tag in DataBase.tags:
            if DataBase.tags[each_tag]['__type'] == 'label':
                widget = DataBase.glade_widgets[each_tag]
                tag = DataBase.get_value(str(each_tag))
                widget.set_label(str(tag))

    def __str__(self):
        return tags
