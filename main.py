import os
import sys
from PyQt5.QtWidgets import QApplication
from game_window import GameWindow

# Указываем путь к папке PLUGINS (не к файлу!)
QT_PLUGIN_PATH = r"C:\Users\Максим\PycharmProjects\Game 5\.venv\Lib\site-packages\PyQt5\Qt5\plugins"

# Проверяем существование папки с плагинами
if not os.path.exists(QT_PLUGIN_PATH):
    print(f"ОШИБКА: Папка с плагинами Qt не найдена по пути: {QT_PLUGIN_PATH}")
    print("Проверьте:")
    print("1. Что PyQt5 установлен правильно (pip install PyQt5 PyQt5-Qt5)")
    print("2. Что виртуальное окружение активировано")
    sys.exit(1)

# Настраиваем окружение Qt
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QT_PLUGIN_PATH
os.environ["QT_QPA_PLATFORM"] = "windows"  # Явно указываем платформу для Windows

# Добавляем путь к Qt\bin в PATH (если нужно)
QT_BIN_PATH = os.path.join(os.path.dirname(QT_PLUGIN_PATH), "bin")
if os.path.exists(QT_BIN_PATH):
    os.environ["PATH"] = QT_BIN_PATH + ";" + os.environ["PATH"]

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        game = GameWindow()
        game.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"ОШИБКА: Не удалось запустить приложение")
        print(f"Детали: {str(e)}")
        print("Попробуйте:")
        print("1. Переустановить PyQt5: pip install --force-reinstall PyQt5 PyQt5-Qt5")
        print("2. Проверить, что в папке 'plugins/platforms' есть qwindows.dll")
        sys.exit(1)