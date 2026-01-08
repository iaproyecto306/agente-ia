import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS MAESTRO (CON ANIMACIONES DE INPUT Y RESULTADO) ---
st.markdown("""
<style>
    /* 1. TIPOGRAFÍA BASE LIMPIA */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }
    .stApp {
        background: rgba(0,0,0,0.8);
        color: #FFFFFF;
    }
    
    /* VIDEO DE FONDO */
    #background-video {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
        z-index: -1;
    }

    /* 2. TÍTULOS ESTILO ORIGINAL */
    .neon-title {
        font-size: 3.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        color: white;
        text-shadow: 0 0 25px rgba(0, 210, 255, 0.6);
        line-height: 1.2;
    }
    .neon-highlight {
        color: #00d2ff;
        text-shadow: 0 0 40px rgba(0, 210, 255, 0.9);
    }
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #cfd8dc;
        margin-top: 5px;
        margin-bottom: 40px;
        font-weight: 300;
    }

    /* 3. CONTENEDORES GLASS BASE */
    .glass-container {
        background: rgba(30, 30, 30, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        transition: all 0.4s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* --- INPUT BOX "VIVO" (Modificación pedida) --- */
    .stTextArea textarea {
        background-color: rgba(0,0,0,0.5) !important;
        border: 1px solid #555 !important;
        color: #ccc !important; /* Color gris claro cuando no está en foco */
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    /* Cuando haces clic para escribir: */
    .stTextArea textarea:focus {
        border-color: #00d2ff !important; /* Borde neón */
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4) !important; /* Resplandor */
        color: #00d2ff !important; /* Texto neón al escribir */
        background-color: rgba(0,0,0,0.7) !important;
    }

    /* --- ANIMACIÓN DE RESULTADO FINALIZADO (Modificación pedida) --- */
    @keyframes finishFlash {
        0% { box-shadow: 0 0 0 rgba(0, 210, 255, 0); border-color: #00d2ff; }
        50% { box-shadow: 0 0 50px rgba(0, 210, 255, 1); border-color: white; } /* Flash intenso */
        100% { box-shadow: 0 0 25px rgba(0, 210, 255, 0.5); border-color: #00d2ff; } /* Se queda brillando */
    }
    .result-box {
        background: rgba(20, 20, 20, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #00d2ff;
        /* Aplicamos la animación al aparecer */
        animation: finishFlash 1.2s ease-out forwards;
    }

    /* --- TIPOGRAFÍA DE PLANES ARREGLADA --- */
    .plan-price {
        font-size: 3rem;
        font-weight: 700;
        margin: 15px 0;
        font-family: 'Helvetica Neue', sans-serif !important;
    }
    .benefit-list {
        text-align: left;
        margin-top: 20px;
        font-size: 1.05rem;
        color: #e0e0e0;
        line-height: 1.7;
        /* Forzamos la tipografía correcta */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important; 
        letter-spacing: 0.3px;
    }
    .benefit-list div {
        margin-bottom: 10px;
        display: flex;
        align-items: center;
    }
    .check-icon {margin-right: 10px;}

    /* --- HOVER EFFECTS PLANES (Mantenidos de V5) --- */
    .glass-container.plan-free:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.3); }
    .glass-container.plan-pro { border: 1px solid rgba(0, 210, 255, 0.3); background: rgba(0, 210, 255, 0.05); }
    .glass-container.plan-pro:hover { transform: translateY(-10px) scale(1.02); box-shadow: 0 0 30px rgba(0, 210, 255, 0.4); border-color: #00d2ff; }
    .glass-container.plan-agency:hover { transform: translateY(-10px) scale(1.02); box-shadow: 0 0 30px rgba(221, 160, 221, 0.4); border-color: #DDA0DD; }

    /* BOTONES */
    div.stButton > button { background: transparent; border: 1px solid white; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; transition: all 0.3s; width: 100%; text-transform: uppercase; letter-spacing: 0.5px; }
    div.stButton > button:hover { background: rgba(255,255,255,0.1); }
    [data-testid="column"]:nth-of-type(2) div.stButton > button { background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%); border: none; color: #000; font-weight: 800; box-shadow: 0 0 15px rgba(0, 201, 255, 0.4); }
    [data-testid="column"]:nth-of-type(2) div.stButton > button:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(0, 201, 255, 0.8); }
</style>

<video autoplay muted loop id="background-video">
    <source src="https://assets.mixkit.co/videos/preview/mixkit-digital-animation-of-blue-lines-and-dots-996-large.mp4" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<h1 class='neon-title'>Convierte Anuncios Aburridos en <br><span class='neon-highlight'>Imanes de Ventas</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>La herramienta IA secreta de los agentes top productores.</p>", unsafe_allow_html=True)

# --- INPUT AREA ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container" style="justify-content: center;">', unsafe_allow_html=True)
    user_input = st.text_area("", height=120, placeholder="Ej: Casa en Dallas, 3 habitaciones, piscina renovada, cerca de colegios...")
    st.markdown("<br>", unsafe_allow_html=True)
    gen_btn = st.button("✨ GENERAR DESCRIPCIÓN MÁGICA")
    st.markdown('</div>', unsafe_allow_html=True)

# --- RESPUESTA IA ---
if 'generated' not in st.session_state: st.session_state.generated = False

if gen_btn and user_input:
    with c2:
        with st.spinner("Analizando psicología del comprador..."):
            time.sleep(1.5)
            st.session_state.generated = True
            mock_res = f"""
            🔥 **¡OFERTA IRRESISTIBLE!**
            
            Descubre el lujo accesible. Esta propiedad no es solo una casa, es el estilo de vida que mereces.
            
            ✅ **Espacios:** {user_input[:20]}... amplitud y diseño.
            ✅ **Ubicación:** Conectividad y tranquilidad.
            
            *Agenda tu visita hoy.*
            """

if st.session_state.generated:
    st.markdown("<br>", unsafe_allow_html=True)
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        # Usamos la nueva clase 'result-box' que tiene la animación
        st.markdown(f'<div class="result-box">{mock_res}</div>', unsafe_allow_html=True)

# --- PLANES DE PRECIOS ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
p1, p2, p3 = st.columns([1, 1, 1])

# --- PLAN 1: GRATIS ---
with p1:
    st.markdown("""
    <div class='glass-container plan-free' style='text-align: center;'>
        <h3 style='color: #ccc; margin:0;'>Starter</h3>
        <div class='plan-price'>$0</div>
        <p style='color: #aaa;'>Para probar</p>
        <hr style='border-color: #555; opacity: 0.5;'>
        
        <div class='benefit-list'>
            <div><span class='check-icon'>✅</span> 3 Descripciones / día</div>
            <div><span class='check-icon'>✅</span> Tono Estándar</div>
            <div style='color: #666;'><span class='check-icon'>❌</span> Optimización SEO</div>
            <div style='color: #666;'><span class='check-icon'>❌</span> Pack Redes Sociales</div>
        </div>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("EMPEZAR GRATIS")

# --- PLAN 2: PRO (EL QUE VENDE) ---
with p2:
    st.markdown("""
    <div class='glass-container plan-pro' style='text-align: center; position: relative;'>
        <div style='position: absolute; top: -12px; right: 0; left: 0; margin: auto; width: fit-content; background: #00d2ff; color: black; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 800; letter-spacing: 1px;'>POPULAR</div>
        <h3 style='color: #00d2ff; margin:0;'>AGENTE PRO</h3>
        <div class='plan-price'>$49<small>/mes</small></div>
        <p style='color: #ccc;'>Para cerrar ventas</p>
        <hr style='border-color: #00d2ff; opacity: 0.5;'>
        
        <div class='benefit-list'>
            <div><span class='check-icon'>✅</span> <b>Generaciones ILIMITADAS</b></div>
            <div><span class='check-icon'>✅</span> <b>Pack Instagram & FB</b></div>
            <div><span class='check-icon'>✅</span> <b>Optimización SEO Google</b></div>
            <div><span class='check-icon'>✅</span> Email Follow-ups</div>
        </div>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("MEJORAR AHORA 🚀")

# --- PLAN 3: AGENCIA ---
with p3:
    st.markdown("""
    <div class='glass-container plan-agency' style='text-align: center;'>
        <h3 style='color: #DDA0DD; margin:0;'>Agencia</h3>
        <div class='plan-price'>$199<small>/mes</small></div>
        <p style='color: #aaa;'>Para equipos</p>
        <hr style='border-color: #555; opacity: 0.5;'>
        
        <div class='benefit-list'>
            <div><span class='check-icon'>✅</span> Todo lo del plan PRO</div>
            <div><span class='check-icon'>✅</span> <b>Hasta 5 Usuarios</b></div>
            <div><span class='check-icon'>✅</span> Panel de Control</div>
            <div><span class='check-icon'>✅</span> Soporte Prioritario</div>
        </div>
        <br>
    </div>
    """, unsafe_allow_html=True)
    st.button("CONTACTAR VENTAS")

st.markdown("<br><br>", unsafe_allow_html=True)
