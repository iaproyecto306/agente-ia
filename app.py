import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE IA ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error de configuración inicial: {e}")

def generar_texto(prompt, idioma):
    # Lista de modelos compatibles
    modelos_a_probar = ['gemini-1.5-flash', 'gemini-pro']
    ultimo_error = "No se inició la generación"
    
    for nombre_modelo in modelos_a_probar:
        try:
            model = genai.GenerativeModel(nombre_modelo)
            prompt_final = f"Actúa como un experto inmobiliario. Escribe exclusivamente en {idioma}: {prompt}"
            response = model.generate_content(prompt_final)
            
            # Verificamos que la respuesta exista y tenga texto
            if response and hasattr(response, 'text') and response.text:
                return response.text
        except Exception as e:
            ultimo_error = str(e)
            continue
            
    # Si llegamos aquí, algo falló en todos los modelos
    return f"ERROR_SISTEMA: {ultimo_error}"

# --- 2. INTERFAZ Y TRADUCCIONES ---
if "idioma" not in st.session_state: 
    st.session_state.idioma = "Español"

traducciones = {
    "Español": {"title": "IA Realty Pro", "btn": "GENERAR", "placeholder": "Describe la propiedad..."},
    "English": {"title": "AI Realty Pro", "btn": "GENERATE", "placeholder": "Describe the property..."}
}

L = traducciones[st.session_state.idioma]

st.title(L["title"])
user_input = st.text_area(L["placeholder"], height=150)

if st.button(L["btn"]):
    if user_input:
        with st.spinner("Procesando..."):
            # Llamamos a la función
            resultado = generar_texto(user_input, st.session_state.idioma)
            
            # Verificación de seguridad para evitar el TypeError
            if resultado is None:
                st.error("La IA devolvió un resultado vacío (None).")
            elif "ERROR_SISTEMA" in resultado:
                st.error("Hubo un problema con la API de Google.")
                st.info(f"Detalle técnico: {resultado}")
            else:
                st.success("¡Listo!")
                st.write(resultado)
    else:
        st.warning("Por favor escribe una descripción.")
