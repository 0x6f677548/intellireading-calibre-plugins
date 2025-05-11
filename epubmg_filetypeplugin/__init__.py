import os

# pylint: disable=import-error

from calibre_plugins.epubmgfiletype import (
    common,
    metaguiding,
)
from calibre.customize import (
    FileTypePlugin,
)

__license__ = "GPL v3"
__copyright__ = "2025, Hugo Batista <intellireading at hugobatista.com>"
__docformat__ = "markdown en"


class MetaguidedEpubFileType(FileTypePlugin):
    """Plugin to convert epub files to metaguided epub files."""

    name = "Epub Metaguider post processor (intellireading.com)"
    description = "Works on post conversion/import and converts epub files to a metaguided format, improving your focus and reading speed (sometimes called bionic reading)."
    supported_platforms = ["windows", "osx", "linux"]
    author = "Hugo Batista"
    version = (1, 1, 0)
    file_types = set(["epub", "kepub"])
    minimum_calibre_version = (6, 5, 0)

    def __init__(self, *args, **kwargs):
        common.log.debug(f"Initializing {self.name} plugin")
        # point the metaguiding logger to the common logger
        metaguiding._logger = common.log

        # Load plugin settings
        from calibre_plugins.epubmgfiletype.config import prefs
        
        # Event settings control when the plugin runs
        self.on_postprocess = prefs['enable_on_postprocess']
        self.on_import = prefs['enable_on_import']
        
        # File type settings control which files get processed
        self.process_filetypes = {
            'epub': prefs['process_epub'],
            'kepub': prefs['process_kepub']
        }
        
        super().__init__(*args, **kwargs)

    def run(self, path_to_ebook):
        common.log.debug(f"Running {self.name} plugin")

        # Check if metaguiding is enabled for this file type
        file_ext = os.path.splitext(path_to_ebook)[1][1:].lower()  # Remove dot and convert to lowercase
        file_type = 'epub' if file_ext == 'epub' else 'kepub' if file_ext == 'kepub' else None
        
        if not file_type or file_type not in self.process_filetypes:
            common.log.error(f"Unsupported file type for {path_to_ebook}")
            return path_to_ebook
            
        # Check if this file type should be processed
        if not self.process_filetypes[file_type]:
            common.log.debug(f"Processing disabled for {file_type} files")
            return path_to_ebook

        # add " (metaguided)" to the output file name
        # TODO: it seems we need to create this file using temporaryfile # pylint: disable=fixme
        # (or something similar) to avoid conflicts
        _output_path = (
            os.path.splitext(path_to_ebook)[0]
            + " (metaguided)"
            + os.path.splitext(path_to_ebook)[1]
        )
        try:
            metaguiding.metaguide_epub_file(path_to_ebook, _output_path)
        except Exception as e:
            common.log.error(f"Error running {self.name} plugin: {e}")
            raise e
        return _output_path

    def is_customizable(self):
        """This method must return True to enable customization."""
        return True

    def config_widget(self):
        """Create a configuration widget for the plugin."""
        from calibre_plugins.epubmgfiletype.config_ui import ConfigWidget
        return ConfigWidget(self)

    def save_settings(self, config_widget):
        """Save the settings from the configuration widget."""
        config_widget.save_settings()
        # Reload settings
        from calibre_plugins.epubmgfiletype.config import prefs
        
        # Event settings control when the plugin runs
        self.on_postprocess = prefs['enable_on_postprocess']  
        self.on_import = prefs['enable_on_import']
        
        # File type settings control which files get processed
        self.process_filetypes = {
            'epub': prefs['process_epub'],
            'kepub': prefs['process_kepub']
        }
