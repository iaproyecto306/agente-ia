import streamlit as st
from google import genai

# --- 1. CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

# Conexión estable v1
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})

def generar_texto(prompt, idioma):
    # Lista corregida de nombres de modelos
    modelos_a_probar = [
        'gemini-1.5-flash',
        'gemini-1.5-flash-002',
        'gemini-1.5-pro'
    ]
    
    ultimo_error = ""
    
    for nombre in modelos_a_probar:
        try:
            response = client.models.generate_content(
                model=nombre,
                contents=f"Actúa como experto inmobiliario. Escribe en {idioma}: {prompt}"
            )
            if response and response.text:
                return response.text
        except Exception as e:
            ultimo_error = str(e)
            continue
            
    # SI TODO FALLA: Esto nos dirá qué modelos tienes tú permitidos exactamente
    try:
        modelos_reales = [m.name for m in client.models.list()]
        return f"ERROR_SISTEMA: No se encontró el modelo. Modelos disponibles en tu cuenta: {modelos_reales}"
    except:
        return f"ERROR_SISTEMA: Error crítico. Detalle: {ultimo_error}"

# --- 2. INTERFAZ ---
st.set_page_config(page_title="IA Realty Pro", layout="centered")
st.title("🏢 IA Realty Pro")

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"

idioma = st.radio("Idioma:", ["Español", "English"], horizontal=True)
st.session_state.idioma = idioma

user_input = st.text_area("Describe la propiedad (ej: Apartamento moderno en el centro):")

if st.button("✨ GENERAR ANUNCIO"):
    if user_input:
        with st.spinner("Buscando el modelo correcto en tu cuenta..."):
            resultado = generar_texto(user_input, st.session_state.idioma)
            
            if "ERROR_SISTEMA" in resultado:
                st.error("Error de configuración de Google")
                st.info(resultado)
            else:
                st.success("¡Anuncio generado!")
                st.write(resultado)
    else:
        st.warning("Por favor, ingresa una descripción.")
