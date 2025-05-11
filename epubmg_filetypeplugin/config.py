"""
Configuration for the Epub Metaguider post processor plugin.
"""

__license__ = "GPL v3"
__copyright__ = "2025, Hugo Batista <intellireading at hugobatista.com>"
__docformat__ = "markdown en"

# pylint: disable=import-error
from calibre.utils.config import JSONConfig

prefs = JSONConfig('plugins/epubmg_filetype')

# Event settings - when the plugin should run
prefs.defaults['enable_on_postprocess'] = False
prefs.defaults['enable_on_import'] = False

# File type settings - which files to process
prefs.defaults['process_epub'] = True
prefs.defaults['process_kepub'] = True
