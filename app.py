import streamlit as st

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS (AÑADIENDO TOOLTIPS) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* ESTILO PARA LOS TOOLTIPS (EXPLICACIONES) */
    .info-icon {
        display: inline-block;
        width: 14px;
        height: 14px;
        background-color: rgba(255, 255, 255, 0.2);
        color: #fff;
        border-radius: 50%;
        text-align: center;
        font-size: 10px;
        line-height: 14px;
        margin-left: 5px;
        cursor: help;
        position: relative;
    }
    
    .info-icon:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: #333;
        color: #fff;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: normal;
        width: 180px;
        z-index: 100;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* RECTÁNGULO DE VIDEO / PUBLICIDAD */
    .video-placeholder {
        border: 1px solid rgba(0, 210, 255, 0.2);
        border-radius: 12px;
        height: 220px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
        background-size: cover;
        background-position: center;
        animation: float 4s ease-in-out infinite, adCarousel 15s infinite;
    }
    @keyframes adCarousel {
        0%, 30% { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'); }
        33%, 63% { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80'); }
        66%, 100% { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'); }
    }
    .ad-overlay { background: linear-gradient(0deg, rgba(0,0,0,0.8) 0%, transparent 100%); width: 100%; padding: 15px; text-align: center; }
    .ad-badge { position: absolute; top: 15px; left: 15px; background: rgba(0, 210, 255, 0.9); color: black; padding: 4px 12px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }

    /* CONTENEDOR DE INPUT */
    .glass-container { background: rgba(38, 39, 48, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; }
    .stTextArea textarea { background-color: rgba(0,0,0,0.3) !important; border: 1px solid #444 !important; color: #eee !important; }

    /* BOTONES */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; 
        border: none !important; 
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important;
        transition: all 0.4s ease !important;
        color: white !important;
        font-weight: 700 !important;
    }
    div.stButton > button[kind="primary"]:hover { transform: scale(1.05) !important; box-shadow: 0 0 30px rgba(0, 210, 255, 0.7) !important; }

    /* TARJETAS DE PLANES */
    .free-card, .pro-card, .agency-card { transition: all 0.4s ease-out !important; }
    .free-card:hover { transform: translateY(-10px) !important; border: 1px solid rgba(255, 255, 255, 0.4) !important; }
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.3) !important; }
    .pro-card:hover { transform: translateY(-10px) !important; border-color: #00d2ff !important; box-shadow: 0 0 40px rgba(0, 210, 255, 0.4) !important; }
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.3) !important; }
    .agency-card:hover { transform: translateY(-10px) !important; border-color: #DDA0DD !important; box-shadow: 0 0 40px rgba(221, 160, 221, 0.4) !important; }

    /* BOTONES DE COMPRA */
    [data-testid="column"]:nth-child(1) button { border: 1px solid #444 !important; color: #888 !important; }
    [data-testid="column"]:nth-child(2) button { border: 2px solid #00d2ff !important; color: #00d2ff !important; }
    [data-testid="column"]:nth-child(3) button { border: 2px solid #DDA0DD !important; color: #DDA0DD !important; }
    div.stButton > button:hover { transform: translateY(-5px) !important; }

    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.8rem; z-index: 10; }
</style>
""", unsafe_allow_html=True)

# --- 3. CONTENIDO CON EXPLICACIONES (TOOLTIPS) ---
# Aquí definimos el HTML para cada lista de beneficios con sus tooltips
desc_free = """
3 descripciones / día <span class="info-icon" data-tooltip="Límite diario de generaciones para probar la herramienta.">i</span><br>
Soporte Básico <span class="info-icon" data-tooltip="Ayuda técnica vía email con respuesta en 48hs.">i</span><br>
Marca de Agua <span class="info-icon" data-tooltip="Los textos incluyen una pequeña mención a nuestra web.">i</span>
"""

desc_pro = """
<b>Generaciones Ilimitadas</b> <span class="info-icon" data-tooltip="Sin límites. Genera todas las descripciones que necesites.">i</span><br>
Pack Redes Sociales <span class="info-icon" data-tooltip="Crea automáticamente el post para Instagram y Facebook con hashtags.">i</span><br>
Optimización SEO <span class="info-icon" data-tooltip="Textos redactados para aparecer primero en Google y portales.">i</span><br>
✨ <b>Banner Principal</b> <span class="info-icon" data-tooltip="Tus propiedades rotarán en la página de inicio para todos los usuarios.">i</span>
"""

desc_agency = """
5 Usuarios / Cuentas <span class="info-icon" data-tooltip="Acceso individual para 5 miembros de tu inmobiliaria.">i</span><br>
Panel de Equipo <span class="info-icon" data-tooltip="Gestiona y supervisa el trabajo de todos tus agentes.">i</span><br>
Acceso vía API <span class="info-icon" data-tooltip="Conecta nuestra IA directamente con el sistema de tu inmobiliaria.">i</span><br>
🔥 <b>Prioridad en Banner</b> <span class="info-icon" data-tooltip="Tus anuncios aparecerán con el doble de frecuencia en la home.">i</span>
"""

# --- 4. INTERFAZ ---
st.markdown('<div class="header-logo">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
st.markdown(f"<h1 class='neon-title'>Convierte Anuncios Aburridos en <br><span class='neon-highlight'>Imanes de Ventas</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>La herramienta IA secreta de los agentes top productores.</p>", unsafe_allow_html=True)

# BANNER
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="video-placeholder"><div class="ad-badge">PROPIEDAD DESTACADA</div><div class="ad-overlay">Propiedades de la Comunidad</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.text_area("", placeholder="Pega el link aquí...", label_visibility="collapsed")
    st.button("✨ GENERAR DESCRIPCIÓN", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# PLANES
st.markdown("<br><br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='glass-container free-card'><h3>Inicial</h3><h1>$0</h1><hr style='opacity:0.2;'><p>{desc_free}</p></div>", unsafe_allow_html=True)
    st.button("REGISTRO GRATIS", key="f1")

with col2:
    st.markdown(f"<div class='glass-container pro-card'><div class='popular-badge'>MÁS POPULAR</div><h3 style='color:#00d2ff;'>Agente Pro</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'><p>{desc_pro}</p></div>", unsafe_allow_html=True)
    st.button("MEJORAR AHORA", key="f2")

with col3:
    st.markdown(f"<div class='glass-container agency-card'><h3 style='color:#DDA0DD;'>Agencia</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'><p>{desc_agency}</p></div>", unsafe_allow_html=True)
    st.button("CONTACTAR VENTAS", key="f3")
