import pandas as pd
import random
from datetime import datetime, timedelta

# Buat data penjualan
data = []
tanggal_mulai = datetime(2024, 1, 1)

for i in range(365): # Selama 1 tahun
    tanggal = tanggal_mulai + timedelta(days=i)

    # Data random yang realistis
    penjualan = random.randint(50, 200) # 50 - 200 item per hari
    pendapatan = penjualan * random. randint(10000, 50000) # Harga item
    kategori = random.choice(['Elektronik', 'Pakaian', 'Makanan', 'Buku'])

    data.append({
        'tanggal': tanggal,
        'penjualan': penjualan,
        'pendapatan': pendapatan,
        'kategori': kategori
    })

# Simpan ke file CSV
df = pd.DataFrame(data)
df.to_csv('data_penjualan.csv', index=False)
print("Data berhasil dibuat!")