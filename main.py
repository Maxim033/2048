# main.py
import os
import sys
from PyQt5.QtWidgets import QApplication
from game_window import GameWindow


def configure_qt_environment():
    """Configure Qt environment paths."""
    try:
        # Попробуем автоматически определить путь к плагинам
        from PyQt5.QtCore import QLibraryInfo
        qt_plugin_path = QLibraryInfo.location(QLibraryInfo.PluginsPath)
        if os.path.exists(qt_plugin_path):
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = qt_plugin_path
            return
    except:
        pass

    # Пути для ручной проверки
    possible_paths = [
        r"C:\Users\Максим\PycharmProjects\Game 5\.venv\Lib\site-packages\PyQt5\Qt5\plugins",
        os.path.join(sys.prefix, "Lib", "site-packages", "PyQt5", "Qt", "plugins"),
        os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages", "PyQt5", "Qt", "plugins")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = path
            return

    print("Error: Qt plugins path not found!")
    print("Tried paths:")
    for path in possible_paths:
        print(f"- {path}")
    sys.exit(1)


def main():
    configure_qt_environment()

    try:
        app = QApplication(sys.argv)
        game = GameWindow()
        game.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()