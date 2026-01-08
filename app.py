import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS PREMIUM (GLASSMORPHISM + NEON) ---
st.markdown("""
<style>
    /* FONDO DEGRADADO PROFESIONAL */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #FAFAFA;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* ELIMINAR ELEMENTOS MOLESTOS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* EFECTO CRISTAL (GLASSMORPHISM) PARA CONTENEDORES */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    /* BOTÓN CON EFECTO GLOW */
    div.stButton > button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 1.1em;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 0 10px rgba(0, 210, 255, 0.3);
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.7);
    }

    /* TÍTULOS NEÓN */
    .neon-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
    }
    .neon-highlight {
        color: #00d2ff;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.5);
    }

    /* TARJETA DESTACADA (PRO PLAN) */
    .pro-card {
        border: 2px solid #00d2ff !important;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.2) !important;
        transform: scale(1.02);
    }

    /* INPUT FIELDS TRANSPARENTES */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: rgba(0, 0, 0, 0.3) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- variables de estado ---
if 'generated' not in st.session_state: st.session_state.generated = False

# --- HERO SECTION ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<h1 class='neon-title'>Convierte Anuncios Aburridos en <br><span class='neon-highlight'>Imanes de Ventas</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 1.3rem; color: #aab2bd;'>La herramienta IA secreta de los agentes top productores.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- ÁREA DE INPUT PRINCIPAL (CRISTAL) ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    user_input = st.text_area("Pega los detalles de la propiedad o link aquí:", height=120, placeholder="Ej: Casa en Miami, 3 habitaciones, piscina, cocina renovada...")
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("✨ Generar Descripción Mágica")
    st.markdown('</div>', unsafe_allow_html=True)

# --- LÓGICA DE GENERACIÓN (SIMULADA) ---
if generate_btn and user_input:
    with c2:
        with st.spinner("Analizando el mercado... Redactando texto persuasivo..."):
            time.sleep(2)
            st.session_state.generated = True
            mock_response = f"""
            🌟 **¡VIVE EL LUJO EN SU MÁXIMA EXPRESIÓN!** 🌟
            
            Descubre el equilibrio perfecto entre estilo y confort en esta residencia soñada.
            
            ✅ **Elegancia Moderna:** {user_input if len(user_input) > 5 else "Interiores amplios y luminosos..."}
            ✅ **Cocina de Chef:** Ideal para entretener invitados.
            ✅ **Oasis Privado:** Tu refugio personal con piscina.
            
            *No pierdas esta oportunidad. ¡Agenda tu visita privada hoy mismo!*
            #BienesRaices #CasaDeEnsueño #LuxuryLiving
            """

if st.session_state.generated:
    st.markdown("<br>", unsafe_allow_html=True)
    c1_r, c2_r, c3_r = st.columns([1, 2, 1])
    with c2_r:
        st.markdown(f'<div class="glass-container"><h3>Tu Descripción Premium:</h3>{mock_response}</div>', unsafe_allow_html=True)
        st.button("📋 Copiar Texto")

# --- PRUEBA SOCIAL ---
st.markdown("<br><br>", unsafe_allow_html=True)
col_sp1, col_sp2, col_sp3, col_sp4 = st.columns(4)
with col_sp1: st.markdown("<h4 style='text-align: center; color: #6E7681; opacity: 0.6;'>RE/MAX</h4>", unsafe_allow_html=True)
with col_sp2: st.markdown("<h4 style='text-align: center; color: #6E7681; opacity: 0.6;'>KELLER W.</h4>", unsafe_allow_html=True)
with col_sp3: st.markdown("<h4 style='text-align: center; color: #6E7681; opacity: 0.6;'>CENTURY 21</h4>", unsafe_allow_html=True)
with col_sp4: st.markdown("<h4 style='text-align: center; color: #6E7681; opacity: 0.6;'>SOTHEBY'S</h4>", unsafe_allow_html=True)

# --- SECCIÓN DE PRECIOS (CRISTAL) ---
st.markdown("<br><br><h2 style='text-align: center; font-weight: 800;'>Planes Flexibles</h2><br>", unsafe_allow_html=True)

p1, p2, p3 = st.columns([1, 1, 1])

with p1:
    st.markdown("""
    <div class='glass-container' style='text-align: center;'>
        <h3>Gratis</h3>
        <h1>$0</h1>
        <p>Para probar</p>
        <hr style='border-color: rgba(255,255,255,0.1);'>
        <p>3 Descripciones / día</p>
        <p>Soporte Básico</p>
        <br>
        <button style='background: transparent; border: 1px solid white; color: white; padding: 10px; border-radius: 8px; width:100%;'>Registrarse Gratis</button>
    </div>
    """, unsafe_allow_html=True)

with p2:
    # Plan destacado PRO
    st.markdown("""
    <div class='glass-container pro-card' style='text-align: center; position: relative;'>
        <span style='position: absolute; top: -15px; right: 25%; background: #00d2ff; padding: 5px 15px; border-radius: 20px; font-size: 0.8em; font-weight: bold;'>MÁS POPULAR</span>
        <h3 style='color: #00d2ff;'>Agente PRO 🚀</h3>
        <h1>$49<small>/mes</small></h1>
        <p>Para top producers</p>
        <hr style='border-color: rgba(255,255,255,0.1);'>
        <p><b>Generaciones Ilimitadas</b></p>
        <p>Textos para Instagram/FB Ads</p>
        <p>Optimización SEO</p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("Empezar Ahora ($49)", key="btn_pro")

with p3:
    st.markdown("""
    <div class='glass-container' style='text-align: center;'>
        <h3>Agencia</h3>
        <h1>$199<small>/mes</small></h1>
        <p>Para equipos</p>
        <hr style='border-color: rgba(255,255,255,0.1);'>
        <p>Hasta 5 Usuarios</p>
        <p>Acceso a API</p>
        <p>Soporte Prioritario</p>
        <br>
        <button style='background: transparent; border: 1px solid white; color: white; padding: 10px; border-radius: 8px; width:100%;'>Contactar Ventas</button>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
