from PySide6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QMessageBox, QDialog, QHeaderView, QFileDialog, QInputDialog
)
import os
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QDate
from ui.dialog_form import AddEditDialog
from controllers.diary_controller import DiaryController
from ui.search_dialog import SearchDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.controller = DiaryController()

        self.setWindowTitle("MyMemoria | The art of remembering")
        self.setMinimumSize(870, 600)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Tanggal", "Judul", "Kategori", "Mood"]
        )
        self.table.setColumnHidden(0, True)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)

        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 400)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 150)

        self.btn_tambah = QPushButton("Tambah Story")
        self.btn_edit = QPushButton("Edit Story")
        self.btn_hapus = QPushButton("Hapus Story")

        self.btn_hapus.setObjectName("btn_hapus")

        layout_btn = QHBoxLayout()
        layout_btn.addWidget(self.btn_tambah)
        layout_btn.addWidget(self.btn_edit)
        layout_btn.addWidget(self.btn_hapus)

        self.status_label = QLabel("myMemoria siap digunakan")
        self.label_nama_nim = QLabel("Alysa Meliana | F1D02310035")
 
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(layout_btn)
        layout.addWidget(self.status_label)
        layout.addWidget(self.label_nama_nim)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
 
        menubar = self.menuBar()

        # FILE MENU
        menu_file = menubar.addMenu("File")

        action_new = QAction("New Story", self)
        action_new.triggered.connect(self._on_tambah_clicked)

        action_edit = QAction("Edit Story", self)
        action_edit.triggered.connect(self._on_edit_clicked)

        action_delete = QAction("Delete Story", self)
        action_delete.triggered.connect(self._on_hapus_clicked)

        action_export = QAction("Export Story", self)
        action_export.triggered.connect(self._on_export_clicked)

        action_import = QAction("Import Story", self)
        action_import.triggered.connect(self._on_import_clicked)

        menu_file.addAction(action_new)
        menu_file.addAction(action_edit)
        menu_file.addAction(action_delete)
        menu_file.addSeparator()
        menu_file.addAction(action_export)
        menu_file.addAction(action_import)

        # SEARCH MENU 
        menu_search = menubar.addMenu("Search")

        action_search = QAction("Search Story", self)
        action_search.triggered.connect(self._on_search_clicked)

        menu_search.addAction(action_search)

        # VIEW MENU
        menu_view = menubar.addMenu("View")

        action_about = QAction("About", self)
        action_about.triggered.connect(self._show_about)

        menu_view.addAction(action_about)

        self.btn_tambah.clicked.connect(self._on_tambah_clicked)
        self.btn_edit.clicked.connect(self._on_edit_clicked)
        self.btn_hapus.clicked.connect(self._on_hapus_clicked)

        self.load_entries()

    def load_entries(self):
        entries = self.controller.get_entries()
        self._fill_table(entries)

    def _fill_table(self, entries):
        self.table.setRowCount(len(entries))

        for row_index, entry in enumerate(entries):
            id_, tanggal, judul, isi, kategori, mood = entry

            self.table.setItem(row_index, 0, QTableWidgetItem(str(id_)))
            self.table.setItem(row_index, 1, QTableWidgetItem(tanggal))
            self.table.setItem(row_index, 2, QTableWidgetItem(judul))
            self.table.setItem(row_index, 3, QTableWidgetItem(kategori))
            self.table.setItem(row_index, 4, QTableWidgetItem(mood))

    # TAMBAH 
    def _on_tambah_clicked(self):
        dialog = AddEditDialog(self)

        if dialog.exec() == QDialog.Accepted:
            data, error = dialog.get_data()

            if data is None:
                QMessageBox.warning(self, "Error", error)
                return

            self.controller.add_entry(data)
            self.load_entries()

    # EDIT 
    def _on_edit_clicked(self):

        if self.table.currentRow() < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih catatan dulu!")
            return

        row = self.table.currentRow()
        entry_id = int(self.table.item(row, 0).text())

        entries = self.controller.get_entries()
        selected = None

        for e in entries:
            if e[0] == entry_id:
                selected = e
                break

        dialog = AddEditDialog(self, selected)

        if dialog.exec() == QDialog.Accepted:
            data, _ = dialog.get_data()
            self.controller.update_entry(entry_id, data)
            self.load_entries()

    # DELETE
    def _on_hapus_clicked(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih catatan dulu!")
            return

        entry_id = int(self.table.item(row, 0).text())
        judul = self.table.item(row, 2).text()

        msg = QMessageBox(self)
        msg.setWindowTitle("Hapus Story")
        msg.setText(f"Yakin mau hapus '{judul}'?")
        msg.setIcon(QMessageBox.Warning)

        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        confirm = msg.exec()

        if confirm == QMessageBox.Yes:
            self.controller.delete_entry(entry_id)
            self.load_entries()

    # SEARCH 
    def _on_search_clicked(self):
        dialog = SearchDialog()

        if dialog.exec():
            keyword = dialog.get_value()

            if keyword:
                results = self.controller.search_entries(keyword)
                self._fill_table(results)
            else:
                self.load_entries()

    # EXPORT
    def _on_export_clicked(self):
        row = self.table.currentRow()

        if row < 0:
            QMessageBox.warning(self, "Export", "Pilih story dulu!")
            return

        entry_id = int(self.table.item(row, 0).text())
        tanggal = self.table.item(row, 1).text()
        judul = self.table.item(row, 2).text()
        kategori = self.table.item(row, 3).text()
        mood = self.table.item(row, 4).text()

        entries = self.controller.get_entries()
        isi = ""

        for e in entries:
            if e[0] == entry_id:
                isi = e[3]
                break

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Story",
            f"{judul}",
            "Text File (*.txt);;PDF File (*.pdf)"
        )

        if not file_path:
            return

        try:
            if file_path.endswith(".txt"):
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("=== myMemoria ===\n\n")
                    f.write(f"Judul: {judul}\n")
                    f.write(f"Tanggal: {tanggal}\n")
                    f.write(f"Kategori: {kategori}\n")
                    f.write(f"Mood: {mood}\n")
                    f.write(f"Isi: {isi}\n")

                QMessageBox.information(self, "Export", "Berhasil export TXT!")

            elif file_path.endswith(".pdf"):
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet

                doc = SimpleDocTemplate(file_path)
                styles = getSampleStyleSheet()

                content = []

                content.append(Paragraph("=== myMemoria ===", styles["Title"]))
                content.append(Spacer(1, 12))

                content.append(Paragraph(f"<b>Judul:</b> {judul}", styles["Normal"]))
                content.append(Paragraph(f"<b>Tanggal:</b> {tanggal}", styles["Normal"]))
                content.append(Paragraph(f"<b>Kategori:</b> {kategori}", styles["Normal"]))
                content.append(Paragraph(f"<b>Mood:</b> {mood}", styles["Normal"]))
                content.append(Spacer(1, 5))
                content.append(Paragraph(f"<b>Isi:</b><br/>{isi}", styles["Normal"]))

                doc.build(content)

                QMessageBox.information(self, "Export", "Berhasil export PDF!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # IMPORT 
    def _on_import_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Story",
            "",
            "Text File (*.txt)"
        )

        if not file_path:
            return

        try:
            # FILE 
            judul = os.path.splitext(os.path.basename(file_path))[0]

            with open(file_path, "r", encoding="utf-8") as f:
                isi = f.read().strip()

            # INPUT USER
            kategori, ok1 = QInputDialog.getItem(
                self,
                "Kategori Story",
                "Pilih kategori:",
                [
                    "University Life",
                    "Lovers",
                    "The Fams",
                    "Wanderlust",
                    "Dreams Future",
                    "Self Reflection"
                ],
                0,
                False
            )

            if not ok1:
                return

            mood, ok2 = QInputDialog.getItem(
                self,
                "Mood Story",
                "Pilih mood:",
                [
                    "Happy",
                    "Low Battery",
                    "Unbothered",
                    "Chill",
                    "Butterfly Era",
                    "Cloudy",
                    "Full Power"
                ],
                0,
                False
            )

            if not ok2:
                return

            tanggal = QDate.currentDate().toString("yyyy-MM-dd")

            # SAVE 
            self.controller.add_entry({
                "tanggal": tanggal,
                "judul": judul,
                "isi_catatan": isi,
                "kategori": kategori,
                "mood": mood
            })

            self.load_entries()

            QMessageBox.information(self, "Import", "Berhasil import + setting kategori & mood!")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ABOUT
    def _show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About MyMemoria")
        dialog.setFixedSize(370, 300)

        layout = QVBoxLayout()

        # TITLE
        title = QLabel("|| MyMemoria ||")
        title.setObjectName("about_title")
        title.setAlignment(Qt.AlignCenter)

        desc = QLabel(
            "myMemoria adalah tentang ingatan yang menderu.\n"
            "Penjaga cerita agar tak lebur oleh waktu.\n"
            "Biarkan aksara bicara saat suara mulai meredup.\n"
            "Menjadi saksi bisu atas indahnya sebuah hidup.\n"
            "Menenun sisa waktu menjadi cahaya yang abadi.\n"
            "Agar esok hari, engkau tetap hidup di sini.\n"
            "Satu hari, satu baris, satu keabadian."
        )
        desc.setObjectName("about_desc")
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)

        identity = QLabel("Alysa Meliana | F1D02310035")
        identity.setObjectName("about_identity")
        identity.setAlignment(Qt.AlignCenter)

        author = QLabel(
            "Mencari pola di antara kenangan\n"
            "Menemukan makna di setiap kesimpulan\n"
            "@___analysa"
        )
        author.setObjectName("about_author")
        author.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addWidget(desc)
        layout.addSpacing(10)
        layout.addWidget(identity)
        layout.addStretch()
        layout.addWidget(author)

        dialog.setLayout(layout)
        dialog.exec()