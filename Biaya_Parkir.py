import tkinter as tk
from datetime import datetime, timedelta
from ctypes import resize 
from tkinter import ttk
from tkinter.messagebox import * 

class ParkirApp: #oop
    def __init__(self, root): 
        self.root = root #gui
        self.root.geometry("310x200")
        self.root.resizable(False, True)
        self.root.title("Aplikasi Parkir")

        self.label_nomor = tk.Label(root, text="Nomor Kendaraan:")
        self.label_nomor.grid(row=0, column=0, padx=10, pady=5)
        self.entry_nomor = tk.Entry(root)
        self.entry_nomor.grid(row=0, column=1, padx=10, pady=5)

        self.label_roda = tk.Label(root, text="Jumlah Roda:")
        self.label_roda.grid(row=1, column=0, padx=10, pady=5)
        self.entry_roda = ttk.Combobox(root, value = ["2", "4"], state = "readonly")
        self.entry_roda.grid(row=1, column=1, padx=10, pady=5)
        self.entry_roda.current(0)

        self.button_masuk = tk.Button(root, text="Masuk", command=self.masuk)
        self.button_masuk.grid(row=2, column=0, padx=10, pady=5)

        self.button_keluar = tk.Button(root, text="Keluar", command=self.keluar)
        self.button_keluar.grid(row=2, column=1, padx=10, pady=5)

        self.button_lihat_parkir = tk.Button(root, text="Lihat Kendaraan Parkir", command=self.lihat_kendaraan_parkir)
        self.button_lihat_parkir.grid(row=3, column=0, columnspan=2, padx=10)

        self.label_parkir = tk.Label(root, text = "")
        self.label_parkir.grid(row = 4, column = 0, columnspan = 2, padx =10)
        self.parkir = Parkir()

    def masuk(self):
        nomor_kendaraan = str(self.entry_nomor.get())
        plat = len(nomor_kendaraan)
        roda = self.entry_roda.get()
        if plat > 0 and plat <= 6 : 
            self.parkir.masuk(nomor_kendaraan, roda)
        else:
            print(showinfo("Biaya Parkir",f"nomor plat {nomor_kendaraan} yang anda masukkan tidak valid"))
        self.entry_nomor.delete(0, tk.END)

    def keluar(self):
        nomor_kendaraan = self.entry_nomor.get()
        self.parkir.keluar(nomor_kendaraan)
        self.entry_nomor.delete(0, tk.END)


    def lihat_kendaraan_parkir(self):
        kendaraan_parkir = self.parkir.get_kendaraan_parkir()
        self.label_parkir.config(text="")

        # Membuat frame dengan border
        frame = tk.LabelFrame(self.root, text="Kendaraan Terparkir", padx=10, pady=5)
        frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Menampilkan informasi kendaraan di dalam frame
        for i, (nomor, data) in enumerate(kendaraan_parkir.items()):
            tk.Label(frame, text=f"Nomor: {nomor}, Masuk: {data['waktu_masuk']}").grid(row=i, column=0, sticky="w")


class Parkir:
    def __init__(self): #function
        self.data_parkir = {}
        self.stack = []

    def masuk(self, nomor_kendaraan, roda):
        if nomor_kendaraan in self.data_parkir: #pengkondisian 
            print("Kendaraan sudah masuk.")
        else:
            waktu_masuk = datetime.now()
            self.data_parkir[nomor_kendaraan] = {'waktu_masuk': waktu_masuk, 'roda': roda}
            self.stack.append(nomor_kendaraan)
            print(f"Kendaraan dengan nomor plat {nomor_kendaraan} masuk pada waktu:", waktu_masuk)

    def keluar(self, nomor_kendaraan):
        if nomor_kendaraan in self.data_parkir:
            data_kendaraan = self.data_parkir[nomor_kendaraan]
            waktu_masuk = data_kendaraan['waktu_masuk']
            roda = data_kendaraan['roda']
            waktu_keluar = datetime.now()
            durasi = waktu_keluar - waktu_masuk
            biaya = self.hitung_biaya(durasi, roda)
            del self.data_parkir[nomor_kendaraan]
            self.stack.remove(nomor_kendaraan)
            print("Kendaraan keluar pada waktu:", waktu_keluar)
            print("Durasi parkir:", durasi)
            print("Biaya parkir:", biaya)
            print(showinfo("Biaya Parkir",f"Biaya Parkir untuk kendaraan {nomor_kendaraan} adalah {biaya}"))
        else:
            print("Kendaraan tidak ditemukan.")

    def hitung_biaya(self, durasi, roda):
        biaya_per_jam = 2000  # Biaya per jam
        biaya_pertama = 1000 # Biaya gratis untuk 30 menit pertama
        durasi_total_menit = durasi.total_seconds() / 60  # Konversi durasi ke menit
        durasi_jam = durasi_total_menit / 60  # Durasi dalam jam
        if durasi_jam <= 0.5:
            return biaya_pertama  # Gratis untuk 30 menit pertama
        else:
            biaya_selanjutnya = (durasi_jam - 0.5) * biaya_per_jam  # Biaya untuk jam selanjutnya
            return biaya_pertama + biaya_selanjutnya

    def get_kendaraan_parkir(self):
        return self.data_parkir


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkirApp(root)
    root.mainloop()
