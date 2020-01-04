"The direcory where database related stuff should go"

from orator import DatabaseManager, Model
from bot import bot_instance

# Setup the Model reference for Orator
Model.set_connection_resolver(bot_instance.db)
