import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from db import koneksi

class BerandaFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#c9c9c9")
        self.pack(fill="both", expand=True)

        tk.Label(self, text="Selamat Datang di BengkelKu", font=("Arial", 16, "bold"), bg="#c9c9c9").pack(pady=50)
        tk.Label(self, text="📊 Grafik Transaksi Sparepart", font=("Arial", 11), bg="#c9c9c9").pack(pady=0)

        self.tampilkan_grafik_sparepart()

    def tampilkan_grafik_sparepart(self):
        try:
            db = koneksi()
            cursor = db.cursor()
            cursor.execute("""
                SELECT s.nama, SUM(sr.qty) as total_terjual
                FROM service sr
                JOIN sparepart s ON sr.sparepart_id = s.id
                GROUP BY sr.sparepart_id
                ORDER BY total_terjual DESC
            """)
            hasil = cursor.fetchall()
            db.close()
        except Exception as e:
            tk.Label(self, text=f"Gagal mengambil data: {e}", fg="red", bg="#c9c9c9").pack()
            return

        if not hasil:
            tk.Label(self, text="Tidak ada data sparepart terjual", fg="gray", bg="#c9c9c9").pack()
            return

        nama_sparepart = [row[0] for row in hasil]
        total_terjual = [row[1] for row in hasil]

        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.bar(nama_sparepart, total_terjual, color="#FF9800")
        ax.set_xlabel("Sparepart", fontsize=10)
        ax.set_ylabel("Jumlah Terjual", fontsize=10)
        ax.tick_params(axis='x', labelrotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=10, pady=10)

