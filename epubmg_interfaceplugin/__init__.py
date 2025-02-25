__license__ = "GPL v3"
__copyright__ = "2024, 0x6f677548 (Hugo Batista)<Ox6f677548 at outlook dot com>"
# pylint: disable=import-error

# The class that all Interface Action plugin wrappers must inherit from
from calibre.customize import (
    InterfaceActionBase,
)


class InterfacePluginWrapper(InterfaceActionBase):
    """
    This class is a simple wrapper that provides information about the actual
    plugin class. The actual interface plugin class is called InterfacePlugin
    and is defined in the ui.py file, as specified in the actual_plugin field
    below.

    The reason for having two classes is that it allows the command line
    calibre utilities to run without needing to load the GUI libraries.
    """

    name = "Epub Metaguider GUI (intellireading.com)"
    description = "Adds a button to toolbar and context menu, to convert epub and kepub files to a metaguided format, improving your focus and reading speed (sometimes called bionic reading)."
    supported_platforms = ["windows", "osx", "linux"]
    author = "0x6f677548 (Hugo Batista)"
    version = (1, 1, 0)
    minimum_calibre_version = (6, 5, 0)

    #: This field defines the GUI plugin class that contains all the code
    #: that actually does something. Its format is module_path:class_name
    #: The specified class must be defined in the specified module.
    actual_plugin = "calibre_plugins.epubmginterface.action:InterfacePlugin"

    def is_customizable(self):
        """
        This method must return True to enable customization via
        Preferences->Plugins
        """
        return False
