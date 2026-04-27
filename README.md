# 🛒 Brazilian E-Commerce Dashboard

Dashboard analisis data penjualan **Olist Brazilian E-Commerce** menggunakan Streamlit.

## 📁 Struktur Folder

```
submission/
├── dashboard/
│   └── dashboard.py
├── dataset/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── Proyek_Analisis_Data.ipynb
├── requirements.txt
└── README.md
```

## 🔧 Cara Menjalankan Dashboard

### 1. Clone / Download proyek ini

### 2. Buat virtual environment (opsional tapi disarankan)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Streamlit
```bash
streamlit run dashboard/dashboard.py
```

### 5. Buka browser
Streamlit akan otomatis membuka browser di `http://localhost:8501`

---

## 📊 Pertanyaan Bisnis

1. **Bagaimana tren jumlah pesanan dan total revenue bulanan selama tahun 2017–2018, dan pada bulan apa penjualan mencapai puncaknya?**

2. **Kategori produk apa yang menghasilkan total revenue tertinggi, dan bagaimana hubungannya dengan rata-rata skor ulasan pelanggan?**

## ✅ Kesimpulan

- Puncak penjualan terjadi pada **November 2017** (Black Friday), dengan pertumbuhan stabil di 2018.
- Kategori **health_beauty**, **watches_gifts**, dan **bed_bath_table** mendominasi revenue sekaligus memiliki kepuasan pelanggan yang baik.
