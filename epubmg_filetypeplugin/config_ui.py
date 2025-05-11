"""
Configuration interface for the Epub Metaguider post processor plugin.
"""

__license__ = "GPL v3"
__copyright__ = "2025, Hugo Batista <intellireading at hugobatista.com>"
__docformat__ = "markdown en"

# pylint: disable=import-error
try:
    from qt.core import QWidget, QVBoxLayout, QCheckBox, QGroupBox, QLabel
except ImportError:
    from PyQt5.Qt import QWidget, QVBoxLayout, QCheckBox, QGroupBox, QLabel

from calibre_plugins.epubmgfiletype.config import prefs

class ConfigWidget(QWidget):
    """Configuration widget for the Epub Metaguider post processor plugin."""

    def __init__(self, plugin_action):
        """Initialize the configuration widget."""
        QWidget.__init__(self)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Event settings
        event_group = QGroupBox("When to Run")
        event_layout = QVBoxLayout()
        
        # Post-process checkbox
        self.postprocess_checkbox = QCheckBox(
            'Enable metaguiding after conversion (post-process)', self)
        self.postprocess_checkbox.setChecked(prefs['enable_on_postprocess'])
        event_layout.addWidget(self.postprocess_checkbox)

        # Import checkbox
        self.import_checkbox = QCheckBox(
            'Enable metaguiding when importing files', self)
        self.import_checkbox.setChecked(prefs['enable_on_import'])
        event_layout.addWidget(self.import_checkbox)
        
        event_group.setLayout(event_layout)
        self.layout.addWidget(event_group)

        # File type settings
        file_group = QGroupBox("File Types to Process")
        file_layout = QVBoxLayout()
        
        # EPUB checkbox
        self.epub_checkbox = QCheckBox('Process EPUB files', self)
        self.epub_checkbox.setChecked(prefs['process_epub'])
        file_layout.addWidget(self.epub_checkbox)

        # KEPUB checkbox
        self.kepub_checkbox = QCheckBox('Process KEPUB files', self)
        self.kepub_checkbox.setChecked(prefs['process_kepub'])
        file_layout.addWidget(self.kepub_checkbox)
        
        file_group.setLayout(file_layout)
        self.layout.addWidget(file_group)

        # Add info label
        info_label = QLabel(
            'Note: Changes will take effect after restarting Calibre'
        )
        self.layout.addWidget(info_label)
        
        self.layout.addStretch()

    def save_settings(self):
        """Save the current configuration."""
        # Save event settings
        prefs['enable_on_postprocess'] = self.postprocess_checkbox.isChecked()
        prefs['enable_on_import'] = self.import_checkbox.isChecked()
        
        # Save file type settings
        prefs['process_epub'] = self.epub_checkbox.isChecked()
        prefs['process_kepub'] = self.kepub_checkbox.isChecked()
