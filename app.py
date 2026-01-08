import streamlit as st

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. LOGICA DE TRADUCCIÓN INTEGRAL ---
if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"

# Diccionario Maestro de Idiomas
traducciones = {
    "Español": {
        "title1": "Convierte Anuncios Aburridos en",
        "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores.",
        "placeholder": "🏠 Pega el link de la propiedad o describe brevemente los ambientes y detalles...",
        "btn_gen": "✨ GENERAR DESCRIPCIÓN",
        "p_destacada": "PROPIEDAD DESTACADA",
        "comunidad": "Propiedades de la Comunidad",
        "popular": "MÁS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agencia",
        "desc1": "3 descripciones / día", "t1_1": "Límite diario de generaciones.",
        "desc2": "Soporte Básico", "t1_2": "Ayuda técnica vía email en 48hs.",
        "desc3": "Marca de Agua", "t1_3": "Los textos incluyen mención a nuestra web.",
        "desc4": "Generaciones Ilimitadas", "t2_1": "Sin límites para tu negocio.",
        "desc5": "Pack Redes Sociales", "t2_2": "Post para Instagram y Facebook con hashtags.",
        "desc6": "Optimización SEO", "t2_3": "Textos preparados para Google.",
        "desc7": "Banner Principal", "t2_4": "Tus fotos rotan en nuestra home.",
        "desc8": "5 Usuarios / Cuentas", "t3_1": "Acceso para 5 miembros de tu equipo.",
        "desc9": "Panel de Equipo", "t3_2": "Gestiona el trabajo de tus agentes.",
        "desc10": "Acceso vía API", "t3_3": "Conexión directa con tu sistema.",
        "desc11": "Prioridad en Banner", "t3_4": "Tus anuncios aparecen más seguido.",
        "btn1": "REGISTRO GRATIS", "btn2": "MEJORAR AHORA", "btn3": "CONTACTAR VENTAS"
    },
    "English": {
        "title1": "Turn Boring Listings into",
        "title2": "Sales Magnets",
        "sub": "The secret AI tool used by top producers.",
        "placeholder": "🏠 Paste the property link or briefly describe the rooms and details...",
        "btn_gen": "✨ GENERATE DESCRIPTION",
        "p_destacada": "FEATURED PROPERTY",
        "comunidad": "Community Properties",
        "popular": "MOST POPULAR",
        "plan1": "Starter", "plan2": "Agent Pro", "plan3": "Agency",
        "desc1": "3 descriptions / day", "t1_1": "Daily generation limit.",
        "desc2": "Basic Support", "t1_2": "Email technical support in 48h.",
        "desc3": "Watermark", "t1_3": "Texts include a mention of our site.",
        "desc4": "Unlimited Generations", "t2_1": "No limits for your business.",
        "desc5": "Social Media Pack", "t2_2": "Posts for Instagram & FB with hashtags.",
        "desc6": "SEO Optimization", "t2_3": "Texts ready for Google ranking.",
        "desc7": "Main Banner", "t2_4": "Your photos rotate on our home page.",
        "desc8": "5 Users / Accounts", "t3_1": "Individual access for 5 team members.",
        "desc9": "Team Dashboard", "t3_2": "Manage your agents' work.",
        "desc10": "API Access", "t3_3": "Direct connection to your system.",
        "desc11": "Banner Priority", "t3_4": "Your ads appear more frequently.",
        "btn1": "FREE SIGN UP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES"
    },
    "Português": {
        "title1": "Transforme Anúncios Chatos em",
        "title2": "Ímãs de Vendas",
        "sub": "A ferramenta de IA secreta dos principais corretores.",
        "placeholder": "🏠 Cole o link do imóvel ou descreva brevemente os cômodos e detalhes...",
        "btn_gen": "✨ GERAR DESCRIÇÃO",
        "p_destacada": "PROPRIEDADE EM DESTAQUE",
        "comunidad": "Propriedades da Comunidade",
        "popular": "MAIS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agência",
        "desc1": "3 descrições / dia", "t1_1": "Limite diário de gerações.",
        "desc2": "Suporte Básico", "t1_2": "Ajuda técnica por email em 48h.",
        "desc3": "Marca d'Água", "t1_3": "Os textos incluem menção ao nosso site.",
        "desc4": "Gerações Ilimitadas", "t2_1": "Sem limites para o seu negócio.",
        "desc5": "Pacote Redes Sociais", "t2_2": "Post para Instagram e FB com hashtags.",
        "desc6": "Otimização SEO", "t2_3": "Textos prontos para o Google.",
        "desc7": "Banner Principal", "t2_4": "Suas fotos rotacionam em nossa home.",
        "desc8": "5 Usuários / Contas", "t3_1": "Acesso individual para 5 membros.",
        "desc9": "Painel de Equipe", "t3_2": "Gerencie o trabalho de seus corretores.",
        "desc10": "Acesso via API", "t3_3": "Conexão direta com seu sistema.",
        "desc11": "Prioridade no Banner", "t3_4": "Seus anúncios aparecem mais vezes.",
        "btn1": "REGISTRO GRÁTIS", "btn2": "MELHORAR AGORA", "btn3": "CONTATO VENDAS"
    }
}

# --- 3. ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .header-logo { font-size: 1.5rem; font-weight: 700; color: #fff; display: flex; align-items: center; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    .info-icon {
        display: inline-block; width: 14px; height: 14px;
        background-color: rgba(255, 255, 255, 0.2); color: #fff; border-radius: 50%;
        text-align: center; font-size: 10px; line-height: 14px; margin-left: 5px;
        cursor: help; position: relative;
    }
    .info-icon:hover::after {
        content: attr(data-tooltip); position: absolute; bottom: 20px; left: 50%;
        transform: translateX(-50%); background-color: #333; color: #fff;
        padding: 8px 12px; border-radius: 6px; font-size: 12px; white-space: normal;
        width: 180px; z-index: 100; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .video-placeholder {
        border: 1px solid rgba(0, 210, 255, 0.2); border-radius: 12px; height: 220px;
        display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
        margin-bottom: 20px; position: relative; overflow: hidden; background-size: cover; background-position: center;
        animation: float 4s ease-in-out infinite, adCarousel 15s infinite;
    }
    @keyframes adCarousel {
        0%, 30% { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'); }
        33%, 63% { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80'); }
        66%, 100% { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'); }
    }
    .ad-overlay { background: linear-gradient(0deg, rgba(0,0,0,0.8) 0%, transparent 100%); width: 100%; padding: 15px; text-align: center; }
    .ad-badge { position: absolute; top: 15px; left: 15px; background: rgba(0, 210, 255, 0.9); color: black; padding: 4px 12px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }

    .glass-container { background: rgba(38, 39, 48, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; }
    .stTextArea textarea { background-color: rgba(0,0,0,0.3) !important; border: 1px solid #444 !important; color: #eee !important; }

    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; 
        border: none !important; box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important;
        transition: all 0.4s ease !important; color: white !important; font-weight: 700 !important;
    }
    div.stButton > button[kind="primary"]:hover { transform: scale(1.05) !important; box-shadow: 0 0 30px rgba(0, 210, 255, 0.7) !important; }

    .card-wrapper { display: flex; flex-direction: column; height: 100%; }
    .free-card, .pro-card, .agency-card { 
        transition: all 0.4s ease-out !important; height: 420px !important; 
        display: flex; flex-direction: column; justify-content: flex-start;
    }
    .free-card:hover { transform: translateY(-10px) !important; border: 1px solid rgba(255, 255, 255, 0.4) !important; }
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.3) !important; }
    .pro-card:hover { transform: translateY(-10px) !important; border-color: #00d2ff !important; box-shadow: 0 0 40px rgba(0, 210, 255, 0.4) !important; }
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.3) !important; }
    .agency-card:hover { transform: translateY(-10px) !important; border-color: #DDA0DD !important; box-shadow: 0 0 40px rgba(221, 160, 221, 0.4) !important; }

    [data-testid="column"] button { width: 100% !important; }
    [data-testid="column"]:nth-child(1) button { border: 1px solid #444 !important; color: #888 !important; }
    [data-testid="column"]:nth-child(2) button { border: 2px solid #00d2ff !important; color: #00d2ff !important; }
    [data-testid="column"]:nth-child(3) button { border: 2px solid #DDA0DD !important; color: #DDA0DD !important; }
    div.stButton > button:hover { transform: translateY(-5px) !important; background: transparent !important; }

    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.8rem; z-index: 10; }
</style>
""", unsafe_allow_html=True)

# --- 4. INTERFAZ SUPERIOR ---
col_logo, _, col_lang = st.columns([2, 4, 1.5])
with col_logo:
    st.markdown('<div class="header-logo">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
with col_lang:
    idioma_selec = st.selectbox("", ["Español", "English", "Português"], label_visibility="collapsed")
    st.session_state.idioma = idioma_selec

L = traducciones[st.session_state.idioma]

st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)

# --- 5. CUERPO PRINCIPAL ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(f'<div class="video-placeholder"><div class="ad-badge">{L["p_destacada"]}</div><div class="ad-overlay">{L["comunidad"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.text_area("", placeholder=L['placeholder'], label_visibility="collapsed")
    st.button(L['btn_gen'], type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. PLANES TRADUCIDOS ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    desc_f = f"{L['desc1']} <span class='info-icon' data-tooltip='{L['t1_1']}'>i</span><br>{L['desc2']} <span class='info-icon' data-tooltip='{L['t1_2']}'>i</span><br>{L['desc3']} <span class='info-icon' data-tooltip='{L['t1_3']}'>i</span>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container free-card'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'><p>{desc_f}</p></div></div>", unsafe_allow_html=True)
    st.button(L['btn1'], key="f1")

with col2:
    desc_p = f"<b>{L['desc4']}</b> <span class='info-icon' data-tooltip='{L['t2_1']}'>i</span><br>{L['desc5']} <span class='info-icon' data-tooltip='{L['t2_2']}'>i</span><br>{L['desc6']} <span class='info-icon' data-tooltip='{L['t2_3']}'>i</span><br>✨ <b>{L['desc7']}</b> <span class='info-icon' data-tooltip='{L['t2_4']}'>i</span>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container pro-card'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'><p>{desc_p}</p></div></div>", unsafe_allow_html=True)
    st.button(L['btn2'], key="f2")

with col3:
    desc_a = f"{L['desc8']} <span class='info-icon' data-tooltip='{L['t3_1']}'>i</span><br>{L['desc9']} <span class='info-icon' data-tooltip='{L['t3_2']}'>i</span><br>{L['desc10']} <span class='info-icon' data-tooltip='{L['t3_3']}'>i</span><br>🔥 <b>{L['desc11']}</b> <span class='info-icon' data-tooltip='{L['t3_4']}'>i</span>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container agency-card'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'><p>{desc_a}</p></div></div>", unsafe_allow_html=True)
    st.button(L['btn3'], key="f3")
