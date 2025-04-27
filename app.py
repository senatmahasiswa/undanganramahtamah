import streamlit as st
import pandas as pd
import qrcode
from PIL import Image
from io import BytesIO

# Load invitation data
@st.cache_data
def load_data():
    df = pd.read_excel("export-sebar.xlsx")
    df['Nama Penerima'] = df['Nama Penerima'].astype(str).str.strip().str.upper()
    return df

data = load_data()

# Styling
st.set_page_config(page_title="Undangan Ramah Tamah IBB", layout="centered")
st.markdown("<h1 style='text-align: center; color: navy;'>🎓 UNDANGAN RAMAH TAMAH IBB</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Masukkan nama Anda untuk melihat undangan ramah tamah IBB.</p>", unsafe_allow_html=True)

# Load logo
logo_path = "LOGO SEMA IBB.jpg"  # atau "LOGO SEMA IBB.png"
logo = Image.open(logo_path)

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

            # Generate QR code
            qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H  # high correction untuk bisa tempel logo
            )
            qr.add_data(row['Link'])
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

            # Resize logo
            logo_size = 60
            logo = logo.resize((logo_size, logo_size))

            # Paste logo ke tengah QR
            pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
            qr_img.paste(logo, pos)

            # Show QR code
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            st.image(Image.open(buf), caption="📎 Scan QR untuk akses undangan", use_container_width=True)
    else:
        st.error("❌ Nama tidak ditemukan. Silakan cek kembali ejaan nama Anda.")
else:
    st.info("📥 Silakan masukkan nama Anda di atas untuk mencari undangan.")
