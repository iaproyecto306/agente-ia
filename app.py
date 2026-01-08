import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE LA API (GEMINI) ---
# Usamos la clave que me pasaste para activar el motor
GEN_AI_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"
genai.configure(api_key=GEN_AI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. DICCIONARIO MAESTRO (Traducciones Completas) ---
traducciones = {
    "Español": {
        "title1": "Convierte Anuncios Aburridos en", "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores.",
        "placeholder": "🏠 Pega el link de la propiedad o describe brevemente (ej: Depto 3 dorm, terraza, en Palermo)...",
        "btn_gen": "✨ GENERAR DESCRIPCIÓN", "p_destacada": "PROPIEDAD DESTACADA",
        "comunidad": "Propiedades de la Comunidad", "popular": "MÁS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agencia",
        "desc1": "3 descripciones / día", "t1_1": "Límite diario de generaciones para nuevos usuarios.",
        "desc2": "Soporte Básico", "t1_2": "Ayuda técnica vía email con respuesta en menos de 48hs.",
        "desc3": "Marca de Agua", "t1_3": "Los textos incluyen una pequeña mención a nuestra plataforma.",
        "desc4": "Generaciones Ilimitadas", "t2_1": "Crea tantas descripciones como necesites sin restricciones.",
        "desc5": "Pack Redes Sociales", "t2_2": "Genera automáticamente posts para Instagram, Facebook y TikTok con hashtags.",
        "desc6": "Optimización SEO", "t2_3": "Textos estructurados para aparecer primero en los buscadores.",
        "desc7": "Banner Principal", "t2_4": "Tus propiedades destacadas rotarán en nuestra página de inicio.",
        "desc8": "5 Usuarios / Cuentas", "t3_1": "Acceso individual para hasta 5 miembros de tu equipo inmobiliario.",
        "desc9": "Panel de Equipo", "t3_2": "Supervisa y gestiona las descripciones creadas por tus agentes.",
        "desc10": "Acceso vía API", "t3_3": "Conecta nuestra IA directamente con tu propio software o CRM.",
        "desc11": "Prioridad en Banner", "t3_4": "Tus anuncios aparecerán con el doble de frecuencia en la home.",
        "btn1": "REGISTRO GRATIS", "btn2": "MEJORAR AHORA", "btn3": "CONTACTAR VENTAS",
        "status": "Generando anuncio de alto impacto...",
        "resultado_header": "✅ Tu Anuncio Profesional (Método AIDA)"
    },
    "English": {
        "title1": "Turn Boring Listings into", "title2": "Sales Magnets",
        "sub": "The secret AI tool used by top producing agents.",
        "placeholder": "🏠 Paste the property link or describe briefly...",
        "btn_gen": "✨ GENERATE DESCRIPTION", "p_destacada": "FEATURED PROPERTY",
        "comunidad": "Community Properties", "popular": "MOST POPULAR",
        "plan1": "Starter", "plan2": "Pro Agent", "plan3": "Agency",
        "desc1": "3 descriptions / day", "t1_1": "Daily generation limit for new users.",
        "desc2": "Basic Support", "t1_2": "Technical help via email with response in less than 48 hours.",
        "desc3": "Watermark", "t1_3": "Generated texts include a small mention of our platform.",
        "desc4": "Unlimited Generations", "t2_1": "Create as many descriptions as you need without any restrictions.",
        "desc5": "Social Media Pack", "t2_2": "Automatically generate posts for Instagram, Facebook, and TikTok with hashtags.",
        "desc6": "SEO Optimization", "t2_3": "Structured texts designed to rank first in search engines.",
        "desc7": "Main Banner", "t2_4": "Your featured properties will rotate on our homepage.",
        "desc8": "5 Users / Accounts", "t3_1": "Individual access for up to 5 members of your real estate team.",
        "desc9": "Team Dashboard", "t3_2": "Monitor and manage the descriptions created by your agents.",
        "desc10": "API Access", "t3_3": "Connect our AI directly with your own software or CRM.",
        "desc11": "Banner Priority", "t3_4": "Your listings will appear twice as often on the home screen.",
        "btn1": "FREE SIGNUP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES",
        "status": "Generating high impact listing...",
        "resultado_header": "✅ Your Professional Ad (AIDA Method)"
    }
    # (Las demás traducciones se mantienen igual en tu código final)
}

# --- 4. ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    /* BOTÓN GENERAR */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; border: none !important; 
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4) !important; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important; 
        color: white !important; font-weight: 700 !important; height: 3.5rem !important; width: 100% !important;
    }
    div.stButton > button[kind="primary"]:hover { 
        background: #000000 !important; color: #ffffff !important;
        transform: scale(1.03) translateY(-2px) !important;
        box-shadow: 0 0 50px rgba(0, 210, 255, 1) !important; 
        border: 2px solid #00d2ff !important;
    }

    /* GLASS CONTAINER */
    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; }
    
    /* RESULT BOX */
    .result-box {
        background: rgba(0, 210, 255, 0.05);
        border: 1px solid #00d2ff;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        color: #e0e0e0;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* (Resto de los estilos de cards y carrusel que ya tenías...) */
</style>
""", unsafe_allow_html=True)

# --- 5. LÓGICA DE NAVEGACIÓN E IDIOMA ---
if "idioma" not in st.session_state: st.session_state.idioma = "Español"
col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo: st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
with col_lang:
    idioma_selec = st.selectbox("", list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma), label_visibility="collapsed")
    st.session_state.idioma = idioma_selec

L = traducciones[st.session_state.idioma]

# --- 6. PÁGINA DE INICIO ---
st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # Carrusel visual (Simulado con CSS que ya tenías)
    st.markdown(f'''
        <div style="background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'); height:230px; border-radius:12px; margin-bottom:20px; display:flex; align-items:flex-end; padding:20px; border:1px solid #00d2ff; box-shadow: 0 0 20px rgba(0,210,255,0.2);">
            <div style="background:rgba(0,210,255,1); color:black; padding:5px 10px; border-radius:4px; font-weight:bold; font-size:12px;">{L["p_destacada"]}</div>
        </div>
    ''', unsafe_allow_html=True)

    with st.container():
        user_input = st.text_area("", placeholder=L['placeholder'], label_visibility="collapsed", height=120)
        
        if st.button(L['btn_gen'], key="main_gen", type="primary"):
            if user_input:
                with st.spinner(L['status']):
                    # PROMPT ESTRATÉGICO AIDA
                    prompt = f"""
                    Actúa como un experto en Copywriting Inmobiliario de lujo. 
                    Idioma: {st.session_state.idioma}
                    Tarea: Crea una descripción irresistible para la siguiente propiedad usando el método AIDA (Atención, Interés, Deseo, Acción).
                    Propiedad: {user_input}
                    Requisitos:
                    - Título impactante.
                    - Texto emocional y persuasivo.
                    - Lista de beneficios clave.
                    - Llamado a la acción (CTA) claro.
                    """
                    try:
                        response = model.generate_content(prompt)
                        st.markdown(f"### {L['resultado_header']}")
                        st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("⚠️ Por favor, ingresa información de la propiedad.")

# --- 7. SECCIÓN DE PLANES (Manteniendo tu estética) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
# (Aquí iría el resto del código de tus planes tal cual lo tenías)
with col1:
    st.markdown(f"<div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><p>{L['desc1']}</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='glass-container' style='border-color:#00d2ff'><h3>{L['plan2']}</h3><h1>$49</h1><p>{L['desc4']}</p></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='glass-container'><h3>{L['plan3']}</h3><h1>$199</h1><p>{L['desc8']}</p></div>", unsafe_allow_html=True)
