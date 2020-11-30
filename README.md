![version](https://img.shields.io/badge/version-0.8-orange)
![python](https://img.shields.io/badge/python-3.6+-blue)
![discord.py](https://img.shields.io/pypi/v/discord.py?label=discord.py)

# Basic Bot Template

This was mainly created for use with my [discord-bot-cli](https://github.com/stroupbslayen/discord-bot-cli) but it can be used on it's own as well. You'd only need to add a `config.json` file or rename the example one. I just wanted something that was pretty easy and helpful for new devs, albeit maybe bot quite so "basic". This is mainly just for a consistant bot template and simple organization/modularity. 

## Features
- Built in commands for bot owners to make debugging and logging easier.
- Auto loading extensions for discord.py. Cogs/Commands can be placed into the respective folders just to keep things organized but you can also create subfolders for keeping groups of Cogs/Commands together for less clutter.
- Support for co-owners. (Not discord official co-owners) These members are allowed to use the same commands as the ower.
- And probably some other things that I'm forgetting

### Reserved Bot Attributes
The core uses a revised `commands.Bot` class that prevents overwriting the helper attributes. Attempting to overwrite these will raise an `AttributeError`.
- `bot.config`

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

# [v0.8]
## Changelog
- Simplified a bit
- Removed clutter and unnecessary requirements
- Added support for the new [Discord Gateway Intents](https://discordpy.readthedocs.io/en/latest/intents.html?highlight=gateway%20intents). These can be set in the `INTENTS` field in the `config.json` file. If this is empyt it'll use `Intents.default()`
- Added support for custome "reserved" attributes. These are attributes you'd like to prevent being overwritten in your bot. Just like with `bot.config`, these attributes can be modified, but not re-assigned.
- You can select what built-in utils cogs to load in the `config` file as well. All of them will be loaded by default.