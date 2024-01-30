"""Configuration for exporting epubmg files."""

__license__ = "GPL v3"
__copyright__ = "2024, 0x6f677548 (Hugo Batista)<Ox6f677548 at outlook dot com>"
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

        from PyQt5 import QtWidgets  # pylint: disable=import-error # type: ignore
        from PyQt5 import QtCore  # pylint: disable=import-error # type: ignore

        _rows = self.gridLayout.rowCount() - 1

        spacer = self.gridLayout.itemAtPosition(_rows, 0)
        self.gridLayout.removeItem(spacer)

        self.opt_additional_conversion_options = QtWidgets.QLabel(
            _("Additional Conversion options") + ":"  # type: ignore # noqa
        )
        self.gridLayout.addWidget(
            self.opt_additional_conversion_options, _rows, 0, 1, 1
        )

        # epubmg_enable_metaguiding
        self.opt_epubmg_enable_metaguiding = QtWidgets.QCheckBox(Form)
        self.opt_epubmg_enable_metaguiding.setObjectName(
            "opt_epubmg_enable_metaguiding"
        )
        self.opt_epubmg_enable_metaguiding.setText(
            _("Enable metaguiding")  # type: ignore # noqa
        )
        self.gridLayout.addWidget(self.opt_epubmg_enable_metaguiding, _rows, 1, 1, 1)

        _rows += 1

        self.gridLayout.addItem(spacer, _rows, 0, 1, 1)

        # Copy from calibre.gui2.convert.epub_output_ui.Ui_Form to make the
        # new additions work
        QtCore.QMetaObject.connectSlotsByName(Form)


class OutputOptions(BaseOutputOptions):
    """This allows adding our options to the output process."""

    def __init__(self, *args, **kwargs):
        """Initialize the output options."""
        print("epubmg: OutputOptions.__init__")
        super(OutputOptions, self).__init__(*args, **kwargs)

    def load_conversion_widgets(self):
        """Add our configuration to the output process."""
        # pylint:disable=access-member-before-definition
        # pylint:disable=attribute-defined-outside-init
        print("epubmg: OutputOptions.load_conversion_widgets")
        super(OutputOptions, self).load_conversion_widgets()
        self.conversion_widgets.append(PluginWidget)
        self.conversion_widgets = sorted(self.conversion_widgets, key=lambda x: x.TITLE)
