from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Search Story")
        self.setMinimumSize(450, 220)
        self.resize(500, 230)

        self.setFont(QFont("Segoe UI", 10))

        # TITLE 
        self.title_label = QLabel("Search Your Story")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 14pt;
            font-weight: bold;
            color: #ff7bab;
        """)

        # INPUT 
        self.input = QLineEdit()
        self.input.setPlaceholderText("Masukkan judul story...")
        self.input.setStyleSheet("""
            padding: 10px;
            font-size: 11pt;
            border: 1px solid #ffd1e0;
            border-radius: 8px;
        """)

        self.input.setFocus()

        self.btn_search = QPushButton("Search")
        self.btn_cancel = QPushButton("Cancel")

        self.btn_search.setStyleSheet("""
            background-color: #ffa7c4;
            padding: 8px;
            border-radius: 8px;
            font-weight: bold;
        """)

        self.btn_cancel.setStyleSheet("""
            background-color: #e0e0e0;
            padding: 8px;
            border-radius: 8px;
        """)

        # BUTTON LAYOUT
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_search)
        btn_layout.addWidget(self.btn_cancel)

        # MAIN LAYOUT 
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addSpacing(10)
        layout.addWidget(self.input)
        layout.addSpacing(15)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # CONNECT 
        self.btn_search.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_value(self):
        return self.input.text().strip()