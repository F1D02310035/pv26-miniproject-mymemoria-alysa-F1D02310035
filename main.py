import sys
import os

sys.path.append(os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from database.database import create_table
from ui.main_window import MainWindow


if __name__ == "__main__":
    create_table()

    app = QApplication(sys.argv)

    style_path = os.path.join(os.path.dirname(__file__), "styles", "main.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())