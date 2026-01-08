import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="AI Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS AVANZADOS (DARK PREMIUM + GLOW) ---
st.markdown("""
<style>
    /* FONDO Y TIPOGRAFÍA */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* ELIMINAR ELEMENTOS MOLESTOS DE STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* BOTÓN CON EFECTO GLOW (LUZ GIRATORIA) */
    div.stButton > button {
        position: relative;
        background: #1F2937;
        color: white;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-size: 1.1em;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        background-clip: padding-box; /* Importante para el borde */
        width: 100%;
    }

    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        border-color: #00FFFF;
        color: #00FFFF;
    }

    /* EFECTO DE TEXTO NEÓN PARA TÍTULOS */
    .neon-text {
        background: -webkit-linear-gradient(45deg, #00FFFF, #00CCFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* TARJETAS DE PRECIOS Y RESULTADOS */
    .card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 20px;
        transition: transform 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .card:hover {
        transform: translateY(-5px);
        border-color: #00FFFF;
    }
    
    /* INPUT FIELDS */
    .stTextInput > div > div > input {
        background-color: #0D1117;
        color: white;
        border: 1px solid #30363D;
        border-radius: 8px;
    }
    
    /* FADE IN ANIMATION */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .fade-in {
        animation: fadeIn 0.8s ease-out forwards;
    }
</style>
""", unsafe_allow_html=True)

# --- VARIABLES DE ESTADO ---
if 'generated' not in st.session_state:
    st.session_state.generated = False

# --- HEADER & IDIOMA ---
col_logo, col_lang = st.columns([6, 1])
with col_logo:
    st.markdown("### 🏢 **AI Realty Pro**")
with col_lang:
    lang = st.selectbox("", ["🇺🇸 EN", "🇪🇸 ES", "🇧🇷 PT"], label_visibility="collapsed")

# Definir textos según idioma
if "EN" in lang:
    title_text = "Turn Boring Listings into <span class='neon-text'>Sales Magnets</span>"
    subtitle_text = "The AI tool used by top 1% agents to write descriptions in seconds."
    input_label = "Paste property details or Zillow link here:"
    button_text = "✨ Generate Magic Description"
    loading_text = "Analyzing market data... Crafting persuasive copy..."
    result_title = "Your Premium Description:"
elif "ES" in lang:
    title_text = "Convierte Anuncios Aburridos en <span class='neon-text'>Ventas Seguras</span>"
    subtitle_text = "La herramienta IA que usan los agentes top para escribir en segundos."
    input_label = "Pega los detalles de la propiedad o link aquí:"
    button_text = "✨ Generar Descripción Mágica"
    loading_text = "Analizando datos del mercado... Creando texto persuasivo..."
    result_title = "Tu Descripción Premium:"
else: # PT
    title_text = "Transforme Anúncios Chatos em <span class='neon-text'>Vendas Rápidas</span>"
    subtitle_text = "A ferramenta de IA usada pelos melhores corretores."
    input_label = "Cole os detalhes da propriedade aqui:"
    button_text = "✨ Gerar Descrição Mágica"
    loading_text = "Analisando dados... Criando texto persuasivo..."
    result_title = "Sua Descrição Premium:"

# --- HERO SECTION ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<h1 style='text-align: center; font-size: 3.5rem;' class='fade-in'>{title_text}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 1.2rem; color: #8B949E;' class='fade-in'>{subtitle_text}</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- ÁREA DE INPUT PRINCIPAL ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(f"<div class='fade-in'>", unsafe_allow_html=True)
    user_input = st.text_area(input_label, height=150, placeholder="Ex: 3 bed, 2 bath in Miami, pool, renovated kitchen...")
    
    generate_btn = st.button(button_text)
    st.markdown("</div>", unsafe_allow_html=True)

# --- LÓGICA DE GENERACIÓN (SIMULADA POR AHORA) ---
if generate_btn and user_input:
    with c2:
        with st.spinner(loading_text):
            time.sleep(2) # Simula el tiempo de pensar de la IA
            st.session_state.generated = True
            
            # Aquí conectaríamos la API de OpenAI real después
            mock_response = f"""
            🌟 **LUXURY LIVING AWAITS!** 🌟
            
            Discover the perfect blend of style and comfort in this stunning residence. featuring:
            
            ✅ **Modern Elegance:** {user_input if user_input else "Spacious interiors..."}
            ✅ **Chef's Kitchen:** Perfect for entertaining guests.
            ✅ **Oasis Backyard:** Your private retreat.
            
            *Don't miss this opportunity. Schedule your private tour today!*
            #RealEstate #DreamHome #LuxuryLiving
            """

if st.session_state.generated:
    st.markdown("<br>", unsafe_allow_html=True)
    c1_res, c2_res, c3_res = st.columns([1, 2, 1])
    with c2_res:
        st.markdown(f"<div class='card fade-in'><h3>{result_title}</h3>{mock_response}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("📋 Copy to Clipboard")

# --- SECCIÓN DE PRUEBA SOCIAL (Social Proof) ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #484F58;'>TRUSTED BY AGENTS AT</h4>", unsafe_allow_html=True)
col_sp1, col_sp2, col_sp3, col_sp4 = st.columns(4)
with col_sp1: st.markdown("<h3 style='text-align: center; color: #6E7681;'>Re/Max</h3>", unsafe_allow_html=True)
with col_sp2: st.markdown("<h3 style='text-align: center; color: #6E7681;'>Keller W.</h3>", unsafe_allow_html=True)
with col_sp3: st.markdown("<h3 style='text-align: center; color: #6E7681;'>Century 21</h3>", unsafe_allow_html=True)
with col_sp4: st.markdown("<h3 style='text-align: center; color: #6E7681;'>Sotheby's</h3>", unsafe_allow_html=True)

# --- SECCIÓN DE PRECIOS (PRICING) ---
st.markdown("<br><hr style='border-color: #30363D;'><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Pricing Plans</h2>", unsafe_allow_html=True)

p1, p2, p3 = st.columns([1, 1, 1])

with p1:
    st.markdown("""
    <div class='card' style='text-align: center;'>
        <h3>Starter</h3>
        <h1>Free</h1>
        <p style='color: #8B949E;'>For new agents</p>
        <hr style='border-color: #30363D;'>
        <p>3 Descriptions / day</p>
        <p>Basic Support</p>
        <br>
        <button style='background: transparent; border: 1px solid white; color: white; padding: 10px; border-radius: 5px;'>Try Free</button>
    </div>
    """, unsafe_allow_html=True)

with p2:
    # Plan destacado con borde brillante
    st.markdown("""
    <div class='card' style='text-align: center; border: 1px solid #00FFFF; box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);'>
        <h3 style='color: #00FFFF;'>Pro Agent 🚀</h3>
        <h1>$49<small style='font-size: 0.5em'>/mo</small></h1>
        <p style='color: #8B949E;'>For top producers</p>
        <hr style='border-color: #30363D;'>
        <p><b>Unlimited</b> Generations</p>
        <p>Instagram & Facebook Ads</p>
        <p>SEO Optimization</p>
        <br>
        <button style='background: #00FFFF; color: black; border: none; padding: 10px; border-radius: 5px; font-weight: bold; width: 100%;'>Get Started</button>
    </div>
    """, unsafe_allow_html=True)

with p3:
    st.markdown("""
    <div class='card' style='text-align: center;'>
        <h3>Agency</h3>
        <h1>$199<small style='font-size: 0.5em'>/mo</small></h1>
        <p style='color: #8B949E;'>For teams</p>
        <hr style='border-color: #30363D;'>
        <p>5 Users Included</p>
        <p>API Access</p>
        <p>Priority Support</p>
        <br>
        <button style='background: transparent; border: 1px solid white; color: white; padding: 10px; border-radius: 5px;'>Contact Sales</button>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
