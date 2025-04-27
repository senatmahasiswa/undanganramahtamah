import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from PIL import Image

# Load invitation data
@st.cache_data
def load_data():
    df = pd.read_excel("export-sebar.xlsx")
    df['Nama Penerima'] = df['Nama Penerima'].astype(str).str.strip().str.upper()
    return df

data = load_data()

# Styling
st.set_page_config(page_title="Undangan Ramah Tamah IBB", layout="centered")
st.markdown("<h1 style='text-align: center; color: navy;'>📜 UNDANGAN RAMAH TAMAH IBB</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Masukkan nama Anda untuk melihat undangan ramah tamah IBB.</p>", unsafe_allow_html=True)

# Input nama
query = st.text_input("Masukkan nama lengkap Anda:")

if query:
    query = query.strip().upper()
    with st.spinner('Mencari undangan...'):
        results = data[data['Nama Penerima'].str.contains(query)]

    if not results.empty:
        for idx, row in results.iterrows():
            st.success(f"🎉 Ditemukan: {row['Nama Penerima']}")
            st.markdown(f"<p style='text-align: center; font-size:20px;'>🔗 <a href='{row['Link']}' target='_blank'>Klik untuk membuka undangan</a></p>", unsafe_allow_html=True)

            # Generate QR code from the link
            qr = qrcode.make(row['Link'])
            buf = BytesIO()
            qr.save(buf)
            st.image(Image.open(buf), caption="📎 Scan QR untuk akses undangan", use_container_width=True)
    else:
        st.error("❌ Nama tidak ditemukan. Silakan cek kembali ejaan nama Anda.")
else:
    st.info("📥 Silakan masukkan nama Anda di atas untuk mencari undangan.")
