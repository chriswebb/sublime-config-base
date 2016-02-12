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


from .config import ConfigBaseWindowCommand, set_status

class UpdateWindowSettingsCommand(ConfigBaseWindowCommand):
    def description(self):
        return 'Updates the current window\'s settings based on the inputs.'
    def run(self, edit, *args, **kwargs):
        self.settings = dict(*args, **kwargs)
        set_status('Window configuration updated.')

class ClearWindowSettingsCommand(ConfigBaseWindowCommand):
    def description(self):
        return 'Clears any non-default values from the window settings.'
    def is_enabled(self):
        return self.settings.has_user_specified()
    def run(self, edit, *args, **kwargs):
        self.settings.clear()
        set_status('Window configuration cleared to defaults.')
        
class SaveWindowSettingsCommand(ConfigBaseWindowCommand):
    def description(self):
        return 'Saves the current window settings to the defaults.'
    def is_enabled(self):
        return self.settings.has_user_specified()
    def run(self, edit, *args, **kwargs):
        self.settings.save()
        set_status('Window configuration saved to defaults.')


class SetWindowSettingCommand(ConfigBaseWindowCommand):  
    def description(self):
        return 'Uses {"name": name, "value": value} to set the window setting. It prompts if either argument is missing.'
    
    def run(self, edit, *args, **kwargs): 
        self.__edit = edit
        self.kwargs = kwargs

        if 'name' not in self.kwargs:
            self.window.show_input_panel('Enter window configuration variable name:', '', self.__set_name, None, self.__cancelled)
        else:
            self.__set_name(self.kwargs['name'])

    def __cancelled(self):
        set_status('Window configuration variable setting cancelled.')

    def __set_user_specified(self, value):
        self.settings.set_user_specified(self.config_name, value)
        set_status('Window configuration variable \'' + self.config_name + '\' set.')

    def __set_name(self, name):
        self.config_name = name

        if 'value' not in self.kwargs:
            self.window.show_input_panel('Enter ' + self.config_name + ':', '', self.__set_user_specified, None, self.__cancelled)
        else:
            self.__set_user_specified(self.kwargs['value'])
            
            

class UnsetWindowSettingCommand(ConfigBaseWindowCommand):  
    def description(self):
        return 'Uses {"name": name} to unset the window setting. It prompts if the argument is missing.'
    
    def run(self, edit, *args, **kwargs): 
        if 'name' not in kwargs:
            self.window.show_input_panel('Enter window configuration variable name:', '', self.__set_name, None, self.__cancelled)
        else:
            self.__set_name(kwargs['name'])

    def __cancelled(self):
        set_status('Window configuration variable unsetting cancelled.')

    def __set_name(self, name):
        self.config_name = name
        self.settings.unset_user_specified(self.config_name)
        set_status('Window configuration variable \'' + self.config_name + '\' unset.')
