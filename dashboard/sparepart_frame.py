import tkinter as tk
from tkinter import ttk, messagebox
from db import koneksi


class SparepartFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#c9c9c9")
        self.master = master
        self.pack(fill="both", expand=True)
        self.selected_id = None
        self.build_ui()
        self.load_data()

    def build_ui(self):
        # Judul Halaman
        tk.Label(self, text="Data Sparepart", font=("Arial", 18, "bold"), bg="#c9c9c9").pack(pady=10)

        # Form Input
        form = tk.Frame(self, bg="#c9c9c9")
        form.pack(anchor="w", padx=20, pady=10)

        # Baris 1: Nama Sparepart
        tk.Label(form, text="Nama Sparepart:", bg="#c9c9c9", anchor="w", width=15).grid(row=0, column=0, sticky="w",
                                                                                      pady=5)
        self.entry_nama = tk.Entry(form, width=40)
        self.entry_nama.grid(row=0, column=1, pady=5, padx=5)

        # Baris 2: Stok
        tk.Label(form, text="Stok:", bg="#c9c9c9", anchor="w", width=15).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_stok = tk.Entry(form, width=40)
        self.entry_stok.grid(row=1, column=1, pady=5, padx=5)

        # Baris 3: Harga
        tk.Label(form, text="Harga:", bg="#c9c9c9", anchor="w", width=15).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_harga = tk.Entry(form, width=40)
        self.entry_harga.grid(row=2, column=1, pady=5, padx=5)

        # Baris 4: Harga Jasa
        tk.Label(form, text="Harga Jasa:", bg="#c9c9c9", anchor="w", width=15).grid(row=3, column=0, sticky="w", pady=5)
        self.entry_hargaJasa = tk.Entry(form, width=40)
        self.entry_hargaJasa.grid(row=3, column=1, pady=5, padx=5)

        # Baris Tombol (di baris ke-5, kolom penuh)
        button_frame = tk.Frame(form, bg="#c9c9c9")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_simpan = tk.Button(button_frame, text="Simpan", width=12, bg="#4CAF50", fg="white",
                                    command=self.simpan_data)
        self.btn_simpan.pack(side="left", padx=5)

        self.btn_update = tk.Button(button_frame, text="Update", width=12, bg="#2196F3", fg="white",
                                    command=self.update_data)
        self.btn_update.pack(side="left", padx=5)

        self.btn_hapus = tk.Button(button_frame, text="Hapus", width=12, bg="#F44336", fg="white",
                                   command=self.hapus_data)
        self.btn_hapus.pack(side="left", padx=5)

        self.btn_batal = tk.Button(button_frame, text="Batal", width=12, bg="#9E9E9E", fg="white",
                                   command=self.clear_form)
        self.btn_batal.pack(side="left", padx=5)

        # Treeview
        tree_frame = tk.Frame(self, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Nama", "Stok", "Harga", "HargaJasa"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nama", text="Sparepart")
        self.tree.heading("Stok", text="Stok")
        self.tree.heading("Harga", text="Harga")
        self.tree.heading("HargaJasa", text="Harga Jasa")

        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Nama", width=200, anchor="w")
        self.tree.column("Stok", width=100, anchor="center")
        self.tree.column("Harga", width=120, anchor="e")
        self.tree.column("HargaJasa", width=120, anchor="e")

        self.tree.pack(fill="both", expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        self.tree.bind("<Double-1>", self.on_double_click)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        db = koneksi()
        cursor = db.cursor()
        cursor.execute("SELECT id, nama, stok, harga, harga_jasa FROM sparepart")
        for id_sp, nama, stok, harga, harga_jasa in cursor.fetchall():
            self.tree.insert('', 'end', iid=id_sp, values=(id_sp, nama, stok, harga, harga_jasa))
        db.close()

    def simpan_data(self):
        nama = self.entry_nama.get().strip()
        stok = self.entry_stok.get().strip()
        harga = self.entry_harga.get().strip()
        harga_jasa = self.entry_hargaJasa.get().strip()

        if not nama or not stok or not harga or not harga_jasa:
            messagebox.showwarning("Peringatan", "Semua field harus diisi")
            return

        db = koneksi()
        cursor = db.cursor()
        if self.selected_id:
            cursor.execute("UPDATE sparepart SET nama=%s, stok=%s, harga=%s, harga_jasa=%s WHERE id=%s",
                           (nama, stok, harga, harga_jasa, self.selected_id))

        else:
            cursor.execute("INSERT INTO sparepart (nama, stok, harga, harga_jasa) VALUES (%s, %s, %s, %s)",
                           (nama, stok, harga, harga_jasa))

        db.commit()
        db.close()

        self.clear_form()
        self.load_data()

    def update_data(self):

        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data dari tabel untuk di-update.")
            return

        nama = self.entry_nama.get().strip()
        stok = self.entry_stok.get().strip()
        harga = self.entry_harga.get().strip()
        harga_jasa = self.entry_hargaJasa.get().strip()

        if not nama or not stok or not harga or not harga_jasa:
            messagebox.showwarning("Peringatan", "Semua field harus diisi")
            return

        db = koneksi()
        cursor = db.cursor()
        cursor.execute("UPDATE sparepart SET nama=%s, stok=%s, harga=%s, harga_jasa=%s WHERE id=%s",
                       (nama, stok, harga, harga_jasa, self.selected_id))
        db.commit()
        db.close()

        self.clear_form()
        self.load_data()
        messagebox.showinfo("Sukses", "Data berhasil diupdate")

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data dari tabel untuk dihapus.")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus sparepart ini?"):
            db = koneksi()
            cursor = db.cursor()
            cursor.execute("DELETE FROM sparepart WHERE id=%s", (self.selected_id,))
            db.commit()
            db.close()

            self.clear_form()
            self.load_data()
            messagebox.showinfo("Sukses", "Data berhasil dihapus")

    def on_double_click(self, event):
        selected_item = self.tree.selection()[0]
        self.selected_id = selected_item
        values = self.tree.item(selected_item)['values']

        # Kosongkan semua field sebelum mengisi ulang
        self.entry_nama.delete(0, tk.END)
        self.entry_stok.delete(0, tk.END)
        self.entry_harga.delete(0, tk.END)
        self.entry_hargaJasa.delete(0, tk.END)

        # Masukkan data ke field
        self.entry_nama.insert(0, values[1])
        self.entry_stok.insert(0, values[2])
        self.entry_harga.insert(0, values[3])
        self.entry_hargaJasa.insert(0, values[4])

    def clear_form(self):
        self.entry_nama.delete(0, tk.END)
        self.entry_stok.delete(0, tk.END)
        self.entry_harga.delete(0, tk.END)
        self.entry_hargaJasa.delete(0, tk.END)
        self.selected_id = None


