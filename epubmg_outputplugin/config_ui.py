"""Configuration for exporting epubmg files."""

__license__ = "GPL v3"
__copyright__ = "2025, Hugo Batista <intellireading at hugobatista.com>"
__docformat__ = "markdown en"

# pylint: disable=import-error
from calibre.ebooks.conversion.config import OPTIONS
from calibre.gui2.convert import Widget
from calibre.gui2.convert.epub_output import PluginWidget as EPUBPluginWidget
from calibre.gui2.convert.epub_output_ui import Ui_Form as EPUBUIForm
from calibre.gui2.preferences.conversion import OutputOptions as BaseOutputOptions

from calibre_plugins.epubmgoutput import common


class PluginWidget(EPUBPluginWidget, EPUBUIForm):
    """The plugin configuration widget for a epubmg output plugin."""

    # pylint:disable=undefined-variable
    TITLE = "Epub Output (metaguided)"
    HELP = _("Options specific to Epub output (metaguided)")  # type: ignore # noqa
    COMMIT_NAME = "epubmg_output"

    # A near copy of calibre.gui2.convert.epub_output.PluginWidget#__init__
    # If something seems wrong, start by checking for changes there.
    # We copy that instead of calling super().__init__() because the super __init__
    # calls Widget.__init__() with ePub options and there's no easy way to add and link
    # new UI elements once that's been done.
    def __init__(self, parent, get_option, get_help, db=None, book_id=None):
        """Initialize the epubmg output configuration widget."""
        common.log.debug("Initalizing epubmg output plugin widget")

        Widget.__init__(
            self,
            parent,
            OPTIONS["output"].get("epub", tuple()) + ("epubmg_enable_metaguiding",),
        )
        self.opt_no_svg_cover.toggle()
        self.opt_no_svg_cover.toggle()
        _ev = get_option("epub_version")
        self.opt_epub_version.addItems(list(_ev.option.choices))
        self.db, self.book_id = db, book_id
        self.initialize_options(get_option, get_help, db, book_id)

    def setupUi(self, Form):  # noqa: N802, N803
        """Set up the plugin widget UI."""
        # pylint:disable=undefined-variable
        # pylint:disable=attribute-defined-outside-init
        common.log.debug("Setting up epubmg output plugin widget")
        super(PluginWidget, self).setupUi(Form)
