import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE IA ---
# Tu clave según tus capturas está activa y funcionando.
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Error de configuración: {e}")

# CORRECCIÓN AQUÍ: Ahora acepta 'idioma' para evitar el TypeError
def generar_texto(prompt, idioma):
    # Lista de nombres de modelos para probar (de más nuevo a más compatible)
    modelos_a_probar = [
        'gemini-1.5-flash',        # Ruta estándar
        'models/gemini-1.5-flash', # Ruta técnica completa
        'gemini-pro'               # Ruta clásica estable
    ]
    
    ultimo_error = ""
    
    for nombre_modelo in modelos_a_probar:
        try:
            model = genai.GenerativeModel(nombre_modelo)
            prompt_final = f"Como experto inmobiliario, escribe en {idioma}: {prompt}"
            response = model.generate_content(prompt_final)
            
            if response and response.text:
                return response.text
        except Exception as e:
            ultimo_error = str(e)
            continue # Si falla uno, intenta el siguiente
            
    return f"ERROR_SISTEMA: No se pudo conectar con ningún modelo. Último error: {ultimo_error}" {str(e_alt)}"
# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="IA Realty Pro", page_icon="🏢", layout="wide")

# --- 3. DICCIONARIO DE TRADUCCIONES ---
traducciones = {
    "Español": {
        "title1": "Convierte Anuncios en", "title2": "Imanes de Ventas",
        "sub": "IA para agentes inmobiliarios.", "placeholder": "🏠 Describe la propiedad...",
        "btn_gen": "✨ GENERAR DESCRIPCIÓN", "plan1": "Inicial", "plan2": "Pro", "plan3": "Agencia"
    },
    "English": {
        "title1": "Turn Listings into", "title2": "Sales Magnets",
        "sub": "AI for real estate agents.", "placeholder": "🏠 Describe the property...",
        "btn_gen": "✨ GENERATE DESCRIPTION", "plan1": "Starter", "plan2": "Pro", "plan3": "Agency"
    }
}

# --- 4. INTERFAZ ---
if "idioma" not in st.session_state: st.session_state.idioma = "Español"

# Selector de idioma
col_logo, _, col_lang = st.columns([2, 4, 1])
with col_lang:
    idioma_selec = st.selectbox("", list(traducciones.keys()), label_visibility="collapsed")
    st.session_state.idioma = idioma_selec

L = traducciones[st.session_state.idioma]

# Títulos
st.markdown(f"<h1 style='text-align:center;'>{L['title1']} <span style='color:#00d2ff;'>{L['title2']}</span></h1>", unsafe_allow_html=True)

# Cuadro de entrada
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    user_input = st.text_area("", placeholder=L['placeholder'], height=150)
    
    if st.button(L['btn_gen'], type="primary", use_container_width=True):
        if user_input:
            with st.spinner("Creando descripción..."):
                # LLAMADA CORREGIDA: Pasamos dos argumentos
                resultado = generar_texto(user_input, st.session_state.idioma)
                
                if "ERROR_SISTEMA" in resultado:
                    st.error("Error técnico. Verifica que la API Key sea correcta en Google AI Studio.")
                    st.info(f"Detalle técnico: {resultado}")
                else:
                    st.success("¡Generado con éxito!")
                    st.markdown(f"--- \n {resultado}")
        else:
            st.warning("Escribe algo sobre la propiedad.")

# --- 5. PLANES (Simplificado para evitar errores de CSS) ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1: st.metric(L['plan1'], "$0")
with col2: st.metric(L['plan2'], "$49")
with col3: st.metric(L['plan3'], "$199")
