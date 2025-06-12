# tugas-besar-perpustakaan
Aplikasi ini merupakan mini project Python berbasis GUI (Graphical User Interface) menggunakan **CustomTkinter** dan array statis. Program ini dibuat untuk mendemonstrasikan bagaimana data buku bisa dikelola secara manual dalam struktur array statis, termasuk fitur pencarian, pengurutan, penambahan, penghapusan, dan impor data dari file `.csv`.
Fitur Utama
- Tambah buku baru
- Hapus buku berdasarkan judul
- Cari buku berdasarkan judul atau pengarang
- Urutkan buku berdasarkan judul (A-Z, Z-A) atau tahun (terbaru, terlama)
- Impor data buku dari file `.csv`
- Tampilan antarmuka berbasis GUI menggunakan **CustomTkinter**
Teknologi & Library
- Python 3.x
- CustomTkinter
- Tkinter (bawaan Python)
- CSV
- Dataclass
Struktur Data
- Menggunakan **array statis** (maksimum 115 data)
- Tipe data bentukan (`@dataclass`) untuk merepresentasikan buku
Cara Menjalankan
1. Pastikan Python 3 dan pip sudah terinstal
2. Install `customtkinter` jika belum:
   ```bash
   pip install customtkinter
