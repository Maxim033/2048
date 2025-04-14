from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Tile(QLabel):
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(80, 80)
        self.update_style()

    def update_style(self):
        colors = {
            0: ("#CDC1B4", "#776E65"),
            2: ("#EEE4DA", "#776E65"),
            4: ("#EDE0C8", "#776E65"),
            8: ("#F2B179", "#F9F6F2"),
            16: ("#F59563", "#F9F6F2"),
            32: ("#F67C5F", "#F9F6F2"),
            64: ("#F65E3B", "#F9F6F2"),
            128: ("#EDCF72", "#F9F6F2"),
            256: ("#EDCC61", "#F9F6F2"),
            512: ("#EDC850", "#F9F6F2"),
            1024: ("#EDC53F", "#F9F6F2"),
            2048: ("#EDC22E", "#F9F6F2"),
        }

        bg_color, text_color = colors.get(self.value, ("#3C3A32", "#F9F6F2"))

        self.setStyleSheet(f"""
            background-color: {bg_color};
            color: {text_color};
            border-radius: 5px;
            font-weight: bold;
            font-size: {24 if self.value < 100 else 20 if self.value < 1000 else 16}px;
        """)

        self.setText(str(self.value) if self.value != 0 else "")