import streamlit as st
import time
import pandas as pd
import random

# --- KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="GOZ.AI Pilot",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STYLING (CSS) ---
# Ten blok sprawia, że aplikacja wygląda jak natywna appka mobilna
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #10b981;
        color: white;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #059669;
        color: white;
    }
    .status-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0f172a;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    h1 { color: #0f172a; }
    h3 { color: #334155; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (MENU) ---
with st.sidebar:
    st.title("♻️ GOZ.AI")
    st.info("Wersja demonstracyjna v0.1")
    st.markdown("---")
    st.write("**Zalogowany jako:** Jan Kowalski")
    st.write("**Rola:** Użytkownik Pilotażowy")
    st.write("**Lokalizacja:** Warszawa, Mokotów")
    st.markdown("---")
    st.caption("Powered by Bielik AI & Streamlit")

# --- GŁÓWNY WIDOK ---
col1, col2 = st.columns([1, 5])
with col1:
    st.write("# ♻️")
with col2:
    st.title("GOZ.AI")
    st.caption("Skanuj. Naprawiaj. Zyskaj.")

st.markdown("---")

# --- KROK 1: INPUT ---
st.subheader("1. Skanowanie obiektu")
uploaded_file = st.file_uploader("Zrób zdjęcie uszkodzonego przedmiotu", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Wyświetlenie zdjęcia z zaokrąglonymi rogami (CSS trick w Streamlit nie działa bezpośrednio na img, ale ramka jest ok)
    st.image(uploaded_file, caption='Podgląd z kamery', use_column_width=True)
    
    # Symulacja wyboru AI
    analyze_btn = st.button("✨ Uruchom Analizę Bielik AI")
    
    if analyze_btn:
        with st.spinner('Przetwarzanie obrazu w chmurze...'):
            # Symulacja opóźnienia i kroków procesu
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            steps = [
                (10, "Normalizacja obrazu..."),
                (30, "Wykrywanie obiektu (YOLOv8)..."),
                (50, "Analiza uszkodzeń (Computer Vision)..."),
                (70, "Pobieranie danych producenta (DPP API)..."),
                (85, "Generowanie wyceny naprawy..."),
                (100, "Gotowe!")
            ]
            
            for percent, text in steps:
                time.sleep(random.uniform(0.4, 0.8)) # Losowe opóźnienie dla realizmu
                progress_bar.progress(percent)
                status_text.text(text)
            
            time.sleep(0.5)
            status_text.empty()
            progress_bar.empty()

        # --- KROK 2: WYNIKI ---
        st.success("Analiza zakończona pomyślnie!")
        
        # Karta Produktu (HTML Injection dla lepszego wyglądu)
        st.markdown("""
        <div class="status-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="margin:0; color:#1e293b;">iPhone 12</h2>
                <span style="background:#dcfce7; color:#166534; padding:5px 12px; border-radius:20px; font-weight:bold; font-size:0.8em;">NAPRAWIALNY</span>
            </div>
            <p style="color:#64748b; margin-top:5px;">Model A2403 • 64GB • Black</p>
            <hr style="border-top: 1px solid #e2e8f0;">
            <p><b>🔍 Diagnoza AI:</b> Wykryto mechaniczne uszkodzenie wyświetlacza (typ: pajączek). Ramka i tylna obudowa nienaruszone. Bateria: 84% kondycji.</p>
        </div>
        """, unsafe_allow_html=True)

        # Metryki finansowe
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Koszt naprawy", "350 PLN")
        with c2:
            st.metric("Wartość po", "1600 PLN", "+1200 PLN")
        with c3:
            st.metric("Czas", "24h")

        # --- KROK 3: PASZPORT CYFROWY (JSON) ---
        with st.expander("🇪🇺 Paszport Cyfrowy Produktu (DPP)"):
            st.info("Dane pobrane z centralnej bazy producenta.")
            st.json({
                "uuid": "550e8400-e29b-41d4-a716-446655440000",
                "manufacturer": "Apple Inc.",
                "origin": "Designed in California, Assembled in China",
                "repairability_score": "6.0/10",
                "materials": {
                    "glass": "Front/Back",
                    "aluminum": "Frame (Recycled 100%)",
                    "cobalt": "Battery"
                },
                "lifecycle_events": [
                    {"date": "2021-11-20", "type": "Activation"},
                    {"date": "2024-02-14", "type": "Damage_Detected_AI"}
                ]
            })

        # --- KROK 4: AKCJA ---
        st.subheader("Co chcesz zrobić?")
        
        # Tabs
        tab_repair, tab_sell = st.tabs(["🔧 Napraw Lokalnie", "💰 Sprzedaj na Części"])
        
        with tab_repair:
            st.write("Rekomendowane serwisy w promieniu 5km:")
            
            # Dane do mapy (Przykładowe koordynaty - Warszawa)
            map_data = pd.DataFrame({
                'lat': [52.229676 + random.uniform(-0.01, 0.01) for _ in range(3)],
                'lon': [21.012229 + random.uniform(-0.01, 0.01) for _ in range(3)]
            })
            st.map(map_data)
            
            st.button("Umów Kuriera (InPost) - 14.99 PLN", key="btn_courier")

        with tab_sell:
            st.markdown("""
            <div class="status-card">
                <h3>Oferta Błyskawiczna</h3>
                <p>Firma <b>GreenRefurb Sp. z o.o.</b> oferuje:</p>
                <div class="metric-value" style="color:#10b981;">420 PLN</div>
                <p style="font-size:0.8em; color:#64748b;">Płatność natychmiastowa BLIK</p>
            </div>
            """, unsafe_allow_html=True)
            st.button("Akceptuj Ofertę i Generuj Etykietę", key="btn_sell")