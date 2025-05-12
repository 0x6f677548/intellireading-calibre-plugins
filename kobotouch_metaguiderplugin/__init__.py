from calibre.devices.kobo.driver import KOBOTOUCH
from calibre_plugins.epubmgfiletype import (
    common,
    metaguiding,
    __about_cli__,
)


def metaguide_file(filepath):
    common.log.debug(f"Converting file to metaguiding format: {filepath}")
    try:
        metaguiding.metaguide_epub_file(filepath, filepath, remove_metaguiding=False)
    except Exception as e:  # pylint: disable=broad-except
        common.log.error("Error processing file: %s" % (filepath))
        common.log.error(e)
        raise e

    return filepath


class KoboTouchMetaguider(KOBOTOUCH):
    name = "KoboTouch Metaguider (intellireading.com)"
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

    def upload_books(self, files, names, on_card, end_session=True, metadata=None):
        # Process each file before calling the base upload
        # only process epub and kepub files
        processed_files = []
        from calibre.gui2.ui import get_gui

        gui = get_gui()

        for file, name in zip(files, names):
            if not file.endswith((".epub", ".kepub")):
                common.log.debug(f"File {file} is not a supported format for metaguiding, skipping.")
                processed_files.append(file)
                continue

            gui.status_bar.show_message(f'Metaguiding "{name}"...', 500)
            try:

                common.log.debug(f"Processing file: {file}")
                common.log.debug(f"Is file already metaguided? {metaguiding.is_file_metaguided(file)}")

                # check if the file has already been metaguided
                if file.endswith(".epub") and metaguiding.is_file_metaguided(file):
                    common.log.debug(f"File {file} is already metaguided, skipping.")
                    # Show warning dialog about metaguided epub performance on Kobo
                    gui.status_bar.show_message(
                        f'"{name}" is already metaguided. '
                        "Sending pre-metaguided EPUBs to a Kobo device may cause slow performance "
                        "due to the kepubify process and how it handles spans.\n\n"
                        "Recommended Process:\n"
                        "1. Send the original non-metaguided EPUB to your Kobo\n"
                        "2. Let this driver handle the metaguiding during transfer\n\n"
                        "This ensures optimal performance on your device.",
                        10000,
                    )
                    processed_files.append(file)
                    continue

                processed_file = metaguide_file(file)
                processed_files.append(processed_file)
                gui.status_bar.show_message(f'Successfully metaguided "{name}"', 1000)
            except Exception as e:
                gui.status_bar.show_message(f'Failed to metaguide "{name}": {str(e)}', 5000)
                raise

        # Call the parent method with the processed files
        return super().upload_books(
            files=processed_files,
            names=names,
            on_card=on_card,
            end_session=end_session,
            metadata=metadata,
        )
