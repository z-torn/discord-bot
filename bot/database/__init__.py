"The direcory where database related stuff should go"

from orator import DatabaseManager, Model
from bot import config

# Setup the database manager and model format for Orator
database = DatabaseManager(config.get("databases"))
bot.db = database
Model.set_connection_resolver(database)
