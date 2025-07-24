import tkinter as tk
from tkinter import ttk, messagebox
from db import koneksi
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import platform
import subprocess

class ServiceFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#c9c9c9")
        self.pack(fill="both", expand=True)

        self.selected_temp_item = None
        self.total_var = tk.IntVar()
        self.bayar_var = tk.IntVar()
        self.kembali_var = tk.IntVar()
        self.total_sementara = 0

        self.build_ui()
        self.load_dropdowns()
        self.bayar_var.trace("w", lambda *args: self.hitung_kembalian())
        self.last_insert_ids = []
        style = ttk.Style()
        style.configure("Bayar.TButton", font=("Arial", 11, "bold"))

    def build_ui(self):
        tk.Label(self, text="Transaksi Servis", font=("Arial", 16, "bold"), bg="#c9c9c9").pack(pady=10)

        top_frame = tk.Frame(self, bg="#c9c9c9")
        top_frame.pack(pady=5, fill="x", padx=10)

        form = tk.Frame(top_frame, bg="#c9c9c9")
        form.pack(anchor="w")

        self.entry_id = tk.Entry(form)
        self.entry_id.grid(row=99, column=0)
        self.entry_id.grid_remove()

        horizontal_frame = tk.Frame(self, bg="#c9c9c9")
        horizontal_frame.pack(fill="x", padx=10)

        form = tk.Frame(horizontal_frame, bg="#c9c9c9")
        form.pack(side="left", anchor="n")

        # Nama pelanggan
        tk.Label(form, text="Nama Pelanggan:", bg="#c9c9c9").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_nama_pelanggan = tk.Entry(form, width=27)
        self.entry_nama_pelanggan.grid(row=0, column=1, padx=5, pady=2)

        # Plat kendaraan
        tk.Label(form, text="Plat Kendaraan:", bg="#c9c9c9").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_plat_kendaraan = tk.Entry(form, width=27)
        self.entry_plat_kendaraan.grid(row=1, column=1, padx=5, pady=2)

        # Mekanik
        tk.Label(form, text="Mekanik:", bg="#c9c9c9").grid(row=2, column=0, sticky="w", pady=2)
        self.combo_mekanik = ttk.Combobox(form, state="readonly", width=25)
        self.combo_mekanik.grid(row=2, column=1, padx=5, pady=2)
        tk.Button(form, text="Tambah", width=9, bg="#2196F3", fg="white", command=self.tambah).grid(row=2, column=2, pady=10)

        # Sparepart
        tk.Label(form, text="Sparepart:", bg="#c9c9c9").grid(row=3, column=0, sticky="w", pady=2)
        self.combo_sparepart = ttk.Combobox(form, state="readonly", width=25)
        self.combo_sparepart.grid(row=3, column=1, padx=5, pady=2)
        self.combo_sparepart.bind("<<ComboboxSelected>>", self.update_harga_sparepart)
        tk.Button(form, text="Update", width=9, bg="#2196F3", fg="white", command=self.update_transaksi).grid(row=3, column=2, padx=5, pady=10)

        # Qty
        tk.Label(form, text="Qty:", bg="#c9c9c9").grid(row=4, column=0, sticky="w", pady=2)
        self.entry_qty = tk.Entry(form, width=27)
        self.entry_qty.grid(row=4, column=1, padx=5, pady=2)
        self.entry_qty.bind("<KeyRelease>", lambda e: self.hitung_total())
        tk.Button(form, text="Hapus", width=9, bg="#F44336", fg="white", command=self.hapus_transaksi).grid(row=4, column=2, padx=5, pady=10)

        # Harga Sparepart
        tk.Label(form, text="Harga Sparepart:", bg="#c9c9c9").grid(row=5, column=0, sticky="w", pady=2)
        self.entry_harga_sparepart = tk.Entry(form, state="readonly", width=27)
        self.entry_harga_sparepart.grid(row=5, column=1, padx=5, pady=2)
        tk.Button(form, text="Batal", width=9, bg="#9E9E9E", fg="white", command=self.clear_form).grid(row=5, column=2, padx=5, pady=10)

        # Harga Jasa
        tk.Label(form, text="Harga Jasa:", bg="#c9c9c9").grid(row=6, column=0, sticky="w", pady=2)
        self.entry_harga_jasa = tk.Entry(form, width=27)
        self.entry_harga_jasa.grid(row=6, column=1, padx=5, pady=2)
        self.entry_harga_jasa.bind("<KeyRelease>", lambda e: self.hitung_total())

        # Total
        tk.Label(form, text="Total:", bg="#c9c9c9").grid(row=7, column=0, sticky="w", pady=2)
        self.entry_total = tk.Entry(form, state="readonly", width=27)
        self.entry_total.grid(row=7, column=1, padx=5, pady=2)

        #Pembayaran
        bayar_frame = ttk.LabelFrame(horizontal_frame, text="Pembayaran")
        bayar_frame.pack(side="left", anchor="n", padx=20, pady=5)

        ttk.Label(bayar_frame, text="Total").grid(row=0, column=0, sticky="w")
        ttk.Entry(bayar_frame, textvariable=self.total_var, state="readonly", width=20).grid(row=0, column=1)

        ttk.Label(bayar_frame, text="Bayar").grid(row=1, column=0, sticky="w")
        ttk.Entry(bayar_frame, textvariable=self.bayar_var, width=20).grid(row=1, column=1)

        ttk.Label(bayar_frame, text="Kembalian").grid(row=2, column=0, sticky="w")
        ttk.Entry(bayar_frame, textvariable=self.kembali_var, state="readonly", width=20).grid(row=2, column=1)

        ttk.Button(bayar_frame, text="Cetak Struk", command=self.cetak_struk,
                   style="Bayar.TButton").grid(row=3, column=1, pady=5, sticky="e")

        ttk.Button(bayar_frame, text="Simpan Transaksi", command=self.simpan_transaksi,
                   style="Bayar.TButton").grid(row=4, column=1, pady=5, sticky="e")

        # Tabel Data Transaksi sementara
        tree_frame = tk.Frame(self, bg="#c9c9c9")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(tree_frame, text="Daftar Transaksi Sementara", font=("Arial", 11, "bold"), bg="#c9c9c9").pack(anchor="w", pady=(0,5))
        # Treeview  sementara
        self.temp_tree = ttk.Treeview(tree_frame, columns=("Mekanik", "Sparepart", "Qty", "Jasa", "Total", "Tanggal"), show='headings', height=5)
        for col in self.temp_tree["columns"]:
            self.temp_tree.heading(col, text=col)
            self.temp_tree.column(col, width=100, anchor="center")

        scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")
        self.temp_tree.pack(fill="x", pady=(0, 10))
        self.temp_tree.bind("<ButtonRelease-1>", self.on_row_select_temp)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not self.last_insert_ids:
            return

        db = koneksi()
        cursor = db.cursor()

        # Gunakan WHERE id IN (...)
        format_strings = ','.join(['%s'] * len(self.last_insert_ids))
        query = f"""
            SELECT s.id, m.nama, sp.nama, s.qty, s.harga_jasa, s.total, s.tanggal
            FROM service s
            JOIN mekanik m ON s.mekanik_id = m.id
            JOIN sparepart sp ON s.sparepart_id = sp.id
            WHERE s.id IN ({format_strings})
            ORDER BY s.id DESC
        """
        cursor.execute(query, tuple(self.last_insert_ids))
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        db.close()

        self.last_insert_ids.clear()

    def load_dropdowns(self):
        db = koneksi()
        cursor = db.cursor()

        cursor.execute("SELECT id, nama FROM mekanik")
        self.mekanik_map = {nama: id_ for id_, nama in cursor.fetchall()}
        self.combo_mekanik['values'] = list(self.mekanik_map.keys())

        cursor.execute("SELECT id, nama, harga, stok FROM sparepart")
        self.sparepart_map = {}
        for id_, nama, harga, stok in cursor.fetchall():
            self.sparepart_map[nama] = {'id': id_, 'harga': harga, 'stok': stok}
        self.combo_sparepart['values'] = list(self.sparepart_map.keys())
        db.close()

    def update_harga_sparepart(self, event=None):
        selected = self.combo_sparepart.get()
        if selected:
            harga = self.sparepart_map[selected]['harga']
            self.entry_harga_sparepart.config(state="normal")
            self.entry_harga_sparepart.delete(0, tk.END)
            self.entry_harga_sparepart.insert(0, str(harga))
            self.entry_harga_sparepart.config(state="readonly")
            self.hitung_total()

    def hitung_total(self):
        try:
            qty = int(self.entry_qty.get())
            harga = int(self.entry_harga_sparepart.get())
            jasa = int(self.entry_harga_jasa.get())
            total = qty * harga + jasa
        except:
            total = 0
        self.entry_total.config(state="normal")
        self.entry_total.delete(0, tk.END)
        self.entry_total.insert(0, str(total))
        self.entry_total.config(state="readonly")
        self.total_var.set(total)

    def hitung_kembalian(self):
        try:
            total = self.total_var.get()
            bayar = self.bayar_var.get()
            kembali = bayar - total if bayar >= total else 0
            self.kembali_var.set(kembali)
        except:
            self.kembali_var.set(0)

    def simpan_transaksi(self):
        if not self.temp_tree.get_children():
            messagebox.showwarning("Peringatan", "Tidak ada data transaksi yang akan disimpan.")
            return

        total = self.total_var.get()
        bayar = self.bayar_var.get()
        kembali = self.kembali_var.get()

        # 💡 VALIDASI PEMBAYARAN
        if bayar <= 0:
            messagebox.showwarning("Peringatan", "Pembayaran belum dilakukan.")
            return

        if bayar < total:
            messagebox.showwarning("Peringatan", "Jumlah bayar kurang dari total.")
            return

        try:
            db = koneksi()
            cursor = db.cursor()

            nama_pelanggan = self.entry_nama_pelanggan.get().strip()
            plat_kendaraan = self.entry_plat_kendaraan.get().strip()

            if not nama_pelanggan or not plat_kendaraan:
                messagebox.showwarning("Peringatan", "Nama pelanggan dan plat kendaraan harus diisi.")
                return

            for item in self.temp_tree.get_children():
                values = self.temp_tree.item(item)["values"]
                mekanik_nama = values[0]
                sparepart_nama = values[1]
                qty = int(values[2])
                harga_jasa = int(values[3])
                total = int(values[4])
                tanggal = values[5]

                mekanik_id = self.mekanik_map.get(mekanik_nama)
                sparepart = self.sparepart_map.get(sparepart_nama)

                if not mekanik_id or not sparepart:
                    continue

                cursor.execute("""
                    INSERT INTO service (mekanik_id, sparepart_id, qty, harga_sparepart, harga_jasa, total, tanggal, nama_pelanggan, plat_kendaraan)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    mekanik_id,
                    sparepart['id'],
                    qty,
                    sparepart['harga'],
                    harga_jasa,
                    total,
                    tanggal,
                    nama_pelanggan,
                    plat_kendaraan
                ))
                # Kurangi stok
                cursor.execute("UPDATE sparepart SET stok = stok - %s WHERE id = %s", (qty, sparepart['id']))

            db.commit()
            db.close()

            # Reset semua tampilan dan form
            self.temp_tree.delete(*self.temp_tree.get_children())
            self.total_var.set(0)
            self.bayar_var.set(0)
            self.kembali_var.set(0)
            self.total_sementara = 0
            self.clear_form()
            messagebox.showinfo("Sukses", "Transaksi berhasil disimpan.")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan transaksi: {e}")

    def tambah(self):
        try:
            mekanik = self.combo_mekanik.get()
            sparepart = self.combo_sparepart.get()
            qty = int(self.entry_qty.get())
            harga_jasa = int(self.entry_harga_jasa.get())
            harga_sparepart = int(self.entry_harga_sparepart.get())

            if not mekanik or not sparepart or qty <= 0:
                messagebox.showwarning("Peringatan", "Lengkapi semua input dan pastikan jumlah > 0")
                return

            if sparepart not in self.sparepart_map:
                messagebox.showerror("Error", "Sparepart tidak valid.")
                return

            stok = self.sparepart_map[sparepart]['stok']
            if qty > stok:
                messagebox.showerror("Stok Habis", f"Stok {sparepart} hanya {stok}")
                return

            total = qty * harga_sparepart + harga_jasa
            tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Masukkan data ke Treeview sementara
            self.temp_tree.insert("", "end", values=(mekanik, sparepart, qty, harga_jasa, total, tanggal))

            # Update total
            self.total_sementara += total
            self.total_var.set(self.total_sementara)
            self.hitung_kembalian()

            # Reset form input
            self.combo_sparepart.set("")
            self.entry_qty.delete(0, tk.END)
            self.entry_harga_sparepart.config(state="normal")
            self.entry_harga_sparepart.delete(0, tk.END)
            self.entry_harga_sparepart.config(state="readonly")
            self.entry_harga_jasa.delete(0, tk.END)
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.config(state="readonly")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah ke tabel: {e}")

    def cetak_struk(self):
        if not self.temp_tree.get_children():
            messagebox.showwarning("Struk", "Belum ada transaksi.")
            return

        try:
            no_id = f"TEMP-{datetime.now().strftime('%H%M%S')}"
            total = self.total_var.get()
            bayar = self.bayar_var.get()
            kembali = self.kembali_var.get()
            now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

            folder = "struk"
            os.makedirs(folder, exist_ok=True)
            filename = os.path.abspath(os.path.join(folder, f"struk_{no_id}.pdf"))

            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            y = height - 40
            left = 50
            right = width - 50

            # Header
            c.setFont("Courier-Bold", 14)
            c.drawCentredString(width / 2, y, "BengkelKu")
            y -= 18
            c.setFont("Courier", 10)
            c.drawCentredString(width / 2, y, "Jl. Planet Mars No. 99")
            y -= 10
            c.line(left, y, right, y)  # garis atas
            y -= 12
            c.drawString(left, y, f"No. ID     : F{no_id.zfill(6)}")
            y -= 12
            c.drawString(left, y, f"Tanggal    : {now}")
            y -= 10
            c.line(left, y, right, y)  # garis bawah header

            # Header kolom
            y -= 15
            c.drawString(left, y, "Barang")
            c.drawString(left + 110, y, "Qty x Harga")
            c.drawString(left + 230, y, "Jasa")
            c.drawString(left + 300, y, "Subtotal")
            y -= 10
            c.line(left, y, right, y)

            # Data
            for item in self.temp_tree.get_children():
                values = self.temp_tree.item(item)['values']
                sparepart = values[1]
                qty = values[2]
                jasa = values[3]
                harga_sp = self.sparepart_map[sparepart]['harga']
                total_item = harga_sp * qty + jasa

                # Baris data
                y -= 12
                c.drawString(left, y, f"{sparepart[:15]}")
                c.drawString(left + 110, y, f"{qty} x {harga_sp:,}".replace(",", "."))
                c.drawString(left + 230, y, f"Rp{jasa:,}".replace(",", "."))
                c.drawString(left + 300, y, f"Rp{total_item:,}".replace(",", "."))

                if y < 80:
                    c.showPage()
                    y = height - 40

            # Garis akhir data
            y -= 10
            c.line(left, y, right, y)

            # Total
            y -= 15
            c.drawString(left, y, f"Total      : Rp {total:,}".replace(",", "."))
            y -= 12
            c.drawString(left, y, f"Bayar      : Rp {bayar:,}".replace(",", "."))
            y -= 12
            c.drawString(left, y, f"Kembalian  : Rp {kembali:,}".replace(",", "."))

            y -= 15
            c.line(left, y, right, y)
            y -= 15
            c.drawCentredString(width / 2, y, "TERIMA KASIH TELAH BERKUNJUNG")
            y -= 10
            c.line(left, y, right, y)

            c.save()

            # === Teks Preview Struk ===
            lines = [
                "=" * 40,
                "              BengkelKu              ",
                "        Jl. Planet Mars No. 99       ",
                "=" * 40,
                f"No. ID     : F{no_id.zfill(6)}",
                f"Tanggal    : {now}",
                "-" * 40,
                "Barang         Qty x Harga   Jasa   Subtotal",
                "-" * 40
            ]

            for item in self.temp_tree.get_children():
                values = self.temp_tree.item(item)['values']
                nama = str(values[1])[:13].ljust(13)  # maksimal 13 huruf nama
                qty = values[2]
                jasa = values[3]
                harga_sparepart = self.sparepart_map[values[1]]['harga']
                subtotal = harga_sparepart * qty + jasa
                line = f"{nama}  {qty} x {harga_sparepart:>6,}   {jasa:>5,}  {subtotal:>7,}"
                lines.append(line)

            lines.extend([
                "-" * 40,
                f"Total      : Rp {total:,}",
                f"Bayar      : Rp {bayar:,}",
                f"Kembalian  : Rp {kembali:,}",
                "=" * 40,
                "    TERIMA KASIH TELAH BERKUNJUNG    ",
                "=" * 40
            ])

            # Tampilkan di jendela popup
            preview_win = tk.Toplevel(self)
            preview_win.title("Struk - Service")
            preview_win.geometry("450x500")
            text_area = tk.Text(preview_win, font=("Courier New", 10), wrap=tk.WORD)
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.insert(tk.END, "\n".join(lines))
            text_area.config(state=tk.DISABLED)

            # Tombol buka PDF
            ttk.Button(preview_win, text="Buka PDF", command=lambda: self.open_pdf(filename)).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Gagal cetak struk:\n{e}")

    def open_pdf(self, filename):
        try:
            if not os.path.isfile(filename):
                messagebox.showerror("Gagal Buka PDF", f"File tidak ditemukan: {filename}")
                return

            system = platform.system()
            if system == "Windows":
                os.startfile(filename)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", filename], check=True)
            elif system == "Linux":
                subprocess.run(["xdg-open", filename], check=True)
            else:
                messagebox.showerror("Error", "Sistem operasi tidak dikenali.")
        except Exception as e:
            messagebox.showerror("Gagal Buka PDF", f"Error saat membuka file:\n{e}")

    def update_transaksi(self):
        if not self.selected_temp_item:
            messagebox.showwarning("Peringatan", "Pilih data di tabel sementara yang ingin diubah.")
            return

        try:
            mekanik = self.combo_mekanik.get()
            sparepart = self.combo_sparepart.get()
            qty = int(self.entry_qty.get())
            harga_jasa = int(self.entry_harga_jasa.get())
            harga_sparepart = int(self.entry_harga_sparepart.get())

            if not mekanik or not sparepart or qty <= 0:
                messagebox.showwarning("Peringatan", "Lengkapi semua input dan pastikan jumlah > 0")
                return

            if sparepart not in self.sparepart_map:
                messagebox.showerror("Error", "Sparepart tidak valid.")
                return

            stok = self.sparepart_map[sparepart]['stok']
            # Hitung total
            total = qty * harga_sparepart + harga_jasa
            tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Update baris di temp_tree
            self.temp_tree.item(self.selected_temp_item,
                                values=(mekanik, sparepart, qty, harga_jasa, total, tanggal))

            # Hitung ulang total semua transaksi sementara
            self.total_sementara = 0
            for item in self.temp_tree.get_children():
                self.total_sementara += int(self.temp_tree.item(item)['values'][4])
            self.total_var.set(self.total_sementara)
            self.hitung_kembalian()

            self.clear_form()
            self.selected_temp_item = None
            messagebox.showinfo("Sukses", "Data sementara berhasil diubah.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengubah data sementara: {e}")

    def on_row_select_temp(self, event):
        selected = self.temp_tree.selection()
        if selected:
            self.selected_temp_item = selected[0]
            values = self.temp_tree.item(self.selected_temp_item)["values"]

            # Isi form berdasarkan data baris
            self.combo_mekanik.set(values[0])
            self.combo_sparepart.set(values[1])
            self.update_harga_sparepart()
            self.entry_qty.delete(0, tk.END)
            self.entry_qty.insert(0, values[2])
            self.entry_harga_jasa.delete(0, tk.END)
            self.entry_harga_jasa.insert(0, values[3])
            self.entry_total.config(state="normal")
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, values[4])
            self.entry_total.config(state="readonly")

    def hapus_transaksi(self):
        if not self.selected_temp_item:
            messagebox.showwarning("Peringatan", "Pilih data di tabel sementara yang ingin dihapus.")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini dari transaksi sementara?")
        if confirm:
            try:
                # Kurangi total sementara
                nilai = self.temp_tree.item(self.selected_temp_item)['values']
                total_baris = int(nilai[4])
                self.total_sementara -= total_baris
                self.total_var.set(self.total_sementara)
                self.hitung_kembalian()

                # Hapus baris dari temp_tree
                self.temp_tree.delete(self.selected_temp_item)
                self.selected_temp_item = None
                self.clear_form()
                messagebox.showinfo("Sukses", "Data berhasil dihapus dari transaksi sementara.")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus data: {e}")

    def clear_form(self):
        self.combo_mekanik.set("")
        self.combo_sparepart.set("")
        self.entry_qty.delete(0, tk.END)
        self.entry_harga_sparepart.config(state="normal")
        self.entry_harga_sparepart.delete(0, tk.END)
        self.entry_harga_sparepart.config(state="readonly")
        self.entry_harga_jasa.delete(0, tk.END)
        self.entry_total.config(state="normal")
        self.entry_total.delete(0, tk.END)
        self.entry_total.config(state="readonly")
        self.selected_item_id = None
        self.entry_nama_pelanggan.delete(0, tk.END)
        self.entry_plat_kendaraan.delete(0, tk.END)
