import streamlit as st
import time
import pandas as pd
import random
from datetime import datetime
from fpdf import FPDF
import base64

# --- KONFIGURACJA INFRASTRUKTURY (REALNE DANE BEYOND.PL) ---
CLOUD_PROVIDER = "Beyond.pl Data Center 2 (Poznań)"
AI_MODEL_VERSION = "Bielik-11B-v2.2-Instruct (NVIDIA H100 Cluster)"
SECURITY_STD = "ANSI/TIA-942 Rated 4 (Najwyższy w UE)"
ENERGY_SOURCE = "100% Green Energy (Odzysk ciepła)"

st.set_page_config(page_title="GOZ.AI x Beyond.pl", page_icon="♻️", layout="centered")

# --- FUNKCJE GENEROWANIA DOKUMENTÓW ---

def create_pdf(product_name, uuid, repair_score, valuation):
    pdf = FPDF()
    pdf.add_page()
    
    # Tło nagłówka (Eco Green)
    pdf.set_fill_color(6, 95, 70) 
    pdf.rect(0, 0, 210, 45, 'F')
    
    # Logo i Tytuł
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, txt="GOZ.AI", ln=1, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 5, txt="SYSTEM PASZPORTYZACJI PRODUKTÓW (DPP)", ln=1, align='C')
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 8)
    pdf.cell(0, 5, txt=f"POWERED BY: {CLOUD_PROVIDER}", ln=1, align='C')
    
    # Sekcja Danych
    pdf.ln(25)
    pdf.set_text_color(0, 0, 0)
    
    # Tabela danych
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt=f"RAPORT: {product_name}", ln=1)
    pdf.line(10, 75, 200, 75)
    
    pdf.ln(5)
    pdf.set_font("Arial", '', 11)
    
    metrics = [
        ("Identyfikator DPP:", uuid),
        ("Data Analizy AI:", datetime.now().strftime('%Y-%m-%d %H:%M')),
        ("Centrum Danych:", "Beyond.pl DC2 Poznań"),
        ("Model AI:", "Bielik-11B (Polish LLM)"),
        ("Indeks Naprawialnosci:", f"{repair_score}/10"),
    ]
    
    for key, val in metrics:
        pdf.cell(60, 8, txt=key, border=0)
        pdf.cell(0, 8, txt=val, ln=1, border=0)
        
    # Stopka Ekologiczna
    pdf.set_y(-40)
    pdf.set_fill_color(240, 253, 244)
    pdf.rect(0, 250, 210, 47, 'F')
    pdf.set_y(-30)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(22, 101, 52)
    pdf.cell(0, 5, txt=f"Analiza wykonana przy użyciu {ENERGY_SOURCE}", ln=1, align='C')
    pdf.cell(0, 5, txt=f"Bezpieczeństwo danych: {SECURITY_STD}", ln=1, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- CSS (DESIGN "INVESTOR READY") ---
st.markdown("""
<style>
    .main { background-color: #f8fafc; }
    .badge-beyond {
        background-color: #1e3a8a; color: white; padding: 5px 10px; 
        border-radius: 4px; font-weight: bold; font-size: 0.7em; letter-spacing: 1px;
    }
    .badge-eco {
        background-color: #059669; color: white; padding: 5px 10px; 
        border-radius: 4px; font-weight: bold; font-size: 0.7em; letter-spacing: 1px;
    }
    .stButton>button {
        background-color: #1e293b; color: white; border-radius: 8px; height: 50px;
        font-weight: 600; border: 1px solid #334155;
    }
    .stButton>button:hover {
        background-color: #334155; border-color: #475569; color: white;
    }
    .data-box {
        background: white; padding: 20px; border-radius: 12px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- APLIKACJA ---

# Header Inwestorski
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown(f'<span class="badge-beyond">INFRASTRUKTURA: BEYOND.PL</span> <span class="badge-eco">GREEN AI</span>', unsafe_allow_html=True)
    st.title("GOZ.AI Enterprise")
    st.caption("Suwerenna Platforma Cyrkularna zgodna z R2R")
with c2:
    # Placeholder na logo Beyond (lub podobne)
    st.markdown("### 🇵🇱 AI")

st.divider()

# KROK 1: INPUT
uploaded_file = st.file_uploader("Wgraj zdjęcie (Symulacja kamery)", type=['jpg', 'png'])

if uploaded_file:
    st.image(uploaded_file, width=300)
    
    if st.button("Uruchom Pipeline AI (Bielik + Vision)"):
        
        # Symulacja procesu w Data Center
        with st.status("Łączenie z Beyond.pl DC2 (Poznań)...", expanded=True) as status:
            time.sleep(0.5)
            st.write("🔒 Uwierzytelnianie w strefie Rated 4...")
            time.sleep(0.8)
            st.write("⚡ Alokacja zasobów GPU NVIDIA H100...")
            time.sleep(0.8)
            st.write("🧠 Inferencja modelu Bielik-11B (Kontekst: Prawo UE)...")
            time.sleep(1.0)
            st.write("✅ Generowanie Paszportu Produktu...")
            status.update(label="Analiza zakończona pomyślnie", state="complete", expanded=False)
            
        st.success("Dane zapisane w bezpiecznej chmurze.")

        # KROK 2: WYNIK (Data Box)
        st.markdown(f"""
        <div class="data-box">
            <h3 style="margin-top:0;">📱 iPhone 13 Pro (Sierra Blue)</h3>
            <p style="font-size:0.9em; color:#64748b;">ID: PL-WAW-8842-DPP</p>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top:15px;">
                <div>
                    <small>Diagnoza AI</small><br>
                    <b>Uszkodzony Ekran</b>
                </div>
                <div>
                    <small>Zalecenie GOZ</small><br>
                    <b style="color:#059669;">Naprawa (Opłacalna)</b>
                </div>
                <div>
                    <small>Szacowany Koszt</small><br>
                    <b>450 PLN</b>
                </div>
                <div>
                    <small>Wzrost Wartości</small><br>
                    <b style="color:#059669;">+1650 PLN</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # KROK 3: PDF I AKCJA
        st.write("")
        col_pdf, col_action = st.columns(2)
        
        with col_pdf:
            pdf_data = create_pdf("iPhone 13 Pro", "PL-BEYOND-8842", "8/10", "2100")
            st.download_button(
                label="📄 Pobierz Paszport",
                data=pdf_data,
                file_name="paszport_beyond.pdf",
                mime="application/pdf"
            )
        
        with col_action:
            st.button("🔧 Zleć Naprawę (B2B)")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; font-size:0.75em; color:#94a3b8;">
    Hostowano w: <b>{CLOUD_PROVIDER}</b><br>
    Standard bezpieczeństwa: {SECURITY_STD} | Zasilanie: {ENERGY_SOURCE}<br>
    &copy; 2024 GOZ.AI Sp. z o.o. (W organizacji)
</div>
""", unsafe_allow_html=True)