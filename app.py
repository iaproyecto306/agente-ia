import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide"
)

# --- DISEÑO CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stTextArea textarea { border-radius: 10px; border: 1px solid #cbd5e1; }
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: #1e40af; color: white; font-weight: bold;
    }
    .anuncio-container { 
        background-color: white; padding: 25px; border-radius: 12px; 
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border-left: 6px solid #1e40af;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE IA ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"
genai.configure(api_key=API_KEY)

def generar_anuncio(descripcion, idioma, estilo, plataforma):
    try:
        # Usamos el modelo estable
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Actúa como experto en marketing inmobiliario.
        Crea un anuncio para {plataforma} en idioma {idioma}.
        Tono: {estilo}.
        Detalles de la propiedad: {descripcion}
        Usa emojis, estructura clara y un fuerte llamado a la acción.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR_TECNICO: {str(e)}"

# --- INTERFAZ DE USUARIO ---
st.title("🏢 IA Realty Pro")
st.markdown("### Generador de Copywriting Inmobiliario de Alto Impacto")

# BARRA LATERAL (SIDEBAR)
with st.sidebar:
    st.header("⚙️ Ajustes del Anuncio")
    idioma_opt = st.selectbox("Idioma de salida", ["Español", "English", "Português", "Italiano"])
    estilo_opt = st.select_slider("Tono del mensaje", options=["Económico", "Profesional", "Persuasivo", "Lujo"])
    plataforma_opt = st.radio("Optimizar para:", ["Marketplace / Web", "Instagram / Redes", "WhatsApp / E-mail"])
    st.divider()
    st.info("Configura los filtros para que la IA adapte el lenguaje a tu cliente ideal.")

# CUERPO PRINCIPAL (COLUMNAS)
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("#### 📝 Datos de la Propiedad")
    descripcion_input = st.text_area(
        "Describe la propiedad (m2, ubicación, comodidades...)",
        placeholder="Ej: Penthouse en el Centro, 2 dormitorios, terraza con parrillero, vigilancia 24hs...",
        height=280
    )
    
    boton_ejecutar = st.button("✨ GENERAR ANUNCIO AHORA")

with col_output:
    st.markdown("#### 📄 Resultado")
    if boton_ejecutar:
        if descripcion_input:
            with st.spinner("La IA está redactando..."):
                resultado_final = generar_anuncio(descripcion_input, idioma_opt, estilo_opt, plataforma_opt)
                
                if "ERROR_TECNICO" in resultado_final:
                    st.error("Error de Conexión")
                    st.warning("Google requiere que esta API Key tenga facturación activa o sea regenerada en AI Studio.")
                    st.caption(f"Detalle técnico: {resultado_final}")
                else:
                    st.markdown(f'<div class="anuncio-container">{resultado_final}</div>', unsafe_allow_html=True)
                    st.divider()
                    st.download_button("📥 Descargar Texto", resultado_final, file_name="anuncio_realty.txt")
        else:
            st.warning("Por favor, ingresa los detalles de la propiedad en el cuadro de la izquierda.")

# PIE DE PÁGINA
st.markdown("---")
st.caption("© 2026 IA Realty Pro - Desarrollado para optimizar ventas inmobiliarias.")
