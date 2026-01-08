import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE IA (Corregida para estabilidad) ---
API_KEY = "AIzaSyBuTXGDypKhTM1V1I6k6Qc6tdkNcrOu0dA"

genai.configure(api_key=API_KEY)

def generar_texto(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR_TECNICO: {str(e)}"

# --- 2. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. DICCIONARIO MAESTRO (Traducciones Completas y Corregidas) ---
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
        "sub": "The secret AI tool used by top producing agents.",
        "placeholder": "🏠 Paste the property link or describe briefly...",
        "btn_gen": "✨ GENERATE DESCRIPTION", "p_destacada": "FEATURED PROPERTY",
        "comunidad": "Community Properties", "popular": "MOST POPULAR",
        "plan1": "Starter", "plan2": "Pro Agent", "plan3": "Agency",
        "desc1": "3 descriptions / day", "t1_1": "Daily generation limit for new users.",
        "desc2": "Basic Support", "t1_2": "Technical help via email with response in less than 48 hours.",
        "desc3": "Watermark", "t1_3": "Generated texts include a small mention of our platform.",
        "desc4": "Unlimited Generations", "t2_1": "Create as many descriptions as you need without any restrictions.",
        "desc5": "Social Media Pack", "t2_2": "Automatically generate posts for Instagram, Facebook, and TikTok with hashtags.",
        "desc6": "SEO Optimization", "t2_3": "Structured texts designed to rank first in search engines.",
        "desc7": "Main Banner", "t2_4": "Your featured properties will rotate on our homepage.",
        "desc8": "5 Users / Accounts", "t3_1": "Individual access for up to 5 members of your real estate team.",
        "desc9": "Team Dashboard", "t3_2": "Monitor and manage the descriptions created by your agents.",
        "desc10": "API Access", "t3_3": "Connect our AI directly with your own software or CRM.",
        "desc11": "Banner Priority", "t3_4": "Your listings will appear twice as often on the home screen.",
        "btn1": "FREE SIGNUP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES"
    },
    "Português": {
        "title1": "Transforme Anúncios Tediosos em", "title2": "Ímãs de Vendas",
        "sub": "A ferramenta de IA secreta dos agentes de alto desempenho.",
        "placeholder": "🏠 Cole o link do imóvel ou descreva brevemente...",
        "btn_gen": "✨ GERAR DESCRIÇÃO", "p_destacada": "IMÓVEL EM DESTAQUE",
        "comunidad": "Propriedades da Comunidade", "popular": "MAIS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agência",
        "desc1": "3 descrições / dia", "t1_1": "Limite diário de gerações para novos usuários.",
        "desc2": "Suporte Básico", "t1_2": "Ajuda técnica por e-mail com resposta em menos de 48 horas.",
        "desc3": "Marca d'Água", "t1_3": "Os textos incluem uma pequena menção à nossa plataforma.",
        "desc4": "Gerações Ilimitadas", "t2_1": "Crie quantas descrições precisar, sem restrições.",
        "desc5": "Pack Redes Sociais", "t2_2": "Gere automaticamente posts para Instagram, Facebook e TikTok com hashtags.",
        "desc6": "Otimização SEO", "t2_3": "Textos estruturados para aparecer primeiro nos motores de busca.",
        "desc7": "Banner Principal", "t2_4": "Seus imóveis de destaque rodarão em nossa página inicial.",
        "desc8": "5 Usuários / Contas", "t3_1": "Acesso individual para até 5 membros da sua equipe imobiliária.",
        "desc9": "Painel de Equipe", "t3_2": "Supervisione e gerencie as descrições criadas por seus agentes.",
        "desc10": "Acesso via API", "t3_3": "Conecte nossa IA diretamente com seu próprio software ou CRM.",
        "desc11": "Prioridade no Banner", "t3_4": "Seus anúncios aparecerão com o dobro de frequência na home.",
        "btn1": "REGISTRO GRÁTIS", "btn2": "MELHORAR AGORA", "btn3": "CONTATO VENDAS"
    },
    "中文": {
        "title1": "将枯燥的广告转化为", "title2": "销售磁铁",
        "sub": "顶级房产经纪人的秘密人工智能工具。",
        "placeholder": "🏠 粘贴房产链接或简要描述...",
        "btn_gen": "✨ 生成描述", "p_destacada": "精选房产",
        "comunidad": "社区房产", "popular": "最受欢迎",
        "plan1": "基础版", "plan2": "专业经纪人", "plan3": "机构版",
        "desc1": "每天 3 条描述", "t1_1": "新用户的每日生成限制。",
        "desc2": "基础支持", "t1_2": "通过电子邮件提供技术帮助，48小时内回复。",
        "desc3": "水印", "t1_3": "生成的文本包含对我们平台的简短提及。",
        "desc4": "无限生成", "t2_1": "根据需要创建任意数量的描述，无任何限制。",
        "desc5": "社交媒体包", "t2_2": "自动为 Instagram、Facebook 和 TikTok 生成带标签的帖子。",
        "desc6": "SEO 优化", "t2_3": "结构化文本，旨在搜索引擎中排名第一。",
        "desc7": "主页横幅", "t2_4": "您的精选房产将在我们的主页上轮播展示。",
        "desc8": "5 个用户/账户", "t3_1": "房产团队中最多 5 名成员的个人访问权限。",
        "desc9": "团队面板", "t3_2": "监控并管理您的经纪人创建的描述。",
        "desc10": "API 访问", "t3_3": "将我们的人工智能直接与您自己的软件或 CRM 连接。",
        "desc11": "横幅优先级", "t3_4": "您的广告在主页上出现的频率将增加一倍。",
        "btn1": "免费注册", "btn2": "立即升级", "btn3": "联系销售"
    },
    "Français": {
        "title1": "Transformez vos Annonces en", "title2": "Aimants à Ventes",
        "sub": "L'outil IA secret des agents immobiliers les plus performants.",
        "placeholder": "🏠 Collez le lien de la propriété ou décrivez brièvement...",
        "btn_gen": "✨ GÉNÉRER LA DESCRIPTION", "p_destacada": "PROPRIÉTÉ À LA UNE",
        "comunidad": "Propriétés de la Communauté", "popular": "PLUS POPULAIRE",
        "plan1": "Initial", "plan2": "Agent Pro", "plan3": "Agence",
        "desc1": "3 descriptions / jour", "t1_1": "Limite quotidienne de générations pour les nouveaux utilisateurs.",
        "desc2": "Support de Base", "t1_2": "Aide technique par e-mail avec réponse en moins de 48 heures.",
        "desc3": "Filigrane", "t1_3": "Les textes incluent une petite mention de notre plateforme.",
        "desc4": "Générations Illimitées", "t2_1": "Créez autant de descriptions que nécessaire sans restrictions.",
        "desc5": "Pack Réseaux Sociaux", "t2_2": "Générez automatiquement des posts pour Instagram, Facebook et TikTok avec hashtags.",
        "desc6": "Optimisation SEO", "t2_3": "Textes structurés pour apparaître en premier dans les moteurs de recherche.",
        "desc7": "Bannière Principale", "t2_4": "Vos propriétés à la une tourneront sur notre page d'accueil.",
        "desc8": "5 Utilisateurs / Comptes", "t3_1": "Accès individuel pour jusqu'à 5 membres de votre équipe immobilière.",
        "desc9": "Tableau de Bord Équipe", "t3_2": "Supervisez et gérez les descriptions créées par vos agents.",
        "desc10": "Accès via API", "t3_3": "Connectez notre IA directement à votre propre logiciel ou CRM.",
        "desc11": "Priorité Bannière", "t3_4": "Vos annonces apparaîtront deux fois plus souvent sur la page d'accueil.",
        "btn1": "INSCRIPTION GRATUITE", "btn2": "AMÉLIORER MAINTENANT", "btn3": "CONTACTER VENTES"
    },
    "Deutsch": {
        "title1": "Verwandeln Sie Anzeigen in", "title2": "Verkaufsmagnete",
        "sub": "Das geheime KI-Tool der Top-Immobilienmakler.",
        "placeholder": "🏠 Link einfügen oder kurz beschreiben...",
        "btn_gen": "✨ BESCHREIBUNG GENERIEREN", "p_destacada": "TOP-IMMOBILIE",
        "comunidad": "Community-Immobilien", "popular": "AM BELIEBTESTEN",
        "plan1": "Basis", "plan2": "Pro Makler", "plan3": "Agentur",
        "desc1": "3 Beschreibungen / Tag", "t1_1": "Tägliches Limit für neue Benutzer.",
        "desc2": "Basis-Support", "t1_2": "Technische Hilfe per E-Mail mit Antwort in weniger als 48 Stunden.",
        "desc3": "Wasserzeichen", "t1_3": "Die Texte enthalten einen kleinen Hinweis auf unsere Plattform.",
        "desc4": "Unbegrenzte Generierungen", "t2_1": "Erstellen Sie so viele Beschreibungen wie nötig ohne Einschränkungen.",
        "desc5": "Social Media Paket", "t2_2": "Erstellen Sie automáticamente Posts für Instagram, Facebook und TikTok mit Hashtags.",
        "desc6": "SEO-Optimierung", "t2_3": "Strukturierte Texte, um in Suchmaschinen ganz oben zu stehen.",
        "desc7": "Haupt-Banner", "t2_4": "Ihre Top-Immobilien rotieren auf unserer Startseite.",
        "desc8": "5 Benutzer / Konten", "t3_1": "Einzelzugriff für bis zu 5 Mitglieder Ihres Immobilienteams.",
        "desc9": "Team-Panel", "t3_2": "Überwachen und verwalten Sie die von Ihren Maklern erstellten Beschreibungen.",
        "desc10": "API-Zugang", "t3_3": "Verbinden Sie unsere KI direkt mit Ihrer eigenen Software oder Ihrem CRM.",
        "desc11": "Banner-Priorität", "t3_4": "Ihre Anzeigen erscheinen doppelt so häufig auf der Startseite.",
        "btn1": "GRATIS REGISTRIEREN", "btn2": "JETZT UPGRADEN", "btn3": "VERTRIEB KONTAKTIEREN"
    }
}

# --- 4. ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }

    /* BOTÓN GENERAR */
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

    /* PLANES */
    .card-wrapper { transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.6s cubic-bezier(0.165, 0.84, 0.44, 1); border-radius: 12px; height: 480px; }
    .card-wrapper:hover { transform: translateY(-15px); }
    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; height: 100%; }
    
    .free-card { box-shadow: 0 0 20px rgba(255, 255, 255, 0.03); }
    .free-card:hover { box-shadow: 0 10px 40px rgba(255, 255, 255, 0.1); }
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.4) !important; box-shadow: 0 0 25px rgba(0, 210, 255, 0.15); }
    .pro-card:hover { box-shadow: 0 15px 60px rgba(0, 210, 255, 0.5); }
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.4) !important; box-shadow: 0 0 25px rgba(221, 160, 221, 0.15); }
    .agency-card:hover { box-shadow: 0 15px 60px rgba(221, 160, 221, 0.5); }

    /* TOOLTIPS */
    .info-icon { display: inline-block; width: 16px; height: 16px; border-radius: 50%; text-align: center; font-size: 11px; line-height: 16px; margin-left: 8px; cursor: help; position: relative; font-weight: bold; }
    .i-free { background-color: rgba(255, 255, 255, 0.1); color: #fff; border: 1px solid rgba(255, 255, 255, 0.3); }
    .i-pro { background-color: rgba(0, 210, 255, 0.15); color: #00d2ff; border: 1px solid rgba(0, 210, 255, 0.5); }
    .i-agency { background-color: rgba(221, 160, 221, 0.15); color: #DDA0DD; border: 1px solid rgba(221, 160, 221, 0.5); }
    
    .info-icon:hover::after {
        content: attr(data-tooltip); position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
        background-color: #1a1c23; color: #fff; padding: 12px 16px; border-radius: 8px; font-size: 12px; width: 230px; z-index: 999;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9); border: 1px solid rgba(255,255,255,0.1); line-height: 1.5; text-align: left; font-weight: normal;
    }

    .feature-list { text-align: left; margin: 25px auto; display: inline-block; font-size: 0.95rem; color: #ddd; line-height: 2.2; }
    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 6px 18px; border-radius: 20px; font-weight: 900; font-size: 0.85rem; z-index: 10; box-shadow: 0 0 15px rgba(0, 210, 255, 0.5); }

   /* VIDEO CARRUSEL (Timing 24s original con colores sincronizados) */
    .video-placeholder {
        border-radius: 12px; 
        height: 230px; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: flex-end;
        margin-bottom: 25px; 
        position: relative; 
        overflow: hidden; 
        background-size: cover; 
        background-position: center;
        transition: all 0.8s ease-in-out;
        animation: float 5s ease-in-out infinite, adCarousel 24s infinite alternate, auraChange 24s infinite alternate;
        border: 1px solid rgba(255,255,255,0.1);
        color: transparent;
        text-indent: -9999px;
    }

    .dynamic-tag {
        position: absolute; top: 15px; left: 15px; 
        color: black; padding: 5px 14px; border-radius: 4px; 
        font-size: 0.75rem; font-weight: 900;
        transition: background-color 0.8s ease;
        animation: tagColorChange 24s infinite alternate;
        text-indent: 0px; color: black;
    }

    .carousel-label {
        background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, transparent 100%); 
        width: 100%; padding: 20px; text-align: center; color: white;
        text-indent: 0px;
    }

  @keyframes auraChange {
        /* Cian: de la imagen 1 a la 3 */
        0%, 69% { box-shadow: 0 0 45px rgba(0, 210, 255, 0.5); border-color: rgba(0, 210, 255, 0.4); } 
        /* Violeta: Justo cuando entra la imagen 4 */
        70%, 95% { box-shadow: 0 0 45px rgba(221, 160, 221, 0.5); border-color: rgba(221, 160, 221, 0.4); } 
    }

    @keyframes tagColorChange {
        /* Cian: de la imagen 1 a la 3 */
        0%, 69% { background: rgba(0, 210, 255, 1); } 
        /* Violeta: Justo cuando entra la imagen 4 */
        70%, 95% { background: rgba(221, 160, 221, 1); } 
    }

    @keyframes adCarousel {
        /* Imagen 1 */
        0%, 20% { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'); opacity: 1; }
        24% { opacity: 0.8; }
        /* Imagen 2 */
        25%, 45% { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80'); opacity: 1; }
        49% { opacity: 0.8; }
        /* Imagen 3 */
        50%, 70% { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'); opacity: 1; }
        74% { opacity: 0.8; }
        /* Imagen 4 - CAMBIO A VIOLETA SIMULTÁNEO (75%) */
        75%, 100% { background-image: url('https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=800&q=80'); opacity: 1; }
    }
    
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-12px); } 100% { transform: translateY(0px); } }
</style>
""", unsafe_allow_html=True)

# --- 5. INTERFAZ ---
if "idioma" not in st.session_state: st.session_state.idioma = "Español"
col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo: st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
with col_lang:
    idioma_selec = st.selectbox("", list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma), label_visibility="collapsed")
    st.session_state.idioma = idioma_selec

L = traducciones[st.session_state.idioma]
st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)

# --- 6. SECCIÓN CENTRAL ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(f'''
        <div class="video-placeholder">
            <div class="dynamic-tag">{L["p_destacada"]}</div>
            <div class="carousel-label">{L["comunidad"]}</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="glass-container" style="height:auto; box-shadow: 0 0 30px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
    user_input = st.text_area("", placeholder=L['placeholder'], key="input_ia", label_visibility="collapsed")
    
    if st.button(L['btn_gen'], key="main_gen", type="primary"):
        if user_input:
            with st.spinner("Generando..."):
                prompt = f"Actúa como un experto inmobiliario de lujo. Crea un anuncio persuasivo en {st.session_state.idioma} basado en la siguiente información: {user_input}. Usa un tono profesional y atractivo."
                resultado = generar_texto(prompt)
                
                if "ERROR_TECNICO" in resultado:
                    st.error("Hubo un problema de conexión. Por favor, verifica tu API Key en la configuración.")
                else:
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #00d2ff; margin-top:20px; text-align:left; color:white;'>{resultado}</div>", unsafe_allow_html=True)
        else:
            st.warning("Por favor, ingresa los detalles de la propiedad.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- NUEVA SECCIÓN: CÓMO FUNCIONA ---
st.markdown("<br><br><h2 style='text-align:center; color:white;'>¿Cómo funciona IA Realty Pro?</h2>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div style='text-align:center;'><h1 style='color:#00d2ff;'>1</h1><p><b>Pega el Link</b><br>O escribe una descripción breve.</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div style='text-align:center;'><h1 style='color:#00d2ff;'>2</h1><p><b>IA Analiza</b><br>Optimizamos para SEO y ventas.</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div style='text-align:center;'><h1 style='color:#00d2ff;'>3</h1><p><b>Publica</b><br>Copia el texto y atrae clientes.</p></div>", unsafe_allow_html=True)

# --- AGREGADO: ESTADÍSTICAS (Impacto) ---
st.markdown("<br>", unsafe_allow_html=True)
col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1:
    st.markdown("""
        <div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);">
            <h2 style="color:#00d2ff; margin:0;">+10k</h2>
            <p style="color:#aaa; font-size:0.9rem;">Anuncios Optimizados</p>
        </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown("""
        <div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);">
            <h2 style="color:#00d2ff; margin:0;">-80%</h2>
            <p style="color:#aaa; font-size:0.9rem;">Tiempo Ahorrado</p>
        </div>
    """, unsafe_allow_html=True)

with col_stat3:
    st.markdown("""
        <div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);">
            <h2 style="color:#00d2ff; margin:0;">+45%</h2>
            <p style="color:#aaa; font-size:0.9rem;">Más Consultas</p>
        </div>
    """, unsafe_allow_html=True)

# --- 7. PLANES ---
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    desc_f = f"<div class='feature-list'>{L['desc1']}<span class='info-icon i-free' data-tooltip='{L['t1_1']}'>i</span><br>{L['desc2']}<span class='info-icon i-free' data-tooltip='{L['t1_2']}'>i</span><br>{L['desc3']}<span class='info-icon i-free' data-tooltip='{L['t1_3']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper free-card'><div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'>{desc_f}</div></div>", unsafe_allow_html=True)
    st.button(L['btn1'], key="btn_f")

with col2:
    desc_p = f"<div class='feature-list'><b>{L['desc4']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_1']}'>i</span><br>{L['desc5']}<span class='info-icon i-pro' data-tooltip='{L['t2_2']}'>i</span><br>{L['desc6']}<span class='info-icon i-pro' data-tooltip='{L['t2_3']}'>i</span><br><b>{L['desc7']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'>{desc_p}</div></div>", unsafe_allow_html=True)
    st.button(L['btn2'], key="btn_p")

with col3:
    desc_a = f"<div class='feature-list'>{L['desc8']}<span class='info-icon i-agency' data-tooltip='{L['t3_1']}'>i</span><br>{L['desc9']}<span class='info-icon i-agency' data-tooltip='{L['t3_2']}'>i</span><br>{L['desc10']}<span class='info-icon i-agency' data-tooltip='{L['t3_3']}'>i</span><br><b>{L['desc11']}</b><span class='info-icon i-agency' data-tooltip='{L['t3_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'>{desc_a}</div></div>", unsafe_allow_html=True)
    st.button(L['btn3'], key="btn_a")

# --- AGREGADO: TESTIMONIOS (Glassmorphism) ---
st.markdown("<br><br><h2 style='text-align:center; color:white;'>Lo que dicen los Expertos</h2>", unsafe_allow_html=True)
ct1, ct2, ct3 = st.columns(3)

testimonio_style = """
    <div style="padding:20px; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); height:180px; transition: 0.3s;">
        <p style="font-style:italic; color:#ddd; font-size:0.9rem;">"{texto}"</p>
        <p style="color:#00d2ff; font-weight:bold; margin-top:15px;">- {autor}</p>
    </div>
"""

with ct1:
    st.markdown(testimonio_style.format(texto="Mis ventas en Instagram subieron un 50% desde que uso la IA para los copies.", autor="Carlos R. (RE/MAX)"), unsafe_allow_html=True)
with ct2:
    st.markdown(testimonio_style.format(texto="Increíble cómo resume las características de los links de portales. Ahorro horas.", autor="Ana M. (Century 21)"), unsafe_allow_html=True)
with ct3:
    st.markdown(testimonio_style.format(texto="La mejor inversión para mi agencia este año. El plan Pro vale cada centavo.", autor="Luis P. (Independiente)"), unsafe_allow_html=True)

# --- AGREGADO: FOOTER ---
st.markdown("""
    <br><br><br>
    <div style="border-top: 1px solid rgba(255,255,255,0.1); padding: 40px 0px; text-align: center;">
        <div style="font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom:10px;">🏢 IA REALTY PRO</div>
        <p style="color:#666; font-size:0.8rem;">
            © 2026 IA Realty Pro - Herramientas de Inteligencia Artificial para Inmuebles.<br>
            Términos de Servicio | Política de Privacidad | Soporte
        </p>
        <div style="margin-top:15px; color:#00d2ff; font-size:1.2rem;">
            🌐 📸 🐦 💼
        </div>
    </div>
""", unsafe_allow_html=True)
