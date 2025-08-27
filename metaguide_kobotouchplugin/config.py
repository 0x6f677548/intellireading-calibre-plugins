"""
Configuration for the KoboTouch Metaguide driver plugin.
"""

__license__ = "GPL v3"
__copyright__ = "2025, Hugo Batista <intellireading at hugobatista.com>"

from calibre.utils.config import JSONConfig

# This is where all preferences for this plugin will be stored
# Remember that this name (metaguidekobotouch) must be unique
# as calibre creates global config files using it
prefs = JSONConfig("plugins/metaguidekobotouch")

# Set defaults
prefs.defaults["show_welcome_message"] = True  # whether to show the welcome message on first run
prefs.defaults["kepubify"] = True  # whether to convert EPUBs to KEPUBs before metaguiding
