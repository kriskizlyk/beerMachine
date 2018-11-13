class Window():
    def __init__(self, window_name):
        self.window = window_name
        self.test = 'hello'

    def name(self):
        return self.window

    def lmo(self):
        self.test = 'beaver'

class Overview(Window):
    def __init__(self, window_name):
        Window.__init__(self, window_name)

    def get_name(self):
        return self.name()

x = Overview('settings')
print(x.get_name())
print(x.test)
