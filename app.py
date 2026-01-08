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
        "title1": "Turn Boring Listings into", "title2": "Sales Magnets",
        "sub": "The secret AI tool used by top producers.",
        "placeholder": "🏠 Paste the property link or briefly describe...",
        "btn_gen": "✨ GENERATE DESCRIPTION", "p_destacada": "FEATURED PROPERTY",
        "comunidad": "Community Properties", "popular": "MOST POPULAR",
        "plan1": "Starter", "plan2": "Agent Pro", "plan3": "Agency",
        "desc1": "3 descriptions / day", "t1_1": "Daily generation limit.",
        "desc2": "Basic Support", "t1_2": "Email support in 48h.",
        "desc3": "Watermark", "t1_3": "Texts include our website mention.",
        "desc4": "Unlimited Generations", "t2_1": "No limits for your business.",
        "desc5": "Social Media Pack", "t2_2": "Instagram & FB posts with hashtags.",
        "desc6": "SEO Optimization", "t2_3": "Texts ready for Google.",
        "desc7": "Main Banner", "t2_4": "Your photos rotate on our home.",
        "desc8": "5 Users / Accounts", "t3_1": "Access for 5 team members.",
        "desc9": "Team Panel", "t3_2": "Manage your agents' work.",
        "desc10": "API Access", "t3_3": "Direct connection to your system.",
        "desc11": "Banner Priority", "t3_4": "Your ads appear more frequently.",
        "btn1": "FREE SIGN UP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES"
    },
    "Português": {
        "title1": "Transforme Anúncios Chatos em", "title2": "Ímãs de Vendas",
        "sub": "A ferramenta de IA secreta dos principais corretores.",
        "placeholder": "🏠 Cole o link do imóvel ou descreva...",
        "btn_gen": "✨ GERAR DESCRIÇÃO", "p_destacada": "PROPRIEDADE EM DESTAQUE",
        "comunidad": "Propriedades da Comunidade", "popular": "MAIS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agência",
        "desc1": "3 descrições / dia", "t1_1": "Limite diário de gerações.",
        "desc2": "Suporte Básico", "t1_2": "Ajuda técnica em 48h.",
        "desc3": "Marca d'Água", "t1_3": "Textos incluem menção ao site.",
        "desc4": "Gerações Ilimitadas", "t2_1": "Sem limites.",
        "desc5": "Pack Redes Sociais", "t2_2": "Posts para IG e FB.",
        "desc6": "Otimização SEO", "t2_3": "Textos prontos para Google.",
        "desc7": "Banner Principal", "t2_4": "Fotos rotacionam na home.",
        "desc8": "5 Usuários / Contas", "t3_1": "Acesso para 5 membros.",
        "desc9": "Painel de Equipe", "t3_2": "Gerencie seus corretores.",
        "desc10": "Acesso via API", "t3_3": "Conexão com seu sistema.",
        "desc11": "Prioridade no Banner", "t3_4": "Mais frequência na home.",
        "btn1": "REGISTRO GRÁTIS", "btn2": "MELHORAR AGORA", "btn3": "CONTATO VENDAS"
    },
    "中文": {
        "title1": "将枯燥的广告转化为", "title2": "销售磁铁",
        "sub": "顶级制作人使用的秘密 AI 工具。",
        "placeholder": "🏠 粘贴房产链接或简要描述...",
        "btn_gen": "✨ 生成描述", "p_destacada": "精选物业",
        "comunidad": "社区物业", "popular": "最受欢迎",
        "plan1": "入门版", "plan2": "专业代理", "plan3": "代理机构",
        "desc1": "每天 3 条描述", "t1_1": "每日生成限制。",
        "desc2": "基础支持", "t1_2": "48小时内邮件支持。",
        "desc3": "水印", "t1_3": "文字包含我们的网站引用。",
        "desc4": "无限生成", "t2_1": "业务无限制。",
        "desc5": "社交媒体包", "t2_2": "带标签的 IG 和 FB 帖子。",
        "desc6": "SEO 优化", "t2_3": "为 Google 准备的文字。",
        "desc7": "主横幅", "t2_4": "您的照片在首页轮换。",
        "desc8": "5 个用户 / 账户", "t3_1": "5 名团队成员的权限。",
        "desc9": "团队面板", "t3_2": "管理代理人的工作。",
        "desc10": "API 访问", "t3_3": "直接连接到您的系统。",
        "desc11": "横幅优先级", "t3_4": "您的广告出现频率更高。",
        "btn1": "免费注册", "btn2": "立即升级", "btn3": "联系销售"
    },
    "Français": {
        "title1": "Transformez vos annonces en", "title2": "Aimants à Ventes",
        "sub": "L'outil IA secret des agents top producteurs.",
        "placeholder": "🏠 Collez le lien ou décrivez brièvement...",
        "btn_gen": "✨ GÉNÉRER LA DESCRIPTION", "p_destacada": "PROPRIÉTÉ EN VEDETTE",
        "comunidad": "Propriétés de la Communauté", "popular": "PLUS POPULAIRE",
        "plan1": "Initial", "plan2": "Agent Pro", "plan3": "Agence",
        "desc1": "3 descriptions / jour", "t1_1": "Limite de génération.",
        "desc2": "Support de base", "t1_2": "Support par email en 48h.",
        "desc3": "Filigrane", "t1_3": "Les textes incluent notre site.",
        "desc4": "Générations Illimitées", "t2_1": "Aucune limite.",
        "desc5": "Pack Réseaux Sociaux", "t2_2": "Posts IG et FB avec hashtags.",
        "desc6": "Optimisation SEO", "t2_3": "Prêt pour Google.",
        "desc7": "Bannière Principale", "t2_4": "Vos photos tournent sur l'accueil.",
        "desc8": "5 Utilisateurs / Comptes", "t3_1": "Accès pour 5 membres.",
        "desc9": "Tableau de Bord", "t3_2": "Gérez vos agents.",
        "desc10": "Accès API", "t3_3": "Connexion directe.",
        "desc11": "Priorité Bannière", "t3_4": "Plus de fréquence sur l'accueil.",
        "btn1": "INSCRIPTION GRATUITE", "btn2": "AMÉLIORER", "btn3": "CONTACTER VENTES"
    },
    "Deutsch": {
        "title1": "Verwandeln Sie Anzeigen in", "title2": "Verkaufsmagnete",
        "sub": "Das geheime KI-Tool der Top-Produzenten.",
        "placeholder": "🏠 Link einfügen oder kurz beschreiben...",
        "btn_gen": "✨ BESCHREIBUNG GENERIEREN", "p_destacada": "TOP-IMMOBILIE",
        "comunidad": "Community-Immobilien", "popular": "AM BELIEBTESTEN",
        "plan1": "Basis", "plan2": "Agent Pro", "plan3": "Agentur",
        "desc1": "3 Beschreibungen / Tag", "t1_1": "Tägliches Limit.",
        "desc2": "Basis-Support", "t1_2": "E-Mail-Support in 48h.",
        "desc3": "Wasserzeichen", "t1_3": "Texte enthalten Web-Link.",
        "desc4": "Unbegrenzte KI-Texte", "t2_1": "Keine Grenzen.",
        "desc5": "Social Media Paket", "t2_2": "IG & FB Posts mit Hashtags.",
        "desc6": "SEO-Optimierung", "t2_3": "Bereit für Google.",
        "desc7": "Hauptbanner", "t2_4": "Ihre Fotos auf der Startseite.",
        "desc8": "5 Benutzer / Konten", "t3_1": "Zugang für 5 Mitglieder.",
        "desc9": "Team-Panel", "t3_2": "Verwalten Sie Ihre Makler.",
        "desc10": "API-Zugang", "t3_3": "Direkte Anbindung.",
        "desc11": "Banner-Priorität", "t3_4": "Höhere Frequenz auf Home.",
        "btn1": "ANMELDEN", "btn2": "JETZT UPGRADEN", "btn3": "KONTAKT"
    }
}

# --- 3. ESTILOS CSS (RESTAURANDO ANIMACIONES Y AURA) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .header-logo { font-size: 1.5rem; font-weight: 700; color: #fff; }
    
    .neon-title { 
        font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; 
        text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); 
    }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    .info-icon {
        display: inline-block; width: 14px; height: 14px; background-color: rgba(255, 255, 255, 0.2);
        color: #fff; border-radius: 50%; text-align: center; font-size: 10px; line-height: 14px; margin-left: 5px;
        cursor: help; position: relative;
    }
    .info-icon:hover::after {
        content: attr(data-tooltip); position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
        background-color: #333; color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 12px; width: 180px; z-index: 100;
    }

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

    /* SIMETRÍA DEFINITIVA */
    .card-wrapper { display: flex; flex-direction: column; height: 100%; }
    .free-card, .pro-card, .agency-card { 
        height: 420px !important; display: flex; flex-direction: column; justify-content: flex-start;
        transition: all 0.4s ease-out !important; 
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
if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"

col_logo, _, col_lang = st.columns([2, 4, 1.5])
with col_logo:
    st.markdown('<div class="header-logo">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
with col_lang:
    idioma_selec = st.selectbox("", list(traducciones.keys()), label_visibility="collapsed")
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
