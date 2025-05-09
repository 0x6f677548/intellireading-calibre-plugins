__license__ = "GPL v3"
__copyright__ = "2025, Hugo Batista <intellireading at hugobatista.com>"

# pylint: disable=import-error
# pylint: disable=undefined-variable
try:
    from qt.core import QToolButton, QMenu
except ImportError:
    from PyQt5.Qt import QToolButton, QMenu
from calibre.gui2 import question_dialog


# The class that all interface action plugins must inherit from
from calibre.gui2.actions import (
    InterfaceAction,
)
from calibre_plugins.epubmginterface import (
    common,
    metaguiding,
)


class InterfacePlugin(InterfaceAction):
    """Interface plugin for metaguiding epubs"""

    name = "Intellireading Interface Plugin"

    # Declare the main action associated with this plugin
    # The keyboard shortcut can be None if you dont want to use a keyboard
    # shortcut. Remember that currently calibre has no central management for
    # keyboard shortcuts, so try to use an unusual/unused shortcut.
    # action_spec = ('Intellireading Interface Plugin', None,
    #        'Run the Intellireading Interface Plugin', 'Shift+M')

    # Create our top-level menu/toolbar action (text, icon_path, tooltip, keyboard shortcut)
    action_spec = (
        _("Metaguide"),  # type: ignore # noqa
        None,
        _("Generate a metaguided epub"),  # type: ignore # noqa
        "Shift+M",
    )
    action_type = "current"
    popup_type = QToolButton.MenuButtonPopup
    dont_add_to = frozenset([])  # type: ignore
    dont_remove_from = frozenset([])  # type: ignore

    def genesis(self):
        # This method is called once per plugin, do initial setup here

        # Set the icon for this interface action
        # The get_icons function is a builtin function defined for all your
        # plugin code. It loads icons from the plugin zip file. It returns
        # QIcon objects, if you want the actual data, use the analogous
        # get_resources builtin function.
        #
        # Note that if you are loading more than one icon, for performance, you
        # should pass a list of names to get_icons. In this case, get_icons
        # will return a dictionary mapping names to QIcons. Names that
        # are not found in the zip file will result in null QIcons.
        _icon = get_icons("images/icon.png", "Metaguide")  # type: ignore # noqa

        # The qaction is automatically created from the action_spec defined
        # above
        # self.is_library_selected = True
        self.qaction.setIcon(_icon)

        # Create the menu
        self.menu = self.qaction.menu()
        if self.menu is None:
            self.menu = QMenu()
            self.qaction.setMenu(self.menu)

        # Add default action
        self.qaction.triggered.connect(self.metaguide_epub_selection)

        # Add epub action to menu
        epub_action = self.menu.addAction(_("Metaguide epub"))  # type: ignore # noqa
        epub_action.triggered.connect(self.metaguide_epub_selection)

        # Add kepub action to menu
        kepub_action = self.menu.addAction(_("Metaguide kepub"))  # type: ignore # noqa
        kepub_action.triggered.connect(self.metaguide_kepub_selection)

        # Add separator
        self.menu.addSeparator()

        # Add remove metaguiding action to menu
        remove_metaguiding_action = self.menu.addAction(_("Remove metaguiding"))  # type: ignore # noqa
        remove_metaguiding_action.triggered.connect(
            self.remove_metaguiding_epub_selection
        )

        # point the metaguiding logger to the common logger
        metaguiding._logger = common.log

    def metaguide_selection_format(
        self, format_to_find: str, *, remove_metaguiding: bool = False
    ):
        from calibre.gui2 import (
            error_dialog,
            info_dialog,
        )

        # warn the user that remove_metaguiding is an EXPERIMENTAL feature and
        # that it may not work as expected.
        if remove_metaguiding:
            if not question_dialog(
                self.gui,
                "Remove metaguiding is an EXPERIMENTAL feature",
                "This feature is still in development and may not work as expected. "
                "It should only be used if you deleted your ORIGINAL_format file and you want to try "
                "to remove the metaguiding. Some original format may not be restored. "
                "Please make sure to backup your library before using this feature.\n\n"
                "Do you want to continue?",
                show_copy_button=True,
                default_yes=False,
            ):
                return
        else:
            if not question_dialog(
                self.gui,
                "Metaguiding will modify your files",
                "This feature will modify your files by adding metaguiding to them. "
                "The original file will be saved as ORIGINAL_format (ex: ORIGINAL_EPUB), and the new file will overwrite the original file. "
                "Any previous ORIGINAL_format file will be overwritten and lost. "
                "Please make sure to backup your library before using this feature.\n\n"
                "Do you want to continue?",
                show_copy_button=True,
                default_yes=False,
            ):
                return

        action_text = "remove metaguiding" if remove_metaguiding else "add metaguiding"

        # Get currently selected books
        selected_rows = self.gui.library_view.selectionModel().selectedRows()
        if not selected_rows or len(selected_rows) == 0:
            return error_dialog(
                self.gui, f"Cannot {action_text}", "No books selected", show=True
            )
        # Map the rows to book ids
        selected_ids = list(map(self.gui.library_view.model().id, selected_rows))
        current_database = self.gui.current_db.new_api
        epubs_found_count = 0
        for book_id in selected_ids:
            if current_database.has_format(book_id, format_to_find):
                epubs_found_count += 1
                temp_file = current_database.format(
                    book_id, format_to_find, as_path=True
                )
                common.log.debug(
                    "Converting book id: %d, format: %s" % (book_id, format_to_find)
                )

                try:
                    metaguiding.metaguide_epub_file(
                        temp_file, temp_file, remove_metaguiding=remove_metaguiding
                    )
                except Exception as e:  # pylint: disable=broad-except
                    common.log.error(
                        "Error processing book id: %d, format: %s"
                        % (book_id, format_to_find)
                    )
                    common.log.error(e)
                    return error_dialog(
                        self.gui,
                        f"Cannot {action_text}. Please verify that the epub is valid.",
                        "Error processing book id: %d, format: %s, error details: %s"
                        % (book_id, format_to_find, e),
                        show=True,
                    )

                current_database.save_original_format(book_id, format_to_find)
                result = current_database.add_format(
                    book_id, format_to_find, temp_file, replace=True, run_hooks=False
                )

                if not result:
                    return error_dialog(
                        self.gui,
                        f"Failed to {action_text}",
                        f"Failed to {action_text} format %s to book id %d"
                        % (format_to_find, book_id),
                        show=True,
                    )

        info_dialog(
            self.gui,
            "Updated files",
            "Successfully processed %d files from %d books"
            % (epubs_found_count, len(selected_ids)),
            show=True,
        )
        current_idx = self.gui.library_view.currentIndex()
        self.gui.library_view.model().current_changed(current_idx, current_idx)
        self.gui.library_view.model().refresh_ids(selected_ids)

    def metaguide_epub_selection(self):
        self.metaguide_selection_format("epub")

    def metaguide_kepub_selection(self):
        self.metaguide_selection_format("kepub")

    def remove_metaguiding_epub_selection(self):
        self.metaguide_selection_format("epub", remove_metaguiding=True)
