import streamlit as st
import requests
import json

# --- CONFIGURACIÓN ---
API_KEY = "AIzaSyDft6Yxc6BDF8s_k7DzjM4ahBAbW6KJYPQ"

def obtener_modelo_y_generar(prompt):
    # PASO 1: Preguntar a Google qué modelos tienes disponibles
    list_url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
    
    try:
        list_res = requests.get(list_url)
        list_json = list_res.json()
        
        # Buscamos un modelo que permita generar contenido
        modelos = [m['name'] for m in list_json.get('models', []) if 'generateContent' in m.get('supportedMethods', [])]
        
        if not modelos:
            return "ERROR_API: Tu clave no tiene modelos de generación habilitados. Revisa AI Studio."
        
        # Seleccionamos el primero disponible (suele ser gemini-pro o flash)
        modelo_elegido = modelos[0] 
        
        # PASO 2: Generar el contenido con el nombre exacto que nos dio Google
        gen_url = f"https://generativelanguage.googleapis.com/v1/{modelo_elegido}:generateContent?key={API_KEY}"
        
        data = {
            "contents": [{
                "parts": [{"text": f"Eres un experto inmobiliario. Crea un anuncio para: {prompt}"}]
            }]
        }
        
        gen_res = requests.post(gen_url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
        gen_json = gen_res.json()
        
        if 'candidates' in gen_json:
            return gen_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"ERROR_DETALLE: No se pudo generar con {modelo_elegido}. Respuesta: {json.dumps(gen_json)}"

    except Exception as e:
        return f"ERROR_SISTEMA: {str(e)}"

# --- INTERFAZ ---
st.title("🏢 IA Realty Pro (Auto-Config)")
user_input = st.text_area("Describe la propiedad:")

if st.button("✨ GENERAR"):
    if user_input:
        with st.spinner("Buscando modelo compatible en tu cuenta..."):
            resultado = obtener_modelo_y_generar(user_input)
            if "ERROR_" in resultado:
                st.error("Problema con la cuenta de Google")
                st.code(resultado)
            else:
                st.success("¡Logrado!")
                st.write(resultado)
