from calibre.devices.kobo.driver import KOBOTOUCH
from typing import List, Optional, Tuple
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.metaguidekobotouch import common, metaguiding, __about_cli__

# Constants
MSG_ALREADY_METAGUIDED = (
    '"{name}" is already metaguided. '
    "Sending pre-metaguided EPUBs to a Kobo device may cause slow performance "
    "due to the kepubify process and the way it handles the bold tag.\n\n"
    "Recommended Process:\n"
    "1. Send the original non-metaguided EPUB to your Kobo\n"
    "2. Let this driver handle the metaguiding during transfer\n\n"
    "This ensures optimal performance on your device."
)


def metaguide_file(filepath: str) -> str:
    common.log.debug(f"Converting file to metaguiding format: {filepath}")
    try:
        metaguiding.metaguide_epub_file(filepath, filepath, remove_metaguiding=False)
    except Exception as e:  # pylint: disable=broad-except
        common.log.error(f"Error processing file: {filepath}")
        common.log.error(str(e))
        raise e

    return filepath


class KoboTouchMetaguider(KOBOTOUCH):
    name = "Metaguide - KoboTouch Driver (intellireading.com)"
    description = (
        "Kobo Touch driver with metaguiding support for epub and kepub files. "
        "This driver is a modified version of the KoboTouch driver from calibre, enabling "
        "conversion of epub and kepub files to a metaguiding format before "
        "uploading to the device. "
        "This is done to improve your focus and reading speed (sometimes called bionic reading)."
        " Intellireading CLI version: " + __about_cli__.__version__ + "."
    )
    supported_platforms = ["windows", "osx", "linux"]
    version = (2, 0, 0)
    minimum_calibre_version = (8, 4, 0)
    author = "Hugo Batista"

    def initialize(self) -> None:
        common.log.debug("Initializing KoboTouchMetaguider")
        super().initialize()

    def _convert_epub_to_kepub(self, input_path: str, output_path: str, metadata: Optional[Metadata] = None) -> str:
        """
        Convert an EPUB file to KEPUB format.

        Args:
            input_path: Path to the input EPUB file
            output_path: Path where the KEPUB file should be saved
            metadata: Optional metadata to apply to the converted file

        Returns:
            str: Path to the converted KEPUB file
        """
        from calibre.ebooks.conversion.config import load_defaults
        from calibre.ebooks.conversion.plumber import Plumber
        from calibre.utils.logging import default_log

        # Create and setup the plumber
        plumber = Plumber(input_path, output_path, default_log)

        # Setup options with defaults
        plumber.setup_options()

        # Load KEPUB conversion defaults
        kepub_defaults = load_defaults("kepub_output")

        # Update conversion options
        for key, value in kepub_defaults.items():
            setattr(plumber.opts, key, value)

        # Set any additional options needed
        plumber.opts.prefer_author_sort = False
        plumber.opts.kepub_hyphenate = True
        plumber.opts.kepub_clean_markup = True
        plumber.opts.kepub_replace_fonts = False
        plumber.opts.output_profile = "tablet"
        plumber.opts.input_profile = "tablet"

        # Apply metadata if provided
        if metadata:
            plumber.override_input_metadata = True
            plumber.user_metadata = metadata

        common.log.debug(f"Converting EPUB to KEPUB: {input_path} -> {output_path}")

        # Run the conversion
        plumber.run()

        return output_path

    def _log_and_show_message(self, message: str, duration: int = 5000) -> None:
        """
        Log a message and show it in the status bar.

        Args:
            message: The message to log and display
            duration: How long to show the message in milliseconds
        """
        common.log.debug(message)
        from calibre.gui2.ui import get_gui

        gui = get_gui()
        gui.status_bar.show_message(f"KoboTouchMetaguider: {message}", duration)

    def upload_books(
        self,
        files: List[str],
        names: List[str],
        on_card: bool = False,
        end_session: bool = True,
        metadata: Optional[List[Metadata]] = None,
    ) -> Tuple[List[str], List[str]]:
        """
        Upload books to the device, converting them to metaguided format if needed.

        Args:
            files: List of file paths to upload
            names: List of names for the files
            on_card: Whether to upload to the memory card
            end_session: Whether to end the session after upload
            metadata: Optional list of metadata for the files

        Returns:
            Tuple containing processed files and names
        """
        processed_files = []
        processed_names = []
        from calibre.gui2.ui import get_gui
        from calibre.ptempfile import PersistentTemporaryFile

        gui = get_gui()

        for file, name, mi in zip(files, names, metadata or [None] * len(files)):
            if not file.lower().endswith((".epub", ".kepub")):
                common.log.debug(f"File {file} is not a supported format for metaguiding, skipping.")
                processed_files.append(file)
                processed_names.append(name)
                continue

            self._log_and_show_message(f'Metaguiding "{name}" with file {file}', 500)
            try:
                is_file_metaguided = metaguiding.is_file_metaguided(file)
                common.log.debug(f"is_file_metaguided ({file}): {is_file_metaguided}")

                if file.lower().endswith(".epub"):
                    if not is_file_metaguided:
                        # Only convert to kepub if enabled in preferences and not a Tolino device
                        do_kepubify = self.get_pref("kepubify") and not self.isTolinoDevice()
                        if do_kepubify:
                            # Convert EPUBs to KEPUBs before metaguiding for optimal performance
                            # this will avoid additional spans for each bold tag
                            # as reported at https://go.hugobatista.com/gh/intellireading-calibre-plugins/issues/13
                            with PersistentTemporaryFile(suffix=".kepub") as temp_file:
                                temp_file.close()  # Close it so other processes can access it
                                try:
                                    converted_file = self._convert_epub_to_kepub(file, temp_file.name, mi)
                                    self._log_and_show_message(f'Converted "{name}" to KEPUB...', 1000)
                                    name = name.replace(".epub", ".kepub")
                                    # Metaguide the converted file
                                    file = metaguide_file(converted_file)
                                    self._log_and_show_message(f'Successfully metaguided "{name}"', 1000)
                                except Exception as e:
                                    common.log.error(f"Error converting {file} to kepub: {e}")
                                    raise
                        else:
                            # If kepubify is disabled or it's a Tolino device, just metaguide the epub directly
                            file = metaguide_file(file)
                            self._log_and_show_message(f'Successfully metaguided "{name}"', 1000)
                    else:
                        # Show warning dialog about metaguided epub performance on Kobo
                        gui.status_bar.show_message(
                            MSG_ALREADY_METAGUIDED.format(name=name),
                            10000,
                        )
                else:
                    # Handle kepub files
                    if not is_file_metaguided:
                        file = metaguide_file(file)
                        self._log_and_show_message(f'Successfully metaguided "{name}"', 1000)

                # Add the processed file and name to the lists
                processed_files.append(file)
                processed_names.append(name)

            except Exception as e:
                self._log_and_show_message(f'Failed to metaguide "{name}": {str(e)}', 5000)
                raise

        # Call the parent method with the processed files
        return super().upload_books(
            files=processed_files,
            names=processed_names,
            on_card=on_card,
            end_session=end_session,
            metadata=metadata,
        )
