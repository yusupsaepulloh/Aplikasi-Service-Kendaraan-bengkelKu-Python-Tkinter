import tkinter as tk
from tkinter import font

class Sidebar(tk.Frame):
    def __init__(self, parent, root, callback, role):
        super().__init__(root, bg="#1c1a16", width=200)
        self.pack(side="left", fill="y")
        self.callback = callback
        self.role = role

        self.custom_font = font.Font(family="Arial", size=11, weight="bold")
        self.menu_font = font.Font(family="Arial", size=11)

        self.create_buttons()


    def create_buttons(self):
        # Tombol Beranda
        tk.Button(
            self, text="🏠 Beranda", anchor="w", bg="#ededed", fg="#1c1a16", bd=0,
            font=self.menu_font, command=lambda: self.callback("Beranda")
        ).pack(fill="x", padx=10, pady=(10, 0))

        # Frame Input Data Bengkel
        if self.role == "admin":
            frame_input = tk.Frame(self, bg="#1c1a16", bd=1, relief="solid")
            frame_input.pack(padx=5, pady=10, fill="x")

            tk.Label(frame_input, text="📁 Input Data Bengkel", font=self.custom_font,
                     bg="#ff1100", fg="white", anchor="w").pack(fill="x", pady=(0, 5), padx=5)

            tk.Button(frame_input, text="👥 Data Mekanik", font=self.menu_font, anchor="w", bg="#ededed", fg="#1c1a16", bd=0,
                          command=lambda: self.callback("Data Mekanik")).pack(fill="x", padx=10, pady=2)

            tk.Button(frame_input, text="⚙️ Data Sparepart", font=self.menu_font, anchor="w", bg="#ededed", fg="#1c1a16", bd=0,
                          command=lambda: self.callback("Data Sparepart")).pack(fill="x", padx=10, pady=2)

        # Frame Transaksi
        frame_trans = tk.Frame(self, bg="#1c1a16", bd=1, relief="solid")
        frame_trans.pack(padx=5, pady=10, fill="x")

        tk.Label(frame_trans, text="📁 Input Data Transaksi", font=self.custom_font,
                 bg="#ff1100", fg="white", anchor="w").pack(fill="x", pady=(0, 5), padx=5)

        tk.Button(frame_trans, text="🛠️ Data Service", font=self.menu_font, anchor="w", bg="#ededed", fg="#1c1a16", bd=0,
                  command=lambda: self.callback("Data Service")).pack(fill="x", padx=10, pady=2)

        tk.Button(frame_trans, text="📄 Laporan Transaksi", font=self.menu_font, anchor="w", bg="#ededed", fg="#1c1a16", bd=0,
                  command=lambda: self.callback("Laporan Transaksi")).pack(fill="x", padx=10, pady=2)

        # Frame Kelola Akun
        frame_akun = tk.Frame(self, bg="#1c1a16", bd=1, relief="solid")
        frame_akun.pack(padx=5, pady=10, fill="x")

        tk.Label(frame_akun, text="👤 Akun", font=self.custom_font,
                 bg="#ff1100",fg="white", anchor="w").pack(fill="x", pady=(0, 5), padx=5)

        if self.role == "admin":
            tk.Button(frame_akun, text="🔑 Kelola Akun", font=self.menu_font, anchor="w",
                      bg="#ededed", fg="#1c1a16", bd=0,
                      command=lambda: self.callback("Kelola Akun")).pack(fill="x", padx=10, pady=2)

        # Tombol Logout
        tk.Button(frame_akun, text="🔙 Logout", font=self.menu_font, anchor="w", bg="#ededed", fg="#1c1a16", bd=0,
                  command=lambda: self.callback("Logout")).pack(fill="x", padx=10, pady=2)
