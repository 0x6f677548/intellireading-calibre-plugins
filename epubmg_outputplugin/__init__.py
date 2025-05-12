"""Init epubmg output plugin."""

from typing import Any
from typing import Set
from typing import Tuple

# pylint: disable=import-error
from calibre.ebooks.conversion.plugins.epub_output import EPUBOutput
from calibre.customize.conversion import OptionRecommendation

from calibre_plugins.epubmgoutput import (  # pylint: disable=import-error # type: ignore
    common,
    metaguiding,
    __about_cli__
)

__license__ = "GPL v3"
__copyright__ = "2025, Hugo Batista <intellireading at hugobatista.com>"
__docformat__ = "markdown en"


class MetaguidedEpubOutput(EPUBOutput):
    """Allows calibre to convert any known source format to a metaguided epub file."""

    name = "Epub Metaguider output format (intellireading.com)"
    description = (
        "Adds additional options to Epub Output conversion, enabling epub files conversion to a metaguided format, improving your focus and reading speed (sometimes called bionic reading)."
        " This plugin is for ADVANCED users only. It is not recommended for beginners. If you are new to metaguiding, please use the '" \
        + common.GUI_PLUGIN_NAME + "' plugin instead." \
        " Intellireading CLI version: " + __about_cli__.__version__ + "."
    )

    supported_platforms = ["windows", "osx", "linux"]
    author = "Hugo Batista"
    version = (2, 0, 0)
    file_type = "epub"
    minimum_calibre_version = (6, 5, 0)
    on_postprocess = True
    # Run this plugin after conversion is complete
    on_import = False  # Run this plugin on import
    commit_name = "epubmg_output"

    epubmg_options: Set[OptionRecommendation] = {
        OptionRecommendation(
            name="epubmg_enable_metaguiding",
            recommended_value=False,
            help=" ".join(
                [
                    _("Select this to enable text metaguiding."),  # type: ignore # noqa
                    _(  # type: ignore # noqa
                        "This will convert your epub to a metaguided format (better focus and fast reading)"
                    ),
                ]
            ),
        ),
    }
    epubmg_recommendations: Set[Tuple[str, Any, int]] = {("epub_version", "3", OptionRecommendation.LOW)}

    def __init__(self, *args, **kwargs):
        common.log.debug(f"Initalizing {self.name}")
        # point the metaguiding logger to the common logger
        metaguiding._logger = common.log

        common.log.debug(f"Adding options for plugin: {self.name}")
        self.options = self.options.union(self.epubmg_options)
        self.recommendations = self.recommendations.union(self.epubmg_recommendations)
        EPUBOutput.__init__(self, *args, **kwargs)

    def gui_configuration_widget(self, parent, get_option_by_name, get_option_help, db, book_id=None):
        """Set up the plugin configuration widget."""
        _name = self.name.lower().replace(" ", "_")
        common.log.debug(f"Creating GUI configuration widget for {_name}")

        from calibre_plugins.epubmgoutput.config_ui import PluginWidget

        return PluginWidget(parent, get_option_by_name, get_option_help, db, book_id)

    def convert(self, oeb_book, output, input_plugin, opts, logger):  # pylint: disable=unused-argument
        common.log.debug(
            f"Convert called on {self.name}. \
            Input Plugin: {input_plugin}. Output: {output}"
        )

        EPUBOutput.convert(self, oeb_book, output, input_plugin, opts, common.log)

        if opts.epubmg_enable_metaguiding:
            common.log.debug("Running epubmg conversion")
