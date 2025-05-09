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
    file_types = set(["epub"])
    minimum_calibre_version = (6, 5, 0)
    on_postprocess = True  # Run this plugin after conversion is complete
    on_import = True  # Run this plugin on import

    def __init__(self, *args, **kwargs):
        common.log.debug(f"Initializing {self.name} plugin")
        # point the metaguiding logger to the common logger
        metaguiding._logger = common.log

        # this is where additional plugin settings should be applied.
        # example:
        # common.log.debug("Applying settings for plugin: %s" % self.name)
        # from calibre_plugins.epubmgfiletype.config import (
        #    prefs,
        # )
        # self.some_setting = prefs['some_setting']
        super().__init__(*args, **kwargs)

    def run(self, path_to_ebook):
        common.log.debug(f"Running {self.name} plugin")

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
        return False
