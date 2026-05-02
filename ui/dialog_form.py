from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QTextEdit,
    QComboBox, QVBoxLayout, QPushButton, QHBoxLayout,
    QDateEdit, QMessageBox
)
from PySide6.QtGui import QFont


class AddEditDialog(QDialog):
    def __init__(self, parent=None, entry_data=None):
        super().__init__(parent)

        self.setWindowTitle(
            "Tambah Story" if entry_data is None else "Edit Story"
        )

        self.setMinimumSize(500, 500)
        self.resize(500, 500)

        self.entry_id = None

        font = QFont("Segoe UI", 9)
        self.setFont(font)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("dd MMMM yyyy")
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setButtonSymbols(QDateEdit.NoButtons)

        self.line_judul = QLineEdit()
        self.line_judul.setPlaceholderText("Masukkan judul story...")

        self.combo_kategori = QComboBox()
        self.combo_kategori.addItems([
            "University Life",
            "Lovers",
            "The Fams",
            "Wanderlust",
            "Dreams Future",
            "Self Reflection"
        ])

        self.combo_mood = QComboBox()
        self.combo_mood.addItems([
            "Happy",
            "Low Battery",
            "Unbothered",
            "Chill",
            "Butterfly Era",
            "Cloudy",
            "Full Power"
        ])

        self.text_isi = QTextEdit()
        self.text_isi.setPlaceholderText("Tulis story hari ini...")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)

        form_layout.addRow("Tanggal:", self.date_edit)
        form_layout.addRow("Judul:", self.line_judul)
        form_layout.addRow("Kategori:", self.combo_kategori)
        form_layout.addRow("Mood:", self.combo_mood)
        form_layout.addRow("Isi Story:", self.text_isi)

        # BUTTON 
        self.btn_simpan = QPushButton("Simpan")
        self.btn_batal = QPushButton("Batal")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_simpan)
        btn_layout.addWidget(self.btn_batal)

        # MAIN LAYOUT 
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # EDIT 
        if entry_data is not None:
            self.entry_id = entry_data[0]

            self.date_edit.setDate(
                QDate.fromString(entry_data[1], "yyyy-MM-dd")
            )

            self.line_judul.setText(entry_data[2])
            self.text_isi.setPlainText(entry_data[3])

            idx_kat = self.combo_kategori.findText(
                entry_data[4], Qt.MatchContains
            )
            if idx_kat >= 0:
                self.combo_kategori.setCurrentIndex(idx_kat)

            idx_mood = self.combo_mood.findText(
                entry_data[5], Qt.MatchContains
            )
            if idx_mood >= 0:
                self.combo_mood.setCurrentIndex(idx_mood)

        # CONNECT
        self.btn_simpan.clicked.connect(self.validate_and_accept)
        self.btn_batal.clicked.connect(self.reject)

    def validate_and_accept(self):
        if not self.line_judul.text().strip():
            QMessageBox.warning(self, "Error", "Judul tidak boleh kosong!")
            return

        self.accept()

    # GET DATA 
    def get_data(self):
        data = {
            "tanggal": self.date_edit.date().toString("yyyy-MM-dd"),
            "judul": self.line_judul.text().strip(),
            "isi_catatan": self.text_isi.toPlainText().strip(),
            "kategori": self.combo_kategori.currentText(),
            "mood": self.combo_mood.currentText()
        }

        return data, None