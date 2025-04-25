
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

st.title("📜 Cari Undangan Ta")
st.write("Silakan ketik nama Anda untuk melihat undangan ramah tamah ibb.")

# Input nama
query = st.text_input("Masukkan nama Anda:")

if query:
    query = query.strip().upper()
    results = data[data['Nama Penerima'].str.contains(query)]

    if not results.empty:
        for idx, row in results.iterrows():
            st.subheader(row['Nama Penerima'])
            st.write("🔗 [Link Undangan](%s)" % row['Link'])
            st.write(row['Teks Sebar'])

            # Generate QR code from the link
            qr = qrcode.make(row['Link'])
            buf = BytesIO()
            qr.save(buf)
            st.image(Image.open(buf), caption="QR Undangan", use_column_width=False)
    else:
        st.warning("Nama tidak ditemukan. Coba cek kembali ejaan nama Anda.")
else:
    st.info("Masukkan nama Anda untuk mencari undangan.")
