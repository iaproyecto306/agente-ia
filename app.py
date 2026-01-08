import streamlit as st
import requests
import json

# --- CONFIGURACIÓN ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

def generar_texto_directo(prompt):
    # Forzamos la URL a la versión estable v1 manualmente
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    headers = {'Content-Type': 'application/json'}
    
    data = {
        "contents": [{
            "parts": [{"text": f"Actúa como experto inmobiliario. Genera un anuncio para: {prompt}"}]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        res_json = response.json()
        
        # Extraemos el texto del formato JSON de Google
        if 'candidates' in res_json:
            texto = res_json['candidates'][0]['content']['parts'][0]['text']
            return texto
        else:
            return f"ERROR_API: {json.dumps(res_json)}"
            
    except Exception as e:
        return f"ERROR_CONEXION: {str(e)}"

# --- INTERFAZ ---
st.set_page_config(page_title="IA Realty Pro")
st.title("🏢 IA Realty Pro (Conexión Directa)")

user_input = st.text_area("Describe la propiedad:")

if st.button("✨ GENERAR ANUNCIO"):
    if user_input:
        with st.spinner("Llamando directamente a Google v1..."):
            resultado = generar_texto_directo(user_input)
            
            if "ERROR_" in resultado:
                st.error("Error en la respuesta de Google")
                st.code(resultado)
            else:
                st.success("¡Logrado!")
                st.write(resultado)
    else:
        st.warning("Escribe una descripción.")
