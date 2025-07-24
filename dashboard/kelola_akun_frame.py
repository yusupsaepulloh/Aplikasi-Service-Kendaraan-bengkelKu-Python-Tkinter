import tkinter as tk
from tkinter import ttk, messagebox
from db import koneksi

class KelolaAkunFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#c9c9c9")
        self.pack(fill="both", expand=True)
        self.selected_id = None
        self.build_ui()
        self.load_data()

    def build_ui(self):
        tk.Label(self, text="Kelola Akun", font=("Arial", 18, "bold"), bg="#c9c9c9").pack(pady=10)

        form_frame = tk.Frame(self, bg="#c9c9c9")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Username:", bg="#c9c9c9").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_username = tk.Entry(form_frame, width=30)
        self.entry_username.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Password:", bg="#c9c9c9").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_password = tk.Entry(form_frame, width=30, show="*")
        self.entry_password.grid(row=1, column=1, padx=5)

        tk.Label(form_frame, text="Role:", bg="#c9c9c9").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combo_role = ttk.Combobox(form_frame, values=["admin", "petugas"], state="readonly", width=28)
        self.combo_role.grid(row=2, column=1, padx=5)

        # Tombol aksi
        btn_frame = tk.Frame(self, bg="#c9c9c9")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Simpan", command=self.simpan, bg="#4CAF50", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_data, bg="#2196F3", fg="white", width=10).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Hapus", command=self.hapus, bg="#F44336", fg="white", width=10).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Batal", command=self.reset_form, bg="#9E9E9E", fg="white", width=10).pack(side="left", padx=5)

        # Treeview
        tree_frame = tk.Frame(self, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "username", "password", "role"), show="headings")
        for col in ("id", "username", "password", "role"):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")
        self.tree.column("id", width=50)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.on_row_double_click)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        db = koneksi()
        cursor = db.cursor()
        cursor.execute("SELECT id_user, username, password, role FROM akun_login")
        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)
        db.close()

    def simpan(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        role = self.combo_role.get().strip()

        if not username or not password or not role:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return

        db = koneksi()
        cursor = db.cursor()

        if self.selected_id:  # Update
            cursor.execute("UPDATE akun_login SET username=%s, password=%s, role=%s WHERE id_user=%s",
                           (username, password, role, self.selected_id))
        else:  # Insert
            cursor.execute("INSERT INTO akun_login (username, password, role) VALUES (%s, %s, %s)",
                           (username, password, role))

        db.commit()
        db.close()

        self.load_data()
        self.reset_form()
        messagebox.showinfo("Sukses", "Data berhasil disimpan.")

    def update_data(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin diperbarui.")
            return

        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        role = self.combo_role.get().strip()

        if not username or not password or not role:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return

        db = koneksi()
        cursor = db.cursor()
        cursor.execute("UPDATE akun_login SET username=%s, password=%s, role=%s WHERE id_user=%s",
                       (username, password, role, self.selected_id))
        db.commit()
        db.close()

        self.load_data()
        self.reset_form()
        messagebox.showinfo("Sukses", "Data berhasil diperbarui.")

    def hapus(self):
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus.")
            return

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus akun ini?"):
            db = koneksi()
            cursor = db.cursor()
            cursor.execute("DELETE FROM akun_login WHERE id_user=%s", (self.selected_id,))
            db.commit()
            db.close()

            self.load_data()
            self.reset_form()
            messagebox.showinfo("Sukses", "Data berhasil dihapus.")

    def reset_form(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.combo_role.set("")
        self.selected_id = None

    def on_row_double_click(self, event):
        selected = self.tree.selection()
        if selected:
            data = self.tree.item(selected[0])["values"]
            self.selected_id = data[0]
            self.entry_username.delete(0, tk.END)
            self.entry_username.insert(0, data[1])
            self.entry_password.delete(0, tk.END)
            self.entry_password.insert(0, data[2])
            self.combo_role.set(data[3])
