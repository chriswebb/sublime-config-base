# The MIT License (MIT)

# Copyright (c) 2016 Chris Webb

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from sublime import save_settings, load_settings, status_message, active_window, set_timeout
from sublime_plugin import TextCommand, WindowCommand, EventListener
from collections import MutableMapping 
from abc import ABCMeta

def set_status(msg):
    set_timeout(lambda:status_message(msg))

class ConfigBaseTextCommand(TextCommand, metaclass=ABCMeta):  

    __settings = None
    __window = None
    @property
    def window(self):
        if self.__window is None:
            self.__window = self.view.window()
            if self.__window is None:
                self.__window = active_window()
        return self.__window

    @property
    def settings(self):
        if self.__settings is None:
            self.__settings = ConfigSettings(window=self.window)
        return self.__settings

    @settings.setter
    def function(self, *args, **kwargs):
        self.__settings.update(dict(*args, **kwargs))

class ConfigBaseWindowCommand(WindowCommand, metaclass=ABCMeta):  

    __settings = None
    @property
    def settings(self):
        if self.__settings is None:
            self.__settings = ConfigSettings(window=self.window)
        return self.__settings

    @settings.setter
    def function(self, *args, **kwargs):
        self.__settings.update(dict(*args, **kwargs))
        
        
class ConfigSettingsEventListener(EventListener):  
    def post_window_command(window, command_name, args):
        if command_name == 'close_window':
            ConfigSettings.window_closed(window)


class ConfigSettings(MutableMapping):
    __settings_name = 'My Plugin.sublime-settings'  # Name of the settings file for the current plugin.
    __settings = None
    __windows = {}

    def __new__(cls, window=None, *args, **kwargs):
        if window is not None:
            if window.id() not in cls.__windows:
                cls.__windows[window.id()] = MutableMapping.__new__(cls, *args, **kwargs)
            return cls.__windows[window.id()]
        return MutableMapping.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.__defaults = {}
        self.__userspecified = {}
        self.__reload()
        kwargs.pop('window', None)
        self.update(dict(*args, **kwargs))


    @classmethod
    def window_closed(self, window):
        if window.id() in self.__windows:
            del self.__windows[window.id()]

    @classmethod
    def __get_settings(cls):
        if cls.__settings is None:
            cls.__settings = load_settings(cls.__settings_name)
            cls.__settings.clear_on_change('reload')
            cls.__settings.add_on_change('reload', cls.__reload_all_windows)
        return cls.__settings

    @classmethod
    def __reload_all_windows(cls):
        for window in cls.__windows:
            cls.__windows[window].__reload()

    def __getitem__(self, name):
        return self.__get(self.__keytransform__(name))

    def __setitem__(self, name, value):
        self.__defaults[self.__keytransform__(name)] = value

    def __delitem__(self, name):
        del self.__defaults[self.__keytransform__(name)]

    def __iter__(self):
        return iter(self.__defaults)

    def __len__(self):
        return len(self.__defaults)

    def __contains__(self, name):
        if self.__keytransform__(name) in self.__defaults:
            return True
        else:
            value = self.__get_settings().get('default_'+name)
            if value:
                return True
        return False

    def __keytransform__(self, name):
        return name

    def __get(self, name):
        if self.__keytransform__(name) not in self.__defaults:
            value = self.__get_settings().get('default_'+name)
            if value:
                self.__defaults[self.__keytransform__(name)] = value
        return self.__defaults[self.__keytransform__(name)]

    def __reload(self):
        self.__defaults = self.__userspecified.copy()

    def save(self):
        updates = False
        for name in self.__userspecified:
            updates = True
            self.__get_settings().set('default_' + name, self.__userspecified[name])
        if updates:
            save_settings(self.__settings_name)
            self.clear()

    def clear(self):
        self.__userspecified = {}
        self.__reload()

    def has_user_specified(self):
        return len(self.__userspecified) > 0

    def set_user_specified(self, name, value):
        self.__userspecified[name] = value

    def unset_user_specified(self, name):
        if name in self.__userspecified:
            del self.__userspecified[name]
