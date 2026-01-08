import streamlit as st
from google import genai
from google.genai import types

# --- CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

# Forzamos al cliente a usar la versión 'v1' de la API para evitar el error 404
client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})

def generar_texto(prompt, idioma):
    # Lista de nombres técnicos exactos que Google acepta en el nivel gratuito
    modelos_maestros = [
        'gemini-1.5-flash-002', 
        'gemini-1.5-flash',
        'gemini-1.5-pro'
    ]
    
    ultimo_error = ""
    
    for nombre in modelos_a_probar:
        try:
            # Quitamos el prefijo 'models/' porque el SDK nuevo lo pone solo
            response = client.models.generate_content(
                model=nombre,
                contents=f"Como experto inmobiliario, escribe en {idioma}: {prompt}"
            )
            if response and response.text:
                return response.text
        except Exception as e:
            ultimo_error = str(e)
            continue
            
    # SI TODO FALLA: Este bloque nos dirá EXACTAMENTE qué modelos tienes tú permitidos
    try:
        modelos_disponibles = [m.name for m in client.models.list()]
        return f"ERROR_SISTEMA: No encontré el modelo. Tus modelos permitidos son: {modelos_disponibles}"
    except:
        return f"ERROR_SISTEMA: Error crítico de conexión. {ultimo_error}"

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
