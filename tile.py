# tile.py
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette


class Tile(QLabel):
    """Visual representation of a game tile."""

    TILE_COLORS = {
        0: (QColor(205, 193, 180), QColor(119, 110, 101)),
        2: (QColor(238, 228, 218), QColor(119, 110, 101)),
        4: (QColor(237, 224, 200), QColor(119, 110, 101)),
        8: (QColor(242, 177, 121), QColor(249, 246, 242)),
        16: (QColor(245, 149, 99), QColor(249, 246, 242)),
        32: (QColor(246, 124, 95), QColor(249, 246, 242)),
        64: (QColor(246, 94, 59), QColor(249, 246, 242)),
        128: (QColor(237, 207, 114), QColor(249, 246, 242)),
        256: (QColor(237, 204, 97), QColor(249, 246, 242)),
        512: (QColor(237, 200, 80), QColor(249, 246, 242)),
        1024: (QColor(237, 197, 63), QColor(249, 246, 242)),
        2048: (QColor(237, 194, 46), QColor(249, 246, 242)),
    }

    def __init__(self, value: int):
        super().__init__()
        self.value = value
        self._setup_ui()
        self.update_style()

    def _setup_ui(self):
        """Initialize UI elements."""
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(80, 80)
        font = QFont("Arial", 24, QFont.Bold)
        self.setFont(font)

    def update_style(self):
        """Update tile appearance based on its value."""
        bg_color, text_color = self.TILE_COLORS.get(self.value, (QColor(60, 58, 50), QColor(249, 246, 242)))

        palette = self.palette()
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, text_color)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Adjust font size based on tile value
        font = self.font()
        if self.value < 100:
            font.setPointSize(24)
        elif self.value < 1000:
            font.setPointSize(20)
        else:
            font.setPointSize(16)
        self.setFont(font)

        self.setText(str(self.value) if self.value != 0 else "")
        self.setStyleSheet("border-radius: 5px;")