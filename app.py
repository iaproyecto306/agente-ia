import streamlit as st
import time

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ESTILOS CSS ---
st.markdown("""
<style>
    /* FONDO GENERAL */
    .stApp {
        background-color: #0e1117;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* CABECERA */
    .header-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #fff;
        display: flex;
        align-items: center;
    }
    .header-logo span { margin-right: 10px; }

    /* TÍTULOS */
    .neon-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 10px;
        color: white;
        text-shadow: 0 0 25px rgba(0, 210, 255, 0.5);
    }
    .neon-highlight {
        color: #00d2ff;
        text-shadow: 0 0 40px rgba(0, 210, 255, 0.8);
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #aaa;
        margin-bottom: 40px;
        font-weight: 300;
    }

    /* CAJAS DE CRISTAL (BASE) */
    .glass-container {
        background: rgba(38, 39, 48, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        height: 100%;
        text-align: center;
        transition: all 0.3s ease; /* Suavidad para movimiento y brillo */
        position: relative;
    }
    /* Hover genérico para la gratis (movimiento sutil sin aura fuerte) */
    .glass-container:hover {
        transform: translateY(-5px);
        border-color: rgba(255,255,255,0.2);
    }

    /* INPUT TEXTAREA */
    .stTextArea textarea {
        background-color: rgba(0,0,0,0.3) !important;
        border: 1px solid #444 !important;
        color: #eee !important;
    }
    .stTextArea textarea:focus {
        border-color: #00d2ff !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3) !important;
    }

    /* BOTÓN GENERAR PRINCIPAL */
    button[kind="primary"] {
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important;
    }
    button[kind="primary"]:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.7) !important;
    }

    /* --- ESTILOS
