import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

# Configuración básica
genai.configure(api_key=API_KEY)

def generar_texto(prompt, idioma):
    try:
        # Usamos el nombre de modelo más estable
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Respuesta simple
        response = model.generate_content(
            f"Actúa como experto inmobiliario. Escribe en {idioma}: {prompt}"
        )
        
        if response and response.text:
            return response.text
        else:
            return "ERROR: El modelo no devolvió texto."
            
    except Exception as e:
        return f"ERROR_TECNICO: {str(e)}"

# --- INTERFAZ ---
st.title("🏢 IA Realty Pro")
user_input = st.text_area("Describe la propiedad:")

if st.button("✨ GENERAR ANUNCIO"):
    if user_input:
        with st.spinner("Conectando con Google AI..."):
            resultado = generar_texto(user_input, "Español")
            if "ERROR" in resultado:
                st.error("Error en la conexión")
                st.code(resultado)
            else:
                st.success("¡Anuncio generado!")
                st.write(resultado)
