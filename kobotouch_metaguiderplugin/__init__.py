from calibre.devices.kobo.driver import KOBOTOUCH
from calibre_plugins.epubmgfiletype import (
    common,
    metaguiding,
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
        "Kobo Touch driver with metaguiding support for epub and kepub files."
        "This driver is a modified version of the KoboTouch driver from calibre, enabling "
        "conversion of epub and kepub files to a metaguiding format before "
        "uploading to the device. "
        "This is done to improve your focus and reading speed (sometimes called bionic reading)."
    )
    supported_platforms = ["windows", "osx", "linux"]
    version = (2, 0, 0)
    minimum_calibre_version = (6, 5, 0)
    author = "Hugo Batista"

    def upload_books(self, files, names, on_card, end_session=True, metadata=None):
        # Process each file before calling the base upload
        # only process epub and kepub files
        processed_files = []
        for file in files:

            if not file.endswith((".epub", ".kepub")):
                common.log.debug(f"File {file} is not a supported format for metaguiding, skipping.")
                processed_files.append(file)
                continue

            processed_file = metaguide_file(file)
            processed_files.append(processed_file)
        # Call the parent method with the processed files

        return super().upload_books(
            files=processed_files,
            names=names,
            on_card=on_card,
            end_session=end_session,
            metadata=metadata,
        )
