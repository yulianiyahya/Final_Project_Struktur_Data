import csv
import os
from datetime import datetime

# File CSV untuk menyimpan data transaksi
FILE_NAME = 'transaksi_keuangan.csv'
# Dictionary kategori pengeluaran (HashMap)
KATEGORI_PENGELUARAN = {
    '1': 'Makanan',
    '2': 'Transportasi',
    '3': 'Hiburan',
    '4': 'Belanja',
    '5': 'Kesehatan',
    '6': 'Lainnya'
}

def init_csv():
    """Inisialisasi file CSV dengan header jika file belum ada"""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                'id', 'jenis', 'jumlah', 'kategori', 'tanggal', 'deskripsi'
            ])
            writer.writeheader()

def baca_transaksi():
    """Membaca semua data transaksi dari CSV ke dalam list"""
    transaksi = []
    with open(FILE_NAME, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transaksi.append(row)
    
    # Urutkan berdasarkan tanggal
    transaksi.sort(key=lambda x: datetime.strptime(x['tanggal'], "%Y-%m-%d"))
    return transaksi

def simpan_transaksi(transaksi):
    """Menyimpan list transaksi ke file CSV"""
    # Urutkan berdasarkan tanggal sebelum menyimpan
    transaksi.sort(key=lambda x: datetime.strptime(x['tanggal'], "%Y-%m-%d"))
    
    # Atur ulang ID agar berurutan
    for i, t in enumerate(transaksi, start=1):
        t['id'] = str(i)
    
    with open(FILE_NAME, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'id', 'jenis', 'jumlah', 'kategori', 'tanggal', 'deskripsi'
        ])
        writer.writeheader()
        writer.writerows(transaksi)

def tambah_transaksi():
    """Menambahkan transaksi baru (CREATE)"""
    jenis = input("\nJenis transaksi (1 = Pemasukan, 2 = Pengeluaran): ")
    if  jenis not in ['1', '2']:
        print("Pilihan tidak valid!")
        return
    
    try:
        jumlah = float(input("Jumlah: "))
    except ValueError:
        print("Jumlah harus angka!")
        return
    
    if jenis == '2':  # Hanya pengeluaran yang punya kategori
        print("\nKategori Pengeluaran:")
        for key, value in KATEGORI_PENGELUARAN.items():
            print(f"{key}. {value}")
        kategori = input("Pilih kategori: ")
        if kategori not in KATEGORI_PENGELUARAN:
            print("Kategori tidak valid!")
            return
        kategori = KATEGORI_PENGELUARAN[kategori]
    else:
        kategori = "Pemasukan"
    
    deskripsi = input("Deskripsi: ")
    tanggal = input("Tanggal (YYYY-MM-DD) [kosongkan untuk hari ini]: ")
    if not tanggal:
        tanggal = datetime.now().strftime("%Y-%m-%d")
    
    # Validasi format tanggal
    try:
        datetime.strptime(tanggal, "%Y-%m-%d")
    except ValueError:
        print("Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
        return
    
    transaksi = baca_transaksi()
    
    transaksi_baru = {
        'id': str(len(transaksi) + 1),  # ID sementara, nanti diatur ulang saat simpan
        'jenis': "Pemasukan" if jenis == '1' else "Pengeluaran",
        'jumlah': jumlah,
        'kategori': kategori,
        'tanggal': tanggal,
        'deskripsi': deskripsi
    }
    
    transaksi.append(transaksi_baru)
    simpan_transaksi(transaksi)
    print("\nTransaksi berhasil ditambahkan!")

def tampilkan_transaksi(transaksi=None):
    """Menampilkan daftar transaksi (READ)"""
    if transaksi is None:
        transaksi = baca_transaksi()
    
    if not transaksi:
        print("\nTidak ada transaksi!")
        return
    
    print("\nDaftar Transaksi:")
    print("-" * 85)
    # Mengatur lebar kolom yang lebih presisi
    print(f"{'ID':<5} {'Tanggal':<12} {'Jenis':<12} {'Kategori':<15} {'Jumlah':<15} {'Deskripsi':<20}")
    print("-" * 85)
    
    for row in transaksi:
        # Format jumlah menjadi string dengan 2 digit desimal dan rata kanan
        jumlah_str = f"{float(row['jumlah']):.2f}"
        jumlah_formatted = f"{jumlah_str:>10}"  # Rata kanan dengan lebar 10 karakter
        
        # Potong deskripsi jika terlalu panjang
        deskripsi = row['deskripsi']
        if len(deskripsi) > 20:
            deskripsi = deskripsi[:17] + "..."
            
        print(f"{row['id']:<5} {row['tanggal']:<12} {row['jenis']:<12} {row['kategori']:<15} {jumlah_formatted}  {deskripsi:<20}")

    print("-" * 85)

def update_transaksi():
    """Memperbarui data transaksi (UPDATE)"""
    tampilkan_transaksi()
    try:
        id_transaksi = input("\nMasukkan ID transaksi yang akan diupdate: ")
        transaksi = baca_transaksi()
        ditemukan = False
        
        for row in transaksi:
            if row['id'] == id_transaksi:
                print("\nData transaksi yang akan diupdate:")
                print(f"1. Jenis: {row['jenis']}")
                print(f"2. Jumlah: {row['jumlah']}")
                print(f"3. Kategori: {row['kategori']}")
                print(f"4. Tanggal: {row['tanggal']}")
                print(f"5. Deskripsi: {row['deskripsi']}")
                
                kolom = input("\nPilih nomor data yang akan diupdate: ")
                if kolom == '1':
                    jenis = input("Jenis baru (1=Pemasukan, 2=Pengeluaran): ")
                    if jenis not in ['1', '2']:
                        print("Pilihan tidak valid!")
                        return
                    row['jenis'] = "Pemasukan" if jenis == '1' else "Pengeluaran"
                elif kolom == '2':
                    try:
                        row['jumlah'] = float(input("Jumlah baru: "))
                    except ValueError:
                        print("Jumlah harus angka!")
                        return
                elif kolom == '3':
                    if row['jenis'] == "Pengeluaran":
                        print("\nKategori Pengeluaran:")
                        for key, value in KATEGORI_PENGELUARAN.items():
                            print(f"{key}. {value}")
                        kategori = input("Pilih kategori baru: ")
                        if kategori not in KATEGORI_PENGELUARAN:
                            print("Kategori tidak valid!")
                            return
                        row['kategori'] = KATEGORI_PENGELUARAN[kategori]
                    else:
                        print("Hanya transaksi pengeluaran yang bisa diupdate kategorinya!")
                elif kolom == '4':
                    new_date = input("Tanggal baru (YYYY-MM-DD): ")
                    try:
                        # Validasi format tanggal
                        datetime.strptime(new_date, "%Y-%m-%d")
                        row['tanggal'] = new_date
                    except ValueError:
                        print("Format tanggal tidak valid! Gunakan format YYYY-MM-DD")
                        return
                elif kolom == '5':
                    row['deskripsi'] = input("Deskripsi baru: ")
                else:
                    print("Pilihan tidak valid!")
                    return
                
                ditemukan = True
                simpan_transaksi(transaksi)
                print("\nTransaksi berhasil diupdate!")
                break
        
        if not ditemukan:
            print("\nID transaksi tidak ditemukan!")
    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")

def hapus_transaksi():
    """Menghapus transaksi (DELETE)"""
    tampilkan_transaksi()
    id_transaksi = input("\nMasukkan ID transaksi yang akan dihapus: ")
    transaksi = baca_transaksi()
    transaksi_baru = [row for row in transaksi if row['id'] != id_transaksi]
    
    if len(transaksi) == len(transaksi_baru):
        print("\nID transaksi tidak ditemukan!")
    else:
        simpan_transaksi(transaksi_baru)
        print("\nTransaksi berhasil dihapus!")

def filter_bulan_tahun(transaksi, bulan, tahun):
    """Filter transaksi berdasarkan bulan dan tahun"""
    hasil = []
    for row in transaksi:
        tgl = datetime.strptime(row['tanggal'], "%Y-%m-%d")
        if tgl.month == bulan and tgl.year == tahun:
            hasil.append(row)
    return hasil

def laporan_bulanan():
    """Menampilkan laporan bulanan"""
    try:
        bulan = int(input("Masukkan bulan (1-12): "))
        tahun = int(input("Masukkan tahun: "))
        transaksi = baca_transaksi()
        transaksi_bulanan = filter_bulan_tahun(transaksi, bulan, tahun)
        
        if not transaksi_bulanan:
            print(f"\nTidak ada transaksi pada {bulan}/{tahun}")
            return
        
        tampilkan_transaksi(transaksi_bulanan)
        
        total_pemasukan = 0
        total_pengeluaran = 0
        for row in transaksi_bulanan:
            if row['jenis'] == "Pemasukan":
                total_pemasukan += float(row['jumlah'])
            else:
                total_pengeluaran += float(row['jumlah'])
        
        print("\nRingkasan Bulanan:")
        print(f"Total Pemasukan: {total_pemasukan:.2f}")
        print(f"Total Pengeluaran: {total_pengeluaran:.2f}")
        print(f"Saldo Bulan Ini: {(total_pemasukan - total_pengeluaran):.2f}")
    
    except ValueError:
        print("Input bulan/tahun tidak valid!")

def laporan_tahunan():
    """Menampilkan laporan tahunan"""
    try:
        tahun = int(input("Masukkan tahun: "))
        transaksi = baca_transaksi()
        transaksi_tahunan = [row for row in transaksi if datetime.strptime(row['tanggal'], "%Y-%m-%d").year == tahun]
        
        if not transaksi_tahunan:
            print(f"\nTidak ada transaksi pada tahun {tahun}")
            return
        
        # Tampilkan ringkasan per bulan
        print(f"\nLaporan Tahunan {tahun}:")
        print("-" * 50)
        print(f"{'Bulan':<10} {'Pemasukan':<15} {'Pengeluaran':<15} {'Saldo':<10}")
        print("-" * 50)
        
        saldo_tahunan = 0
        for bulan in range(1, 13):
            transaksi_bulanan = filter_bulan_tahun(transaksi_tahunan, bulan, tahun)
            pemasukan = sum(float(row['jumlah']) for row in transaksi_bulanan if row['jenis'] == "Pemasukan")
            pengeluaran = sum(float(row['jumlah']) for row in transaksi_bulanan if row['jenis'] == "Pengeluaran")
            saldo = pemasukan - pengeluaran
            saldo_tahunan += saldo
            print(f"{bulan:<10} {pemasukan:<15.2f} {pengeluaran:<15.2f} {saldo:<10.2f}")
        
        print("-" * 50)
        print(f"Saldo Akhir Tahun: {saldo_tahunan:.2f}")
    
    except ValueError:
        print("Input tahun tidak valid!")

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    init_csv()
    
    while True:
        print("\n===== DOMPET DIGITAL =====")
        print("1. Tambah Transaksi")
        print("2. Tampilkan Semua Transaksi")
        print("3. Laporan Bulanan")
        print("4. Laporan Tahunan")
        print("5. Update Transaksi")
        print("6. Hapus Transaksi")
        print("7. Keluar")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1':
            tambah_transaksi()
        elif pilihan == '2':
            tampilkan_transaksi()
        elif pilihan == '3':
            laporan_bulanan()
        elif pilihan == '4':
            laporan_tahunan()
        elif pilihan == '5':
            update_transaksi()
        elif pilihan == '6':
            hapus_transaksi()
        elif pilihan == '7':
            print("Terima kasih telah menggunakan aplikasi kami!")
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()