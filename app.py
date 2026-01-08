import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS MAESTRO ---
st.markdown("""
<style>
    /* 1. ESTILO GENERAL */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }
    .stApp {
        background: rgba(0,0,0,0.8);
        color: #FFFFFF;
    }
    
    /* VIDEO DE FONDO */
    #background-video {
        position: fixed;
        right: 0;
        bottom: 0;
        min-width: 100%; 
        min-height: 100%;
        z-index: -1;
    }

    /* 2. TÍTULOS (ESTILO ORIGINAL) */
    .neon-title {
        font-size: 3.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 10px;
        color: white;
        text-shadow: 0 0 25px rgba(0, 210, 255, 0.6);
        line-height: 1.2;
    }
    .neon-highlight {
        color: #00d2ff;
        text-shadow: 0 0 40px rgba(0, 210, 255, 0.9);
    }
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #cfd8dc;
        margin-top: 5px;
        margin-bottom: 40px;
        font-weight: 300;
    }

    /* 3. CONTENEDORES GLASS */
    .glass-container {
        background: rgba(30, 30, 30, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        transition: all 0.4s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center; /* Centramos todo como en la V1 */
    }

    /* --- INPUT BOX "VIVO" --- */
    .stTextArea textarea {
        background-color: rgba(0,0,0,0.5) !important;
        border: 1px solid #555 !important;
        color: #ccc !important;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #00d2ff !important;
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4) !important;
        color: #00d2ff !important;
        background-color: rgba(0,0,0,0.7) !important;
    }

    /* --- ANIMACIÓN RESULTADO --- */
    @keyframes finishFlash {
        0% { box-shadow: 0 0 0 rgba(0, 210, 255, 0); border-color: #00d2ff; }
        50% { box-shadow: 0 0 50px rgba(0, 210, 255, 1); border-color: white; }
        100% { box-shadow: 0 0 25px rgba(0, 210, 255, 0.5); border-color: #00d2ff; }
    }
    .result-box {
        background: rgba(20, 20, 20, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #00d2ff;
        animation: finishFlash 1.2s ease-out forwards;
    }

    /* --- BOTONES --- */
    
    /* 1. BOTÓN GENERAR (PRINCIPAL) - CIAN NEÓN COMO AL PRINCIPIO */
    /* Apuntamos al botón primary que definiremos en Python */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        padding: 0.8em 1.5em !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.8) !important;
    }

    /* 2. BOTONES DE PLANES (SECUNDARIOS) */
    div.stButton > button {
        background: transparent;
        border: 1px solid white;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        width: 100%;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background: rgba(255,255,255,0.1);
    }

    /* BOTÓN PLAN PRO (COLUMNA 2) */
    [data-testid="column"]:nth-of-type(2) div.stButton > button {
        border-color: #00d2ff;
        color: #00d2ff;
        font-weight: bold;
    }
    [data-testid="column"]:nth-of-type(2) div.stButton > button:
