import streamlit as st
from google import genai

# --- CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

# Nueva forma de conectar (SDK oficial 2026)
client = genai.Client(api_key=API_KEY)

def generar_texto(prompt, idioma):
    try:
        # La nueva librería usa 'models.generate_content'
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Actúa como un experto inmobiliario. Escribe en {idioma}: {prompt}"
        )
        
        if response and response.text:
            return response.text
        else:
            return "ERROR_SISTEMA: No se recibió texto de la IA."
            
    except Exception as e:
        return f"ERROR_SISTEMA: {str(e)}"

# --- INTERFAZ ---
st.set_page_config(page_title="IA Realty Pro", layout="centered")
st.title("🏢 IA Realty Pro")

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"

idioma = st.radio("Idioma:", ["Español", "English"], horizontal=True)
st.session_state.idioma = idioma

user_input = st.text_area("Describe la propiedad:")

if st.button("✨ GENERAR ANUNCIO"):
    if user_input:
        with st.spinner("Conectando con el nuevo SDK de Google..."):
            resultado = generar_texto(user_input, st.session_state.idioma)
            
            if "ERROR_SISTEMA" in resultado:
                st.error("Error técnico detectado")
                st.info(f"Detalle: {resultado}")
            else:
                st.success("¡Generado correctamente!")
                st.write(resultado)
    else:
        st.warning("Por favor, ingresa una descripción.")
