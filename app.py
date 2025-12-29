import tkinter as tk
from tkinter import messagebox
from fuzzywuzzy import process, fuzz

class FuzzyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FuzzyWuzzy String Matcher")
        self.root.geometry("400x500")

        # Dataset
        self.data_pilihan = [
            "Apple iPhone 15", "Samsung Galaxy S23", "Google Pixel 8",
            "MacBook Pro M3", "Dell XPS 13", "Sony WH-1000XM5",
            "Asus ROG Zephyrus", "Logitech MX Master 3"
        ]

        tk.Label(root, text="Daftar Produk:", font=('Arial', 10, 'bold')).pack(pady=5)
        
        self.listbox = tk.Listbox(root, height=6)
        for item in self.data_pilihan:
            self.listbox.insert(tk.END, item)
        self.listbox.pack(pady=5, padx=20, fill=tk.X)

        tk.Label(root, text="Masukkan Kata Pencarian:").pack(pady=5)
        self.entry_search = tk.Entry(root, font=('Arial', 12))
        self.entry_search.pack(pady=5, padx=20, fill=tk.X)

        self.btn_search = tk.Button(root, text="Cari Kecocokan", command=self.cari_fuzzy, bg="#4CAF50", fg="white")
        self.btn_search.pack(pady=10)

        self.label_hasil = tk.Label(root, text="-", font=('Arial', 12), fg="blue")
        self.label_hasil.pack(pady=5)

        self.label_skor = tk.Label(root, text="Skor Kemiripan: 0%", font=('Arial', 10))
        self.label_skor.pack(pady=5)

    def cari_fuzzy(self):
        query = self.entry_search.get()
        if not query:
            messagebox.showwarning("Input Kosong", "Silakan masukkan kata kunci!")
            return

        # Proses pencarian
        hasil_terbaik, skor = process.extractOne(query, self.data_pilihan, scorer=fuzz.token_sort_ratio)

        # Update UI (Perbaikan di sini)
        if skor > 50:
            self.label_hasil.config(text=hasil_terbaik)
            self.label_skor.config(text=f"Skor Kemiripan: {skor}%")
        else:
            self.label_hasil.config(text="Tidak ditemukan kecocokan")
            self.label_skor.config(text=f"Skor tertinggi hanya: {skor}%")

if __name__ == "__main__":
    root = tk.Tk()
    app = FuzzyApp(root)
    root.mainloop()
