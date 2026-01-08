import streamlit as st
import time

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (Fondo Oscuro Sólido + Neón) ---
st.markdown("""
<style>
    /* FONDO GENERAL (Gris muy oscuro casi negro, elegante) */
    .stApp {
        background-color: #0e1117;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* CABECERA (LOGO Y NOMBRE) */
    .header-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
        display: flex;
        align-items: center;
    }
    .header-logo span {
        margin-right: 10px;
    }

    /* TÍTULO PRINCIPAL */
    .neon-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
        color: white;
        text-shadow: 0 0 25px rgba(0, 210, 255, 0.5);
    }
    .neon-highlight {
        color: #00d2ff;
        text-shadow: 0 0 40px rgba(0, 210, 255, 0.8);
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #aaa;
        margin-bottom: 40px;
        font-weight: 300;
    }

    /* CONTENEDORES (CAJAS DE CRISTAL) */
    .glass-container {
        background: rgba(38, 39, 48, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        height: 100%;
        text-align: center; /* Texto centrado para planes */
    }

    /* INPUT TEXTAREA ESTILIZADO */
    .stTextArea textarea {
        background-color: rgba(0,0,0,0.3) !important;
        border: 1px solid #444 !important;
        color: #eee !important;
    }
    .stTextArea textarea:focus {
        border-color: #00d2ff !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3) !important;
    }

    /* BOTÓN GENERAR (PRIMARY - CIAN) */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        transition: transform 0.2s;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.6) !important;
    }

    /* BOTONES DE LOS PLANES (SECUNDARIOS) */
    div.stButton > button {
        background: transparent;
        border: 1px solid #555;
        color: #ddd;
        border-radius: 6px;
        width: 100%;
    }
    div.stButton > button:hover {
        border-color: #fff;
        color: #fff;
    }

    /* PLAN PRO DESTACADO */
    .pro-card {
        border: 1px solid #00d2ff !important;
        background: rgba(0, 210, 255, 0.05) !important;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.1);
    }
    .pro-text {
        color: #00d2ff;
        font-weight: bold;
    }

    /* ANIMACIÓN RESULTADO */
    @keyframes flash {
        0% { border-color: #fff; box-shadow: 0 0 20px #fff; }
        100% { border-color: #00d2ff; box-shadow: 0 0 10px rgba(0,210,255,0.3); }
    }
    .result-box {
        border: 1px solid #00d2ff;
        padding: 20px;
        border-radius: 10px;
        background: rgba(0,0,0,0.2);
        animation: flash 1s ease-out;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. BARRA SUPERIOR (HEADER) ---
# Usamos columnas para simular una barra de navegación
col_logo, col_space, col_lang = st.columns([2, 4, 1])

with col_logo:
    st.markdown('<div class="header-logo"><span>🏢</span> IA REALTY PRO</div>', unsafe_allow_html=True)

with col_lang:
    # Selector de idioma (Funcional visualmente)
    idioma = st.selectbox("", ["🇺🇸 English", "🇪🇸 Español"], label_visibility="collapsed")

# --- 4. HERO SECTION (Títulos) ---
st.markdown("<br>", unsafe_allow_html=True)
if "Español" in idioma:
    st.markdown(f"<h1 class='neon-title'>Convierte Anuncios Aburridos en <br><span class='neon-highlight'>Imanes de Ventas</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>La herramienta IA secreta de los agentes top productores.</p>", unsafe_allow_html=True)
    placeholder_text = "Ej: Casa en Miami, 3 habitaciones, cocina renovada, vista al mar..."
    btn_text = "✨ GENERAR DESCRIPCIÓN"
else:
    st.markdown(f"<h1 class='neon-title'>Turn Boring Listings into <br><span class='neon-highlight'>Sales Magnets</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>The secret AI tool used by top producers.</p>", unsafe_allow_html=True)
    placeholder_text = "Ex: House in Miami, 3 bedrooms, renovated kitchen, ocean view..."
    btn_text = "✨ GENERATE DESCRIPTION"

# --- 5. ÁREA DE TRABAJO (INPUT) ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container" style="padding-bottom: 10px;">', unsafe_allow_html=True)
    user_input = st.text_area("", height=120, placeholder=placeholder_text)
    st.markdown("<br>", unsafe_allow_html=True)
    # Botón Principal
    gen_btn = st.button(btn_text, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. RESULTADO (Output) ---
if 'generated' not in st.session_state: st.session_state.generated = False

if gen_btn and user_input:
    with c2:
        with st.spinner("Analyzing property details..."):
            time.sleep(1.5)
            st.session_state.generated = True
            
            # Texto simulado
            if "Español" in idioma:
                mock_res = f"""
                🔥 **¡OFERTA IRRESISTIBLE!**
                Descubre el lujo accesible. Esta propiedad no es solo una casa, es el estilo de vida que mereces.
                ✅ **Espacios:** {user_input[:15]}... amplitud y diseño.
                *Agenda tu visita hoy.*
                """
            else:
                mock_res = f"""
                🔥 **IRRESISTIBLE OFFER!**
                Discover accessible luxury. This property is not just a house, it's the lifestyle you deserve.
                ✅ **Spaces:** {user_input[:15]}... spacious design.
                *Schedule your visit today.*
                """

if st.session_state.generated:
    st.markdown("<br>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        st.markdown(f'<div class="result-box">{mock_res}</div>', unsafe_allow_html=True)

# --- 7. PLANES DE PRECIOS (Simple y Limpio) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
p1, p2, p3 = st.columns([1, 1, 1])

# PLAN GRATIS
with p1:
    st.markdown("""
    <div class='glass-container'>
        <h3 style='color: #ccc; margin-top:0;'>Starter</h3>
        <h1 style='font-size: 3rem; margin: 10px 0;'>$0</h1>
        <p style='color: #aaa;'>Trial / Prueba</p>
        <hr style='border-color: #444; opacity: 0.3;'>
        <p style='line-height: 1.6;'>
            3 Descripciones / día<br>
            Soporte Básico<br>
            Marca de Agua
        </p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("FREE SIGN UP" if "English" in idioma else "REGISTRO GRATIS")

# PLAN PRO (Destacado)
with p2:
    st.markdown("""
    <div class='glass-container pro-card'>
        <h3 class='pro-text' style='margin-top:0;'>AGENTE PRO</h3>
        <h1 style='font-size: 3rem; margin: 10px 0;'>$49<small style='font-size:1rem'>/mo</small></h1>
        <p style='color: #00d2ff;'>Top Seller Choice</p>
        <hr style='border-color: #00d2ff; opacity: 0.3;'>
        <p style='line-height: 1.6;'>
            <b>Generaciones Ilimitadas</b><br>
            Pack Redes Sociales (IG/FB)<br>
            SEO Optimization
        </p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("UPGRADE NOW" if "English" in idioma else "MEJORAR AHORA")

# PLAN AGENCIA
with p3:
    st.markdown("""
    <div class='glass-container'>
        <h3 style='color: #DDA0DD; margin-top:0;'>Agency</h3>
        <h1 style='font-size: 3rem; margin: 10px 0;'>$199<small style='font-size:1rem'>/mo</small></h1>
        <p style='color: #aaa;'>Teams / Equipos</p>
        <hr style='border-color: #444; opacity: 0.3;'>
        <p style='line-height: 1.6;'>
            5 Usuarios / Users<br>
            Panel de Equipo<br>
            API Access
        </p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("CONTACT SALES" if "English" in idioma else "CONTACTAR VENTAS")

st.markdown("<br><br>", unsafe_allow_html=True)
