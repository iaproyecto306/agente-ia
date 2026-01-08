import streamlit as st
from google import genai

# --- 1. CONFIGURACIÓN DE IA (Según la Guía Nueva) ---
# REEMPLAZA ESTA CLAVE por la que sacaste de AI Studio
LLAVE_IA = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA" 

client = genai.Client(api_key=LLAVE_IA)

# --- 2. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. DICCIONARIO DE TRADUCCIONES ---
traducciones = {
    "Español": {
        "title1": "Convierte Anuncios Aburridos en", "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores.",
        "placeholder": "🏠 Pega el link de la propiedad o describe brevemente...",
        "btn_gen": "✨ GENERAR DESCRIPCIÓN", "p_destacada": "PROPIEDAD DESTACADA",
        "comunidad": "Propiedades de la Comunidad", "popular": "MÁS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agencia",
        "btn1": "REGISTRO GRATIS", "btn2": "MEJORAR AHORA", "btn3": "CONTACTAR VENTAS"
    },
    "English": {
        "title1": "Turn Boring Listings into", "title2": "Sales Magnets",
        "sub": "The secret AI tool used by top producing agents.",
        "placeholder": "🏠 Paste the property link or describe briefly...",
        "btn_gen": "✨ GENERATE DESCRIPTION", "p_destacada": "FEATURED PROPERTY",
        "comunidad": "Community Properties", "popular": "MOST POPULAR",
        "plan1": "Starter", "plan2": "Pro Agent", "plan3": "Agency",
        "btn1": "FREE SIGNUP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES"
    }
}
# (Mantenemos la lógica de idiomas simplificada para la prueba)

# --- 4. ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; }
    .neon-title { font-size: 3rem; font-weight: 800; text-align: center; color: white; text-shadow: 0 0 20px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; }
    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; }
    div.stButton > button { background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; color: white !important; width: 100%; font-weight: bold; border: none !important; }
</style>
""", unsafe_allow_html=True)

# --- 5. INTERFAZ ---
if "idioma" not in st.session_state: st.session_state.idioma = "Español"
idioma_selec = st.selectbox("", ["Español", "English"], label_visibility="collapsed")
st.session_state.idioma = idioma_selec
L = traducciones[st.session_state.idioma]

st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    user_input = st.text_area("", placeholder=L['placeholder'], label_visibility="collapsed")
    
    if st.button(L['btn_gen'], type="primary"):
        if user_input:
            with st.spinner("Generando con Gemini 2.0..."):
                try:
                    # Usamos el modelo más nuevo de tu guía: gemini-2.0-flash
                    response = client.models.generate_content(
                        model="gemini-2.0-flash", 
                        contents=f"Actúa como experto inmobiliario. Crea un anuncio persuasivo para: {user_input}"
                    )
                    st.markdown(f"<div style='border:1px solid #00d2ff; padding:15px; border-radius:10px; margin-top:20px;'>{response.text}</div>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error técnico: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
