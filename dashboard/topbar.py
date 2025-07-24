import tkinter as tk
from datetime import datetime

class TopBar(tk.Frame):
    def __init__(self, parent, title, on_logout_callback):
        super().__init__(parent, bg="#FFFFFF")
        self.config(height=50)
        self.pack(fill="x", side="top")
        self.pack_propagate(False)

        self.on_logout_callback = on_logout_callback

        # Judul kiri
        self.title_label = tk.Label(self, text=title, bg="#FFFFFF", fg="#000000",
                                    font=("Arial", 14, "bold"))
        self.title_label.pack(side="left", padx=20)

        # Tanggal kanan
        tanggal = datetime.now().strftime("%A, %d-%m-%Y")
        self.date_label = tk.Label(self, text=tanggal, bg="#FFFFFF", fg="#000000", font=("Arial", 10))
        self.date_label.pack(side="right", padx=10)



    def update_title(self, new_title):
        self.title_label.config(text=new_title)
