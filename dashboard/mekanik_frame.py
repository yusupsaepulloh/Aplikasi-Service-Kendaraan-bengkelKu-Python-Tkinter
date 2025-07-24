import tkinter as tk
from tkinter import ttk, messagebox
from db import koneksi

class MekanikFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#c9c9c9")
        self.master = master
        self.selected_id = None
        self.pack(fill="both", expand=True)
        self.build_ui()
        self.load_data()

    def build_ui(self):
        tk.Label(self, text="Data Mekanik", font=("Arial", 18, "bold"), bg="#c9c9c9").pack(pady=10)

        main_frame = tk.Frame(self, bg="#c9c9c9")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Kiri: Form input
        form_frame = tk.Frame(main_frame, bg="#c9c9c9")
        form_frame.pack(side="left", fill="y", padx=(0, 20))

        tk.Label(form_frame, text="Nama Mekanik:", bg="#c9c9c9", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nama = tk.Entry(form_frame, width=30)
        self.entry_nama.grid(row=0, column=1, pady=5)

        # Tombol aksi
        btn_frame = tk.Frame(form_frame, bg="#c9c9c9")
        btn_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.btn_simpan = tk.Button(btn_frame, text="Simpan", command=self.tambah_data, bg="#4CAF50", fg="white", width=10)
        self.btn_simpan.pack(side="left", padx=5)

        self.btn_update = tk.Button(btn_frame, text="Update", command=self.ubah_data, bg="#2196F3", fg="white", width=10)
        self.btn_update.pack(side="left", padx=5)

        self.btn_hapus = tk.Button(btn_frame, text="Hapus", command=self.hapus_data, bg="#F44336", fg="white", width=10)
        self.btn_hapus.pack(side="left", padx=5)

        self.btn_batal = tk.Button(btn_frame, text="Batal", command=self.bersihkan_form, bg="#9E9E9E", fg="white", width=10)
        self.btn_batal.pack(side="left", padx=5)

        # Kanan: Treeview
        tree_frame = tk.Frame(main_frame, bg="white")
        tree_frame.pack(side="right", fill="both", expand=True)

        scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Nama"),
            show="headings",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nama", text="Nama Mekanik")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nama", width=200, anchor="w")

        self.tree.pack(fill="both", expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        self.tree.bind("<Double-1>", self.on_double_click)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        db = koneksi()
        cursor = db.cursor()
        cursor.execute("SELECT id, nama FROM mekanik")
        for id_mekanik, nama in cursor.fetchall():
            self.tree.insert('', 'end', iid=id_mekanik, values=(id_mekanik, nama))
        db.close()

    def tambah_data(self):
        nama = self.entry_nama.get().strip()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama mekanik harus diisi")
            return

        db = koneksi()
        cursor = db.cursor()
        cursor.execute("INSERT INTO mekanik (nama) VALUES (%s)", (nama,))
        db.commit()
        db.close()

        self.bersihkan_form()
        self.load_data()

    def ubah_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data dari tabel yang ingin diubah.")
            return

        nama = self.entry_nama.get().strip()
        if not nama:
            messagebox.showwarning("Peringatan", "Nama mekanik harus diisi")
            return

        db = koneksi()
        cursor = db.cursor()
        cursor.execute("UPDATE mekanik SET nama=%s WHERE id=%s", (nama, self.selected_id))
        db.commit()
        db.close()

        self.bersihkan_form()
        self.load_data()

    def hapus_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?")
        if confirm:
            db = koneksi()
            cursor = db.cursor()
            cursor.execute("DELETE FROM mekanik WHERE id=%s", (self.selected_id,))
            db.commit()
            db.close()

            self.bersihkan_form()
            self.load_data()

    def on_double_click(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_id = selected_item[0]
            nama = self.tree.item(self.selected_id)['values'][1]
            self.entry_nama.delete(0, tk.END)
            self.entry_nama.insert(0, nama)

    def bersihkan_form(self):
        self.entry_nama.delete(0, tk.END)
        self.selected_id = None
