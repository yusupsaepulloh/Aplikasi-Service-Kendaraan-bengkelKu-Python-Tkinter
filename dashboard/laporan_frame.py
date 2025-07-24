import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db import koneksi
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

class LaporanFrame(tk.Frame):
    def __init__(self, master, role):
        super().__init__(master, bg="#c9c9c9")
        self.pack(fill="both", expand=True)
        self.role = role
        self.build_ui()
        self.load_data()

    def build_ui(self):
        tk.Label(self, text="Laporan Servis BengkelKu", font=("Arial", 16, "bold"), bg="#c9c9c9").pack(pady=10)

        filter_frame = tk.Frame(self, bg="#c9c9c9")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Nama Pelanggan:", bg="#c9c9c9").pack(side="left", padx=(10, 0))
        self.entry_nama = tk.Entry(filter_frame, width=15)
        self.entry_nama.pack(side="left", padx=5)

        tk.Label(filter_frame, text="Plat Kendaraan:", bg="#c9c9c9").pack(side="left")
        self.entry_plat = tk.Entry(filter_frame, width=15)
        self.entry_plat.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Cari", command=self.cari_data, bg="#607D8B", fg="white").pack(side="left",
                                                                                                    padx=(10, 0))
        tk.Label(filter_frame, text="Cari Berdasarkan Tanggal:", bg="#c9c9c9").pack(side="left")

        self.entry_filter = DateEntry(filter_frame, width=12, background='darkblue',
                                      foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_filter.pack(side="left", padx=5)

        tk.Button(filter_frame, text="Tampilkan", command=self.filter_data, bg="#2196F3", fg="white").pack(side="left")
        tk.Button(filter_frame, text="Reset", command=self.load_data, bg="#FF9800", fg="white").pack(side="left", padx=5)
        if self.role == "admin":
            tk.Button(filter_frame, text="Hapus", command=self.hapus_data, bg="#F44336", fg="white").pack(side="left", padx=5)

        tk.Button(filter_frame, text="Cetak PDF", command=self.cetak_laporan, bg="#4CAF50", fg="white").pack(side="left", padx=5)

        # Treeview
        tree_frame = tk.Frame(self, bg="white")
        tree_frame.pack(fill="both", expand=True, pady=10)

        scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Tanggal", "Pelanggan", "Plat", "Mekanik", "Sparepart", "Qty", "Jasa", "Total"),
            show='headings',
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        self.tree.pack(fill="both", expand=True)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)



    def load_data(self, tanggal=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        db = koneksi()
        cursor = db.cursor()
        if tanggal:
            cursor.execute("""
                SELECT s.tanggal, s.nama_pelanggan, s.plat_kendaraan, m.nama, s2.nama, s.qty, s.harga_jasa, s.total
                FROM service s
                JOIN mekanik m ON s.mekanik_id = m.id
                JOIN sparepart s2 ON s.sparepart_id = s2.id
                WHERE DATE(s.tanggal) = %s
            """, (tanggal,))
        else:
            cursor.execute("""
                SELECT s.tanggal, s.nama_pelanggan, s.plat_kendaraan, m.nama, s2.nama, s.qty, s.harga_jasa, s.total
                FROM service s
                JOIN mekanik m ON s.mekanik_id = m.id
                JOIN sparepart s2 ON s.sparepart_id = s2.id
            """)

        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        db.close()

    def filter_data(self):
        tanggal = self.entry_filter.get()
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            self.load_data(tanggal)
        except ValueError:
            messagebox.showerror("Format Salah", "Tanggal tidak valid. Pilih dari kalender.")

    def cari_data(self):
        nama = self.entry_nama.get().strip()
        plat = self.entry_plat.get().strip()

        if not nama and not plat:
            messagebox.showwarning("Peringatan", "Masukkan Nama atau Plat untuk pencarian.")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        db = koneksi()
        cursor = db.cursor()

        query = """
            SELECT s.tanggal, s.nama_pelanggan, s.plat_kendaraan, m.nama, s2.nama, s.qty, s.harga_jasa, s.total
            FROM service s
            JOIN mekanik m ON s.mekanik_id = m.id
            JOIN sparepart s2 ON s.sparepart_id = s2.id
            WHERE 1=1
        """
        params = []

        if nama:
            query += " AND s.nama_pelanggan LIKE %s"
            params.append(f"%{nama}%")
        if plat:
            query += " AND s.plat_kendaraan LIKE %s"
            params.append(f"%{plat}%")

        cursor.execute(query, tuple(params))
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        db.close()

    def hapus_data(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih salah satu data yang ingin dihapus.")
            return

        konfirmasi = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?")
        if not konfirmasi:
            return

        try:
            item = self.tree.item(selected[0])['values']
            tanggal = item[0]
            pelanggan = item[1]
            plat = item[2]
            mekanik_nama = item[3]
            sparepart_nama = item[4]
            qty = int(item[5])
            harga_jasa = int(item[6])
            total = int(item[7])

            db = koneksi()
            cursor = db.cursor()
            cursor.execute("""
                DELETE FROM service 
                WHERE mekanik_id = (SELECT id FROM mekanik WHERE nama = %s)
                AND sparepart_id = (SELECT id FROM sparepart WHERE nama = %s)
                AND qty = %s AND harga_jasa = %s AND total = %s AND tanggal = %s
                AND nama_pelanggan = %s AND plat_kendaraan = %s
                LIMIT 1
            """, (mekanik_nama, sparepart_nama, qty, harga_jasa, total, tanggal, pelanggan, plat))
            db.commit()
            db.close()

            self.tree.delete(selected[0])
            messagebox.showinfo("Sukses", "Data berhasil dihapus.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus data:\n{e}")

    

    def cetak_laporan(self):
        try:
            filename = os.path.abspath(
                os.path.join("laporan", f"laporan_servis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"))
            os.makedirs("laporan", exist_ok=True)

            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            y = height - 40
            left = 50
            right = width - 50

            # Header
            c.setFont("Courier-Bold", 14)
            c.drawCentredString(width / 2, y, "LAPORAN SERVIS BENGKELKU")
            y -= 20
            c.setFont("Courier", 10)
            periode = datetime.now().strftime('%Y-%m-%d')
            c.drawCentredString(width / 2, y, f"Periode: {periode} s.d {periode}")
            y -= 40

            db = koneksi()
            cursor = db.cursor()
            cursor.execute("""
                SELECT s.id, s.tanggal, s.nama_pelanggan, s.plat_kendaraan,
                       m.nama AS mekanik, sp.nama AS sparepart, s.qty, s.harga_sparepart,
                       s.harga_jasa, s.total
                FROM service s
                JOIN mekanik m ON s.mekanik_id = m.id
                JOIN sparepart sp ON s.sparepart_id = sp.id
                ORDER BY s.id, s.tanggal
            """)
            data = cursor.fetchall()
            db.close()

            current_id = None
            subtotal = 0

            for row in data:
                id_servis, tanggal, nama, plat, mekanik, sparepart, qty, harga_sp, jasa, total = row

                if id_servis != current_id:
                    # Cetak subtotal sebelumnya
                    if current_id is not None:
                        y -= 5
                        c.setFont("Courier-Bold", 10)
                        c.drawRightString(width - 50, y, f"Subtotal: Rp{subtotal:,.0f}".replace(",", "."))
                        y -= 10
                        c.setFont("Courier", 10)
                        c.line(left, y, right, y)
                        y -= 12

                    # Halaman baru bila ruang kurang
                    if y < 120:
                        c.showPage()
                        y = height - 40

                    # Header transaksi
                    c.setFont("Courier-Bold", 10)
                    c.drawString(50, y, f"ID: {id_servis}    Tanggal: {tanggal.strftime('%Y-%m-%d')}")
                    y -= 15
                    c.setFont("Courier", 10)
                    c.drawString(50, y, f"Pelanggan : {nama}    Plat: {plat}")
                    y -= 15

                    # Judul kolom
                    c.drawString(60, y, "Mekanik")
                    c.drawString(130, y, "Sparepart")
                    c.drawString(250, y, "Qty x Harga")
                    c.drawString(350, y, "Jasa")
                    c.drawString(430, y, "Subtotal")
                    y -= 12
                    c.line(left, y, right, y)  # garis atas
                    y -= 12

                    current_id = id_servis

                subtotal += total
                qty_harga = f"{qty} x {harga_sp:,.0f}".replace(",", ".")
                total_fmt = f"Rp{total:,.0f}".replace(",", ".")
                jasa_fmt = f"Rp{jasa:,.0f}".replace(",", ".")

                # Baris data servis
                c.drawString(60, y, f"{mekanik:<10}")
                c.drawString(130, y, f"{sparepart:<20}")
                c.drawString(250, y, f"{qty_harga:<15}")
                c.drawString(350, y, f"{jasa_fmt:<10}")
                c.drawString(430, y, f"{total_fmt:<10}")

                y -= 12
                if y < 80:
                    c.showPage()
                    y = height - 40

            # Subtotal terakhir
            if current_id is not None:
                y -= 5
                c.setFont("Courier-Bold", 10)
                c.drawRightString(width - 50, y, f"Subtotal: Rp{subtotal:,.0f}".replace(",", "."))
                y -= 10
                c.setFont("Courier", 10)
                c.line(left, y, right, y)
                y -= 12

            c.save()
            messagebox.showinfo("Sukses", f"Laporan berhasil disimpan ke {filename}")
            os.startfile(filename) if os.name == 'nt' else os.system(f"open '{filename}'")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal mencetak laporan:\n{e}")


