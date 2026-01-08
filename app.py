import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro | Generador de Anuncios",
    page_icon="🏢",
    layout="wide"
)

# --- ESTILOS CSS AVANZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #d1d5db; }
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        height: 3.5em; 
        background-color: #2563eb; 
        color: white; 
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1d4ed8; border: none; }
    .result-box { 
        background-color: white; 
        padding: 20px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        border-left: 5px solid #2563eb;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURACIÓN DE IA ---
# Nota: Si decides cambiar a OpenAI, solo reemplazaremos esta sección
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"
genai.configure(api_key=API_KEY)

def generar_anuncio(descripcion, idioma, estilo, plataforma):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Actúa como un copywriter inmobiliario experto. 
        Crea un anuncio para {plataforma} en idioma {idioma}.
        El tono debe ser {estilo}.
        Propiedad: {descripcion}
        Incluye emojis pertinentes, una llamada a la acción clara y resalta los puntos fuertes.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error técnico: {str(e)}"

# --- INTERFAZ DE USUARIO ---
st.title("🏢 IA Realty Pro")
st.markdown("### Transforma descripciones simples en anuncios de alto impacto.")

with st.sidebar:
    st.header("⚙️ Configuración")
    idioma = st.selectbox("Idioma", ["Español", "Inglés", "Portugués", "Francés", "Italiano"])
    estilo = st.select_slider(
        "Tono del Anuncio",
        options=["Económico", "Estándar", "Persuasivo", "Lujoso/Premium"]
    )
    plataforma = st.radio(
        "Optimizar para:",
        ["Marketplace/Web", "Instagram/TikTok", "LinkedIn", "E-mail Marketing"]
    )
    st.info("Configura estos parámetros para ajustar la personalidad del texto generado.")

# --- ÁREA PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 📝 Detalles de la Propiedad")
    descripcion_usuario = st.text_area(
        "Ingresa los datos clave (m2, ubicación, dormitorios, precio, etc.):",
        placeholder="Ej: Casa en Carrasco, 3 dorm, 2 baños, fondo con parrillero, USD 450.000...",
        height=250
    )
    
    boton_generar = st.button("✨ GENERAR ANUNCIO PROFESIONAL")

with col2:
    st.markdown("#### 📄 Anuncio Generado")
    if boton_generar:
        if descripcion_usuario:
            with st.spinner("La IA está redactando tu anuncio..."):
                resultado = generar_anuncio(descripcion_usuario, idioma, estilo, plataforma)
                
                if "Error técnico" in resultado:
                    st.error("Lo sentimos, hubo un problema con la conexión de la API.")
                    st.info("Si el problema persiste, revisa la facturación o la clave en AI Studio.")
                else:
                    st.markdown(f'<div class="result-box">{resultado}</div>', unsafe_allow_html=True)
                    st.divider()
                    st.download_button("📥 Descargar Anuncio", resultado, file_name="anuncio_inmobiliario.txt")
        else:
            st.warning("⚠️ Por favor, ingresa los detalles de la propiedad a la izquierda.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("© 2026 IA Realty Pro - Herramienta de productividad para Real Estate.")
