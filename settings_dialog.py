from PyQt5.QtWidgets import (QDialog, QFormLayout, QSpinBox,
                             QPushButton, QHBoxLayout)


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game Settings")

        layout = QFormLayout(self)

        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(3, 6)
        self.size_spinbox.setValue(4)

        layout.addRow("Grid Size:", self.size_spinbox)

        buttons = QHBoxLayout()
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addRow(buttons)