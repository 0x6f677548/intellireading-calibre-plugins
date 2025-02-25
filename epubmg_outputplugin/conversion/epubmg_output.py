"""Output processing for Metaguided Epub files."""

__license__ = "GPL v3"
__copyright__ = "2024, 0x6f677548 (Hugo Batista)<Ox6f677548 at outlook dot com>"
__docformat__ = "markdown en"

from typing import Any
from typing import Set
from typing import Tuple

# pylint: disable=import-error
from calibre.ebooks.conversion.plugins.epub_output import (
    EPUBOutput,
)

# pylint: disable=import-error
from calibre.customize.conversion import (
    OptionRecommendation,
)

from calibre_plugins.epubmgoutput import (  # pylint: disable=import-error # type: ignore
    common,
    metaguiding,
)


class MetaguidedEpubOutput(EPUBOutput):
    """Allows calibre to convert any known source format to a metaguided epub file."""

    # pylint:disable=undefined-variable

    name = "Epub Metaguider output format (intellireading.com)"
    description = "Adds additional options to Epub Output conversion, enabling epub files conversion to a metaguided format, improving your focus and reading speed (sometimes called bionic reading)."
    supported_platforms = ["windows", "osx", "linux"]
    author = "0x6f677548 (Hugo Batista)"
    version = (1, 1, 0)
    file_type = "epub"
    minimum_calibre_version = (6, 5, 0)
    on_postprocess = True  # Run this plugin after conversion is complete
    on_import = True  # Run this plugin on import
    commit_name = "epubmg_output"

    epubmg_options: Set[OptionRecommendation] = {
        OptionRecommendation(
            name="epubmg_enable_metaguiding",
            recommended_value=True,
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
    epubmg_recommendations: Set[Tuple[str, Any, int]] = {
        ("epub_version", "3", OptionRecommendation.LOW)
    }

    def __init__(self, *args, **kwargs):
        common.log.debug(f"Initalizing {self.name}")
        # point the metaguiding logger to the common logger
        metaguiding._logger = common.log

        common.log.debug(f"Adding options for plugin: {self.name}")
        self.options = self.options.union(self.epubmg_options)
        self.recommendations = self.recommendations.union(self.epubmg_recommendations)
        EPUBOutput.__init__(self, *args, **kwargs)

    def gui_configuration_widget(
        self, parent, get_option_by_name, get_option_help, db, book_id=None
    ):
        """Set up the plugin configuration widget."""
        _name = self.name.lower().replace(" ", "_")
        common.log.debug(f"Creating GUI configuration widget for {_name}")

        from calibre_plugins.epubmgoutput.conversion.output_config import (
            PluginWidget,
        )

        return PluginWidget(parent, get_option_by_name, get_option_help, db, book_id)

    def convert(
        self, oeb_book, output, input_plugin, opts, logger
    ):  # pylint: disable=unused-argument
        common.log.debug(
            f"Convert called on {self.name}. \
            Input Plugin: {input_plugin}. Output: {output}"
        )

        EPUBOutput.convert(self, oeb_book, output, input_plugin, opts, common.log)

        if opts.epubmg_enable_metaguiding:
            common.log.debug("Running epubmg conversion")
            try:
                metaguiding.metaguide_epub_file(output, output)
            except Exception as e:
                common.log.error(f"Error processing {self.name}: {e}")
                raise e

        common.log.debug(f"Convert finished on {self.name}")
        return
