import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURASI ---
UBIDOTS_TOKEN = "BBUS-pWBdotCiO0NOE1cCwrux1U4IablrP6"
DEVICE_LABEL = "smartroom"

VARIABLES = {
    "🌡️ Suhu (°C)": ("suhu", "#ffe0b2"),
    "💧 Kelembapan (%)": ("kelembaban", "#b3e5fc"),
    "💡 Cahaya (lux)": ("cahaya", "#fff9c4"),
    "🚶 Gerakan": ("gerakan", "#c8e6c9")
}

# --- FUNGSI AMBIL DATA DARI UBIDOTS ---
def get_latest_value(variable_label):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/{variable_label}/lv"
    headers = {"X-Auth-Token": UBIDOTS_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return float(response.text)
        except:
            return response.text
    return None

# --- STATUS FUNGSIONAL ---
def status_suhu(suhu):
    if suhu < 24:
        return "Dingin ❄️", "#81d4fa"
    elif suhu <= 30:
        return "Normal ✅", "#aed581"
    else:
        return "Panas 🔥", "#ef9a9a"

def status_cahaya(cahaya):
    if cahaya < 800:
        return "Gelap 🌙", "#b39ddb"
    elif cahaya <= 2000:
        return "Normal ✅", "#aed581"
    else:
        return "Terang ☀️", "#fff176"

def status_gerakan(gerakan):
    if gerakan == 1.0:
        return "Terdeteksi 🚨", "#ffab91"
    else:
        return "Tidak Ada ❌", "#cfd8dc"

# --- DESAIN HALAMAN ---
st.set_page_config(page_title="SmartRoom Realtime Dashboard", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .title-text {
        font-size: 36px;
        font-weight: bold;
        color: #0d47a1;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">📡 SmartRoom IoT - Realtime AI Dashboard</p>', unsafe_allow_html=True)

# --- REFRESH OTOMATIS ---
st_autorefresh(interval=5000, key="data_refresh")

# --- AMBIL SEMUA DATA ---
suhu = get_latest_value("suhu")
kelembaban = get_latest_value("kelembaban")
cahaya = get_latest_value("cahaya")
gerakan = get_latest_value("gerakan")

# --- TAMPILKAN DATA ---
cols = st.columns(4)
data_list = [suhu, kelembaban, cahaya, gerakan]

for i, (label, (var, color)) in enumerate(VARIABLES.items()):
    value = data_list[i]
    with cols[i]:
        if value is not None:
            st.markdown(f"""
                <div style="background-color: {color}; border-radius: 15px; padding: 25px; margin: 10px 0;
                            text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); font-size: 18px;">
                    <h3>{label}</h3>
                    <p style="font-size: 32px; font-weight: bold; color: #0d47a1;">{value}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background-color: {color}; border-radius: 15px; padding: 25px; margin: 10px 0;
                            text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); font-size: 18px;">
                    <h3>{label}</h3>
                    <p style="font-size: 18px; color: #999;">Data belum tersedia</p>
                </div>
            """, unsafe_allow_html=True)

# --- STATUS KONDISI ---
st.markdown("---")
st.subheader("📊 Status Kondisi Lingkungan:")

if suhu is not None and cahaya is not None and gerakan is not None:
    status1, warna1 = status_suhu(suhu)
    status2, warna2 = status_cahaya(cahaya)
    status3, warna3 = status_gerakan(gerakan)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div style='background-color:{warna1}; padding:20px; border-radius:10px; text-align:center'><h4>Status Suhu</h4><p>{status1}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div style='background-color:{warna2}; padding:20px; border-radius:10px; text-align:center'><h4>Status Cahaya</h4><p>{status2}</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div style='background-color:{warna3}; padding:20px; border-radius:10px; text-align:center'><h4>Status Gerakan</h4><p>{status3}</p></div>", unsafe_allow_html=True)
else:
    st.warning("❗ Beberapa data belum tersedia, tunggu beberapa saat...")
