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
        "desc4": "Generaciones Ilimitadas", "t2_1": "Sin límites para tu negocio.",
        "desc8": "5 Usuarios / Cuentas", "t3_1": "Acceso para 5 miembros de tu equipo.",
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
        "desc4": "Unlimited Generations", "t2_1": "No limits for your business.",
        "desc8": "5 Users / Accounts", "t3_1": "Access for 5 team members.",
        "btn1": "FREE SIGN UP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES"
    },
    "Português": {
        "title1": "Transforme Anúncios Chatos em", "title2": "Ímãs de Vendas",
        "sub": "A ferramenta de IA secreta dos principais corretores.",
        "placeholder": "🏠 Cole o link do imóvel ou descreva brevemente...",
        "btn_gen": "✨ GERAR DESCRIÇÃO", "p_destacada": "PROPRIEDADE EM DESTAQUE",
        "comunidad": "Propriedades da Comunidade", "popular": "MAIS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agência",
        "desc1": "3 descrições / dia", "t1_1": "Limite diário de gerações.",
        "desc4": "Gerações Ilimitadas", "t2_1": "Sem limites para o seu negócio.",
        "desc8": "5 Usuários / Contas", "t3_1": "Acesso para 5 membros.",
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
        "desc4": "无限生成", "t2_1": "业务无限制。",
        "desc8": "5 个用户 / 账户", "t3_1": "5 名团队成员的访问权限。",
        "btn1": "免费注册", "btn2": "立即升级", "btn3": "联系销售"
    },
    "Français": {
        "title1": "Transformez vos annonces en", "title2": "Aimants à Ventes",
        "sub": "L'outil IA secret des agents top producteurs.",
        "placeholder": "🏠 Collez le lien ou décrivez brièvement...",
        "btn_gen": "✨ GÉNÉRER LA DESCRIPTION", "p_destacada": "PROPRIÉTÉ EN VEDETTE",
        "comunidad": "Propriétés de la Communauté", "popular": "PLUS POPULAIRE",
        "plan1": "Initial", "plan2": "Agent Pro", "plan3": "Agence",
        "desc1": "3 descriptions / jour", "t1_1": "Limite de génération quotidienne.",
        "desc4": "Générations Illimitées", "t2_1": "Aucune limite pour votre entreprise.",
        "desc8": "5 Utilisateurs / Comptes", "t3_1": "Accès pour 5 membres de l'équipe.",
        "btn1": "INSCRIPTION GRATUITE", "btn2": "AMÉLIORER MAINTENANT", "btn3": "CONTACTER VENTES"
    },
    "Deutsch": {
        "title1": "Verwandeln Sie Anzeigen in", "title2": "Verkaufsmagnete",
        "sub": "Das geheime KI-Tool der Top-Produzenten.",
        "placeholder": "🏠 Link einfügen oder kurz beschreiben...",
        "btn_gen": "✨ BESCHREIBUNG GENERIEREN", "p_destacada": "TOP-IMMOBILIE",
        "comunidad": "Community-Immobilien", "popular": "AM BELIEBTESTEN",
        "plan1": "Basis", "plan2": "Agent Pro", "plan3": "Agentur",
        "desc1": "3 Beschreibungen / Tag", "t1_1": "Tägliches Limit.",
        "desc4": "Unbegrenzte KI-Texte", "t2_1": "Keine Grenzen für Ihr Business.",
        "desc8": "5 Benutzer / Konten", "t3_1": "Zugang für 5 Teammitglieder.",
        "btn1": "KOSTENLOS ANMELDEN", "btn2": "JETZT UPGRADEN", "btn3": "VERKAUF KONTAKTIEREN"
    }
}

# --- 3. ESTILOS CSS (MANTENIENDO SIMETRÍA Y NEÓN) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .header-logo { font-size: 1.5rem; font-weight: 700; color: #fff; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    /* TOOLTIPS */
    .info-icon {
        display: inline-block; width: 14px; height: 14px;
        background-color: rgba(255, 255, 255, 0.2); color: #fff; border-radius: 50%;
        text-align: center; font-size: 10px; line-height: 14px; margin-left: 5px; cursor: help;
    }
    .info-icon:hover::after {
        content: attr(data-tooltip); position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
        background-color: #333; color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 12px; width: 180px; z-index: 100;
    }

    .glass-container { background: rgba(38, 39, 48, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; }
    
    /* TARJETAS CON ALTURA FIJA PARA SIMETRÍA TOTAL */
    .card-wrapper { display: flex; flex-direction: column; height: 100%; }
    .free-card, .pro-card, .agency-card { 
        height: 420px !important; display: flex; flex-direction: column; justify-content: flex-start;
        transition: all 0.4s ease-out !important; 
    }
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.3) !important; }
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.3) !important; }

    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 5px 15px; border-radius: 20px; font-weight: 800; font-size: 0.8rem; z-index: 10; }
</style>
""", unsafe_allow_html=True)

# --- 4. INTERFAZ SUPERIOR ---
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
    st.markdown(f'<div class="glass-container"><textarea placeholder="{L["placeholder"]}" style="width:100%; height:100px; background:transparent; color:white; border:1px solid #444; border-radius:8px; padding:10px;"></textarea><br><br><button style="width:100%; background:linear-gradient(90deg, #00d2ff, #0099ff); border:none; color:white; padding:15px; border-radius:8px; font-weight:bold; cursor:pointer;">{L["btn_gen"]}</button></div>', unsafe_allow_html=True)

# --- 6. PLANES ---
st.markdown("<br><br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card-wrapper'><div class='glass-container free-card'><h3>{L['plan1']}</h3><h1>$0</h1><hr><p>{L['desc1']} <span class='info-icon' data-tooltip='{L['t1_1']}'>i</span></p></div></div>", unsafe_allow_html=True)
    st.button(L['btn1'], key="f1")

with col2:
    st.markdown(f"<div class='card-wrapper'><div class='glass-container pro-card'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>$49</h1><hr><p><b>{L['desc4']}</b> <span class='info-icon' data-tooltip='{L['t2_1']}'>i</span></p></div></div>", unsafe_allow_html=True)
    st.button(L['btn2'], key="f2")

with col3:
    st.markdown(f"<div class='card-wrapper'><div class='glass-container agency-card'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>$199</h1><hr><p>{L['desc8']} <span class='info-icon' data-tooltip='{L['t3_1']}'>i</span></p></div></div>", unsafe_allow_html=True)
    st.button(L['btn3'], key="f3")
