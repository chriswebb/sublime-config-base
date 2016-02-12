# sublime-config-base

## Description 

This repository is storage for a common configuration base that can be extended to new Sublime Text plug-ins.

See: [http://www.sublimetext.com/](http://www.sublimetext.com)

## Installation

Update the settings file name in the config.py file using the new plugin's details.

Extend either ConfigBaseWindowCommand or ConfigBaseTextCommand, and access the settings using self.settings.


## Usage

### Defaults

To setup defaults in the sublime-settings, simply prefix "default_" to any arguments used. 

### Initialization

Because the ConfigSettings is a MutableMapping, it can be initialized with a dictionary. For example:

```python

> settings = ConfigSettings(dict({"name": "value"}}))
> settings['name']
"value"

```

## References

### Classes

#### ConfigSettings : collections.MutableMapping

Stores the configuration settings.

##### Constructor

 - `ConfigSettings(window=None, *args, **kwargs)` 

        Creates a new configuration object.  If window is supplied, the configuration settings are stored for the window.

##### Static Methods 

 - `window_closed(sublime.Window)` : `None` 

        Removes the window's settings from the stored configuration settings.

##### Instance Methods


- `has_user_specified(String)` : `Boolean`

        Returns true if there is a user override defined for the given string.

- `save()` : `None`

        Saves the current ConfigSettings to the defaults.

- `clear()` : `None`

        Clears any non-default values from the ConfigSetting.

- `set_user_specified(String, String)` : `None`

        Sets the user supplied value matching the first parameter with the value in the second parameter.

- `unset_user_specified(String)` : `None`

        Removes the user specified value matching the first parameter.


#### ConfigBaseWindowCommand : sublime_plugin.WindowCommand

A base class used in-place for sublime_plugin.WindowCommand to add a quick reference to the settings object.

##### Properties

- `settings` : `ConfigSettings`

        Returns a ConfigSettings object for the current window.

#### ConfigBaseTextCommand : sublime_plugin.TextCommand

A base class used in-place for sublime_plugin.TextCommand to add a quick reference to the settings object.

##### Properties

- `settings` : `ConfigSettings`

        Returns a ConfigSettings object for the current window.

- `window` : `sublime.Window`

        Returns either the view's window or the active window, if the view does not return a window.

### Functions

 - `set_status(String)` : `None` 

        Calls set_timeout then status_message which is required for Sublime Text 2 plugins.

### Commands

- `update_window_settings` : `args` : `Settings`

        Updates the current window's settings based on the arguments.

- `save_window_settings` : 

        Saves the current window settings to the defaults.

- `clear_window_settings` : 

        Clears any non-default values from the window settings.

- `set_window_setting` : `args` : `{name, value}`

        Uses {"name": name, "value": value} to set the window setting. It prompts if either argument is missing.

- `unset_window_setting` : `args` : `{name}`

        Uses {"name": name} to unset the window setting. It prompts if the argument is missing.


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


## License

MIT License. See LICENSE file.
