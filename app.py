import streamlit as st
from google import genai
from google.genai import types

# --- CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

# Forzamos al cliente a usar la versión 'v1' de la API para evitar el error 404
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})

def generar_texto(prompt, idioma):
    try:
        # Probamos con el nombre corto primero
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Escribe un anuncio inmobiliario en {idioma}: {prompt}"
        )
        
        if response and response.text:
            return response.text
        return "ERROR_SISTEMA: Respuesta vacía."
            
    except Exception as e:
        # Si vuelve a dar 404, intentamos con la ruta técnica completa
        try:
            response_alt = client.models.generate_content(
                model="models/gemini-1.5-flash",
                contents=f"Escribe en {idioma}: {prompt}"
            )
            return response_alt.text
        except Exception as e_alt:
            return f"ERROR_SISTEMA: {str(e_alt)}"

# --- INTERFAZ SIMPLIFICADA PARA PRUEBAS ---
st.title("🏢 IA Realty Pro")

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"

user_input = st.text_area("Describe la propiedad:")

if st.button("GENERAR"):
    if user_input:
        with st.spinner("Conectando..."):
            resultado = generar_texto(user_input, st.session_state.idioma)
            if "ERROR_SISTEMA" in resultado:
                st.error(f"Error técnico: {resultado}")
            else:
                st.success("¡Éxito!")
                st.write(resultado)
