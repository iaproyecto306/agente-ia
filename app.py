import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS MAESTRO (VIDEO + TEXTOS V2 + BOTONES) ---
st.markdown("""
<style>
    /* 1. ESTILO DE LA APP (TRANSPARENTE PARA QUE SE VEA EL VIDEO) */
    .stApp {
        background: rgba(0,0,0,0.7); /* Oscuridad sobre el video para leer bien */
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

    /* 3. TÍTULOS (ESTILO VERSIÓN 2 QUE TE GUSTABA) */
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
    }

    /* 4. CONTENEDORES GLASS */
    .glass-container {
        background: rgba(20, 20, 20, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 30px rgba(0,0,0,0.5);
    }

    /* 5. INPUTS MÁS PROLIJOS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid #444 !important;
        font-size: 1.1rem;
    }

    /* 6. BOTONES PERSONALIZADOS POR COLUMNA (HACK DE CSS) */
    
    /* Botón Genérico (El de generar y el gratis) */
    div.stButton > button {
        background: transparent;
        border: 1px solid white;
        color: white;
        transition: all 0.3s;
        width: 100%;
        padding: 10px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background: rgba(255,255,255,0.1);
        transform: scale(1.02);
    }

    /* OBJETIVO: EL BOTÓN DEL PLAN DEL MEDIO (PRO) - COLUMNA 2 */
    /* Usamos nth-of-type para encontrar el botón dentro de la columna del medio */
    [data-testid="column"]:nth-of-type(2) div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        border: none;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
        color: black; /* Texto negro para contraste */
    }
    [data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.9);
        transform: scale(1.05);
    }

    /* OBJETIVO: EL BOTÓN DE AGENCIA - COLUMNA 3 */
    [data-testid="column"]:nth-of-type(3) div.stButton > button {
         border: 1px solid #DDA0DD;
         color: #DDA0DD;
         box-shadow: 0 0 10px rgba(221, 160, 221, 0.2);
    }
    [data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
         box-shadow: 0 0 20px rgba(221, 160, 221, 0.6);
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
st.markdown(f"<h1 class='neon-title'>Convierte Anuncios en <span class='neon-highlight'>IMANES DE VENTAS</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>La IA secreta que usan los Top Producers para vender más rápido.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- INPUT AREA (CENTRAL) ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    user_input = st.text_area("Datos de la propiedad:", height=120, placeholder="Ej: 3 habs, 2 baños, cocina renovada, vista al lago...")
    st.markdown("<br>", unsafe_allow_html=True)
    # Botón Principal (Le ponemos un estilo inline para que destaque también)
    gen_btn = st.button("✨ GENERAR DESCRIPCIÓN MÁGICA", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTADO ---
if gen_btn and user_input:
    with c2:
        with st.spinner("Conectando neuronas inmobiliarias..."):
            time.sleep(1.5)
            st.session_state.generated = True
            mock_res = f"""
            🚀 **¡TU PRÓXIMO BEST-SELLER!**
            
            Bienvenido a la definición de exclusividad.
            
            ✅ **Espacios:** {user_input[:20]}... diseñados para impresionar.
            ✅ **Estilo:** Acabados de lujo y luz natural.
            
            *Agenda tu visita hoy.* #RealEstate #Luxury
            """

if st.session_state.generated:
    st.markdown("<br>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        st.markdown(f'<div class="glass-container" style="border-color: #00d2ff;">{mock_res}</div>', unsafe_allow_html=True)

# --- PRUEBA SOCIAL ---
st.markdown("<br><br>", unsafe_allow_html=True)
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
with col_s1: st.markdown("<h3 style='text-align:center; color:#666;'>RE/MAX</h3>", unsafe_allow_html=True)
with col_s2: st.markdown("<h3 style='text-align:center; color:#666;'>KELLER</h3>", unsafe_allow_html=True)
with col_s3: st.markdown("<h3 style='text-align:center; color:#666;'>CENTURY</h3>", unsafe_allow_html=True)
with col_s4: st.markdown("<h3 style='text-align:center; color:#666;'>SOTHEBY'S</h3>", unsafe_allow_html=True)

# --- PLANES DE PRECIOS ---
st.markdown("<br><br><h2 style='text-align: center; color: white; font-weight:800;'>PLANES FLEXIBLES</h2><br>", unsafe_allow_html=True)

# Definimos las columnas
p1, p2, p3 = st.columns([1, 1, 1])

# COLUMNA 1: GRATIS
with p1:
    st.markdown("""
    <div class='glass-container' style='text-align: center; height: 350px;'>
        <h3 style='color: #ccc;'>Starter</h3>
        <h1>$0</h1>
        <p style='color: #888;'>Para probar</p>
        <hr style='border-color: #444;'>
        <p>3 Generaciones / día</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("EMPEZAR GRATIS") # Botón fuera del HTML para que funcione en Python

# COLUMNA 2: PRO (EL QUE BRILLA)
with p2:
    st.markdown("""
    <div class='glass-container' style='text-align: center; border: 1px solid #00d2ff; box-shadow: 0 0 20px rgba(0, 210, 255, 0.2); transform: scale(1.05); height: 350px;'>
        <h3 style='color: #00d2ff;'>AGENTE PRO 🚀</h3>
        <h1>$49<small>/mes</small></h1>
        <p style='color: #888;'>Top Producers</p>
        <hr style='border-color: #444;'>
        <p><b>Ilimitado</b></p>
        <p>Textos para Instagram</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("MEJORAR AHORA") # Este botón será atacado por el CSS para ser NEÓN

# COLUMNA 3: AGENCIA
with p3:
    st.markdown("""
    <div class='glass-container' style='text-align: center; height: 350px;'>
        <h3 style='color: #DDA0DD;'>Agencia</h3>
        <h1>$199<small>/mes</small></h1>
        <p style='color: #888;'>Equipos</p>
        <hr style='border-color: #444;'>
        <p>5 Usuarios</p>
        <p>API Access</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("CONTACTAR VENTAS")

st.markdown("<br><br>", unsafe_allow_html=True)
