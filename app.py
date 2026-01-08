import streamlit as st
import time

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (ESTÉTICA PERFECTA) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .header-logo { font-size: 1.5rem; font-weight: 700; color: #fff; display: flex; align-items: center; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    .glass-container { 
        background: rgba(38, 39, 48, 0.6); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 12px; padding: 30px; 
        height: 100%; text-align: center; 
        transition: all 0.3s ease; position: relative; 
    }
    
    .stTextArea textarea { background-color: rgba(0,0,0,0.3) !important; border: 1px solid #444 !important; color: #eee !important; }
    
    button[kind="primary"] { background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; border: none !important; box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important; }
    button[kind="primary"]:hover { transform: scale(1.03) !important; box-shadow: 0 0 30px rgba(0, 210, 255, 0.7) !important; }

    /* PLANES CON AURAS */
    .pro-card { border: 1px solid #00d2ff !important; }
    .pro-card:hover { box-shadow: 0 0 50px rgba(0, 210, 255, 0.5) !important; transform: translateY(-10px) !important; }
    
    .agency-card { border: 1px solid #DDA0DD !important; }
    .agency-card:hover { box-shadow: 0 0 50px rgba(221, 160, 221, 0.5) !important; transform: translateY(-10px) !important; }
    
    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.8rem; z-index: 10; }
    
    div.stButton > button { background: transparent; border: 1px solid #555; color: #ddd; width: 100%; transition: all 0.3s ease; }
    .result-box { border: 1px solid #00d2ff; padding: 20px; border-radius: 10px; background: rgba(0,0,0,0.2); margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 3. DICCIONARIO DE TRADUCCIÓN ---
if "idioma_selec" not in st.session_state:
    st.session_state.idioma_selec = "🇪🇸 Español"

if "Español" in st.session_state.idioma_selec:
    t = {
        "title1": "Convierte Anuncios Aburridos en",
        "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores.",
        "placeholder": "Pega el link o detalles de la propiedad...",
        "btn_gen": "✨ GENERAR DESCRIPCIÓN",
        "p1_name": "Inicial", "p1_desc": "3 descripciones / día<br>Soporte Básico<br>Marca de Agua", "p1_btn": "REGISTRO GRATIS",
        "p2_name": "Agente Pro", "p2_desc": "<b>Generaciones Ilimitadas</b><br>Pack Redes Sociales (IG/FB)<br>Optimización SEO", "p2_btn": "MEJORAR AHORA",
        "p3_name": "Agencia", "p3_desc": "5 Usuarios / Cuentas<br>Panel de Equipo<br>Acceso vía API", "p3_btn": "CONTACTAR VENTAS",
        "popular": "MÁS POPULAR"
    }
else:
    t = {
        "title1": "Turn Boring Listings into",
        "title2": "Sales Magnets",
        "sub": "The secret AI tool used by top producers.",
        "placeholder": "Paste link or property details...",
        "btn_gen": "✨ GENERATE DESCRIPTION",
        "p1_name": "Starter", "p1_desc": "3 descriptions / day<br>Basic Support<br>Watermark", "p1_btn": "FREE SIGN UP",
        "p2_name": "Agent Pro", "p2_desc": "<b>Unlimited Generations</b><br>Social Media Pack (IG/FB)<br>SEO Optimization", "p2_btn": "UPGRADE NOW",
        "p3_name": "Agency", "p3_desc": "5 Users / Accounts<br>Team Dashboard<br>API Access", "p3_btn": "CONTACT SALES",
        "popular": "MOST POPULAR"
    }

# --- 4. INTERFAZ SUPERIOR ---
col_logo, _, col_lang = st.columns([2, 4, 1.5])
with col_logo: 
    st.markdown('<div class="header-logo">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
with col_lang: 
    st.selectbox("", ["🇪🇸 Español", "🇺🇸 English"], label_visibility="collapsed", key="idioma_selec")

st.markdown(f"<h1 class='neon-title'>{t['title1']} <br><span class='neon-highlight'>{t['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{t['sub']}</p>", unsafe_allow_html=True)

# --- 5. ÁREA DE INPUT ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    user_input = st.text_area("", height=120, placeholder=t['placeholder'], label_visibility="collapsed")
    gen_btn = st.button(t['btn_gen'], type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if gen_btn and user_input:
        with st.spinner("..."):
            time.sleep(1)
            st.markdown(f'<div class="result-box">Esto es una simulación. Cuando tengas la API Key, aquí aparecerá el texto real.</div>', unsafe_allow_html=True)

# --- 6. SECCIÓN DE PLANES (TRADUCCIÓN ARREGLADA) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(f"""
    <div class='glass-container'>
        <h3 style='color: #ccc; margin-top:0;'>{t['p1_name']}</h3>
        <h1 style='font-size: 3rem; margin: 10px 0;'>$0</h1>
        <hr style='border-color: #444; opacity: 0.3;'>
        <p style='line-height: 1.6;'>{t['p1_desc']}</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button(t['p1_btn'], key="btn_p1")

with p2:
    st.markdown(f"""
    <div class='glass-container pro-card'>
        <div class='popular-badge'>{t['popular']}</div>
        <h3 style='color: #00d2ff; margin-top:10px;'>{t['p2_name']}</h3>
        <h1 style='font-size: 3rem; margin: 10px 0;'>$49</h1>
        <hr style='border-color: #00d2ff; opacity: 0.3;'>
        <p style='line-height: 1.6;'>{t['p2_desc']}</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button(t['p2_btn'], key="btn_p2")

with p3:
    st.markdown(f"""
    <div class='glass-container agency-card'>
        <h3 style='color: #DDA0DD; margin-top:0;'>{t['p3_name']}</h3>
        <h1 style='font-size: 3rem; margin: 10px 0;'>$199</h1>
        <hr style='border-color: #DDA0DD; opacity: 0.3;'>
        <p style='line-height: 1.6;'>{t['p3_desc']}</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button(t['p3_btn'], key="btn_p3")

st.markdown("<br><br>", unsafe_allow_html=True)
