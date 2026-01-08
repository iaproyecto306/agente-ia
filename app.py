import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INYECCIÓN DE VIDEO DE FONDO Y ESTILOS ---
# Nota: He puesto un video de ejemplo. Luego puedes cambiar el link por el que quieras.
st.markdown("""
<style>
    /* 1. FONDO NEGRO PROFUNDO (PARA QUE NO CANSE LA VISTA) */
    .stApp {
        background-color: #050505; /* Casi negro absoluto */
        color: #FAFAFA;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* 2. VIDEO DE FONDO (FIJO Y DETRÁS DE TODO) */
    #myVideo {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
        z-index: -1; /* Se va al fondo */
        opacity: 0.4; /* Transparencia para que no moleste al leer */
        filter: grayscale(100%) contrast(1.2); /* Lo hacemos más "tech" y serio */
    }

    /* 3. CONTENEDORES DE CRISTAL OSCURO (MÁS ELEGANTES) */
    .glass-container {
        background: rgba(20, 20, 20, 0.7); /* Mucho más oscuro */
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
    }

    /* 4. TÍTULOS */
    .neon-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 5. JERARQUÍA DE BOTONES (ANIMACIONES PROGRESIVAS) */
    
    /* Clase común para todos los botones */
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 700;
        padding: 0.8em 1.2em;
        transition: all 0.4s ease;
        background-color: transparent;
        color: white;
        border: 1px solid #333;
    }

    /* ANIMACIÓN DEL BOTÓN DE GENERAR (El principal) */
    div.stButton > button:first-child {
         border: 1px solid #00FFFF;
         box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
    }
    div.stButton > button:first-child:hover {
         background: rgba(0, 255, 255, 0.1);
         box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
         transform: scale(1.02);
    }
    
    /* EFECTO GLITCH EN INPUTS */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(10, 10, 10, 0.8) !important;
        border: 1px solid #333 !important;
        color: #00FFFF !important; /* Texto neón al escribir */
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #00FFFF !important;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
    }

</style>

<video autoplay muted loop id="myVideo">
  <source src="https://v4.cdnpk.net/videvo_files/video/free/2017-12/large_watermarked/171124_H1_006_preview.mp4" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# --- variables ---
if 'generated' not in st.session_state: st.session_state.generated = False

# --- HERO SECTION ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<h1 class='neon-title'>IA REALTY <span style='color: #00FFFF; -webkit-text-fill-color: #00FFFF;'>PRO</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 1.2rem; color: #888;'>Convierte datos fríos en historias que venden.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- ÁREA INPUT ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    user_input = st.text_area("Datos de la propiedad:", height=100, placeholder="Pega el link de Zillow o escribe: 3 habs, 2 baños, vista al mar...")
    st.markdown("<br>", unsafe_allow_html=True)
    # Este botón tomará el estilo "principal" definido en CSS
    generate_btn = st.button("⚡ GENERAR DESCRIPCIÓN") 
    st.markdown('</div>', unsafe_allow_html=True)

# --- RESPUESTA IA ---
if generate_btn and user_input:
    with c2:
        with st.spinner("Conectando con la Matrix inmobiliaria..."):
            time.sleep(1.5)
            st.session_state.generated = True
            mock_response = f"""
            🔥 **OPORTUNIDAD EXCLUSIVA** 🔥
            
            No es solo una casa, es tu próximo capítulo.
            
            🔹 **Diseño:** {user_input if len(user_input) > 5 else "Espacios abiertos..."}
            🔹 **Estilo de Vida:** Lujo y confort en cada rincón.
            
            *Agenda tu visita antes de que desaparezca del mercado.*
            """

if st.session_state.generated:
    st.markdown("<br>", unsafe_allow_html=True)
    c1r, c2r, c3r = st.columns([1, 2, 1])
    with c2r:
        st.markdown(f'<div class="glass-container" style="border: 1px solid #00FFFF;">{mock_response}</div>', unsafe_allow_html=True)

# --- PRECIOS (JERARQUÍA DE BRILLO) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>PLANES</h2><br>", unsafe_allow_html=True)

p1, p2, p3 = st.columns([1, 1, 1])

# PLAN GRATIS (Brillo bajo)
with p1:
    st.markdown("""
    <div class='glass-container' style='text-align: center; opacity: 0.8;'>
        <h3 style='color: #888;'>Starter</h3>
        <h1>$0</h1>
        <p style='font-size: 0.9em; color: #666;'>3 descripciones / día</p>
        <button style='
            background: transparent; 
            border: 1px solid #444; 
            color: #aaa; 
            padding: 10px 20px; 
            border-radius: 5px; 
            margin-top: 10px;
            width: 100%;
            cursor: pointer;'>
            Empezar Gratis
        </button>
    </div>
    """, unsafe_allow_html=True)

# PLAN PRO (Brillo MEDIO - CIAN - EL QUE QUEREMOS VENDER)
with p2:
    st.markdown("""
    <div class='glass-container' style='text-align: center; border: 1px solid #00FFFF; box-shadow: 0 0 15px rgba(0, 255, 255, 0.15); transform: scale(1.05);'>
        <h3 style='color: #00FFFF;'>AGENTE PRO 🚀</h3>
        <h1 style='color: white;'>$49<span style='font-size:0.5em'>/mes</span></h1>
        <p style='font-size: 0.9em; color: #ccc;'>Ilimitado + Instagram</p>
        <button style='
            background: rgba(0, 255, 255, 0.1); 
            border: 1px solid #00FFFF; 
            color: #00FFFF; 
            padding: 12px 20px; 
            border-radius: 5px; 
            margin-top: 10px;
            width: 100%;
            font-weight: bold;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
            cursor: pointer;'>
            MEJORAR AHORA
        </button>
    </div>
    """, unsafe_allow_html=True)

# PLAN AGENCIA (Brillo ALTO - VIOLETA - EL MÁS CARO)
with p3:
    st.markdown("""
    <div class='glass-container' style='text-align: center;'>
        <h3 style='color: #DDA0DD;'>Agencia</h3>
        <h1>$199</h1>
        <p style='font-size: 0.9em; color: #ccc;'>Para equipos de 5+</p>
        <button style='
            background: transparent; 
            border: 1px solid #DDA0DD; 
            color: #DDA0DD; 
            padding: 10px 20px; 
            border-radius: 5px; 
            margin-top: 10px;
            width: 100%;
            box-shadow: 0 0 15px rgba(221, 160, 221, 0.5);
            cursor: pointer;'>
            Contactar Ventas
        </button>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
