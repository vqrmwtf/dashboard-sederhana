import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set halaman dashboard
st.set_page_config(page_title="Dashboard Penjualan", layout="wide")

# Judul dashboard
st.title("Dashboard Penjualan Toko Makmur Jaya")
st.write("Dashboard sederhana untuk melihat performa penjualan")

# Read data
@st.cache_data
def load_data():
    df = pd.read_csv('data_penjualan.csv')
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    return df

# Load data
df = load_data()

# Buat fitur upload file
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload file CSV", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File berhasil di upload!")
else:
    df = load_data() # Gunakan data default

# Buat filter data
st.sidebar.header("Filter Data")
kategori_pilihan = st.sidebar.multiselect(
    "Pilih Kategori:",
    df['kategori'].unique(),
    default=df['kategori'].unique()
)

# Filter berdasarkan pilihan
data_filtered = df[df['kategori'].isin(kategori_pilihan)]

# Filter tanggal
tanggal_mulai = st.sidebar.date_input("Tanggal Mulai", df['tanggal'].min())
tanggal_selesai = st.sidebar.date_input("Tanggal Selesai", df['tanggal'].max())

data_filtered = data_filtered[
    (data_filtered['tanggal'] >= pd.to_datetime(tanggal_mulai)) &
    (data_filtered['tanggal'] <= pd.to_datetime(tanggal_selesai))
]

# Show data penjualan
st.header("Ringkasan Penjualan")

col1, col2, col3 = st.columns(3)

with col1:
    total_penjualan = data_filtered['penjualan'].sum()
    st.metric("Total Penjualan", f"{total_penjualan:,} item")

with col2:
    total_pendapatan = data_filtered['pendapatan'].sum()
    st.metric("Total Pendapatan", f"Rp{total_pendapatan:,}")

with col3:
    rata_rata_harian = data_filtered['penjualan'].mean()
    st.metric("Rata-rata Harian", f"{rata_rata_harian:.1f} item")

# Buat grafik tren penjualan
st.header("Tren Penjualan Bulanan")

data_bulanan = data_filtered.groupby(data_filtered['tanggal'].dt.to_period('M'))['penjualan'].sum()

fig, ax = plt.subplots(figsize=(10, 6))
data_bulanan.plot(kind='line', marker='o', ax=ax)
ax.set_title("Penjualan per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penjualan")
ax.grid(True)
st.pyplot(fig)

# Buat grafik penjualan per kategori
st.header("Penjualan per Kategori")

kategori_data = data_filtered.groupby('kategori')['penjualan'].sum()

fig, ax = plt.subplots(figsize=(8, 6))
kategori_data.plot(kind='bar', ax=ax, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
ax.set_title("Total Penjualan per Kategori")
ax.set_xlabel('Kategori')
ax.set_ylabel('Jumlah Penjualan')
plt.xticks(rotation=45)
st.pyplot(fig)

# Buat grafik pie distribusi penjualan per kategori
st.header("Distribusi Kategori")

colors_custom = {
    'Buku': '#FF6B6B',
    'Elektronik': '#4ECDC4',
    'Makanan': '#45B7D1',
    'Pakaian': '#FFA07A'
}

# Ambil warna sesuai kategori yang ada
colors = [colors_custom.get(cat, '#CCCCCC') for cat in kategori_data.index]

fig, ax = plt.subplots(figsize=(8, 8))
kategori_data.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=colors)
ax.set_title('Distribusi Penjualan per Kategori')
ax.set_ylabel('') # Hilangkan label y
st.pyplot(fig)

# Buat tabel data
st.header("Data Detail")

# Buat copy data untuk custom header
data_display = data_filtered.copy()

# Rename kolom dengan nama yang user friendly
data_display = data_filtered.rename(columns={
    'tanggal': 'Tanggal Transaksi',
    'penjualan': 'Jumlah Item Terjual',
    'pendapatan': 'Pendapatan (Rupiah)',
    'kategori': 'Kategori Produk'
})

# Format kolom pendapatan
data_display['Pendapatan (Rupiah)'] = data_display['Pendapatan (Rupiah)'].apply(
    lambda x: f"Rp {x:,.0f}"
)

# Format kolom tanggal
data_display['Tanggal Transaksi'] = data_display['Tanggal Transaksi'].dt.strftime('%d-%m-%Y')

# Show 20 data terakhir
st.write("Berikut adalah 20 data terakhir:")
st.dataframe(
    data_display.tail(20),
    use_container_width=True,
    hide_index=True
)

# Info sidebar
st.sidebar.markdown("---")
st.sidebar.info(
    "Dashboard ini menampilkan data penjualan Toko Makmur Jaya"
    "Gunakan filter di atas untuk ,elihat data kategori tertentu"
)