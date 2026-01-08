import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
# Asegúrate de que esta clave sea de AI Studio
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

genai.configure(api_key=API_KEY)

def generar_texto(prompt, idioma):
    try:
        # Usamos el modelo más básico y compatible
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content(
            f"Como experto inmobiliario, escribe en {idioma} un anuncio para: {prompt}"
        )
        
        if response.text:
            return response.text
        else:
            return "La IA no devolvió texto."
    except Exception as e:
        # Si falla el nombre corto, intentamos con el nombre técnico completo
        try:
            model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
            response_alt = model_alt.generate_content(f"Escribe en {idioma}: {prompt}")
            return response_alt.text
        except Exception as e_alt:
            return f"ERROR_FINAL: {str(e_alt)}"

# --- INTERFAZ ---
st.set_page_config(page_title="IA Realty Pro", page_icon="🏢")
st.title("🏢 IA Realty Pro")

user_input = st.text_area("Describe la propiedad (ej: Casa con piscina en Carrasco):")

if st.button("✨ GENERAR ANUNCIO"):
    if user_input:
        with st.spinner("Generando..."):
            resultado = generar_texto(user_input, "Español")
            
            if "ERROR_FINAL" in resultado:
                st.error("Error de conexión con Google")
                st.info("Detalle técnico:")
                st.code(resultado)
            else:
                st.success("¡Anuncio listo!")
                st.write(resultado)
    else:
        st.warning("Por favor, escribe una descripción.")
