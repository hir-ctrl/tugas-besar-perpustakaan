import csv
from tkinter import filedialog

import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from dataclasses import dataclass

# --- Struktur Data dan Array Statis ---
@dataclass
class Buku:
    judul: str
    pengarang: str
    tahun: int
    kategori: str

MAX_BUKU = 115
data_buku = [None] * MAX_BUKU
jumlah_buku = 0

# Fungsi Impor
def import_csv():
    global jumlah_buku

    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if jumlah_buku >= MAX_BUKU:
                    messagebox.showwarning("Penuh", "Data buku sudah mencapai kapasitas maksimum.")
                    break

                try:
                    tahun = int(row["Tahun"])
                except ValueError:
                    continue  # skip baris kalau tahunnya bukan angka

                buku_baru = Buku(
                    judul=row["Judul"],
                    pengarang=row["Pengarang"],
                    tahun=tahun,
                    kategori=row["Kategori"]
                )

                data_buku[jumlah_buku] = buku_baru
                jumlah_buku += 1

        tampilkan_buku()
        messagebox.showinfo("Berhasil", "Data CSV berhasil dimuat.")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membaca file: {e}")

# --- Fungsi Tambah Buku ---
def tambah_buku():
    global jumlah_buku

    if jumlah_buku >= MAX_BUKU:
        messagebox.showwarning("Penuh", "Data buku sudah mencapai batas maksimum.")
        return

    try:
        tahun = int(entry_tahun.get())
    except ValueError:
        messagebox.showerror("Input Salah", "Tahun harus berupa angka.")
        return

    buku_baru = Buku(
        judul=entry_judul.get(),
        pengarang=entry_pengarang.get(),
        tahun=tahun,
        kategori=entry_kategori.get()
    )

    data_buku[jumlah_buku] = buku_baru
    jumlah_buku += 1
    tampilkan_buku()
    kosongkan_form()

# --- Fungsi Tampilkan Buku ---
def tampilkan_buku(data=None):
    # Bersihkan isi treeview
    for row in tree.get_children():
        tree.delete(row)

    if data is None:
        # Tampilkan semua data
        for i in range(jumlah_buku):
            b = data_buku[i]
            tree.insert("", "end", values=(b.judul, b.pengarang, b.tahun, b.kategori))
    else:
        # Tampilkan hasil pencarian dengan tag warna
        for b in data:
            tree.insert("", "end", values=(b.judul, b.pengarang, b.tahun, b.kategori), tags=('highlight',))

# --- Fungsi Kosongkan Form ---
def kosongkan_form():
    entry_judul.delete(0, ctk.END)
    entry_pengarang.delete(0, ctk.END)
    entry_tahun.delete(0, ctk.END)
    entry_kategori.delete(0, ctk.END)

# --- Fungsi Urutkan dan Tampilkan Buku Berdasarkan Pilihan ---
def urutkan_buku(pilihan):
    global data_buku

    data_valid = [b for b in data_buku[:jumlah_buku] if b is not None]

    if pilihan == "A-Z":
        data_valid.sort(key=lambda b: b.judul.lower())
    elif pilihan == "Z-A":
        data_valid.sort(key=lambda b: b.judul.lower(), reverse=True)
    elif pilihan == "Terbaru":
        data_valid.sort(key=lambda b: b.tahun, reverse=True)
    elif pilihan == "Terlama":
        data_valid.sort(key=lambda b: b.tahun)

    # Tampilkan data yang sudah diurutkan
    for row in tree.get_children():
        tree.delete(row)

    for b in data_valid:
        tree.insert("", "end", values=(b.judul, b.pengarang, b.tahun, b.kategori))
# --- Fungsi Hapus Buku ---
def hapus_buku():
    global jumlah_buku
    judul_hapus = entry_judul.get().lower()

    index = -1
    for i in range(jumlah_buku):
        if data_buku[i] and data_buku[i].judul.lower() == judul_hapus:
            index = i
            break

    if index == -1:
        messagebox.showerror("Tidak Ditemukan", "Judul buku tidak ditemukan.")
        return

    for i in range(index, jumlah_buku - 1):
        data_buku[i] = data_buku[i + 1]
    data_buku[jumlah_buku - 1] = None
    jumlah_buku -= 1

    tampilkan_buku()
    kosongkan_form()
    messagebox.showinfo("Berhasil", "Buku berhasil dihapus.")

# --- Fungsi Cari Buku ---
def cari_buku():
    keyword = entry_cari.get().lower()
    hasil = []

    for i in range(jumlah_buku):
        b = data_buku[i]
        if keyword in b.judul.lower() or keyword in b.pengarang.lower():
            hasil.append(b)

    if hasil:
        tampilkan_buku(hasil)
    else:
        messagebox.showinfo("Hasil Pencarian", "Buku tidak ditemukan.")

# --- GUI ---
ctk.set_appearance_mode("System")  # bisa diganti 'Light' atau 'Dark'
ctk.set_default_color_theme("blue")  # bisa diganti tema lain

root = ctk.CTk()
root.title("Aplikasi Perpustakaan Mini")
root.geometry("700x500")

# Frame Input
frame_input = ctk.CTkFrame(root)
frame_input.pack(pady=10)

ctk.CTkLabel(frame_input, text="Judul").grid(row=0, column=0, sticky="w", padx=5, pady=5)
ctk.CTkLabel(frame_input, text="Pengarang").grid(row=1, column=0, sticky="w", padx=5, pady=5)
ctk.CTkLabel(frame_input, text="Tahun").grid(row=2, column=0, sticky="w", padx=5, pady=5)
ctk.CTkLabel(frame_input, text="Kategori").grid(row=3, column=0, sticky="w", padx=5, pady=5)

entry_judul = ctk.CTkEntry(frame_input, width=300)
entry_pengarang = ctk.CTkEntry(frame_input, width=300)
entry_tahun = ctk.CTkEntry(frame_input, width=300)
entry_kategori = ctk.CTkEntry(frame_input, width=300)

entry_judul.grid(row=0, column=1, padx=10, pady=5)
entry_pengarang.grid(row=1, column=1, padx=10, pady=5)
entry_tahun.grid(row=2, column=1, padx=10, pady=5)
entry_kategori.grid(row=3, column=1, padx=10, pady=5)

btn_tambah = ctk.CTkButton(frame_input, text="Tambah Buku", command=tambah_buku)
btn_tambah.grid(row=4, column=1, pady=10,padx=(15,200))

btn_hapus = ctk.CTkButton(master=frame_input, text="Hapus Berdasarkan Judul", command=hapus_buku)
btn_hapus.grid(row=4, column=1, padx=(150,15), pady=5) 

btn_import = ctk.CTkButton(master=frame_input, text="Import(.csv)", command=import_csv)
btn_import.grid(row=6, column=1, pady=5,padx=(200,0))

# --- Frame Cari dan Urutkan ---
frame_cari = ctk.CTkFrame(master=root)
frame_cari.pack(pady=10)

entry_cari = ctk.CTkEntry(master=frame_cari, placeholder_text="Cari judul/pengarang...", width=300)
entry_cari.grid(row=0, column=0, padx=10, pady=(5,5))

btn_cari = ctk.CTkButton(master=frame_cari, text="Cari", command=cari_buku)
btn_cari.grid(row=0, column=1, padx=5,pady=(5,5))

# Dropdown Urutan
label_urut = ctk.CTkLabel(frame_input, text="Urutkan berdasarkan:")
label_urut.grid(row=5, column=0, padx=5, pady=10, sticky="w")

opsi_urutan = ["A-Z", "Z-A", "Terbaru", "Terlama"]
combo_urutan = ctk.CTkOptionMenu(frame_input, values=opsi_urutan, command=urutkan_buku)
combo_urutan.grid(row=5, column=1, padx=(15,10), pady=5, sticky="w")

# Frame Tabel
frame_tabel = ctk.CTkFrame(root)
frame_tabel.pack(pady=10, fill="both", expand=True)

kolom = ("Judul", "Pengarang", "Tahun", "Kategori")
tree = ttk.Treeview(frame_tabel, columns=kolom, show="headings", height=10)

for kol in kolom:
    tree.heading(kol, text=kol)
    tree.column(kol, width=150, anchor="center")

# tree.pack(padx=10, pady=10, fill="both", expand=True)
tree.pack(padx=10, pady=10, fill="both", expand=True)

# Konfigurasi tag untuk highlight biru
tree.tag_configure('highlight', background='lightblue')

root.mainloop()