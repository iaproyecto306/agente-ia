import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

# Configuramos la API de forma directa
genai.configure(api_key=API_KEY)

def generar_texto(prompt, idioma):
    try:
        # Usamos el nombre 'gemini-1.5-flash-latest' que es el más robusto actualmente
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Agregamos una instrucción de sistema explícita
        response = model.generate_content(
            f"Como experto inmobiliario, escribe exclusivamente en {idioma}: {prompt}"
        )
        
        if response and response.text:
            return response.text
        else:
            return "ERROR_INTERNO: La IA no generó texto."
            
    except Exception as e:
        error_str = str(e)
        # Si falla por el 404, intentamos con el modelo Pro (que a veces tiene rutas distintas)
        if "404" in error_str:
            try:
                model_pro = genai.GenerativeModel('gemini-1.5-pro')
                res_pro = model_pro.generate_content(f"Escribe en {idioma}: {prompt}")
                return res_pro.text
            except:
                return f"ERROR_TECNICO: {error_str}"
        return f"ERROR_TECNICO: {error_str}"

# --- INTERFAZ ---
st.title("🏢 IA Realty Pro")
user_input = st.text_area("Describe la propiedad:")

if st.button("✨ GENERAR ANUNCIO"):
    if user_input:
        with st.spinner("Conectando con Google..."):
            resultado = generar_texto(user_input, "Español")
            if "ERROR" in resultado:
                st.error("Sigue habiendo un problema con la API")
                st.info("Esto puede deberse a que la API Key necesita ser regenerada en AI Studio.")
                st.code(resultado)
            else:
                st.success("¡Anuncio generado!")
                st.write(resultado)
