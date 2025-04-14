# settings_dialog.py
from PyQt5.QtWidgets import (QDialog, QFormLayout, QSpinBox,
                             QPushButton, QHBoxLayout, QVBoxLayout)


class SettingsDialog(QDialog):
    """Dialog for game settings configuration."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Initialize UI elements."""
        self.setWindowTitle("Game Settings")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(3, 8)
        self.size_spinbox.setValue(4)
        form_layout.addRow("Grid Size:", self.size_spinbox)

        layout.addLayout(form_layout)

        # Buttons
        button_box = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        button_box.addWidget(ok_btn)
        button_box.addWidget(cancel_btn)
        layout.addLayout(button_box)