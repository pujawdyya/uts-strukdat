import pandas as pd
import os

# Baca file Excel
file_excel = "Struktur_Data_Dataset_Kelas_A_B_C (5).xlsx"
sheet = "Sheet1"
df = pd.read_excel(file_excel, sheet_name=sheet, skiprows=1)

# Ambil kolom yang relevan
papers = df.iloc[:, [5, 6, 7, 8, 9, 10]].copy()
papers.columns = ["Judul", "Tahun", "Penulis", "Abstrak", "Kesimpulan", "Link"]

# Hapus baris yang kosong di bagian penting
papers = papers.dropna(subset=["Judul", "Tahun"]).fillna("-")

# Konversi tahun ke integer
papers["Tahun"] = papers["Tahun"].astype(int)

# Urutkan papers berdasarkan tahun dan nama untuk binary search
papers_by_year = papers.sort_values("Tahun").reset_index(drop=True)
papers_by_judul = papers.sort_values("Judul").reset_index(drop=True)
papers_by_penulis = papers.sort_values("Penulis").reset_index(drop=True)

# Fungsi tampilkan hasil

def tampilkan_paper(baris):
    print("\n=== HASIL DITEMUKAN ===")
    print("Judul      :", baris["Judul"])
    print("Penulis    :", baris["Penulis"])
    print("Tahun      :", baris["Tahun"])
    print("Abstrak    :", baris["Abstrak"])
    print("Kesimpulan :", baris["Kesimpulan"])
    print("Link       :", baris["Link"])
    print("----------------------------")

# Binary Search fungsi umum

def binary_search(data, kolom, keyword):
    kiri, kanan = 0, len(data) - 1
    hasil = []
    keyword = keyword.lower()

    while kiri <= kanan:
        mid = (kiri + kanan) // 2
        value = str(data.loc[mid, kolom]).lower()

        if keyword in value:
            # Cek kiri dan kanan
            i = mid
            while i >= 0 and keyword in str(data.loc[i, kolom]).lower():
                hasil.insert(0, data.loc[i])
                i -= 1
            i = mid + 1
            while i < len(data) and keyword in str(data.loc[i, kolom]).lower():
                hasil.append(data.loc[i])
                i += 1
            break
        elif keyword < value:
            kanan = mid - 1
        else:
            kiri = mid + 1

    return hasil

def binary_search_tahun(data, tahun):
    kiri, kanan = 0, len(data) - 1
    hasil = []

    while kiri <= kanan:
        mid = (kiri + kanan) // 2
        mid_year = data.loc[mid, "Tahun"]

        if mid_year == tahun:
            i = mid
            while i >= 0 and data.loc[i, "Tahun"] == tahun:
                hasil.insert(0, data.loc[i])
                i -= 1
            i = mid + 1
            while i < len(data) and data.loc[i, "Tahun"] == tahun:
                hasil.append(data.loc[i])
                i += 1
            break
        elif mid_year < tahun:
            kiri = mid + 1
        else:
            kanan = mid - 1
    return hasil

# Menu pencarian linear

def menu_linear():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== MENU PENCARIAN (LINEAR) ===")
        print("Cari Paper berdasarkan : ")
        print("1. Judul")
        print("2. Penulis")
        print("3. Tahun")
        print("0. Kembali ke menu utama")
        pilihan = input("Pilihan: ")

        if pilihan == "1":
            keyword = input("Masukkan kata kunci judul: ").lower()
            hasil = papers[papers["Judul"].str.lower().str.contains(keyword)]
            os.system('cls' if os.name == 'nt' else 'clear')
            if hasil.empty:
                print("Tidak ditemukan.")
            else:
                for _, row in hasil.iterrows():
                    tampilkan_paper(row)
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "2":
            keyword = input("Masukkan kata kunci penulis: ").lower()
            hasil = papers[papers["Penulis"].str.lower().str.contains(keyword)]
            os.system('cls' if os.name == 'nt' else 'clear')
            if hasil.empty:
                print("Tidak ditemukan.")
            else:
                for _, row in hasil.iterrows():
                    tampilkan_paper(row)
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "3":
            try:
                tahun = int(input("Masukkan tahun: "))
                hasil = papers[papers["Tahun"] == tahun]
                os.system('cls' if os.name == 'nt' else 'clear')
                if hasil.empty:
                    print("Tidak ditemukan.")
                else:
                    for _, row in hasil.iterrows():
                        tampilkan_paper(row)
            except ValueError:
                print("Input tahun tidak valid.")
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "0":
            break

        else:
            print("Pilihan tidak valid.")
            input("\nTekan Enter untuk kembali...")

# Menu pencarian binary

def menu_binary():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== MENU PENCARIAN (BINARY) ===")
        print("Cari Paper berdasarkan : ")
        print("1. Judul")
        print("2. Penulis")
        print("3. Tahun")
        print("0. Kembali ke menu utama")
        pilihan = input("Pilihan: ")

        if pilihan == "1":
            keyword = input("Masukkan kata kunci judul: ").lower()
            hasil = binary_search(papers_by_judul, "Judul", keyword)
            os.system('cls' if os.name == 'nt' else 'clear')
            if not hasil:
                print("Tidak ditemukan.")
            else:
                for row in hasil:
                    tampilkan_paper(row)
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "2":
            keyword = input("Masukkan kata kunci penulis: ").lower()
            hasil = binary_search(papers_by_penulis, "Penulis", keyword)
            os.system('cls' if os.name == 'nt' else 'clear')
            if not hasil:
                print("Tidak ditemukan.")
            else:
                for row in hasil:
                    tampilkan_paper(row)
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "3":
            try:
                tahun = int(input("Masukkan tahun: "))
                hasil = binary_search_tahun(papers_by_year, tahun)
                os.system('cls' if os.name == 'nt' else 'clear')
                if not hasil:
                    print("Tidak ditemukan.")
                else:
                    for row in hasil:
                        tampilkan_paper(row)
            except ValueError:
                print("Input tahun tidak valid.")
            input("\nTekan Enter untuk kembali...")

        elif pilihan == "0":
            break

        else:
            print("Pilihan tidak valid.")
            input("\nTekan Enter untuk kembali...")

# Menu utama
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== PILIH METODE PENCARIAN ===")
    print("1. Linear Search")
    print("2. Binary Search")
    print("0. Keluar")
    pilihan = input("Pilihan: ")

    if pilihan == "1":
        menu_linear()
    elif pilihan == "2":
        menu_binary()
    elif pilihan == "0":
        print("Terima kasih!")
        break
    else:
        print("Pilihan tidak valid.")
        input("\nTekan Enter untuk kembali ke menu...")
