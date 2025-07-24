import tkinter as tk
from tkinter import ttk, messagebox
from db import koneksi
import threading

class LoginFrame(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.master.title("Sistem Informasi BengkelKu")
        self.master.geometry("900x600")
        self.master.configure(bg="#ffffff")
        self.pack(fill="both", expand=True)

        self.setup_styles()

        main_container = ttk.Frame(self, style="Main.TFrame")
        main_container.pack(fill="both", expand=True, padx=50, pady=50)

        left_panel = ttk.Frame(main_container, style="Illustration.TFrame")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 30))
        self.create_illustration(left_panel)

        right_panel = ttk.Frame(main_container, style="Card.TFrame")
        right_panel.pack(side="right", fill="both", expand=True, padx=(30, 0))

        form_container = ttk.Frame(right_panel, style="Card.TFrame")
        form_container.pack(expand=True, padx=50, pady=60)
        self.create_login_form(form_container)
        self.username_entry.focus()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Main.TFrame", background="#ffffff")
        self.style.configure("Illustration.TFrame", background="#f5f5f7")
        self.style.configure("Card.TFrame", background="#ffffff", borderwidth=1,
                             relief="solid", bordercolor="#eaeaea")
        self.style.configure("Title.TLabel", background="#ffffff",
                             font=("Segoe UI", 24, "bold"), foreground="#1c1a16")
        self.style.configure("Subtitle.TLabel", background="#ffffff",
                             font=("Segoe UI", 12), foreground="#666666")
        self.style.configure("Label.TLabel", background="#ffffff",
                             font=("Segoe UI", 10, "bold"), foreground="#1c1a16")
        self.style.configure("Footer.TLabel", background="#ffffff",
                             font=("Segoe UI", 9), foreground="#888888")
        self.style.configure("Error.TLabel", background="#ffffff",
                             font=("Segoe UI", 9), foreground="red")
        self.style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"),
                             foreground="white", background="#ff1100",
                             borderwidth=0, padding=10)
        self.style.map("Accent.TButton",
                       background=[("active", "#e00e00"), ("pressed", "#cc0d00")],
                       foreground=[("active", "white"), ("pressed", "white")])

    def create_illustration(self, parent):
        container = ttk.Frame(parent, style="Illustration.TFrame")
        container.pack(expand=True, fill="both", padx=40, pady=40)
        ttk.Label(container, text="BengkelKu", style="Title.TLabel",
                  foreground="#ff1100").pack(pady=(0, 10))
        ttk.Label(container, text="Sistem Manajemen Bengkel Terintegrasi",
                  style="Subtitle.TLabel").pack(pady=(0, 40))
        img_placeholder = tk.Canvas(container, bg="#f5f5f7", highlightthickness=0,
                                    width=300, height=250)
        img_placeholder.pack()
        img_placeholder.create_rectangle(50, 100, 250, 150, fill="#e0e0e0", outline="")
        img_placeholder.create_oval(70, 140, 110, 180, fill="#1c1a16", outline="")
        img_placeholder.create_oval(190, 140, 230, 180, fill="#1c1a16", outline="")
        img_placeholder.create_rectangle(150, 70, 200, 100, fill="#ff1100", outline="")

        features = [
            "✓ Manajemen Pelanggan & Kendaraan",
            "✓ Pencatatan Servis & Transaksi",
            "✓ Manajemen Inventori Sparepart",
            "✓ Laporan Transaksi"
        ]
        for feature in features:
            ttk.Label(container, text=feature, style="Subtitle.TLabel",
                      foreground="#1c1a16").pack(anchor="w", pady=5)

    def create_login_form(self, parent):
        ttk.Label(parent, text="Login Aplikasi BengkelKu", style="Title.TLabel").pack(pady=(0, 30))

        username_frame = ttk.Frame(parent, style="Card.TFrame")
        username_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(username_frame, text="Username", style="Label.TLabel").pack(anchor="w", padx=5)
        self.username_entry = ttk.Entry(username_frame, font=("Segoe UI", 11), width=30)
        self.username_entry.pack(fill="x", padx=5, pady=5, ipady=8)

        password_frame = ttk.Frame(parent, style="Card.TFrame")
        password_frame.pack(fill="x", pady=(0, 25))
        ttk.Label(password_frame, text="Password", style="Label.TLabel").pack(anchor="w", padx=5)
        self.password_entry = ttk.Entry(password_frame, show="*", font=("Segoe UI", 11), width=30)
        self.password_entry.pack(fill="x", padx=5, pady=5, ipady=8)

        login_btn = ttk.Button(parent, text="Login", command=self.login, style="Accent.TButton", width=20)
        login_btn.pack(pady=10)

        self.error_label = ttk.Label(parent, text="", style="Error.TLabel")
        self.error_label.pack(pady=(5, 0))

        footer = ttk.Label(parent, text="© 2025 BengkelKu System v1.0", style="Footer.TLabel")
        footer.pack(side="bottom", pady=(30, 0))

        self.password_entry.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        self.error_label.config(text="")

        if not username or not password:
            self.error_label.config(text="Username dan Password wajib diisi!")
            return

        def do_login():
            try:
                db = koneksi()
                cursor = db.cursor()
                cursor.execute("SELECT role FROM akun_login WHERE username=%s AND password=%s", (username, password))
                result = cursor.fetchone()
                cursor.close()
                db.close()

                if result:
                    role = result[0]
                    self.after(100, lambda: [self.destroy(), self.on_login_success(username, role)])
                else:
                    self.after(0, lambda: self.error_label.config(text="Username atau password salah!"))
            except Exception as e:
                self.after(0, lambda: self.error_label.config(text=f"Error: {e}"))

        threading.Thread(target=do_login).start()


class HomeFrame(tk.Frame):
    def __init__(self, master, username, role):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        ttk.Label(self, text=f"Selamat datang, {username}!", font=("Segoe UI", 20)).pack(pady=20)
        ttk.Label(self, text=f"Role Anda: {role}", font=("Segoe UI", 14)).pack(pady=10)


def on_login_success(username, role):
    for widget in root.winfo_children():
        widget.destroy()
    HomeFrame(root, username, role)


if __name__ == "__main__":
    root = tk.Tk()
    LoginFrame(root, on_login_success)
    root.mainloop()
