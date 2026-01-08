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

    /* CAJAS DE CRISTAL */
    .glass-container {
        background: rgba(38, 39, 48, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 30px;
        height: 100%;
        text-align: center;
        transition: transform 0.3s ease;
    }
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

    /* BOTÓN GENERAR PRINCIPAL (Cian Fuerte) */
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

    /* --- ANIMACIÓN Y BRILLO DE BOTONES DE PLANES --- */
    
    /* Base */
    div.stButton > button {
        background: transparent;
        border: 1px solid #555;
        color: #ddd;
        border-radius: 6px;
        width: 100%;
        transition: all 0.3s ease;
        font-weight: 600;
    }

    /* 1. Botón GRATIS */
    [data-testid="column"]:nth-child(1) div.stButton > button:hover {
        background-color: rgba(255,255,255,0.1) !important;
        border-color: white !important;
        color: white !important;
        transform: scale(1.05);
    }

    /* 2. Botón PRO (Brillo CIAN Intenso) */
    [data-testid="column"]:nth-child(2) div.stButton > button {
        border-color: #00d2ff;
        color: #00d2ff;
    }
    /* AQUÍ ESTÁ EL ARREGLO: !important para forzar el brillo */
    [data-testid="column"]:nth-child(2) div.stButton > button:hover {
        background-color: #00d2ff !important; 
        color: black !important;
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.8) !important; /* Brillo fuerte */
        transform: scale(1.08) !important;
