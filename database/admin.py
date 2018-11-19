from gi.repository import Gtk
from database.cache import Cache

class DataBase:
    local_data = {}

    tags = {} # Tag Database in RAM
    __tag_database = Cache('tags') # Tag Database object.

    def create_tag_database(widgets, scope):
        ''' Creates RAM dictonary of TAGS from Window Widgets on creation. '''
        ''' Removes and saves tags NOT found in the database.'''
        ''' Updates the found tags from the database.'''
        widget_type = ''
        for each_widget in widgets:
            if type(each_widget) == Gtk.Button:
                widget_type = 'button'
            elif type(each_widget) == Gtk.Label:
                widget_type = 'label'
            else: pass

            '''Only adds tags that start with a 'h' to denote HMI tag.'''
            if (each_widget.get_name()[0] == "h"):
                DataBase.tags[each_widget.get_name()] = (
                    {'value': '####',
                    '_scope': scope,
                    '_type': widget_type,
                    '_redraw': False,
                    '_read': 0,
                    '_write': 0
                })

        # for each_key in DataBase.tags:
        #     print(each_key)

        ''' If the RAM widget DNE and not Local, remove it. The following Code
        will check for duplicate keys in the saved database and if it is not
        in the created tag database from widget names it will auto remove and save
        the database'''
        file_data = DataBase.__tag_database.get_data()
        remove_keys = []
        for each_key in file_data.keys():
            if each_key not in DataBase.tags.keys() and widget_type != 'local':
                remove_keys.append(each_key)
        DataBase.__tag_database.remove(remove_keys)


        ''' If the tag does not exist in the DataBase but is on the window then
        add it to the database.'''
        file_data = DataBase.__tag_database.get_data()
        add_keys = {}
        for each_key in DataBase.tags.keys():
            if each_key not in file_data.keys():
                add_keys[each_key] = DataBase.tags[each_key]
                print("New tag " + str(each_key) + " found.  Added to database.")
        DataBase.__tag_database.refresh(DataBase.tags)

        '''Update the local RAM tag database from the saved database. '''
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
            if DataBase.tags[each_tag]['_type'] == 'label':
                widget = DataBase.glade_widgets[each_tag]
                tag = DataBase.get_value(str(each_tag))
                widget.set_label(str(tag))

    def __str__(self):
        return tags
