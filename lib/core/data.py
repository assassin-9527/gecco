from lib.core.datatype import AttribDict
from lib.core.log import LOGGER

# logger
logger = LOGGER

# object to share within function and classes command
# line options and settings
conf = AttribDict()

# Dictionary storing
kb = AttribDict()

# object to store original command line options
cmd_line_options = AttribDict()

# object to store merged options (command line, configuration file and default options)
merged_options = AttribDict()

# gecco paths
paths = AttribDict()
