import streamlit as st
from google import genai

# --- 1. CONFIGURACIÓN ---
# PEGA AQUÍ LA NUEVA CLAVE QUE CREASTE EN EL PASO ANTERIOR
API_KEY = "AIzaSyArgWsV8c3_AAZRLIjcU0gykhbnKtZApW0"

client = genai.Client(api_key=API_KEY)

def generar_texto(prompt, idioma):
    try:
        # Usamos el nombre estándar. Si la clave es nueva y de AI Studio, 
        # este nombre funcionará sí o sí.
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Escribe un anuncio inmobiliario profesional en {idioma} para: {prompt}"
        )
        return response.text
    except Exception as e:
        return f"ERROR_SISTEMA: {str(e)}"

# --- 2. INTERFAZ ---
st.title("🏢 IA Realty Pro")
user_input = st.text_area("Describe la propiedad:")

if st.button("GENERAR"):
    if user_input:
        with st.spinner("Generando anuncio..."):
            resultado = generar_texto(user_input, "Español")
            if "ERROR_SISTEMA" in resultado:
                st.error("Error de permisos")
                st.info("La API sigue rechazando la conexión. Verifica que la clave sea de 'AI Studio'.")
                st.code(resultado)
            else:
                st.success("¡Funciona!")
                st.write(resultado)
