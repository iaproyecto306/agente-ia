import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS MAESTRO (VIDEO VISIBLE + FUENTES V2 + ANIMACIONES) ---
st.markdown("""
<style>
    /* 1. FONDO TRANSPARENTE PARA QUE SE VEA EL VIDEO */
    .stApp {
        background: rgba(0,0,0,0.7); /* Oscuridad necesaria para leer, pero deja ver el video */
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* ELIMINAR ELEMENTOS MOLESTOS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 2. VIDEO DE FONDO FIXED (CAPA -1) */
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

    /* 5. DEFINICIÓN DE ANIMACIONES DE LOS BOTONES */
    @keyframes pulse-cyan {
        0% { box-shadow: 0 0 0 0 rgba(0, 210, 255, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(0, 210, 255, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 210, 255, 0); }
    }
    
    @keyframes pulse-purple {
        0% { box-shadow: 0 0 0 0 rgba(221, 160, 221, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(221, 160, 221, 0); }
        100% { box-shadow: 0 0 0 0 rgba(221, 160, 221, 0); }
    }

    /* 6. ESTILOS DE BOTONES PROGRESIVOS */
    
    /* Botón Genérico (Base) */
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

    /* BOTÓN PRO (Columna 2): Brillo Cian + LATIDO */
    [data-testid="column"]:nth-of-type(2) div.stButton > button {
        border: 1px solid #00d2ff;
        color: #00d2ff;
        /* APLICAMOS LA ANIMACIÓN AQUÍ */
        animation: pulse-cyan 2s infinite;
    }
    [data-testid="column"]:nth-of-type(2) div.stButton > button:hover {
        background: #00d2ff;
        color: black;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.9);
        animation: none; /* Se detiene el latido al pasar el mouse para quedar fijo */
    }

    /* BOTÓN AGENCIA (Columna 3): Brillo Violeta + LATIDO SUAVE */
    [data-testid="column"]:nth-of-type(3) div.stButton > button {
         border: 1px solid #DDA0DD;
         color: #DDA0DD;
         animation: pulse-purple 3s infinite;
    }
    [data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
         background: #DDA0DD;
         color: black;
         box-shadow: 0 0 30px rgba(221, 160, 221, 0.8);
    }
    
    /* INPUT FIELDS MÁS PROLIJOS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid #444 !important;
        font-size: 1.1rem;
    }

</style>

<video autoplay muted loop id="background-video">
    <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-lines-and-dots-996-large.mp4" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# --- Variables ---
if 'generated' not in st.session_state: st.session_state.generated = False

# --- HERO SECTION (Restaurado V2) ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<h1 class='neon-title'>Convierte Anuncios Aburridos en <br><span class='neon-highlight'>Imanes de Ventas</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>La herramienta IA secreta de los agentes top productores.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- INPUT AREA ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    user_input = st.text_area("Datos de la propiedad:", height=120, placeholder="Ej: 3 habs, 2 baños, cocina renovada, vista al lago...")
    st.markdown("<br>", unsafe_allow_html=True)
    # Botón Principal con estilo manual inline para que destaque
    gen_btn = st.button("✨ GENERAR DESCRIPCIÓN MÁGICA") 
    st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA ---
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

# --- PLANES DE PRECIOS ---
st.markdown("<br><br><h2 style='text-align: center; color: white; font-weight:800;'>PLANES FLEXIBLES</h2><br>", unsafe_allow_html=True)

p1, p2, p3 = st.columns([1, 1, 1])

# GRATIS
with p1:
    st.markdown("""
    <div class='glass-container' style='text-align: center;'>
        <h3 style='color: #ccc;'>Starter</h3>
        <h1>$0</h1>
        <p style='color: #888;'>Para probar</p>
        <hr style='border-color: #444;'>
        <p>3 Generaciones / día</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("EMPEZAR GRATIS")

# PRO (El botón de aquí tendrá el efecto PUL
