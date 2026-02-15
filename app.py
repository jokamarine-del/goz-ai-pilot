import streamlit as st
import time
import pandas as pd
import random
from datetime import datetime
from fpdf import FPDF
import json
import os
import io

# ============================================
# FAKE DATABASE LOADER
# ============================================

def load_fake_data():
    """Załaduj dane z fake_data.json"""
    if os.path.exists('fake_data.json'):
        with open('fake_data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "products": [],
        "repair_shops": [],
        "buyers": [],
        "recyclers": []
    }

# Załaduj dane
fake_data = load_fake_data()
PRODUCTS_DB = fake_data.get('products', [])
REPAIR_SHOPS = fake_data.get('repair_shops', [])
BUYERS = fake_data.get('buyers', [])
RECYCLERS = fake_data.get('recyclers', [])

# ============================================
# KONFIGURACJA STRONY
# ============================================

st.set_page_config(
    page_title="GOZ.AI Pilot",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# STYLING (CSS)
# ============================================

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
    .shop-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #f1f5f9;
        margin: 10px 0;
        border-left: 4px solid #10b981;
    }
    .buyer-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #eff6ff;
        margin: 10px 0;
        border-left: 4px solid #3b82f6;
    }
    .recycler-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0fdf4;
        margin: 10px 0;
        border-left: 4px solid #10b981;
    }
    .delivery-option {
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        margin: 15px 0;
        background-color: white;
        transition: all 0.3s ease;
    }
    .delivery-option:hover {
        border-color: #10b981;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
    }
    .delivery-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #0f172a;
        margin-bottom: 10px;
    }
    .delivery-desc {
        font-size: 0.9em;
        color: #64748b;
        margin-bottom: 15px;
    }
    .category-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.75em;
        font-weight: bold;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .cat-electronics {
        background-color: #dbeafe;
        color: #1e40af;
    }
    .cat-furniture {
        background-color: #fed7aa;
        color: #92400e;
    }
    .cat-appliance {
        background-color: #d1fae5;
        color: #065f46;
    }
    .confirmation-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f0fdf4;
        border-left: 5px solid #10b981;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
# ============================================

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'selected_shop' not in st.session_state:
    st.session_state.selected_shop = None
if 'selected_buyer' not in st.session_state:
    st.session_state.selected_buyer = None
if 'selected_recycler' not in st.session_state:
    st.session_state.selected_recycler = None

# ============================================
# SIDEBAR (MENU)
# ============================================

with st.sidebar:
    st.title("GOZ.AI")
    st.info("Wersja demonstracyjna v0.3")
    st.markdown("---")
    st.write("**Zalogowany jako:** Jan Kowalski")
    st.write("**Rola:** Uzytkownik Pilotazowy")
    st.write("**Lokalizacja:** Warszawa, Mokotow")
    st.markdown("---")
    st.write("**Produkty w bazie:** " + str(len(PRODUCTS_DB)))
    st.write("**Serwisy dostepne:** " + str(len(REPAIR_SHOPS)))
    st.write("**Kupujacy dostepni:** " + str(len(BUYERS)))
    st.markdown("---")
    
    if st.button("Powrót do strony głównej", use_container_width=True):
        st.session_state.current_page = 'main'
        st.session_state.analysis_result = None
        st.session_state.selected_shop = None
        st.session_state.selected_buyer = None
        st.session_state.selected_recycler = None
        st.rerun()
    
    st.caption("Powered by Bielik AI & Beyond.pl")

# ============================================
# FUNKCJE
# ============================================

def get_category_emoji(category):
    """Zwróć emoji dla kategorii"""
    emojis = {
        "electronics": "💻",
        "furniture": "🪑",
        "appliance": "🍽️"
    }
    return emojis.get(category, "📦")

def get_category_color(category):
    """Zwróć kolor CSS dla kategorii"""
    colors = {
        "electronics": "cat-electronics",
        "furniture": "cat-furniture",
        "appliance": "cat-appliance"
    }
    return colors.get(category, "")

def get_category_name(category):
    """Zwróć polską nazwę kategorii"""
    names = {
        "electronics": "Elektronika",
        "furniture": "Meble",
        "appliance": "Urzadzenia"
    }
    return names.get(category, "Inne")

def filter_shops_by_category(category):
    """Filtruj serwisy po kategorii"""
    return [shop for shop in REPAIR_SHOPS if category in shop.get('specialization', [])]

def filter_buyers_by_category(category):
    """Filtruj kupujacych po kategorii"""
    return [buyer for buyer in BUYERS if buyer.get('category') == category]

def filter_recyclers_by_category(category):
    """Filtruj recyklerow po kategorii"""
    return [recycler for recycler in RECYCLERS if category in recycler.get('accepted', [])]

def fake_ai_analyze(image_data):
    """Symuluj analize AI"""
    
    if not PRODUCTS_DB:
        product = {
            "name": "Nieznany produkt",
            "brand": "Nieznana marka",
            "market_value": 2000,
            "common_damage": ["general_damage"],
            "category": "electronics"
        }
    else:
        product = random.choice(PRODUCTS_DB)
    
    damage_type = random.choice(product.get('common_damage', ["general_damage"]))
    damage_level = random.randint(1, 8)
    
    # Logika biznesowa
    if damage_level <= 2:
        action = "SPRZEDAJ"
        action_text = "SPRZEDAJ"
    elif damage_level <= 5:
        action = "NAPRAW"
        action_text = "NAPRAW"
    else:
        action = "ZUTYLIZUJ"
        action_text = "ZUTYLIZUJ"
    
    repair_cost = random.randint(200, 800) if action == "NAPRAW" else 0
    market_value = product.get('market_value', 2000)
    estimated_value = max(0, market_value - (damage_level * 150))
    
    return {
        'product_name': product.get('name', 'Nieznany produkt'),
        'brand': product.get('brand', 'Nieznana marka'),
        'category': product.get('category', 'electronics'),
        'damage_level': damage_level,
        'damage_type': damage_type.replace('_', ' ').title(),
        'action': action,
        'action_text': action_text,
        'repair_cost': repair_cost,
        'market_value': market_value,
        'estimated_value': estimated_value,
        'confidence': round(random.uniform(0.85, 0.99), 2),
        'dpp_uuid': f"PL-{random.randint(10000, 99999)}-DPP"
    }

def generate_passport_pdf(analysis):
    """Generuj cyfrowy paszport jako PDF"""
    
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_fill_color(16, 185, 129)
    pdf.rect(0, 0, 210, 50, 'F')
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, txt="GOZ.AI - Paszport Cyfrowy", ln=1, align='C')
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, txt="CYFROWY PASZPORT PRODUKTU (DPP)", ln=1, align='C')
    
    # Content
    pdf.ln(15)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt=f"Produkt: {analysis['product_name']}", ln=1)
    
    pdf.set_font("Arial", '', 11)
    
    category_name = get_category_name(analysis['category'])
    
    data = [
        ("Identyfikator DPP:", analysis['dpp_uuid']),
        ("Marka:", analysis['brand']),
        ("Kategoria:", category_name),
        ("Data Analizy:", datetime.now().strftime('%Y-%m-%d %H:%M')),
        ("Poziom Uszkodzenia:", f"{analysis['damage_level']}/10"),
        ("Typ Uszkodzenia:", analysis['damage_type']),
        ("Rekomendacja:", analysis['action']),
        ("Wartosc rynkowa (przed):", f"{analysis['market_value']} PLN"),
        ("Szacunkowy koszt naprawy:", f"{analysis['repair_cost']} PLN"),
        ("Wartosc szacunkowa (po):", f"{analysis['estimated_value']} PLN"),
        ("Pewnosc AI:", f"{analysis['confidence']*100:.0f}%"),
    ]
    
    for label, value in data:
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(70, 8, txt=label)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, txt=str(value), ln=1)
    
    # Footer
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, txt="Dokument wygenerowany przez platforme GOZ.AI", ln=1, align='C')
    pdf.cell(0, 5, txt="Hostowane: Beyond.pl DC2 Poznan | AI: Bielik-11B", ln=1, align='C')
    
    # Zwróć jako bytes
    pdf_buffer = io.BytesIO()
    pdf_bytes = pdf.output()
    pdf_buffer.write(pdf_bytes)
    pdf_buffer.seek(0)
    
    return pdf_buffer.getvalue()

# ============================================
# STRONA GŁÓWNA
# ============================================

if st.session_state.current_page == 'main':
    col1, col2 = st.columns([1, 5])
    with col1:
        st.write("# [R]")
    with col2:
        st.title("GOZ.AI")
        st.caption("Skanuj. Naprawiaj. Zyskaj.")

    st.markdown("---")

    st.subheader("1. Skanowanie obiektu")
    uploaded_file = st.file_uploader("Zrób zdjęcie uszkodzonego przedmiotu", type=['jpg', 'png', 'jpeg'])

    if uploaded_file is not None:
        st.image(uploaded_file, caption='Podgląd z kamery', use_column_width=True)
        
        analyze_btn = st.button("Uruchom Analize Bielik AI")
        
        if analyze_btn:
            with st.spinner('Przetwarzanie obrazu w chmurze...'):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    (10, "Normalizacja obrazu..."),
                    (30, "Wykrywanie obiektu (YOLOv8)..."),
                    (50, "Analiza uszkodzen (Computer Vision)..."),
                    (70, "Pobieranie danych producenta (DPP API)..."),
                    (85, "Generowanie wyceny naprawy..."),
                    (100, "Gotowe!")
                ]
                
                for percent, text in steps:
                    time.sleep(random.uniform(0.4, 0.8))
                    progress_bar.progress(percent)
                    status_text.text(text)
                
                time.sleep(0.5)
                status_text.empty()
                progress_bar.empty()

            st.success("Analiza zakonczona pomyslnie!")
            
            # Analiza AI
            analysis = fake_ai_analyze(uploaded_file)
            st.session_state.analysis_result = analysis
            
            # Karta Produktu
            category_emoji = get_category_emoji(analysis['category'])
            category_color = get_category_color(analysis['category'])
            category_name = get_category_name(analysis['category'])
            
            st.markdown(f"""
            <div class="status-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="margin:0; color:#1e293b;">{category_emoji} {analysis['product_name']}</h2>
                    <span style="background:#dcfce7; color:#166534; padding:5px 12px; border-radius:20px; font-weight:bold; font-size:0.8em;">{analysis['action_text']}</span>
                </div>
                <p style="color:#64748b; margin-top:5px;">Marka: {analysis['brand']} • ID: {analysis['dpp_uuid']}</p>
                <span class="category-badge {category_color}">{category_name}</span>
                <hr style="border-top: 1px solid #e2e8f0;">
                <p><b>Diagnoza AI:</b> {analysis['damage_type']} (Poziom uszkodzenia: {analysis['damage_level']}/10)</p>
            </div>
            """, unsafe_allow_html=True)

            # Metryki finansowe
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Koszt naprawy", f"{analysis['repair_cost']} PLN")
            with c2:
                st.metric("Wartosc rynkowa", f"{analysis['market_value']} PLN")
            with c3:
                st.metric("Pewnosc AI", f"{int(analysis['confidence']*100)}%")

            # Paszport Cyfrowy
            with st.expander("Paszport Cyfrowy Produktu (DPP)"):
                st.info("Dane pobrane z centralnej bazy producenta i systemu GOZ.AI")
                st.json({
                    "uuid": analysis['dpp_uuid'],
                    "product_name": analysis['product_name'],
                    "brand": analysis['brand'],
                    "category": category_name,
                    "damage_level": analysis['damage_level'],
                    "damage_type": analysis['damage_type'],
                    "repair_feasibility": analysis['action'] == 'NAPRAW',
                    "estimated_repair_cost": analysis['repair_cost'],
                    "confidence": analysis['confidence'],
                    "analysis_date": datetime.now().isoformat()
                })

            # PDF download
            pdf_data = generate_passport_pdf(analysis)
            st.download_button(
                label="Pobierz PDF Paszportu",
                data=pdf_data,
                file_name=f"paszport_{analysis['dpp_uuid']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            # Akcje
            st.markdown("---")
            st.subheader("Co chcesz zrobic?")
            
            # Filtruj dane po kategorii
            available_shops = filter_shops_by_category(analysis['category'])
            available_buyers = filter_buyers_by_category(analysis['category'])
            available_recyclers = filter_recyclers_by_category(analysis['category'])
            
            # Tabs
            tab_repair, tab_sell, tab_recycle = st.tabs(["Napraw Lokalnie", "Sprzedaj", "Zutylizuj"])
            
            # ============================================
            # TAB 1: NAPRAWA
            # ============================================
            
            with tab_repair:
                st.write(f"### Rekomendowane serwisy ({len(available_shops)} dostepne):")
                
                if available_shops:
                    # Mapa serwisów
                    map_data = pd.DataFrame({
                        'latitude': [shop['lat'] for shop in available_shops],
                        'longitude': [shop['lon'] for shop in available_shops]
                    })
                    st.map(map_data, zoom=12)
                    
                    # Lista serwisów
                    st.write("\n**Dostepne serwisy:**\n")
                    for shop in available_shops:
                        spec_badges = " ".join([f"<span class='category-badge {get_category_color(cat)}'>{get_category_name(cat)}</span>" for cat in shop.get('specialization', [])])
                        
                        st.markdown(f"""
                        <div class="shop-card">
                            <div style="display:flex; justify-content:space-between;">
                                <div>
                                    <b>{shop['name']}</b><br>
                                    <small>Adres: {shop['address']}</small><br>
                                    <small>Rating: {shop['rating']}/5.0 | Czas odpowiedzi: {shop['response_time']}</small><br>
                                    <div style="margin-top:8px;">
                                        {spec_badges}
                                    </div>
                                </div>
                                <div style="text-align:right; font-weight:bold; color:#10b981;">
                                    {shop['avg_price']} PLN
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Zaakceptuj {shop['name']}", key=f"repair_{shop['id']}", use_container_width=True):
                            st.session_state.selected_shop = shop
                            st.session_state.current_page = 'repair_delivery'
                            st.rerun()
                else:
                    st.warning(f"Brak dostepnych serwisów dla kategorii: {category_name}")
            
            # ============================================
            # TAB 2: SPRZEDAŻ
            # ============================================
            
            with tab_sell:
                st.write(f"### Oferty odkupu produktu ({len(available_buyers)} dostepne):")
                
                if available_buyers:
                    for buyer in available_buyers:
                        offer_price = int(analysis['estimated_value'] * buyer['offer_percent'])
                        
                        st.markdown(f"""
                        <div class="buyer-card">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div>
                                    <b>{buyer['name']}</b><br>
                                    <small>Rating: {buyer['rating']}/5.0</small><br>
                                    <small>Dostarczenie: {buyer['delivery_time']}</small>
                                </div>
                                <div style="text-align:right; font-weight:bold; color:#10b981; font-size:1.3em;">
                                    {offer_price} PLN
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Zaakceptuj {buyer['name']}", key=f"buyer_{buyer['name']}", use_container_width=True):
                            st.session_state.selected_buyer = buyer
                            st.session_state.current_page = 'sell_delivery'
                            st.rerun()
                else:
                    st.warning(f"Brak dostepnych kupujacych dla kategorii: {category_name}")
            
            # ============================================
            # TAB 3: RECYKLING
            # ============================================
            
            with tab_recycle:
                st.write(f"### Certyfikowane punkty recyklingu ({len(available_recyclers)} dostepne):")
                
                if available_recyclers:
                    for recycler in available_recyclers:
                        st.markdown(f"""
                        <div class="recycler-card">
                            <b>{recycler['name']}</b><br>
                            <small>Adres: {recycler['address']}</small><br>
                            <small>Rating: {recycler['rating']}/5.0 | Certyfikowany: {recycler.get('certification', 'WEEE')}</small><br>
                            <small>Przyjmuje: {recycler['materials']}</small><br>
                            <small style="color:#059669; font-weight:bold;">Cena: {recycler['price']}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"Zaakceptuj {recycler['name']}", key=f"recycler_{recycler['id']}", use_container_width=True):
                            st.session_state.selected_recycler = recycler
                            st.session_state.current_page = 'recycle_delivery'
                            st.rerun()
                else:
                    st.warning(f"Brak dostepnych recyklerow dla kategorii: {category_name}")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding:20px; color:#666; font-size:0.85em;">
        <small>
            GOZ.AI Demo 2024 | Hostowane: Beyond.pl DC2 (Poznan) | AI: Bielik-11B | 
            <a href="https://github.com/jokamarine-del/goz-ai-pilot" target="_blank">GitHub</a>
        </small>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# STRONA: OPCJE DOSTAWY DO NAPRAWY
# ============================================

elif st.session_state.current_page == 'repair_delivery':
    st.title("Wybierz sposób dostarczenia do serwisu")
    
    analysis = st.session_state.analysis_result
    shop = st.session_state.selected_shop
    category_emoji = get_category_emoji(analysis['category'])
    
    st.markdown(f"""
    <div class="status-card">
        <h3 style="margin-top:0;">{category_emoji} {analysis['product_name']}</h3>
        <p><b>Serwis:</b> {shop['name']}</p>
        <p><b>Koszt naprawy:</b> {analysis['repair_cost']} PLN</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Jak chcesz dostarczyć produkt do serwisu?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="delivery-option">
            <div class="delivery-title">InPost Paczkomat</div>
            <div class="delivery-desc">
                Wyslij poprzez najblizszy paczkomat InPost.<br>
                <b>Koszt:</b> 14.99 PLN<br>
                <b>Czas:</b> 24-48h
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Zamów kurier InPost", use_container_width=True, key="repair_inpost"):
            st.session_state.current_page = 'repair_confirmation_inpost'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="delivery-option">
            <div class="delivery-title">Dostarcze osobiście</div>
            <div class="delivery-desc">
                Odbioremy produkt od Ciebie.<br>
                <b>Koszt:</b> 0 PLN<br>
                <b>Czas:</b> 2-3 dni
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Umów osobisty odbiór", use_container_width=True, key="repair_personal"):
            st.session_state.current_page = 'repair_confirmation_personal'
            st.rerun()

# ============================================
# POTWIERDZENIE NAPRAWY - INPOST
# ============================================

elif st.session_state.current_page == 'repair_confirmation_inpost':
    analysis = st.session_state.analysis_result
    shop = st.session_state.selected_shop
    category_emoji = get_category_emoji(analysis['category'])
    inpost_cost = 14.99
    total_cost = analysis['repair_cost'] + inpost_cost
    
    st.title("Potwierdzenie - Naprawa przez InPost")
    
    st.markdown(f"""
    <div class="confirmation-box">
        <h3 style="margin-top:0; color:#166534;">Zamówienie potwierdzone!</h3>
        <p style="color:#166534;">Twoja przesyłka została zarejestrowana w systemie.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="status-card">
        <h3>Szczegóły zamówienia</h3>
        <p><b>Produkt:</b> {category_emoji} {analysis['product_name']}</p>
        <p><b>Serwis:</b> {shop['name']}</p>
        <p><b>Adres serwisu:</b> {shop['address']}</p>
        <hr>
        <p><b>Koszt naprawy:</b> {analysis['repair_cost']} PLN</p>
        <p><b>Przesyłka InPost:</b> {inpost_cost} PLN</p>
        <p style="font-size:1.3em; font-weight:bold; color:#10b981;">
            <b>RAZEM: {total_cost} PLN</b>
        </p>
        <hr>
        <p><b>Numer śledzenia:</b> PL-{random.randint(1000000000, 9999999999)}</p>
        <p><b>Przesyłka do serwisu:</b> Od razu</p>
        <p><b>Naprawa:</b> ok. {shop['response_time']}</p>
        <p><b>Przesyłka powrotna:</b> Do 5 dni roboczych</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📧 Potwierdzenie zostało wysłane na Twój email. Dowiesz się o statusie naprawy SMS-em lub mailem.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Pobierz etykietę do wydruku", use_container_width=True):
            st.success("📄 Etykieta gotowa do pobrania!")
            st.info("Instrukcja: Wydrukuj etykietę i dołącz ją do paczki w paczkomacie InPost")
    
    with col2:
        if st.button("Powrót do głównego menu", use_container_width=True):
            st.session_state.current_page = 'main'
            st.session_state.analysis_result = None
            st.rerun()

# ============================================
# POTWIERDZENIE NAPRAWY - OSOBISTY ODBIÓR
# ============================================

elif st.session_state.current_page == 'repair_confirmation_personal':
    analysis = st.session_state.analysis_result
    shop = st.session_state.selected_shop
    category_emoji = get_category_emoji(analysis['category'])
    
    st.title("Potwierdzenie - Osobisty odbiór")
    
    st.markdown(f"""
    <div class="confirmation-box">
        <h3 style="margin-top:0; color:#166534;">Umówienie potwierdzone!</h3>
        <p style="color:#166534;">Serwis potwierdził gotowość do odbioru produktu.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="status-card">
        <h3>Szczegóły umówienia</h3>
        <p><b>Produkt:</b> {category_emoji} {analysis['product_name']}</p>
        <p><b>Serwis:</b> {shop['name']}</p>
        <p><b>Adres:</b> {shop['address']}</p>
        <p><b>Telefon:</b> +48 22 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}</p>
        <hr>
        <p><b>Koszt naprawy:</b> {analysis['repair_cost']} PLN</p>
        <p style="font-size:1.3em; font-weight:bold; color:#10b981;">
            <b>RAZEM: {analysis['repair_cost']} PLN (brak opcji dostawy)</b>
        </p>
        <hr>
        <p><b>ID zamówienia:</b> REP-{random.randint(100000, 999999)}</p>
        <p><b>Odbór:</b> 2-3 dni robocze (Pon-Pt 10:00-18:00)</p>
        <p><b>Naprawa:</b> ok. {shop['response_time']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("⏰ Pamiętaj aby odebrać produkt w ciągu 14 dni od naprawy!")
    st.info("Serwis czeka na Twój telefon w celu ustalenia dokładnego terminu odbioru.")
    
    if st.button("Powrót do głównego menu", use_container_width=True):
        st.session_state.current_page = 'main'
        st.session_state.analysis_result = None
        st.rerun()

# ============================================
# STRONA: OPCJE DOSTAWY DO SPRZEDAŻY
# ============================================

elif st.session_state.current_page == 'sell_delivery':
    st.title("Wybierz sposób dostarczenia produktu")
    
    analysis = st.session_state.analysis_result
    buyer = st.session_state.selected_buyer
    category_emoji = get_category_emoji(analysis['category'])
    offer_price = int(analysis['estimated_value'] * buyer['offer_percent'])
    
    st.markdown(f"""
    <div class="status-card">
        <h3 style="margin-top:0;">{category_emoji} {analysis['product_name']}</h3>
        <p><b>Kupujący:</b> {buyer['name']}</p>
        <p><b>Oferta:</b> {offer_price} PLN</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Jak chcesz dostarczyć produkt do kupującego?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="delivery-option">
            <div class="delivery-title">InPost Paczkomat</div>
            <div class="delivery-desc">
                Wyslij poprzez paczkomat InPost.<br>
                <b>Koszt:</b> 14.99 PLN<br>
                <b>Czas:</b> 24-48h<br>
                <b>Płatność:</b> Po weryfikacji
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Wyslij przez InPost", use_container_width=True, key="sell_inpost"):
            st.session_state.current_page = 'sell_confirmation_inpost'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="delivery-option">
            <div class="delivery-title">Dostarcze osobiście</div>
            <div class="delivery-desc">
                Przebierze je kupujący.<br>
                <b>Koszt:</b> 0 PLN<br>
                <b>Czas:</b> Umówić się<br>
                <b>Płatność:</b> Na miejscu
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Umów spotkanie", use_container_width=True, key="sell_personal"):
            st.session_state.current_page = 'sell_confirmation_personal'
            st.rerun()

# ============================================
# POTWIERDZENIE SPRZEDAŻY - INPOST
# ============================================

elif st.session_state.current_page == 'sell_confirmation_inpost':
    analysis = st.session_state.analysis_result
    buyer = st.session_state.selected_buyer
    category_emoji = get_category_emoji(analysis['category'])
    offer_price = int(analysis['estimated_value'] * buyer['offer_percent'])
    inpost_cost = 14.99
    net_payment = offer_price - inpost_cost
    
    st.title("Potwierdzenie - Sprzedaż przez InPost")
    
    st.markdown(f"""
    <div class="confirmation-box">
        <h3 style="margin-top:0; color:#166534;">Transakcja potwierdzona!</h3>
        <p style="color:#166534;">Przesyłka jest zabezpieczona systemem Escrow.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="status-card">
        <h3>Szczegóły transakcji</h3>
        <p><b>Produkt:</b> {category_emoji} {analysis['product_name']}</p>
        <p><b>Kupujący:</b> {buyer['name']}</p>
        <p><b>Kontakt:</b> {buyer['name']} Support</p>
        <hr>
        <p><b>Cena sprzedaży:</b> {offer_price} PLN</p>
        <p><b>Koszt InPost:</b> {inpost_cost} PLN</p>
        <p style="font-size:1.3em; font-weight:bold; color:#10b981;">
            <b>DO WYPŁATY: {net_payment} PLN</b>
        </p>
        <hr>
        <p><b>Numer śledzenia:</b> PL-{random.randint(1000000000, 9999999999)}</p>
        <p><b>Status Escrow:</b> AKTYWNY</p>
        <p><b>Płatność:</b> Po weryfikacji przez kupującego (3-5 dni)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("💳 Kwota czeka w bezpiecznym Escrow. Trafia na Twoje konto gdy kupujący potwierdzi otrzymanie.")
    st.info("📧 Instrukcje wysłane na email. Pobierz etykietę InPost i wyślij pakiet.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Pobierz etykietę do wydruku", use_container_width=True):
            st.success("📄 Etykieta gotowa!")
    
    with col2:
        if st.button("Powrót do głównego menu", use_container_width=True):
            st.session_state.current_page = 'main'
            st.session_state.analysis_result = None
            st.rerun()

# ============================================
# POTWIERDZENIE SPRZEDAŻY - OSOBISTE SPOTKANIE
# ============================================

elif st.session_state.current_page == 'sell_confirmation_personal':
    analysis = st.session_state.analysis_result
    buyer = st.session_state.selected_buyer
    category_emoji = get_category_emoji(analysis['category'])
    offer_price = int(analysis['estimated_value'] * buyer['offer_percent'])
    
    st.title("Potwierdzenie - Osobiste spotkanie")
    
    st.markdown(f"""
    <div class="confirmation-box">
        <h3 style="margin-top:0; color:#166534;">Umówienie potwierdzone!</h3>
        <p style="color:#166534;">Kupujący czeka na spotkanie.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="status-card">
        <h3>Szczegóły spotkania</h3>
        <p><b>Produkt:</b> {category_emoji} {analysis['product_name']}</p>
        <p><b>Kupujący:</b> {buyer['name']}</p>
        <p><b>Kontakt:</b> +48 22 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}</p>
        <p><b>Email:</b> contact@{buyer['name'].lower()}.pl</p>
        <hr>
        <p><b>Cena:</b> {offer_price} PLN</p>
        <p style="font-size:1.3em; font-weight:bold; color:#10b981;">
            <b>DO WYPŁATY: {offer_price} PLN (na miejscu)</b>
        </p>
        <hr>
        <p><b>ID transakcji:</b> SELL-{random.randint(100000, 999999)}</p>
        <p><b>Termin spotkania:</b> Do uzgodnienia</p>
        <p><b>Forma płatności:</b> Gotówka / Przelew</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("☎️ Skontaktuj się z kupującym celem ustalenia miejsca i czasu spotkania.")
    st.warning("⚠️ Sprawdź dane konta przed przekazaniem produktu!")
    
    if st.button("Powrót do głównego menu", use_container_width=True):
        st.session_state.current_page = 'main'
        st.session_state.analysis_result = None
        st.rerun()

# ============================================
# STRONA: OPCJE DOSTAWY DO RECYKLINGU
# ============================================

elif st.session_state.current_page == 'recycle_delivery':
    st.title("Wybierz sposób dostarczenia do recyklingu")
    
    analysis = st.session_state.analysis_result
    recycler = st.session_state.selected_recycler
    category_emoji = get_category_emoji(analysis['category'])
    
    st.markdown(f"""
    <div class="status-card">
        <h3 style="margin-top:0;">{category_emoji} {analysis['product_name']}</h3>
        <p><b>Punkt recyklingu:</b> {recycler['name']}</p>
        <p><b>Certyfikacja:</b> {recycler.get('certification', 'WEEE')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Jak chcesz dostarczyć produkt do recyklingu?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="delivery-option">
            <div class="delivery-title">Kurier - Darmowy odbiór</div>
            <div class="delivery-desc">
                Kurier odbierze z Twojego domu.<br>
                <b>Koszt:</b> 0 PLN (za darmo)<br>
                <b>Czas:</b> 24h<br>
                <b>Bonus:</b> +5 pkt GOZ.AI
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Zamów kurier", use_container_width=True, key="recycle_courier"):
            st.session_state.current_page = 'recycle_confirmation_courier'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="delivery-option">
            <div class="delivery-title">Dostarcze sam</div>
            <div class="delivery-desc">
                Dowieziesz do punktu recyklingu.<br>
                <b>Koszt:</b> 0 PLN<br>
                <b>Czas:</b> Dostępne godziny<br>
                <b>Bonus:</b> +10 pkt GOZ.AI
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Dostarcze sam", use_container_width=True, key="recycle_personal"):
            st.session_state.current_page = 'recycle_confirmation_personal'
            st.rerun()

# ============================================
# POTWIERDZENIE RECYKLINGU - KURIER
# ============================================

elif st.session_state.current_page == 'recycle_confirmation_courier':
    analysis = st.session_state.analysis_result
    recycler = st.session_state.selected_recycler
    category_emoji = get_category_emoji(analysis['category'])
    
    st.title("Potwierdzenie - Recykling przez kurier")
    
    st.markdown(f"""
    <div class="confirmation-box">
        <h3 style="margin-top:0; color:#166534;">Odbiór zaplanowany!</h3>
        <p style="color:#166534;">Kurier będzie u Ciebie za 24h.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="status-card">
        <h3>Szczegóły odbioru</h3>
        <p><b>Produkt:</b> {category_emoji} {analysis['product_name']}</p>
        <p><b>Punkt docelowy:</b> {recycler['name']}</p>
        <p><b>Adres:</b> {recycler['address']}</p>
        <p><b>Certyfikacja:</b> {recycler.get('certification', 'WEEE')}</p>
        <hr>
        <p><b>Koszt:</b> 0 PLN (darmowy)</p>
        <p><b>Bonus GOZ.AI:</b> +5 pkt</p>
        <hr>
        <p><b>ID zlecenia:</b> REC-{random.randint(100000, 999999)}</p>
        <p><b>Numer kuriera:</b> PL-{random.randint(1000000000, 9999999999)}</p>
        <p><b>Odbór:</b> Jutro 08:00 - 22:00</p>
        <p><b>Zaświadczenie:</b> Otrzymasz mailem</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("♻️ Dzięki za wspieranie gospodarki cyrkularnej!")
    st.info("📧 Potwierdzenie wysłane na email. Będziesz mógł śledzić przesyłkę w systemie GOZ.AI.")
    
    if st.button("Powrót do głównego menu", use_container_width=True):
        st.session_state.current_page = 'main'
        st.session_state.analysis_result = None
        st.rerun()

# ============================================
# POTWIERDZENIE RECYKLINGU - OSOBISTE
# ============================================

elif st.session_state.current_page == 'recycle_confirmation_personal':
    analysis = st.session_state.analysis_result
    recycler = st.session_state.selected_recycler
    category_emoji = get_category_emoji(analysis['category'])
    
    st.title("Potwierdzenie - Osobisty odbiór w punkcie")
    
    st.markdown(f"""
    <div class="confirmation-box">
        <h3 style="margin-top:0; color:#166534;">Punkt recyklingu czeka!</h3>
        <p style="color:#166534;">Możesz pojawić się w podanych godzinach.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="status-card">
        <h3>Szczegóły punktu recyklingu</h3>
        <p><b>Produkt:</b> {category_emoji} {analysis['product_name']}</p>
        <p><b>Punkt:</b> {recycler['name']}</p>
        <p><b>Adres:</b> {recycler['address']}</p>
        <p><b>Rating:</b> {recycler['rating']}/5.0</p>
        <hr>
        <p><b>Godziny otwarcia:</b></p>
        <p>Pon-Pt: 08:00 - 18:00</p>
        <p>Sob: 10:00 - 16:00</p>
        <p>Niedz: ZAMKNIĘTE</p>
        <hr>
        <p><b>Telefon:</b> +48 22 {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}</p>
        <p><b>Koszt:</b> 0 PLN (darmowy)</p>
        <p><b>Bonus GOZ.AI:</b> +10 pkt</p>
        <hr>
        <p><b>ID zlecenia:</b> REC-{random.randint(100000, 999999)}</p>
        <p><b>Zaświadczenie:</b> Otrzymasz w punkcie</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("♻️ Dziękujemy! Twój produkt będzie odpowiednio przetworzony!")
    st.info("💚 Każdy powrót produktu do recyklingu pomaga planecie!")
    
    if st.button("Powrót do głównego menu", use_container_width=True):
        st.session_state.current_page = 'main'
        st.session_state.analysis_result = None
        st.rerun()