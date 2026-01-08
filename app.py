import streamlit as st

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. DICCIONARIO MAESTRO GLOBAL (6 IDIOMAS) ---
traducciones = {
    "Español": {
        "title1": "Convierte Anuncios Aburridos en", "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores.",
        "placeholder": "🏠 Pega el link de la propiedad o describe brevemente...",
        "btn_gen": "✨ GENERAR DESCRIPCIÓN", "p_destacada": "PROPIEDAD DESTACADA",
        "comunidad": "Propiedades de la Comunidad", "popular": "MÁS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agencia",
        "desc1": "3 descripciones / día", "t1_1": "Límite diario de generaciones para nuevos usuarios.",
        "desc2": "Soporte Básico", "t1_2": "Ayuda técnica vía email con respuesta en menos de 48hs.",
        "desc3": "Marca de Agua", "t1_3": "Los textos incluyen una pequeña mención a nuestra plataforma.",
        "desc4": "Generaciones Ilimitadas", "t2_1": "Crea tantas descripciones como necesites sin restricciones.",
        "desc5": "Pack Redes Sociales", "t2_2": "Genera automáticamente posts para Instagram, Facebook y TikTok con hashtags.",
        "desc6": "Optimización SEO", "t2_3": "Textos estructurados para aparecer primero en los buscadores.",
        "desc7": "Banner Principal", "t2_4": "Tus propiedades destacadas rotarán en nuestra página de inicio.",
        "desc8": "5 Usuarios / Cuentas", "t3_1": "Acceso individual para hasta 5 miembros de tu equipo inmobiliario.",
        "desc9": "Panel de Equipo", "t3_2": "Supervisa y gestiona las descripciones creadas por tus agentes.",
        "desc10": "Acceso vía API", "t3_3": "Conecta nuestra IA directamente con tu propio software o CRM.",
        "desc11": "Prioridad en Banner", "t3_4": "Tus anuncios aparecerán con el doble de frecuencia en la home.",
        "btn1": "REGISTRO GRATIS", "btn2": "MEJORAR AHORA", "btn3": "CONTACTAR VENTAS"
    },
    "English": {
        "title1": "Turn Boring Listings into", "title2": "Sales Magnets",
        "sub": "The secret AI tool used by top producers.",
        "placeholder": "🏠 Paste the property link or briefly describe...",
        "btn_gen": "✨ GENERATE DESCRIPTION", "p_destacada": "FEATURED PROPERTY",
        "comunidad": "Community Properties", "popular": "MOST POPULAR",
        "plan1": "Starter", "plan2": "Agent Pro", "plan3": "Agency",
        "desc1": "3 descriptions / day", "t1_1": "Daily generation limit for new users.",
        "desc2": "Basic Support", "t1_2": "Email support under 48h.",
        "desc3": "Watermark", "t1_3": "Generated texts include a small mention of our site.",
        "desc4": "Unlimited Generations", "t2_1": "Create as many descriptions as you need.",
        "desc5": "Social Media Pack", "t2_2": "Auto posts for IG, FB, and TikTok with hashtags.",
        "desc6": "SEO Optimization", "t2_3": "Texts ranked for search engines.",
        "desc7": "Main Banner", "t2_4": "Your properties rotate on our home.",
        "desc8": "5 Users / Accounts", "t3_1": "Access for up to 5 team members.",
        "desc9": "Team Dashboard", "t3_2": "Monitor agents' work.",
        "desc10": "API Access", "t3_3": "Connect AI to your CRM.",
        "desc11": "Banner Priority", "t3_4": "Higher frequency on homepage.",
        "btn1": "FREE SIGN UP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES"
    },
    "Português": { "title1": "Transforme Anúncios Chatos em", "title2": "Ímãs de Vendas", "sub": "A ferramenta de IA secreta dos principais corretores.", "placeholder": "🏠 Cole o link ou descreva...", "btn_gen": "✨ GERAR DESCRIÇÃO", "p_destacada": "EM DESTAQUE", "comunidad": "Comunidade", "popular": "MAIS POPULAR", "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agência", "desc1": "3 descrições / dia", "t1_1": "Limite diário.", "desc2": "Suporte Básico", "t1_2": "Até 48h.", "desc3": "Marca d'Água", "t1_3": "Menção ao site.", "desc4": "Ilimitadas", "t2_1": "Sem limites.", "desc5": "Redes Sociais", "t2_2": "Posts com hashtags.", "desc6": "SEO", "t2_3": "Ranking Google.", "desc7": "Banner Home", "t2_4": "Rotação na home.", "desc8": "5 Contas", "t3_1": "5 usuários.", "desc9": "Painel Equipe", "t3_2": "Gestão de agentes.", "desc10": "API", "t3_3": "Conecte seu CRM.", "desc11": "Prioridade", "t3_4": "Mais visibilidade.", "btn1": "GRÁTIS", "btn2": "UPGRADE", "btn3": "VENDAS" },
    "中文": { "title1": "将枯燥的广告转化为", "title2": "销售磁铁", "sub": "顶级制作人使用的秘密 AI 工具。", "placeholder": "🏠 粘贴房产链接或简要描述...", "btn_gen": "✨ 生成描述", "p_destacada": "精选物业", "comunidad": "社区物业", "popular": "最受欢迎", "plan1": "入门版", "plan2": "专业代理", "plan3": "代理机构", "desc1": "每天 3 条描述", "t1_1": "新用户的每日生成限制。", "desc2": "基础支持", "t1_2": "48小时内回复。", "desc3": "水印", "t1_3": "文本包含引用。", "desc4": "无限生成", "t2_1": "无限制创建。", "desc5": "社交媒体包", "t2_2": "自动生成带标签帖子。", "desc6": "SEO 优化", "t2_3": "搜索排名优化。", "desc7": "主横幅", "t2_4": "首页轮换。", "desc8": "5 个用户", "t3_1": "5 名成员权限。", "desc9": "团队面板", "t3_2": "监督代理人。", "desc10": "API 访问", "t3_3": "连接您的 CRM。", "desc11": "横幅优先级", "t3_4": "首页出现率更高。", "btn1": "免费注册", "btn2": "立即升级", "btn3": "联系销售" },
    "Français": { "title1": "Transformez vos annonces en", "title2": "Aimants à Ventes", "sub": "L'outil IA secret des agents.", "placeholder": "🏠 Collez le lien...", "btn_gen": "✨ GÉNÉRER LA DESCRIPTION", "p_destacada": "EN VEDETTE", "comunidad": "Communauté", "popular": "PLUS POPULAIRE", "plan1": "Initial", "plan2": "Agent Pro", "plan3": "Agence", "desc1": "3 descriptions / jour", "t1_1": "Limite quotidienne.", "desc2": "Support de base", "t1_2": "Sous 48h.", "desc3": "Filigrane", "t1_3": "Mention du site.", "desc4": "Illimitées", "t2_1": "Sans limites.", "desc5": "Pack Social", "t2_2": "Posts avec hashtags.", "desc6": "SEO", "t2_3": "Ranking Google.", "desc7": "Bannière Home", "t2_4": "Rotation home.", "desc8": "5 Utilisateurs", "t3_1": "5 membres.", "desc9": "Dashboard", "t3_2": "Gestion agents.", "desc10": "API", "t3_3": "Connectez CRM.", "desc11": "Priorité", "t3_4": "Plus de fréquence.", "btn1": "GRATUIT", "btn2": "AMÉLIORER", "btn3": "VENTES" },
    "Deutsch": { "title1": "Verwandeln Sie Anzeigen in", "title2": "Verkaufsmagnete", "sub": "Das geheime KI-Tool.", "placeholder": "🏠 Link einfügen...", "btn_gen": "✨ BESCHREIBUNG GENERIEREN", "p_destacada": "TOP-IMMOBILIE", "comunidad": "Community", "popular": "AM BELIEBTESTEN", "plan1": "Basis", "plan2": "Agent Pro", "plan3": "Agentur", "desc1": "3 Beschreibungen / Tag", "t1_1": "Tägliches Limit.", "desc2": "Basis-Support", "t1_2": "Unter 48h.", "desc3": "Wasserzeichen", "t1_3": "Web-Link inkl.", "desc4": "Unbegrenzt", "t2_1": "Ohne Limits.", "desc5": "Social Pack", "t2_2": "Posts & Hashtags.", "desc6": "SEO", "t2_3": "Ranking optimiert.", "desc7": "Hauptbanner", "t2_4": "Rotation Home.", "desc8": "5 Benutzer", "t3_1": "5 Mitglieder.", "desc9": "Team-Panel", "t3_2": "Makler verwalten.", "desc10": "API", "t3_3": "CRM-Anbindung.", "desc11": "Priorität", "t3_4": "Höhere Frequenz.", "btn1": "ANMELDEN", "btn2": "UPGRADE", "btn3": "KONTAKT" }
}

# --- 3. ESTILOS CSS (RESTAURANDO ANIMACIONES Y PERSONALIZANDO TOOLTIPS) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .header-logo { font-size: 1.5rem; font-weight: 700; color: #fff; }
    
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    /* TOOLTIPS BASE */
    .info-icon {
        display: inline-block; width: 15px; height: 15px; border-radius: 50%;
        text-align: center; font-size: 10px; line-height: 15px; margin-left: 8px;
        cursor: help; position: relative; font-weight: bold;
    }
    .info-icon:hover::after {
        content: attr(data-tooltip); position: absolute; bottom: 25px; left: 50%; transform: translateX(-50%);
        background-color: #1a1c23; color: #fff; padding: 10px 14px; border-radius: 8px; font-size: 12px; 
        width: 220px; z-index: 999; box-shadow: 0 10px 30px rgba(0,0,0,0.8); border: 1px solid rgba(255,255,255,0.1);
        line-height: 1.4; text-align: left; font-weight: normal;
    }

    /* COLORES DE TOOLTIPS POR PLAN */
    .i-free { background-color: rgba(255, 255, 255, 0.1); color: #888; border: 1px solid rgba(255, 255, 255, 0.2); }
    .i-pro { background-color: rgba(0, 210, 255, 0.1); color: #00d2ff; border: 1px solid rgba(0, 210, 255, 0.4); }
    .i-agency { background-color: rgba(221, 160, 221, 0.1); color: #DDA0DD; border: 1px solid rgba(221, 160, 221, 0.4); }

    /* ANIMACIONES RESTAURADAS */
    .glass-container { background: rgba(38, 39, 48, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; }
    
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; border: none !important; 
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.4) !important; transition: all 0.4s ease !important; color: white !important; font-weight: 700 !important;
    }
    div.stButton > button[kind="primary"]:hover { transform: scale(1.05) !important; box-shadow: 0 0 30px rgba(0, 210, 255, 0.7) !important; }

    .card-wrapper { display: flex; flex-direction: column; height: 100%; transition: transform 0.4s ease-out; }
    .card-wrapper:hover { transform: translateY(-10px); }

    .free-card, .pro-card, .agency-card { height: 420px !important; display: flex; flex-direction: column; justify-content: flex-start; text-align: center !important; }
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.3) !important; }
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.3) !important; }

    .feature-list { text-align: left; margin: 20px auto; display: inline-block; font-size: 0.95rem; color: #ccc; line-height: 2.2; }
    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.8rem; z-index: 10; }
    
    /* CARRUSEL ANIMADO */
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
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
    .ad-overlay { background: linear-gradient(0deg, rgba(0,0,0,0.8) 0%, transparent 100%); width: 100%; padding: 15px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 4. INTERFAZ SUPERIOR ---
if "idioma" not in st.session_state: st.session_state.idioma = "Español"

col_logo, _, col_lang = st.columns([2, 4, 1.5])
with col_logo: st.markdown('<div class="header-logo">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
with col_lang:
    idioma_selec = st.selectbox("", list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma), label_visibility="collapsed")
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

# --- 6. PLANES ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    desc_f = f"<div class='feature-list'>{L['desc1']}<span class='info-icon i-free' data-tooltip='{L['t1_1']}'>i</span><br>{L['desc2']}<span class='info-icon i-free' data-tooltip='{L['t1_2']}'>i</span><br>{L['desc3']}<span class='info-icon i-free' data-tooltip='{L['t1_3']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container free-card'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'>{desc_f}</div></div>", unsafe_allow_html=True)
    st.button(L['btn1'], key="f1")

with col2:
    desc_p = f"<div class='feature-list'><b>{L['desc4']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_1']}'>i</span><br>{L['desc5']}<span class='info-icon i-pro' data-tooltip='{L['t2_2']}'>i</span><br>{L['desc6']}<span class='info-icon i-pro' data-tooltip='{L['t2_3']}'>i</span><br><b>{L['desc7']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container pro-card'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'>{desc_p}</div></div>", unsafe_allow_html=True)
    st.button(L['btn2'], key="f2")

with col3:
    desc_a = f"<div class='feature-list'>{L['desc8']}<span class='info-icon i-agency' data-tooltip='{L['t3_1']}'>i</span><br>{L['desc9']}<span class='info-icon i-agency' data-tooltip='{L['t3_2']}'>i</span><br>{L['desc10']}<span class='info-icon i-agency' data-tooltip='{L['t3_3']}'>i</span><br><b>{L['desc11']}</b><span class='info-icon i-agency' data-tooltip='{L['t3_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container agency-card'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'>{desc_a}</div></div>", unsafe_allow_html=True)
    st.button(L['btn3'], key="f3")
