# E-Commerce Public Dataset Dashboard

## Deskripsi Proyek

Dashboard interaktif yang dibuat menggunakan Streamlit untuk menganalisis performa bisnis berdasarkan E-Commerce Public Dataset.

Analisis yang ditampilkan meliputi:

- Tren revenue bulanan
- Top 10 kategori produk berdasarkan revenue
- Rata-rata nilai transaksi berdasarkan metode pembayaran
- Distribusi review pelanggan
- Persebaran seller berdasarkan wilayah

## Informasi Proyek

- Nama: Tarwin
- Email: tarwinweelah@gmail.com
- ID Dicoding: sembada14

## Struktur Folder

```text
submission/
│
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
│
├── data/
│   ├── customers_dataset.csv
│   ├── orders_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── products_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── sellers_dataset.csv
│   ├── order_reviews_dataset.csv
│   └── geolocation_dataset.csv
│
├── notebook.ipynb
├── requirements.txt
└── README.md
```

## Instalasi

Install seluruh dependency yang diperlukan:

```bash
pip install -r requirements.txt
```

## Menjalankan Dashboard

Masuk ke folder dashboard:

```bash
cd dashboard
```

Jalankan Streamlit:

```bash
streamlit run dashboard.py
```

Dashboard akan berjalan pada:

```text
http://localhost:8501
```

## Dashboard Features

- Filter Tahun dan Bulan
- KPI Total Revenue
- KPI Total Orders
- KPI Total Customers
- Monthly Revenue Trend
- Top Product Categories
- Average Transaction by Payment Type
- Review Score Distribution
- Top Seller States

## Sumber Dataset

E-Commerce Public Dataset (Sumber)