import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QLabel,
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from game import Game
from tile import Tile
from settings_dialog import SettingsDialog


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.game = Game()
        self.update_ui()

    def initUI(self):
        self.setWindowTitle('2048')
        self.setFixedSize(400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.score_label = QLabel("Score: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(self.score_label)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        layout.addLayout(self.grid_layout)

        button_layout = QHBoxLayout()

        new_game_btn = QPushButton("New Game")
        new_game_btn.clicked.connect(self.new_game)
        button_layout.addWidget(new_game_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.show_settings)
        button_layout.addWidget(settings_btn)

        rules_btn = QPushButton("Rules")
        rules_btn.clicked.connect(self.show_rules)
        button_layout.addWidget(rules_btn)

        layout.addLayout(button_layout)

    def update_ui(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        self.score_label.setText(f"Score: {self.game.score}")

        for i in range(self.game.size):
            for j in range(self.game.size):
                tile = Tile(self.game.grid[i][j])
                self.grid_layout.addWidget(tile, i, j)

        if self.game.game_over:
            QMessageBox.information(self, "Game Over",
                                    f"Game Over!\nYour score: {self.game.score}\nMax tile: {self.game.max_tile}")
            self.new_game()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Up:
            self.game.move(0)
        elif key == Qt.Key_Right:
            self.game.move(1)
        elif key == Qt.Key_Down:
            self.game.move(2)
        elif key == Qt.Key_Left:
            self.game.move(3)
        else:
            return

        self.update_ui()

    def new_game(self):
        self.game.reset()
        self.update_ui()

    def show_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            size = dialog.size_spinbox.value()
            self.game = Game(size)
            self.update_ui()

    def show_rules(self):
        rules = """
        <h1>2048 Game Rules</h1>
        <p><b>How to play:</b> Use arrow keys to move the tiles. 
        When two tiles with the same number touch, they merge into one!</p>
        <p><b>Goal:</b> Reach the 2048 tile!</p>
        <p><b>Controls:</b></p>
        <ul>
            <li>Up arrow - Move tiles up</li>
            <li>Down arrow - Move tiles down</li>
            <li>Left arrow - Move tiles left</li>
            <li>Right arrow - Move tiles right</li>
        </ul>
        """

        msg = QMessageBox()
        msg.setWindowTitle("Game Rules")
        msg.setTextFormat(Qt.RichText)
        msg.setText(rules)
        msg.exec_()