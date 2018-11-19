""""Title:      Cache Module
    Author:     Kris Kizlyk
    Date:       20170922
    Purpose:    The match module handles creating, checking and storing a cache file.
"""

import os
import json

class Cache:
    def __init__(self, filename):
        self.file_name = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/database/' + filename + '.json'
        self.data = self.__load_cache()

    def get_data(self):
        self.data = self.__load_cache()
        return self.data

    def refresh(self, ram_data):
        ''' RAM ---> DATA, DATA --> FILE. '''

        from_file = self.get_data()
        if not from_file:
            from_file = {}
        from_file.update(ram_data) # Update the FILE data with RAM data.
        self.__save(from_file) # Save the FILE data.

    def remove(self, list):
        ''' No checks, removes if it is in the list. '''
        from_file = self.__load_cache()
        for each_element in list:
            if each_element in from_file.keys():
                print("Removing ''" + each_element + "'' from database, not found.")
                from_file.pop(str(each_element))
        self.__save(from_file)

    def __save(self, data):
        try:
            with open(self.file_name, 'w') as f:
                json.dump(data, f, indent=1, sort_keys=True)
        except IOError:
            pass

    def __load_cache(self):
        if os.path.isfile(self.file_name):
            try:
                with open(self.file_name) as json_file:
                    # Need to find a way that if the file exists but is empty, the program will crash.
                    return json.load(json_file)

            except IOError:
                print("File does not exist.  Error loading " + self.file_name + ".")
                return {}

        #  The file does not exist, create a new default file.
        else:
            with open(self.file_name, 'w') as f:
                json.dump({}, f, indent=1, sort_keys=True)
            return {}
