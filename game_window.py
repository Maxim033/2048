# game_window.py
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QLabel,
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QDialog)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QKeyEvent, QPalette, QColor

from game import Game
from settings_dialog import SettingsDialog


class GameWindow(QMainWindow):
    """Main game window and interface."""

    def __init__(self):
        super().__init__()
        self.tiles = {}  # Словарь для хранения виджетов плиток
        self._setup_ui()
        self.game = Game()
        self._init_tiles()
        self._update_ui()

        # Таймер для обработки быстрых нажатий
        self.move_timer = QTimer()
        self.move_timer.setSingleShot(True)
        self.move_timer.timeout.connect(self._process_move)

    def _setup_ui(self):
        """Initialize UI elements."""
        self.setWindowTitle('2048')
        self.setMinimumSize(400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Score display
        self.score_label = QLabel("Score: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(self.score_label)

        # Game board
        self.board_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)
        self.board_widget.setLayout(self.grid_layout)
        main_layout.addWidget(self.board_widget, 1)

        # Buttons
        button_layout = QHBoxLayout()

        self.new_game_btn = QPushButton("New Game")
        self.new_game_btn.clicked.connect(self._new_game)
        self.new_game_btn.setFocusPolicy(Qt.NoFocus)
        button_layout.addWidget(self.new_game_btn)

        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self._show_settings)
        self.settings_btn.setFocusPolicy(Qt.NoFocus)
        button_layout.addWidget(self.settings_btn)

        self.rules_btn = QPushButton("Rules")
        self.rules_btn.clicked.connect(self._show_rules)
        self.rules_btn.setFocusPolicy(Qt.NoFocus)
        button_layout.addWidget(self.rules_btn)

        main_layout.addLayout(button_layout)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def _init_tiles(self):
        """Initialize all tiles at startup."""
        for i in range(self.game.size):
            for j in range(self.game.size):
                tile = QLabel()
                tile.setAlignment(Qt.AlignCenter)
                tile.setFixedSize(80, 80)
                self.grid_layout.addWidget(tile, i, j)
                self.tiles[(i, j)] = tile

    def _update_ui(self):
        """Update the UI to reflect current game state."""
        # Update score
        self.score_label.setText(f"Score: {self.game.score}")

        # Update tiles
        for i in range(self.game.size):
            for j in range(self.game.size):
                value = self.game.grid[i][j]
                self._update_tile_appearance(i, j, value)

        # Adjust window size
        self._adjust_window_size()

        # Check game over
        if self.game.game_over:
            self._show_game_over_message()

    def _update_tile_appearance(self, i, j, value):
        """Update appearance of a single tile."""
        tile = self.tiles[(i, j)]
        colors = {
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

        bg_color, text_color = colors.get(value, (QColor(60, 58, 50), QColor(249, 246, 242)))

        palette = tile.palette()
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, text_color)
        tile.setAutoFillBackground(True)
        tile.setPalette(palette)

        font = QFont("Arial", 24 if value < 100 else 20 if value < 1000 else 16, QFont.Bold)
        tile.setFont(font)

        tile.setText(str(value) if value != 0 else "")
        tile.setStyleSheet("border-radius: 5px;")

    def _adjust_window_size(self):
        """Adjust window size based on grid dimensions."""
        tile_size = 80
        spacing = 10
        width = self.game.size * (tile_size + spacing) + spacing + 40
        height = width + 100
        self.setFixedSize(QSize(width, height))

    def _show_game_over_message(self):
        """Show game over message and offer new game."""
        reply = QMessageBox.question(
            self, "Game Over",
            f"Game Over!\nYour score: {self.game.score}\nMax tile: {self.game.max_tile}\n\nNew game?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            self._new_game()

    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard input for game controls."""
        if self.move_timer.isActive():
            return

        key = event.key()
        direction_map = {
            Qt.Key_Up: 0,
            Qt.Key_Right: 1,
            Qt.Key_Down: 2,
            Qt.Key_Left: 3,
            Qt.Key_W: 0,
            Qt.Key_D: 1,
            Qt.Key_S: 2,
            Qt.Key_A: 3
        }

        if key in direction_map:
            self.move_timer.start(100)  # Задержка 100 мс
            if self.game.move(direction_map[key]):
                self._update_ui()
        else:
            super().keyPressEvent(event)

    def _process_move(self):
        """Process move after timer delay."""
        pass  # Нужно для обработки быстрых нажатий

    def _new_game(self):
        """Start a new game with current settings."""
        self.game.reset()
        self._update_ui()

    def _show_settings(self):
        """Show settings dialog and apply changes if accepted."""
        dialog = SettingsDialog(self)
        dialog.size_spinbox.setValue(self.game.size)

        if dialog.exec_() == QDialog.Accepted:
            size = dialog.size_spinbox.value()
            self.game = Game(size)
            self._init_tiles()
            self._update_ui()

    def _show_rules(self):
        """Show game rules."""
        rules = """
        <h1>2048 Game Rules</h1>
        <p><b>How to play:</b> Use arrow keys (or WASD) to move the tiles. 
        When two tiles with the same number touch, they merge into one!</p>
        <p><b>Goal:</b> Reach the 2048 tile or higher!</p>
        <p><b>Controls:</b></p>
        <ul>
            <li>Up arrow/W - Move tiles up</li>
            <li>Down arrow/S - Move tiles down</li>
            <li>Left arrow/A - Move tiles left</li>
            <li>Right arrow/D - Move tiles right</li>
        </ul>
        <p>Press 'New Game' to restart at any time.</p>
        """

        msg = QMessageBox()
        msg.setWindowTitle("Game Rules")
        msg.setTextFormat(Qt.RichText)
        msg.setText(rules)
        msg.exec_()