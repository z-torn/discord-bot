![version](https://img.shields.io/badge/version-0.7-orange)
![python](https://img.shields.io/badge/python-3.6|3.7-blue)
![discord.py](https://img.shields.io/pypi/v/discord.py?label=discord.py)

# Basic Bot Template

This was mainly created for use with my [discord-bot-cli](https://github.com/stroupbslayen/discord-bot-cli) but it can be used on it's own as well. You'd only need to add a `config.yaml` file or rename the example one. I just wanted something that was pretty easy and helpful for new devs, albeit maybe bot quite so "basic". This is mainly just for a consistant bot template and simple organization/modularity. 

## Features
- Integration with the [Orator ORM](https://orator-orm.com/). Supports the most common SQL database drivers.
- Straight forward access to aiohttp through the bot with `bot.aiohhtp`. Usage would be something like `response = bot.aiohttp.get("https://www.google.com")`. This should be used instead of something like `requests` for working with the web.
- Straight forward access to the database with `bot.db`. Represents an `orator.DatabaseManager` instance for when you don't want to use the awesome Model representations that Orator has.
- Built in commands for bot owners to make debugging and logging easier.
- Auto loading extensions for discord.py. Cogs/Commands can be placed into the respective folders just to keep things organized but you can also create subfolders for keeping groups of Cogs/Commands together for less clutter.
- Support for Orator query logging. Add `log_queries: True` in your database settings to the `config.yaml` to enable it.
- Support for co-owners. These members are allowed to use the same commands as the ower.
- And probably some other things that I'm forgetting

### Reserved Bot Attributes
The core uses a revised `commands.Bot` class that prevents overwriting the helper attributes. Attempting to overwrite these will will raise an `AttributeError`.
- `bot.settings`
-  `bot.db`
- `bot.aiohttp`

## Built in Cogs/Commands
These can be enabled/disabled in the config file
### Bot_Logging:
* `toggle_log`: Toggle what the bot will log
    - `command`       : Log Commands used
    - `command_error` : Log Errors from Commands
    - `error`         : Log Errors
    - `level`         ': Set the logging level (Default Level: INFO)
    - `message`       : Log Messages
    - `message_edit`  : Log Edited Messages

### Bot_Settings
- `add_coowner`: Add a co-owner to your bot
- `change_description` : Change the description for the bot displayed in the help menu
- `coowners`: Check the co-owners of a bot
- `remove_coowner` : Remove a co-owner from your bot
- `set_prefix`: Change the prefix for using bot commands. This will overwrite all prefixes.
 - `toggle_help`: Toggle how the bot send the help menu in a pm
 - `toggle_traceback`: Toggle printing the traceback for debugging

 ### Bot_Utils
- `extensions`: Get a list of currently loaded and unloaded extensions. The names can be used for the load/unload/reload commands
- `load`    : Load an extension
- `reload`  : Reload an extension
- `shutdown`: Shutdown the bot
- `unload`  : Unload an extension
- `uptime`  : See how long the bot has been online

# [v0.7]
## Changelog
- Added `extensions` command to Bot_Settings. This will output the currently loaded extensions and other unloaded possible extensions in the extensions folder
- Revised/fixed the `load/unload/reload` commands. Use the name provided in the new `extensions` command as the arg
- Fixed the bot sending the Help menu in a DM
-  Re-added the `toggle_help` command to toggle sending the help menu in a DM or locally in the channel the command was went in
- Fixed log settings not being saved
- Added logging for db queries. SQL queries and query times will be logged to the console and the discord.log file. Can be enabled or disabled with the `log_queries` bool in the `config.yaml` file
- Added optional config setting specify what default utils to load. Will load all by default.
- Added optional config to set the default logging mode `logging_mode='w'`
- Added revised `commands.Bot` class to reserve basic bot attributes, otherwise it's the same as the default class.