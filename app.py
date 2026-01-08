import streamlit as st

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. DICCIONARIO MAESTRO (6 IDIOMAS) ---
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
    "English": { "title1": "Turn Boring Listings into", "title2": "Sales Magnets", "sub": "The secret AI tool used by top producers.", "placeholder": "🏠 Paste link...", "btn_gen": "✨ GENERATE", "p_destacada": "FEATURED", "comunidad": "Community", "popular": "MOST POPULAR", "plan1": "Starter", "plan2": "Pro", "plan3": "Agency", "desc1": "3/day", "t1_1": "Daily limit.", "desc2": "Basic", "t1_2": "48h response.", "desc3": "Watermark", "t1_3": "Site mention.", "desc4": "Unlimited", "t2_1": "No limits.", "desc5": "Social Pack", "t2_2": "Auto posts.", "desc6": "SEO", "t2_3": "Rank higher.", "desc7": "Banner", "t2_4": "Home rotation.", "desc8": "5 Users", "t3_1": "5 members.", "desc9": "Panel", "t3_2": "Manage agents.", "desc10": "API", "t3_3": "Connect CRM.", "desc11": "Priority", "t3_4": "Double visibility.", "btn1": "SIGN UP", "btn2": "UPGRADE", "btn3": "CONTACT" },
    "Português": { "title1": "Anúncios em", "title2": "Ímãs de Vendas", "sub": "Ferramenta secreta.", "placeholder": "🏠 Cole o link...", "btn_gen": "✨ GERAR", "p_destacada": "DESTAQUE", "comunidad": "Comunidade", "popular": "POPULAR", "plan1": "Inicial", "plan2": "Pro", "plan3": "Agência", "desc1": "3 p/ dia", "t1_1": "Limite.", "desc2": "Suporte", "t1_2": "48h.", "desc3": "Marca", "t1_3": "Menção.", "desc4": "Ilimitado", "t2_1": "Sem limite.", "desc5": "Social", "t2_2": "Posts.", "desc6": "SEO", "t2_3": "Ranking.", "desc7": "Banner", "t2_4": "Home.", "desc8": "5 Contas", "t3_1": "5 membros.", "desc9": "Painel", "t3_2": "Gestão.", "desc10": "API", "t3_3": "CRM.", "desc11": "Prioridade", "t3_4": "Dobra.", "btn1": "GRÁTIS", "btn2": "UPGRADE", "btn3": "VENDAS" },
    "中文": { "title1": "房产广告", "title2": "销售磁铁", "sub": "AI 工具。", "placeholder": "🏠 粘贴...", "btn_gen": "✨ 生成", "p_destacada": "精选", "comunidad": "社区", "popular": "最受欢迎", "plan1": "入门", "plan2": "专业", "plan3": "机构", "desc1": "3条/天", "t1_1": "限制。", "desc2": "支持", "t1_2": "48小时。", "desc3": "水印", "t1_3": "引用。", "desc4": "无限", "t2_1": "无限制。", "desc5": "社交", "t2_2": "帖子。", "desc6": "SEO", "t2_3": "优化。", "desc7": "横幅", "t2_4": "首页。", "desc8": "5用户", "t3_1": "5成员。", "desc9": "面板", "t3_2": "管理。", "desc10": "API", "t3_3": "CRM。", "desc11": "优先级", "t3_4": "双倍。", "btn1": "免费", "btn2": "升级", "btn3": "联系" },
    "Français": { "title1": "Annonces", "title2": "Aimants à Ventes", "sub": "Outil secret.", "placeholder": "🏠 Collez...", "btn_gen": "✨ GÉNÉRER", "p_destacada": "VEDETTE", "comunidad": "Communauté", "popular": "POPULAIRE", "plan1": "Initial", "plan2": "Pro", "plan3": "Agence", "desc1": "3 / jour", "t1_1": "Limite.", "desc2": "Support", "t1_2": "48h.", "desc3": "Filigrane", "t1_3": "Mention.", "desc4": "Illimité", "t2_1": "Sans limite.", "desc5": "Social", "t2_2": "Posts.", "desc6": "SEO", "t2_3": "Ranking.", "desc7": "Bannière", "t2_4": "Home.", "desc8": "5 Comptes", "t3_1": "5 membres.", "desc9": "Dashboard", "t3_2": "Gestion.", "desc10": "API", "t3_3": "CRM.", "desc11": "Priorité", "t3_4": "Fréquence.", "btn1": "GRATUIT", "btn2": "AMÉLIORER", "btn3": "VENTES" },
    "Deutsch": { "title1": "Anzeigen in", "title2": "Verkaufsmagnete", "sub": "KI-Tool.", "placeholder": "🏠 Link...", "btn_gen": "✨ GENERIEREN", "p_destacada": "TOP", "comunidad": "Community", "popular": "BELIEBT", "plan1": "Basis", "plan2": "Pro", "plan3": "Agentur", "desc1": "3 / Tag", "t1_1": "Limit.", "desc2": "Support", "t1_2": "48h.", "desc3": "Wasserzeichen", "t1_3": "Link.", "desc4": "Unbegrenzt", "t2_1": "Keine Limits.", "desc5": "Social", "t2_2": "Posts.", "desc6": "SEO", "t2_3": "Ranking.", "desc7": "Banner", "t2_4": "Home.", "desc8": "5 Benutzer", "t3_1": "5 Mitglieder.", "desc9": "Panel", "t3_2": "Verwalten.", "desc10": "API", "t3_3": "CRM.", "desc11": "Priorität", "t3_4": "Häufigkeit.", "btn1": "ANMELDEN", "btn2": "UPGRADE", "btn3": "KONTAKT" }
}

# --- 3. ESTILOS CSS (RESTAURADOS AL MÁXIMO BRILLO Y FLUIDEZ) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }

    /* BOTÓN GENERAR: ANIMACIÓN "REVERSE NEON" */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; border: none !important; 
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4) !important; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important; 
        color: white !important; font-weight: 700 !important; height: 3.5rem !important; width: 100% !important;
    }
    div.stButton > button[kind="primary"]:hover { 
        background: #000000 !important; color: #ffffff !important;
        transform: scale(1.03) translateY(-2px) !important;
        box-shadow: 0 0 50px rgba(0, 210, 255, 1), 0 0 20px rgba(0, 210, 255, 0.6) !important; 
        border: 2px solid #00d2ff !important;
    }

    /* PLANES: ALTURA IGUALADA Y AURA VIBRANTE PERSISTENTE */
    .card-wrapper { transition: all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1); border-radius: 12px; height: 460px; }
    .card-wrapper:hover { transform: translateY(-15px); }

    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; height: 100%; }
    
    .free-card { box-shadow: 0 0 25px rgba(255, 255, 255, 0.05); }
    
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.4) !important; box-shadow: 0 0 35px rgba(0, 210, 255, 0.2); }
    .pro-card:hover { box-shadow: 0 0 60px rgba(0, 210, 255, 0.5); }
    
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.4) !important; box-shadow: 0 0 35px rgba(221, 160, 221, 0.2); }
    .agency-card:hover { box-shadow: 0 0 60px rgba(221, 160, 221, 0.5); }

    /* TOOLTIPS PERSONALIZADOS */
    .info-icon { display: inline-block; width: 16px; height: 16px; border-radius: 50%; text-align: center; font-size: 11px; line-height: 16px; margin-left: 8px; cursor: help; position: relative; font-weight: bold; }
    .info-icon:hover::after {
        content: attr(data-tooltip); position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
        background-color: #1a1c23; color: #fff; padding: 12px 16px; border-radius: 8px; font-size: 12px; width: 230px; z-index: 999;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9); border: 1px solid rgba(255,255,255,0.1); line-height: 1.5; text-align: left; font-weight: normal;
    }
    .i-free { background-color: rgba(255, 255, 255, 0.1); color: #ccc; border: 1px solid rgba(255, 255, 255, 0.3); }
    .i-pro { background-color: rgba(0, 210, 255, 0.15); color: #00d2ff; border: 1px solid rgba(0, 210, 255, 0.5); }
    .i-agency { background-color: rgba(221, 160, 221, 0.15); color: #DDA0DD; border: 1px solid rgba(221, 160, 221, 0.5); }

    .feature-list { text-align: left; margin: 30px auto; display: inline-block; font-size: 1rem; color: #ddd; line-height: 2.4; }
    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 6px 18px; border-radius: 20px; font-weight: 900; font-size: 0.85rem; z-index: 10; box-shadow: 0 0 15px rgba(0, 210, 255, 0.5); }

    /* VIDEO/BANNER FLOAT */
    .video-placeholder {
        border: 1px solid rgba(0, 210, 255, 0.2); border-radius: 12px; height: 230px; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
        margin-bottom: 25px; position: relative; overflow: hidden; background-size: cover; background-position: center;
        animation: float 5s ease-in-out infinite, adCarousel 18s infinite;
    }
    @keyframes adCarousel {
        0%, 30% { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'); }
        33%, 63% { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80'); }
        66%, 100% { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'); }
    }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
</style>
""", unsafe_allow_html=True)

# --- 4. INTERFAZ ---
if "idioma" not in st.session_state: st.session_state.idioma = "Español"
col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo: st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
with col_lang:
    idioma_selec = st.selectbox("", list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma), label_visibility="collapsed")
    st.session_state.idioma = idioma_selec

L = traducciones[st.session_state.idioma]
st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)

# --- 5. SECCIÓN CENTRAL ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(f'<div class="video-placeholder"><div style="position: absolute; top: 15px; left: 15px; background: rgba(0, 210, 255, 1); color: black; padding: 5px 14px; border-radius: 4px; font-size: 0.75rem; font-weight: 900; box-shadow: 0 0 10px rgba(0,210,255,0.5);">{L["p_destacada"]}</div><div style="background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, transparent 100%); width: 100%; padding: 20px; text-align: center;">{L["comunidad"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-container" style="height:auto; box-shadow: 0 0 30px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
    st.text_area("", placeholder=L['placeholder'], label_visibility="collapsed")
    st.button(L['btn_gen'], type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. PLANES (SIMETRÍA Y BRILLO) ---
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    desc_f = f"<div class='feature-list'>{L['desc1']}<span class='info-icon i-free' data-tooltip='{L['t1_1']}'>i</span><br>{L['desc2']}<span class='info-icon i-free' data-tooltip='{L['t1_2']}'>i</span><br>{L['desc3']}<span class='info-icon i-free' data-tooltip='{L['t1_3']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container free-card'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'>{desc_f}</div></div>", unsafe_allow_html=True)
    st.button(L['btn1'], key="btn_f")

with col2:
    desc_p = f"<div class='feature-list'><b>{L['desc4']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_1']}'>i</span><br>{L['desc5']}<span class='info-icon i-pro' data-tooltip='{L['t2_2']}'>i</span><br>{L['desc6']}<span class='info-icon i-pro' data-tooltip='{L['t2_3']}'>i</span><br><b>{L['desc7']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container pro-card'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'>{desc_p}</div></div>", unsafe_allow_html=True)
    st.button(L['btn2'], key="btn_p")

with col3:
    desc_a = f"<div class='feature-list'>{L['desc8']}<span class='info-icon i-agency' data-tooltip='{L['t3_1']}'>i</span><br>{L['desc9']}<span class='info-icon i-agency' data-tooltip='{L['t3_2']}'>i</span><br>{L['desc10']}<span class='info-icon i-agency' data-tooltip='{L['t3_3']}'>i</span><br><b>{L['desc11']}</b><span class='info-icon i-agency' data-tooltip='{L['t3_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container agency-card'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'>{desc_a}</div></div>", unsafe_allow_html=True)
    st.button(L['btn3'], key="btn_a")
    
