import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# --- CONFIGURACIÓN ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

# Configuramos la clave
genai.configure(api_key=API_KEY)

def generar_texto(prompt, idioma):
    try:
        # FORZAMOS LA VERSIÓN V1 PARA EVITAR EL ERROR 404 DE V1BETA
        # Esta es la configuración técnica que "salta" el error que tienes
        opciones = RequestOptions(api_version='v1')
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(
            f"Como experto inmobiliario, escribe en {idioma}: {prompt}",
            request_options=opciones
        )
        
        if response.text:
            return response.text
        return "ERROR: Respuesta vacía."
            
    except Exception as e:
        return f"ERROR_TECNICO: {str(e)}"

# --- INTERFAZ ---
st.title("🏢 IA Realty Pro")
user_input = st.text_area("Describe la propiedad:")

if st.button("✨ GENERAR ANUNCIO"):
    if user_input:
        with st.spinner("Conectando con la versión estable..."):
            resultado = generar_texto(user_input, "Español")
            if "ERROR" in resultado:
                st.error("Fallo persistente de la API")
                st.code(resultado)
            else:
                st.success("¡Logrado!")
                st.write(resultado)
