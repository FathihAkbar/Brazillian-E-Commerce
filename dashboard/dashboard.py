import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import seaborn as sns
import warnings
import os

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Brazilian E-Commerce Dashboard", page_icon="🛒", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(BASE_DIR, 'main_data.csv'))
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
    df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce')
    df['category_en'] = df['category_en'].fillna('unknown')
    return df

main_df = load_data()

st.title("🛒 Brazilian E-Commerce Dashboard")
st.markdown("Analisis data penjualan Olist E-Commerce tahun **2017–2018**")
st.markdown("---")

# Sidebar
st.sidebar.header("🔍 Filter Data")
years = sorted(main_df['order_purchase_timestamp'].dt.year.dropna().unique().astype(int))
selected_year = st.sidebar.selectbox("Pilih Tahun", ["Semua"] + [str(y) for y in years])

df_filtered = main_df[main_df['order_purchase_timestamp'].dt.year == int(selected_year)] \
    if selected_year != "Semua" else main_df

# KPI
total_revenue   = df_filtered['price'].sum()
total_orders    = df_filtered['order_id'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
avg_review      = df_filtered['review_score'].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Total Revenue",    f"BRL {total_revenue:,.0f}")
c2.metric("📦 Total Pesanan",    f"{total_orders:,}")
c3.metric("🧾 Avg Order Value",  f"BRL {avg_order_value:,.1f}")
c4.metric("⭐ Avg Review Score", f"{avg_review:.2f}")
st.markdown("---")

# ── Pertanyaan 1 ──────────────────────────────────────────────────────────────
st.subheader("📈 Pertanyaan 1: Tren Jumlah Pesanan & Revenue Bulanan")

monthly = df_filtered.groupby('year_month').agg(
    total_orders=('order_id', 'nunique'),
    total_revenue=('price', 'sum')
).reset_index().sort_values('year_month').reset_index(drop=True)

fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
sns.set_theme(style='whitegrid')
x = range(len(monthly))

ax1.bar(x, monthly['total_orders'], color='#4C72B0')
ax1.set_ylabel('Jumlah Pesanan', fontsize=11)
ax1.set_title('Tren Jumlah Pesanan Bulanan (2017–2018)', fontsize=13, fontweight='bold')
peak_idx = int(monthly['total_orders'].idxmax())
ax1.patches[peak_idx].set_facecolor('#E84040')
ax1.annotate(
    f"Puncak: {monthly.loc[peak_idx,'total_orders']:,}",
    xy=(peak_idx, monthly.loc[peak_idx,'total_orders']),
    xytext=(max(0, peak_idx-3), monthly.loc[peak_idx,'total_orders']*0.87),
    arrowprops=dict(arrowstyle='->', color='#E84040'),
    color='#E84040', fontsize=10, fontweight='bold'
)

ax2.bar(x, monthly['total_revenue']/1e6, color='#55A868')
ax2.set_ylabel('Revenue (Juta BRL)', fontsize=11)
ax2.set_title('Tren Total Revenue Bulanan (2017–2018)', fontsize=13, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(monthly['year_month'].tolist(), rotation=45, ha='right', fontsize=9)
peak_rev = int(monthly['total_revenue'].idxmax())
ax2.patches[peak_rev].set_facecolor('#E84040')
ax2.annotate(
    f"Puncak: BRL {monthly.loc[peak_rev,'total_revenue']/1e6:.2f}M",
    xy=(peak_rev, monthly.loc[peak_rev,'total_revenue']/1e6),
    xytext=(max(0, peak_rev-4), monthly.loc[peak_rev,'total_revenue']/1e6*0.85),
    arrowprops=dict(arrowstyle='->', color='#E84040'),
    color='#E84040', fontsize=10, fontweight='bold'
)

plt.tight_layout()
st.pyplot(fig1)

with st.expander("💡 Insight Pertanyaan 1"):
    st.markdown("""
    - Tren penjualan menunjukkan **pertumbuhan konsisten** sepanjang 2017–2018.
    - **Puncak pesanan terjadi pada November 2017**, dipicu oleh event Black Friday.
    - Memasuki 2018, volume pesanan stabil di kisaran **6.000–7.000 pesanan/bulan**.
    """)

st.markdown("---")

# ── Pertanyaan 2 ──────────────────────────────────────────────────────────────
st.subheader("🏆 Pertanyaan 2: Top 10 Kategori Produk Berdasarkan Revenue")

cat_stats = df_filtered.groupby('category_en').agg(
    total_revenue=('price', 'sum'),
    avg_review_score=('review_score', 'mean'),
    total_orders=('order_id', 'nunique')
).reset_index()

top10 = cat_stats.nlargest(10, 'total_revenue').sort_values('total_revenue')
norm   = mcolors.Normalize(vmin=top10['avg_review_score'].min(), vmax=top10['avg_review_score'].max())
colors = cm.RdYlGn(norm(top10['avg_review_score'].values))

fig2, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top10['category_en'], top10['total_revenue']/1e6, color=colors, edgecolor='white')
for bar, rev in zip(bars, top10['total_revenue']):
    ax.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2, f'BRL {rev/1e6:.2f}M', va='center', fontsize=9)
for bar, score in zip(bars, top10['avg_review_score']):
    ax.text(0.1, bar.get_y()+bar.get_height()/2, f'★ {score:.2f}', va='center', fontsize=9, color='white', fontweight='bold')
sm = cm.ScalarMappable(cmap='RdYlGn', norm=norm)
sm.set_array([])
plt.colorbar(sm, ax=ax, label='Avg Review Score', pad=0.01)
ax.set_xlabel('Total Revenue (Juta BRL)', fontsize=11)
ax.set_title('Top 10 Kategori Produk Berdasarkan Revenue\n(Warna = Avg Review Score)', fontsize=13, fontweight='bold')
plt.tight_layout()
st.pyplot(fig2)

with st.expander("💡 Insight Pertanyaan 2"):
    st.markdown("""
    - Kategori **health_beauty**, **watches_gifts**, dan **bed_bath_table** mendominasi revenue.
    - Ketiga kategori tersebut juga memiliki review score baik (rata-rata > 3.9).
    - Kategori **computers_accessories** memiliki potensi peningkatan di sisi kepuasan pelanggan.
    """)

st.markdown("---")
st.subheader("📋 Tabel Top 10 Kategori")
st.dataframe(
    top10[['category_en','total_revenue','avg_review_score','total_orders']]
    .rename(columns={'category_en':'Kategori','total_revenue':'Total Revenue (BRL)',
                     'avg_review_score':'Avg Review Score','total_orders':'Total Pesanan'})
    .sort_values('Total Revenue (BRL)', ascending=False)
    .reset_index(drop=True)
    .style.format({'Total Revenue (BRL)':'{:,.0f}','Avg Review Score':'{:.2f}','Total Pesanan':'{:,}'}),
    use_container_width=True
)
st.caption("Dashboard dibuat menggunakan Streamlit | Data: Brazilian E-Commerce (Olist) Dataset")
