import streamlit as st
from google import genai

# --- CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

# Conexión sin forzar versión de API para que use la que mejor le funcione a tu clave
client = genai.Client(api_key=API_KEY)

def generar_texto(prompt, idioma):
    try:
        # PASO 1: Listamos los modelos que Google te permite usar a TI
        modelos_disponibles = [m.name for m in client.models.list() if 'generateContent' in m.supported_methods]
        
        if not modelos_disponibles:
            return "ERROR_SISTEMA: Tu API Key no tiene modelos con permiso de generación habilitados."

        # PASO 2: Intentamos generar con el primero de la lista (el más compatible)
        # Normalmente el primero es gemini-1.5-flash
        modelo_a_usar = modelos_disponibles[0]
        
        response = client.models.generate_content(
            model=modelo_a_usar,
            contents=f"Como experto inmobiliario, escribe en {idioma}: {prompt}"
        )
        
        if response and response.text:
            return response.text
        return "ERROR_SISTEMA: El modelo respondió pero sin texto."

    except Exception as e:
        return f"ERROR_SISTEMA: {str(e)}"

# --- INTERFAZ ---
st.title("🏢 IA Realty Pro")
user_input = st.text_area("Describe la propiedad:")

if st.button("GENERAR"):
    if user_input:
        with st.spinner("Buscando modelo compatible..."):
            resultado = generar_texto(user_input, "Español")
            if "ERROR_SISTEMA" in resultado:
                st.error(resultado)
                # Mostramos un botón para depurar si falla
                if st.button("Ver mis modelos permitidos"):
                    modelos = [m.name for m in client.models.list()]
                    st.write(modelos)
            else:
                st.success("¡Éxito!")
                st.write(resultado)
