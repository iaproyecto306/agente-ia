import streamlit as st
import time

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (MANTENIENDO TODO TU DISEÑO) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .header-logo { font-size: 1.5rem; font-weight: 700; color: #fff; display: flex; align-items: center; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    /* EL RECTÁNGULO DE VIDEO AHORA ES UN BANNER PUBLICITARIO */
    .video-placeholder {
        background: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-position: center;
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 12px;
        height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        animation: float 4s ease-in-out infinite;
    }
    
    .ad-overlay {
        background: linear-gradient(0deg, rgba(0,0,0,0.8) 0%, transparent 100%);
        width: 100%;
        padding: 15px;
        text-align: center;
    }

    .ad-badge {
        position: absolute;
        top: 15px;
        left: 15px;
        background: rgba(0, 210, 255, 0.9);
        color: black;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 800;
        letter-spacing: 1px;
    }

    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }

    /* CONTENEDOR DE INPUT */
    .glass-container { 
        background: rgba(38, 39, 48, 0.6); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 12px; padding: 30px; 
        text-align: center; position: relative; 
    }
    
    /* BOTONES (LOS QUE YA TENÍAS BIEN) */
    button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; 
        border: none !important; 
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    /* BOTONES DE COMPRA CON TU COLOR Y ANIMACIÓN */
    [data-testid="column"]:nth-child(2) button[kind="secondary"] { border: 2px solid #00d2ff; color: #00d2ff; }
    [data-testid="column"]:nth-child(2) button[kind="secondary"]:hover { 
        background: #00d2ff !important; color: black !important; 
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.8); transform: translateY(-5px); 
    }
    [data-testid="column"]:nth-child(3) button[kind="secondary"] { border: 2px solid #DDA0DD; color: #DDA0DD; }
    [data-testid="column"]:nth-child(3) button[kind="secondary"]:hover { 
        background: #DDA0DD !important; color: black !important; 
        box-shadow: 0 0 30px rgba(221, 160, 221, 0.8); transform: translateY(-5px); 
    }

    /* TARJETAS */
    .pro-card { border: 1px solid #00d2ff !important; }
    .agency-card { border: 1px solid #DDA0DD !important; }
    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.8rem; z-index: 10; }
</style>
""", unsafe_allow_html=True)

# --- 3. INTERFAZ ---
st.markdown('<div class="header-logo">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
st.markdown(f"<h1 class='neon-title'>Convierte Anuncios Aburridos en <br><span class='neon-highlight'>Imanes de Ventas</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>La herramienta IA secreta de los agentes top productores.</p>", unsafe_allow_html=True)

# ÁREA DE PUBLICIDAD Y VIDEO
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # RECUADRO CON IMAGEN DE CLIENTE/PUBLICIDAD
    st.markdown("""
        <div class="video-placeholder">
            <div class="ad-badge">PROPIEDAD DESTACADA - AGENTE PRO</div>
            <div class="ad-overlay">
                <p style="margin:0; font-weight:700;">Penthouse en Puerto Madero - $1.2M</p>
                <p style="margin:0; font-size:0.8rem; color:#00d2ff;">Ver detalles en pestaña nueva ↗</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.text_area("", placeholder="Pega el link de la propiedad...", label_visibility="collapsed")
    st.button("✨ GENERAR DESCRIPCIÓN", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# SECCIÓN DE PLANES
st.markdown("<br><br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='glass-container free-card'><h3>Inicial</h3><h1>$0</h1><hr style='opacity:0.2;'><p>3 descripciones / día<br>Soporte Básico</p></div>", unsafe_allow_html=True)
    st.button("REGISTRO GRATIS", key="f1")

with col2:
    st.markdown(f"<div class='glass-container pro-card'><div class='popular-badge'>MÁS POPULAR</div><h3 style='color:#00d2ff;'>Agente Pro</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'><p>Generaciones Ilimitadas<br>Aparición en Banner Principal</p></div>", unsafe_allow_html=True)
    st.button("MEJORAR AHORA", key="f2")

with col3:
    st.markdown(f"<div class='glass-container agency-card'><h3 style='color:#DDA0DD;'>Agencia</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'><p>5 Usuarios / Cuentas<br>Prioridad en Banner</p></div>", unsafe_allow_html=True)
    st.button("CONTACTAR VENTAS", key="f3")
