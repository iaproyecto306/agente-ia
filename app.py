import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
# Asegúrate de que esta clave sea una NUEVA creada en AI Studio
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

genai.configure(api_key=API_KEY)

def generar_texto(prompt, idioma):
    # Intentamos con las 3 variantes de nombre que Google acepta según la región
    modelos = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'models/gemini-1.5-flash']
    
    for m in modelos:
        try:
            model = genai.GenerativeModel(m)
            response = model.generate_content(f"Escribe en {idioma}: {prompt}")
            if response.text:
                return response.text
        except Exception:
            continue
            
    # Si llega aquí, es que no encontró el modelo. Vamos a listar qué ve la clave:
    try:
        disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_methods]
        return f"ERROR_MODELO: No se halló Flash. Modelos que tu clave SÍ ve: {disponibles}"
    except Exception as e:
        return f"ERROR_CRITICO: {str(e)}"

# --- INTERFAZ ---
st.title("🏢 IA Realty Pro")
user_input = st.text_area("Descripción:")

if st.button("GENERAR"):
    if user_input:
        with st.spinner("Conectando..."):
            res = generar_texto(user_input, "Español")
            if "ERROR" in res:
                st.error("Fallo de conexión")
                st.code(res)
            else:
                st.success("¡Logrado!")
                st.write(res)
