import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS MAESTRO (VIDEO + TEXTOS VENTA + BOTONES) ---
st.markdown("""
<style>
    /* 1. FONDO TRANSPARENTE PARA EL VIDEO */
    .stApp {
        background: rgba(0,0,0,0.75); /* Un poco más oscuro para leer bien los textos largos */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* ELIMINAR ELEMENTOS DE STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 2. VIDEO DE FONDO FIXED */
    #background-video {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
        z-index: -1;
    }

    /* 3. TÍTULOS NEÓN (ESTÉTICA V2) */
    .neon-title {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0;
        color: white;
        text-shadow: 0 0 20px rgba(0, 210, 255, 0.7);
    }
    .neon-highlight {
        color: #00d2ff;
        text-shadow: 0 0 30px rgba(0, 210, 255, 1);
    }
    .subtitle {
        text-align: center;
        font-size: 1.4rem;
        color: #d1d5db;
        margin-top: -10px;
        margin-bottom: 30px;
    }

    /* 4. CONTENEDORES GLASS */
    .glass-container {
        background: rgba(20, 20, 20, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
        height: 100%; /* Para que todas las cajas tengan la misma altura */
    }

    /* LISTAS DE BENEFICIOS */
    .benefit-list {
        text-align: left;
        margin-top: 20px;
        font-size: 0.95rem;
        color: #e0e0e0;
        line-height: 1.8;
    }
    .benefit-list b {
        color: white;
    }

    /* 5. INPUTS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        border: 1px solid #555 !important;
    }

    /* 6. BOTONES PERSONALIZADOS POR COLUMNA */
    div.stButton > button {
        background: transparent;
        border: 1px solid white;
        color: white;
        transition: all 0.3s;
        width: 100%;
        padding: 12px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:hover {
        background: rgba(255,255,255,0.1);
        transform: scale(1.02);
    }

    /* PRO PLAN BUTTON (COLUMNA 2) */
    [data-testid="column"]:nth-of-type(2) div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        border: none;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4);
        color: black;
    }
    [data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        box-shadow: 0 0 40px rgba(0, 210, 255, 0.8);
        transform: scale(1.05);
    }

    /* AGENCY PLAN BUTTON (COLUMNA 3) */
    [data-testid="column"]:nth-of-type(3) div.stButton > button {
         border: 1px solid #DDA0DD;
         color: #DDA0DD;
    }
    [data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
         box-shadow: 0 0 20px rgba(221, 160, 221, 0.4);
         background: rgba(221, 160, 221, 0.1);
    }

</style>

<video autoplay muted loop id="background-video">
    <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-lines-and-dots-996-large.mp4" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# --- Variables ---
if 'generated' not in st.session_state: st.session_state.generated = False

# --- HERO SECTION ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<h1 class='neon-title'>IA REALTY <span class='neon-highlight'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>Escribe descripciones que venden propiedades en segundos.</p>", unsafe_allow_html=True)

# --- INPUT AREA ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    user_input = st.text_area("Pegá el link de Zillow o poné los detalles:", height=100, placeholder="Ej: Casa moderna, 3 habitaciones, cocina de mármol, jardín amplio...")
    st.markdown("<br>", unsafe_allow_html=True)
    gen_btn = st.button("✨ Generar Descripción v4.0")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTADO MOCK ---
if gen_btn and user_input:
    with c2:
        with st.spinner("La IA está analizando el mercado..."):
            time.sleep(1.5)
            st.session_state.generated = True
            mock_res = f"""
            🏡 **TU REFUGIO PERFECTO TE ESPERA**
            
            Imagina despertar cada mañana en esta obra maestra de diseño moderno.
            
            ✨ **Cocina Gourmet:** {user_input[:15]}... ideal para tus mejores cenas.
            ✨ **Espacios Vivos:** Luz natural que inunda cada rincón.
            
            *No dejes pasar esta oportunidad única.*
            """

if st.session_state.generated:
    st.markdown("<br>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        st.markdown(f'<div class="glass-container" style="border-color: #00d2ff;">{mock_res}</div>', unsafe_allow_html=True)

# --- PLANES DE PRECIOS (CON ARGUMENTOS DE VENTA) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
p1, p2, p3 = st.columns([1, 1, 1])

# COLUMNA 1: GRATIS
with p1:
    st.markdown("""
    <div class='glass-container' style='text-align: center;'>
        <h3 style='color: #ccc;'>Principiante</h3>
        <h1>$0</h1>
        <p style='color: #888; font-size: 0.9em;'>Para agentes curiosos</p>
        <hr style='border-color: #444; opacity: 0.5;'>
        
        <div class='benefit-list'>
            ✅ 3 Descripciones al día<br>
            ✅ Tono Estándar<br>
            ❌ Sin Optimización SEO<br>
            ❌ Sin Textos para Redes<br>
            ❌ Marca de agua<br>
        </div>
        <br><br>
    </div>
    """, unsafe_allow_html=True)
    st.button("PROBAR GRATIS")

# COLUMNA 2: PRO (EL FOCO DE VENTA)
with p2:
    st.markdown("""
    <div class='glass-container' style='text-align: center; border: 1px solid #00d2ff; background: rgba(0, 210, 255, 0.05); transform: scale(1.03);'>
        <span style='background: #00d2ff; color: black; padding: 4px 12px; border-radius: 20px; font-size: 0.7em; font-weight: bold; text-transform: uppercase;'>Más Vendido</span>
        <h3 style='color: #00d2ff; margin-top: 10px;'>AGENTE PRO 🚀</h3>
        <h1 style='color: white;'>$49<small style='font-size:0.4em'>/mes</small></h1>
        <p style='color: #ccc; font-size: 0.9em;'>Para cerrar ventas rápido</p>
        <hr style='border-color: #00d2ff; opacity: 0.5;'>
        
        <div class='benefit-list'>
            ✅ <b>Generaciones ILIMITADAS</b><br>
            ✅ <b>Pack Redes Sociales</b> (IG/FB)<br>
            ✅ <b>Optimización SEO</b> (Google)<br>
            ✅ 3 Tonos: Lujo, Urgencia, Pro<br>
            ✅ Emails de Seguimiento<br>
        </div>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("QUIERO VENDER MÁS")

# COLUMNA 3: AGENCIA
with p3:
    st.markdown("""
    <div class='glass-container' style='text-align: center;'>
        <h3 style='color: #DDA0DD;'>Agencia</h3>
        <h1>$199<small style='font-size:0.4em'>/mes</small></h1>
        <p style='color: #888; font-size: 0.9em;'>Para equipos y brokers</p>
        <hr style='border-color: #444; opacity: 0.5;'>
        
        <div class='benefit-list'>
            ✅ <b>Todo lo del plan PRO</b><br>
            ✅ <b>Hasta 5 Usuarios</b><br>
            ✅ Panel de Control de Equipo<br>
            ✅ Integración API / CRM<br>
            ✅ Soporte Prioritario 24/7<br>
        </div>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("CONTACTAR VENTAS")

st.markdown("<br><br>", unsafe_allow_html=True)
