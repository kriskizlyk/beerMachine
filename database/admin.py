from gi.repository import Gtk
from database.cache import Cache

class DataBase:
    local_data = {}

    # Tag Database
    tags = {} # Tag Database in RAM
    __tag_database_object = Cache('tags') # Tag Database object.

    def __init__(self):
        print("DatabBase locally started.")
        DataBase.tags.update(DataBase.__tag_database_object.get_data())

    def create_tag(tagname, value):
        ''' Creates a new tag and adds it to the RAM database. '''
        DataBase.tags[str(tagname)] = (
            {'value': value,
            '_redraw': False,
            '_read': 0,
            '_write': 0})

        print("DataBase.create_tag (" + tagname + ") added to database.")

    def create_tag_database(widgets, scope):
        ''' Creates RAM dictonary of TAGS from Window Widgets on creation. '''
        ''' Removes and saves tags NOT found in the database.'''
        ''' Updates the found tags from the database.'''

        widget_type = ''
        loaded_data = DataBase.__tag_database_object.get_data()

        for each_widget in widgets:
            if type(each_widget) == Gtk.Button:
                widget_type = 'button'
            elif type(each_widget) == Gtk.Label:
                widget_type = 'label'
            else: pass

            '''Only adds tags that start with a 'h_' to denote HMI tag.'''
            if (each_widget.get_name()[0:2] == 'h_'):

                ''' Only add the tags that are NOT recognized. '''
                if (each_widget.get_name() not in loaded_data):
                    DataBase.create_tag(each_widget.get_name(), '####')

        DataBase.__tag_database_object.refresh(DataBase.tags)

        # for each_key in DataBase.tags:
        #     print(each_key + '     ' + str(DataBase.get_value(each_key)))

        ''' If the RAM widget DNE and not Local, remove it. The following Code
        will check for duplicate keys in the saved database and if it is not
        in the created tag database from widget names it will auto remove and save
        the database'''
        # file_data = DataBase.__tag_database_object.get_data()
        # remove_keys = []
        # for each_key in file_data.keys():
        #     if each_key not in DataBase.tags.keys() and widget_type != 'local':
        #         remove_keys.append(each_key)
        # DataBase.__tag_database_object.remove(remove_keys)

        ''' If the tag does not exist in the DataBase but is on the window then
        add it to the database.'''
        # file_data = DataBase.__tag_database_object.get_data()
        # add_keys = {}
        # for each_key in DataBase.tags.keys():
        #     if each_key not in file_data.keys():
        #         add_keys[each_key] = DataBase.tags[each_key]
        #         print("New tag " + str(each_key) + " found.  Added to database.")

        ''' Update the local RAM tag database from the saved database. '''
        # DataBase.tags.update(DataBase.__tag_database_object.get_data())

        ''' Update file data. '''
        # DataBase.__tag_database_object.refresh(DataBase.tags)

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
            DataBase.create_tag(tagname, value)
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
        # print('DataBase refresh.')
        DataBase.__tag_database_object.refresh(DataBase.tags)

    def __str__(self):
        return tags
