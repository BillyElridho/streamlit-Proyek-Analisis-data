import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Title
st.title("Dashboard Penggunaan Sepeda")

# Menambahkan logo di atas sidebar
st.sidebar.image("data/sepeda.png", width=150)
st.sidebar.header("Filter Data")

# Sidebar untuk opsi pengguna
selected_data_type = st.sidebar.selectbox("Pilih Jenis Data", ['Harian', 'Per Jam'])

# Load datasets
@st.cache_data
def load_data():
    day_url = 'https://drive.google.com/uc?id=1fHPg_Gs-yHm4mr2R5aTV7l4a9t1SV-tc&export=download'
    hour_url = 'https://drive.google.com/uc?id=1CZb-jOWyY20Z9oSZNr1KoxypSyqQUUcZ&export=download'
    day_df = pd.read_csv(day_url)
    hour_df = pd.read_csv(hour_url)
    return day_df, hour_df

day_df, hour_df = load_data()

# Menambahkan kolom kategori waktu pada hour_df
def categorize_time(hour):
    if 6 <= hour < 10:
        return 'Pagi'
    elif 10 <= hour < 16:
        return 'Siang'
    elif 16 <= hour < 20:
        return 'Sore'
    else:
        return 'Malam'

# Pastikan kolom jam ditambahkan pada hour_df
hour_df['hour'] = pd.to_datetime(hour_df['dteday']).dt.hour
hour_df['time_category'] = hour_df['hour'].apply(categorize_time)

# Keterangan musim
season_names = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin'
}

# Menambahkan kolom season untuk menyimpan angka musim
hour_df['season'] = hour_df['season'].astype(int)
day_df['season'] = day_df['season'].astype(int)

# Menampilkan data
st.subheader("Data Penggunaan Sepeda")
if selected_data_type == 'Harian':
    st.write(day_df.head())
else:
    st.write(hour_df.head())

# Visualisasi matriks korelasi
st.subheader("Analisis Korelasi")
numeric_df = (day_df if selected_data_type == 'Harian' else hour_df).select_dtypes(include=['number'])
correlation_matrix = numeric_df.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", annot_kws={"size": 10})
plt.title("Korelasi Antara Variabel di Dataset Penggunaan Sepeda", fontsize=16)
plt.xticks(rotation=45, ha="right", fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
st.pyplot(plt)

# Rata-rata Penggunaan Sepeda Berdasarkan Musim
st.subheader("Rata-rata Penggunaan Sepeda di Setiap Musim")

if selected_data_type == 'Harian':
    # Menghitung rata-rata penggunaan sepeda harian berdasarkan musim
    seasonal_usage_day = day_df.groupby('season')['cnt'].mean().reset_index()
    seasonal_usage_day.rename(columns={'cnt': 'mean'}, inplace=True)
    
    plt.figure(figsize=(8, 5))
    sns.barplot(x='season', y='mean', data=seasonal_usage_day)  # Warna default
    plt.title('Rata-rata Penggunaan Sepeda di Setiap Musim (Data Harian)')
    plt.xlabel('Musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Dingin)')
    plt.ylabel('Rata-rata Penggunaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(plt)

else:
    # Menghitung rata-rata penggunaan sepeda per jam berdasarkan musim
    seasonal_usage_hour = hour_df.groupby('season')['cnt'].mean().reset_index()
    seasonal_usage_hour.rename(columns={'cnt': 'mean'}, inplace=True)

    plt.figure(figsize=(8, 5))
    sns.barplot(x='season', y='mean', data=seasonal_usage_hour)  # Warna default
    plt.title('Rata-rata Penggunaan Sepeda di Setiap Musim (Data Per Jam)')
    plt.xlabel('Musim (1: Musim Semi, 2: Musim Panas, 3: Musim Gugur, 4: Musim Dingin)')
    plt.ylabel('Rata-rata Penggunaan Sepeda')
    plt.xticks(rotation=45)
    st.pyplot(plt)
