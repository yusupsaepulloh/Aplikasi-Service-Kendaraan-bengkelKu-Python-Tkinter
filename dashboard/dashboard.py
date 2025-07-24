import tkinter as tk
from login import LoginFrame
from .sidebar import Sidebar
from .beranda import BerandaFrame
from .topbar import TopBar
from tkinter import messagebox

class Dashboard:
    def __init__(self, root, username, role):
        super().__init__()
        self.root = root
        self.username = username
        self.role = role

        self.root.title(f"Sistem Informasi BengkelKu - {username} ({role})")
        root.state('zoomed')

        # 🔵 Tambahkan topbar
        self.topbar = TopBar(self.root, "Beranda", self.logout)

        # 🟦 Sidebar
        self.sidebar = Sidebar(self, root, self.load_frame, role=self.role)

        # 🟩 Area konten
        self.content_frame = tk.Frame(root, bg="#c9c9c9")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.load_frame("Beranda")

    def load_frame(self, name):
        self.topbar.update_title(name)

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if name == "Beranda":
            from .beranda import BerandaFrame
            BerandaFrame(self.content_frame)
        elif name == "Data Mekanik":
            from .mekanik_frame import MekanikFrame
            MekanikFrame(self.content_frame)
        elif name == "Data Sparepart":
            from .sparepart_frame import SparepartFrame
            SparepartFrame(self.content_frame)
        elif name == "Data Service":
            from .service_frame import ServiceFrame
            ServiceFrame(self.content_frame)
        elif name == "Laporan Transaksi":
            from .laporan_frame import LaporanFrame
            LaporanFrame(self.content_frame, self.role)
        elif name == "Kelola Akun":
            from .kelola_akun_frame import KelolaAkunFrame
            KelolaAkunFrame(self.content_frame)
        elif name == "Logout":
            self.logout()

    def logout(self):
        confirm = messagebox.askyesno("Konfirmasi Logout", "Apakah Anda yakin ingin logout?")
        if confirm:
            for widget in self.root.winfo_children():
                widget.destroy()
            LoginFrame(self.root, lambda username, role: Dashboard(self.root, username, role))
