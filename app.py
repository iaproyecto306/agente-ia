import streamlit as st
import time

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (RESTAURACIÓN TOTAL Y BOTONES CON AURA) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .header-logo { font-size: 1.5rem; font-weight: 700; color: #fff; display: flex; align-items: center; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    /* RECTÁNGULO PARA VIDEO (Arriba del input) */
    .video-placeholder {
        background: rgba(255, 255, 255, 0.03);
        border: 1px dashed rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        height: 180px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        color: #666;
        transition: all 0.5s ease;
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* CONTENEDOR DE INPUT */
    .glass-container { 
        background: rgba(38, 39, 48, 0.6); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 12px; padding: 30px; 
        text-align: center; position: relative; 
    }
    
    /* TARJETAS DE PLANES (Animaciones de flotado) */
    .free-card:hover { transform: translateY(-10px) !important; border: 1px solid rgba(255, 255, 255, 0.3); transition: 0.3s; }
    .pro-card { border: 1px solid #00d2ff !important; }
    .pro-card:hover { box-shadow: 0 0 50px rgba(0, 210, 255, 0.5) !important; transform: translateY(-10px) !important; transition: 0.3s; }
    .agency-card { border: 1px solid #DDA0DD !important; }
    .agency-card:hover { box-shadow: 0 0 50px rgba(221, 160, 221, 0.5) !important; transform: translateY(-10px) !important; transition: 0.3s; }

    /* --- ESTILOS DE LOS BOTONES DE COMPRA BAJO LOS PLANES --- */
    div.stButton > button { width: 100%; transition: all 0.3s ease; font-weight: 700; border-radius: 8px; height: 3.5rem; margin-top: 15px; }

    /* Botón Plan Inicial (Free) - Solo sube */
    [data-testid="column"]:nth-child(1) div.stButton > button { background: transparent; border: 1px solid #444; color: #999; }
    [data-testid="column"]:nth-child(1) div.stButton > button:hover { transform: translateY(-5px); border-color: #fff; color: #fff; background: rgba(255,255,255,0.1); }

    /* Botón Plan Pro - Cian con Brillo Aura */
    [data-testid="column"]:nth-child(2) div.stButton > button { background: transparent; border: 2px solid #00d2ff; color: #00d2ff; }
    [data-testid="column"]:nth-child(2) div.stButton > button:hover { transform: translateY(-5px); background: #00d2ff !important; color: #000 !important; box-shadow: 0 0 30px rgba(0, 210, 255, 0.8); }

    /* Botón Plan Agencia - Violeta con Brillo Aura */
    [data-testid="column"]:nth-child(3) div.stButton > button { background: transparent; border: 2px solid #DDA0DD; color: #DDA0DD; }
    [data-testid="column"]:nth-child(3) div.stButton > button:hover { transform: translateY(-5px); background: #DDA0DD !important; color: #000 !important; box-shadow: 0 0 30px rgba(221, 160, 221, 0.8); }

    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.8rem; z-index: 10; }
    .stTextArea textarea { background-color: rgba(0,0,0,0.3) !important; border: 1px solid #444 !important; color: #eee !important; }
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
        "placeholder": "🏠 Pega el link de la propiedad o describe brevemente los ambientes y detalles...", 
        "btn_gen": "✨ GENERAR DESCRIPCIÓN", 
        "p1_name": "Inicial", "p1_desc": "3 descripciones / día<br>Soporte Básico<br>Marca de Agua", "p1_btn": "REGISTRO GRATIS", 
        "p2_name": "Agente Pro", "p2_desc": "<b>Generaciones Ilimitadas</b><br>Pack Redes Sociales (IG/FB)<br>Optimización SEO", "p2_btn": "MEJORAR AHORA", 
        "p3_name": "Agencia", "p3_desc": "5 Usuarios / Cuentas<br>Panel de Equipo<br>Acceso vía API", "p3_btn": "CONTACTAR VENTAS", 
        "popular": "MÁS POPULAR",
        "video_text": "Próximamente Video Demo"
    }
else:
    t = {
        "title1": "Turn Boring Listings into", 
        "title2": "Sales Magnets", 
        "sub": "The secret AI tool used by top producers.", 
        "placeholder": "🏠 Paste the property link or briefly describe the rooms and details...", 
        "btn_gen": "✨ GENERATE DESCRIPTION", 
        "p1_name": "Starter", "p1_desc": "3 descriptions / day<br>Basic Support<br>Watermark", "p1_btn": "FREE SIGN UP", 
        "p2_name": "Agent Pro", "p2_desc": "<b>Unlimited Generations</b><br>Social Media Pack (IG/FB)<br>SEO Optimization", "p2_btn": "UPGRADE NOW", 
        "p3_name": "Agency", "p3_desc": "5 Users / Accounts<br>Team Dashboard<br>API Access", "p3_btn": "CONTACT SALES", 
        "popular": "MOST POPULAR",
        "video_text": "Video Demo Coming Soon"
    }

# --- 4. INTERFAZ ---
col_logo, _, col_lang = st.columns([2, 4, 1.5])
with col_logo: 
    st.markdown('<div class="header-logo">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
with col_lang: 
    st.selectbox("", ["🇪🇸 Español", "🇺🇸 English"], label_visibility="collapsed", key="idioma_selec")

st.markdown(f"<h1 class='neon-title'>{t['title1']} <br><span class='neon-highlight'>{t['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{t['sub']}</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # RECTÁNGULO DE VIDEO RESTAURADO (Arriba del input)
    st.markdown(f'<div class="video-placeholder">{t["video_text"]}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    user_input = st.text_area("", height=120, placeholder=t['placeholder'], label_visibility="collapsed")
    gen_btn = st.button(t['btn_gen'], type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. SECCIÓN DE PLANES ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(f"<div class='glass-container free-card'><h3>{t['p1_name']}</h3><h1>$0</h1><hr style='opacity:0.2;'><p>{t['p1_desc']}</p></div>", unsafe_allow_html=True)
    st.button(t['p1_btn'], key="btn_p1")

with p2:
    st.markdown(f"<div class='glass-container pro-card'><div class='popular-badge'>{t['popular']}</div><h3 style='color:#00d2ff;'>{t['p2_name']}</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'><p>{t['p2_desc']}</p></div>", unsafe_allow_html=True)
    st.button(t['p2_btn'], key="btn_p2")

with p3:
    st.markdown(f"<div class='glass-container agency-card'><h3 style='color:#DDA0DD;'>{t['p3_name']}</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'><p>{t['p3_desc']}</p></div>", unsafe_allow_html=True)
    st.button(t['p3_btn'], key="btn_p3")

st.markdown("<br><br>", unsafe_allow_html=True)
