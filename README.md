Nama : Alysa Meliana  
NIM  : F1D02310035  
Mata Kuliah : Pemrograman Visual 

# myMemoria | The Art of Remembering
myMemoria adalah aplikasi desktop berbasis PySide6 yang digunakan untuk mencatat dan mengelola cerita atau catatan harian (diary). Aplikasi ini dirancang dengan konsep sederhana dan juga dengan tampilan yang mudah untuk digunakan oleh pengguna.

## Deskripsi Aplikasi
myMemoria adalah aplikasi diary digital yang dapat digunakan seperti antara lain menulis cerita harian, mengelola catatan (tambah, edit, hapus), mencari catatan berdasarkan judul, mengekspor dan mengimpor catatan ke file TXT dan PDF catatan.

## Fitur Aplikasi

### CRUD (Create, Read, Update, Delete)
-Tambah story baru
-Lihat daftar story
-Edit story
-Hapus story

### Fitur Search
Fitur search digunakan untuk mencari catatan atau story berdasarkan judul catatan harian.

### Import & Export
Untuk mengexport dan juga mengimport file ke `.txt` dan `.pdf`

### UI & Styling
Aplikasi ini menggunakan PySide6 dan styling dengan QSS dengan tema tampilan yang identik berwarna pink.


## Database
Menggunakan SQLite (`myMemoria.db`) dengan tabel yaitu:
-id (INTEGER, PRIMARY KEY)
-tanggal (TEXT)
-judul (TEXT)
-isi_catatan (TEXT)
-kategori (TEXT)
-mood (TEXT)

## Struktur Project (Separation of Concerns)
Project ini menerapkan prinsip Separation of Concerns (SoC), yaitu memisahkan setiap bagian program agar kode rapi dan mudah dikembangkan. Struktur project dibagi menjadi beberapa bagian:
-Database yg berisi file `database.py` untuk membuat koneksi SQLite, membuat tabel database, operasi CRUD (Create, Read, Update, Delete), dan query pencarian data
-Controllers yg berisi file `diary_controller.py` sebagai penghubung antara UI dan database, seperti mengatur alur data dari UI ke database dan enangani logika aplikasi
-ui berisi `main_window.py`, `dialog_form.py`, `search_dialog.py`  sebagai tampilan utama aplikasi, form tambah/edit story, dan dialog pencarian
-styles berisi file `main.qss` yang digunakan untuk styling tampilan aplikasi agar lebih menarik.
-main.py sebagai entry point utama aplikasi yang berfungsi untuk menjalankan aplikasi PySide6 serta menghubungkan semua komponen UI, controller, database, styling.