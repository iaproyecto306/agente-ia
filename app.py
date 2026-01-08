import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE IA ---
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
    page_title="AI Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. DICCIONARIO MAESTRO (Traducciones Completas de todos los bloques) ---
traducciones = {
    "Español": {
        "title1": "Convierte Anuncios Aburridos en", "title2": "Imanes de Ventas",
        "sub": "La herramienta de IA secreta de los agentes top productores.",
        "placeholder": "🏠 Pega el link de la propiedad o describe brevemente...",
        "btn_gen": "✨ GENERAR DESCRIPCIÓN", "p_destacada": "PROPIEDAD DESTACADA",
        "comunidad": "Propiedades de la Comunidad", "popular": "MÁS POPULAR",
        "como_funciona": "¿Cómo funciona AI Realty Pro?",
        "step1_t": "Pega el Link", "step1_d": "O escribe una descripción breve.",
        "step2_t": "IA Analiza", "step2_d": "Optimizamos para SEO y ventas.",
        "step3_t": "Publica", "step3_d": "Copia el texto y atrae clientes.",
        "stat1_t": "Anuncios Optimizados", "stat2_t": "Tiempo Ahorrado", "stat3_t": "Más Consultas",
        "test_title": "Lo que dicen los Expertos",
        "test1_txt": "Mis ventas en Instagram subieron un 50% desde que uso la IA para los copies.", "test1_aut": "Carlos R. (RE/MAX)",
        "test2_txt": "Increíble cómo resume las características de los links de portales. Ahorro horas.", "test2_aut": "Ana M. (Century 21)",
        "test3_txt": "La mejor inversión para mi agencia este año. El plan Pro vale cada centavo.", "test3_aut": "Luis P. (Independiente)",
        "footer_txt": "Herramientas de Inteligencia Artificial para Inmuebles.",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agencia",
        "desc1": "3 descripciones / día", "t1_1": "Límite diario para nuevos usuarios.",
        "desc2": "Soporte Básico", "t1_2": "Ayuda técnica vía email.",
        "desc3": "Marca de Agua", "t1_3": "Los textos incluyen mención a la plataforma.",
        "desc4": "Generaciones Ilimitadas", "t2_1": "Crea descripciones sin restricciones.",
        "desc5": "Pack Redes Sociales", "t2_2": "Posts para Instagram, Facebook y TikTok.",
        "desc6": "Optimización SEO", "t2_3": "Textos diseñados para buscadores.",
        "desc7": "Banner Principal", "t2_4": "Rotación en nuestra página de inicio.",
        "desc8": "5 Usuarios / Cuentas", "t3_1": "Acceso para hasta 5 miembros.",
        "desc9": "Panel de Equipo", "t3_2": "Gestiona las creaciones de tus agentes.",
        "desc10": "Acceso vía API", "t3_3": "Conecta con tu propio CRM.",
        "desc11": "Prioridad en Banner", "t3_4": "Doble de frecuencia en la home.",
        "btn1": "REGISTRO GRATIS", "btn2": "MEJORAR AHORA", "btn3": "CONTACTAR VENTAS"
    },
    "English": {
        "title1": "Turn Boring Listings into", "title2": "Sales Magnets",
        "sub": "The secret AI tool used by top producing agents.",
        "placeholder": "🏠 Paste the property link or describe briefly...",
        "btn_gen": "✨ GENERATE DESCRIPTION", "p_destacada": "FEATURED PROPERTY",
        "comunidad": "Community Properties", "popular": "MOST POPULAR",
        "como_funciona": "How does AI Realty Pro work?",
        "step1_t": "Paste the Link", "step1_d": "Or write a brief description.",
        "step2_t": "AI Analyzes", "step2_d": "We optimize for SEO and sales.",
        "step3_t": "Publish", "step3_d": "Copy the text and attract leads.",
        "stat1_t": "Optimized Ads", "stat2_t": "Time Saved", "stat3_t": "More Inquiries",
        "test_title": "What Experts Say",
        "test1_txt": "My Instagram sales jumped 50% since I started using AI for my copy.", "test1_aut": "Charles R. (RE/MAX)",
        "test2_txt": "Incredible how it summarizes portal links. Saves me hours.", "test2_aut": "Ann M. (Century 21)",
        "test3_txt": "The best investment for my agency this year. Pro plan is worth every penny.", "test3_aut": "Louis P. (Independent)",
        "footer_txt": "Artificial Intelligence Tools for Real Estate.",
        "plan1": "Starter", "plan2": "Pro Agent", "plan3": "Agency",
        "desc1": "3 descriptions / day", "t1_1": "Daily limit for new users.",
        "desc2": "Basic Support", "t1_2": "Technical help via email.",
        "desc3": "Watermark", "t1_3": "Texts include a small platform mention.",
        "desc4": "Unlimited Generations", "t2_1": "Create descriptions without restrictions.",
        "desc5": "Social Media Pack", "t2_2": "Posts for Instagram, Facebook, and TikTok.",
        "desc6": "SEO Optimization", "t2_3": "Texts built for search engines.",
        "desc7": "Main Banner", "t2_4": "Rotation on our homepage.",
        "desc8": "5 Users / Accounts", "t3_1": "Access for up to 5 team members.",
        "desc9": "Team Dashboard", "t3_2": "Manage descriptions created by agents.",
        "desc10": "API Access", "t3_3": "Connect with your own CRM.",
        "desc11": "Banner Priority", "t3_4": "Twice the frequency on home screen.",
        "btn1": "FREE SIGNUP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES"
    },
    "Português": {
        "title1": "Transforme Anúncios Tediosos em", "title2": "Ímãs de Vendas",
        "sub": "A ferramenta de IA secreta dos agentes de alto desempenho.",
        "placeholder": "🏠 Cole o link do imóvel ou descreva brevemente...",
        "btn_gen": "✨ GERAR DESCRIÇÃO", "p_destacada": "IMÓVEL EM DESTAQUE",
        "comunidad": "Propriedades da Comunidade", "popular": "MAIS POPULAR",
        "como_funciona": "Como funciona o AI Realty Pro?",
        "step1_t": "Cole o Link", "step1_d": "Ou escreva uma breve descrição.",
        "step2_t": "IA Analisa", "step2_d": "Otimizamos para SEO e vendas.",
        "step3_t": "Publicar", "step3_d": "Copie o texto e atraia clientes.",
        "stat1_t": "Anúncios Otimizados", "stat2_t": "Tempo Economizado", "stat3_t": "Mais Consultas",
        "test_title": "O que dizem os especialistas",
        "test1_txt": "Minhas vendas no Instagram subiram 50% desde que uso IA para os copies.", "test1_aut": "Carlos R. (RE/MAX)",
        "test2_txt": "Incrível como resume os links dos portais. Economizo horas.", "test2_aut": "Ana M. (Century 21)",
        "test3_txt": "Melhor investimento para minha agência este ano. O plano Pro vale cada centavo.", "test3_aut": "Luis P. (Independente)",
        "footer_txt": "Ferramentas de Inteligência Artificial para Imóveis.",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agência",
        "desc1": "3 descrições / dia", "t1_1": "Limite diário para novos usuários.",
        "desc2": "Suporte Básico", "t1_2": "Ajuda técnica por e-mail.",
        "desc3": "Marca d'Água", "t1_3": "Os textos incluem menção à plataforma.",
        "desc4": "Gerações Ilimitadas", "t2_1": "Crie descrições sem restrições.",
        "desc5": "Pack Redes Sociais", "t2_2": "Posts para Instagram, Facebook e TikTok.",
        "desc6": "Optimización SEO", "t2_3": "Textos estruturados para busca.",
        "desc7": "Banner Principal", "t2_4": "Rotação na nossa página inicial.",
        "desc8": "5 Usuários / Contas", "t3_1": "Acesso para até 5 membros.",
        "desc9": "Painel de Equipe", "t3_2": "Gerencie as criações dos seus agentes.",
        "desc10": "Acesso via API", "t3_3": "Conecte com seu próprio CRM.",
        "desc11": "Prioridade no Banner", "t3_4": "Dobro de frequência na home.",
        "btn1": "REGISTRO GRÁTIS", "btn2": "MELHORAR AGORA", "btn3": "CONTATO VENDAS"
    },
    "中文": {
        "title1": "将枯燥的广告转化为", "title2": "销售磁铁",
        "sub": "顶级房产经纪人的秘密 AI 工具。",
        "placeholder": "🏠 粘贴房产链接或简要描述...",
        "btn_gen": "✨ 生成描述", "p_destacada": "精选房产",
        "comunidad": "社区房产", "popular": "最受欢迎",
        "como_funciona": "AI Realty Pro 如何运作？",
        "step1_t": "粘贴链接", "step1_d": "或编写简短描述。",
        "step2_t": "AI 分析", "step2_d": "我们针对 SEO 和销售进行优化。",
        "step3_t": "发布", "step3_d": "复制文本并吸引潜在客户。",
        "stat1_t": "优化广告", "stat2_t": "节省时间", "stat3_t": "更多咨询",
        "test_title": "专家评价",
        "test1_txt": "自从使用 AI 撰写文案以来，我的 Instagram 销量增长了 50%。", "test1_aut": "Carlos R. (RE/MAX)",
        "test2_txt": "它总结门户网站链接的方式令人难以置信。节省了数小时。", "test2_aut": "Ana M. (Century 21)",
        "test3_txt": "今年对我机构最好的投资。专业计划物有所值。", "test3_aut": "Luis P. (Independente)",
        "footer_txt": "房地产人工智能工具。",
        "plan1": "基础版", "plan2": "专业经纪人", "plan3": "机构版",
        "desc1": "每天 3 条描述", "t1_1": "新用户的每日限制。",
        "desc2": "基础支持", "t1_2": "通过电子邮件提供帮助。",
        "desc3": "水印", "t1_3": "生成的文本包含平台提及。",
        "desc4": "无限生成", "t2_1": "不受限制地创建描述。",
        "desc5": "社交媒体包", "t2_2": "社交媒体自动帖子。",
        "desc6": "SEO 优化", "t2_3": "专为搜索引擎构建的文本。",
        "desc7": "主页横幅", "t2_4": "您的房产在主页轮播。",
        "desc8": "5 个用户", "t3_1": "最多 5 名成员访问。",
        "desc9": "团队面板", "t3_2": "管理经纪人创建的描述。",
        "desc10": "API 访问", "t3_3": "与您的 CRM 连接。",
        "desc11": "横幅优先级", "t3_4": "在主页出现的频率翻倍。",
        "btn1": "免费注册", "btn2": "立即升级", "btn3": "联系销售"
    },
    "Français": {
        "title1": "Transformez vos Annonces en", "title2": "Aimants à Ventes",
        "sub": "L'outil de IA secret des agents immobiliers les plus performants.",
        "placeholder": "🏠 Collez le lien de la propriété...",
        "btn_gen": "✨ GÉNÉRER LA DESCRIPTION", "p_destacada": "PROPRIÉTÉ À LA UNE",
        "comunidad": "Propriétés de la Communauté", "popular": "PLUS POPULAIRE",
        "como_funciona": "Comment fonctionne AI Realty Pro ?",
        "step1_t": "Collez le lien", "step1_d": "Ou décrivez brièvement.",
        "step2_t": "IA Analyse", "step2_d": "Optimisé pour le SEO et les ventes.",
        "step3_t": "Publiez", "step3_d": "Copiez le texte et attirez des clients.",
        "stat1_t": "Annonces Optimisées", "stat2_t": "Temps Gagné", "stat3_t": "Plus de Consultations",
        "test_title": "L'avis des experts",
        "test1_txt": "Mes ventes sur Instagram ont augmenté de 50% grâce à l'IA.", "test1_aut": "Carlos R. (RE/MAX)",
        "test2_txt": "Incroyable gain de temps sur les descriptions. Un must.", "test2_aut": "Ana M. (Century 21)",
        "test3_txt": "Meilleur investissement de l'année. Le plan Pro vaut le coup.", "test3_aut": "Luis P. (Independiente)",
        "footer_txt": "Outils d'Intelligence Artificielle pour l'immobilier.",
        "plan1": "Initial", "plan2": "Agent Pro", "plan3": "Agence",
        "desc1": "3 descriptions / jour", "t1_1": "Limite quotidienne.",
        "desc2": "Support de Base", "t1_2": "Aide par e-mail.",
        "desc3": "Filigrane", "t1_3": "Les textes incluent notre plateforme.",
        "desc4": "Générations Illimitées", "t2_1": "Sans restrictions.",
        "desc5": "Pack Réseaux Sociaux", "t2_2": "Posts Instagram, Facebook et TikTok.",
        "desc6": "Optimisation SEO", "t2_3": "Textes structurés pour les moteurs.",
        "desc7": "Bannière Principale", "t2_4": "Rotation en page d'accueil.",
        "desc8": "5 Utilisateurs", "t3_1": "Accès pour 5 membres.",
        "desc9": "Tableau de Bord", "t3_2": "Gérez les créations des agents.",
        "desc10": "Accès via API", "t3_3": "Connexion CRM directe.",
        "desc11": "Priorité Bannière", "t3_4": "Fréquence doublée sur la home.",
        "btn1": "INSCRIPTION GRATUITE", "btn2": "AMÉLIORER MAINTENANT", "btn3": "CONTACTER VENTES"
    },
    "Deutsch": {
        "title1": "Verwandeln Sie Anzeigen in", "title2": "Verkaufsmagnete",
        "sub": "Das geheime AI-Tool der Top-Immobilienmakler.",
        "placeholder": "🏠 Link einfügen oder kurz beschreiben...",
        "btn_gen": "✨ BESCHREIBUNG GENERIEREN", "p_destacada": "TOP-IMMOBILIE",
        "comunidad": "Community-Immobilien", "popular": "AM BELIEBTESTEN",
        "como_funciona": "Wie funktioniert AI Realty Pro?",
        "step1_t": "Link einfügen", "step1_d": "Oder kurze Beschreibung.",
        "step2_t": "AI Analyse", "step2_d": "Optimiert für SEO und Verkauf.",
        "step3_t": "Veröffentlichen", "step3_d": "Text kopieren und Kunden gewinnen.",
        "stat1_t": "Optimierte Anzeigen", "stat2_t": "Zeitersparnis", "stat3_t": "Mehr Anfragen",
        "test_title": "Expertenmeinungen",
        "test1_txt": "Meine Instagram-Verkäufe sind um 50% gestiegen dank AI.", "test1_aut": "Carlos R. (RE/MAX)",
        "test2_txt": "Unglaubliche Zeitersparnis bei Portal-Links.", "test2_aut": "Ana M. (Century 21)",
        "test3_txt": "Beste Investition des Jahres. Pro-Plan ist jeden Cent wert.", "test3_aut": "Luis P. (Independiente)",
        "footer_txt": "Künstliche Intelligenz Tools für Immobilien.",
        "plan1": "Basis", "plan2": "Pro Makler", "plan3": "Agentur",
        "desc1": "3 Beschreibungen / Tag", "t1_1": "Tägliches Limit.",
        "desc2": "Basis-Support", "t1_2": "E-Mail Hilfe.",
        "desc3": "Wasserzeichen", "t1_3": "Texte mit Plattform-Hinweis.",
        "desc4": "Unbegrenzte Generierung", "t2_1": "Keine Einschränkungen.",
        "desc5": "Social Media Paket", "t2_2": "Instagram, Facebook & TikTok Posts.",
        "desc6": "SEO-Optimierung", "t2_3": "Strukturierte Texte.",
        "desc7": "Haupt-Banner", "t2_4": "Rotation auf der Startseite.",
        "desc8": "5 Benutzer", "t3_1": "Zugriff für 5 Mitglieder.",
        "desc9": "Team-Panel", "t3_2": "Agenten-Texte verwalten.",
        "desc10": "API-Zugang", "t3_3": "CRM-Verbindung.",
        "desc11": "Banner-Priorität", "t3_4": "Doppelte Home-Frequenz.",
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
    .card-wrapper { transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.6s cubic-bezier(0.165, 0.84, 0.44, 1); border-radius: 12px; height: 480px; }
    .card-wrapper:hover { transform: translateY(-15px); }
    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; height: 100%; }
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
    .video-placeholder { border-radius: 12px; height: 230px; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; margin-bottom: 25px; position: relative; overflow: hidden; background-size: cover; background-position: center; transition: all 0.8s ease-in-out; animation: float 5s ease-in-out infinite, adCarousel 24s infinite alternate, auraChange 24s infinite alternate; border: 1px solid rgba(255,255,255,0.1); }
    @keyframes adCarousel {
        0%, 20% { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'); }
        30%, 45% { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80'); }
        55%, 70% { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'); }
        80%, 100% { background-image: url('https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=800&q=80'); }
    }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-12px); } 100% { transform: translateY(0px); } }
</style>
""", unsafe_allow_html=True)

# --- 5. INTERFAZ ---
if "idioma" not in st.session_state: st.session_state.idioma = "Español"
col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo: st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 AI REALTY PRO</div>', unsafe_allow_html=True)
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
            <div style="position: absolute; top: 15px; left: 15px; background: #00d2ff; color: black; padding: 5px 14px; border-radius: 4px; font-size: 0.75rem; font-weight: 900;">{L["p_destacada"]}</div>
            <div style="background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, transparent 100%); width: 100%; padding: 20px; text-align: center; color: white;">{L["comunidad"]}</div>
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
                    st.error("Error técnico. Verifica tu clave de API.")
                else:
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #00d2ff; margin-top:20px; text-align:left; color:white;'>{resultado}</div>", unsafe_allow_html=True)
        else:
            st.warning("Por favor, ingresa los detalles.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- NUEVA SECCIÓN: CÓMO FUNCIONA ---
st.markdown(f"<br><br><h2 style='text-align:center; color:white;'>{L['como_funciona']}</h2>", unsafe_allow_html=True)
sc1, sc2, sc3 = st.columns(3)
with sc1: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>1</h1><p><b>{L['step1_t']}</b><br>{L['step1_d']}</p></div>", unsafe_allow_html=True)
with sc2: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>2</h1><p><b>{L['step2_t']}</b><br>{L['step2_d']}</p></div>", unsafe_allow_html=True)
with sc3: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>3</h1><p><b>{L['step3_t']}</b><br>{L['step3_d']}</p></div>", unsafe_allow_html=True)

# --- ESTADÍSTICAS ---
st.markdown("<br>", unsafe_allow_html=True)
st1, st2, st3 = st.columns(3)
with st1: st.markdown(f"<div style='text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);'><h2 style='color:#00d2ff; margin:0;'>+10k</h2><p style='color:#aaa; font-size:0.9rem;'>{L['stat1_t']}</p></div>", unsafe_allow_html=True)
with st2: st.markdown(f"<div style='text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);'><h2 style='color:#00d2ff; margin:0;'>-80%</h2><p style='color:#aaa; font-size:0.9rem;'>{L['stat2_t']}</p></div>", unsafe_allow_html=True)
with st3: st.markdown(f"<div style='text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);'><h2 style='color:#00d2ff; margin:0;'>+45%</h2><p style='color:#aaa; font-size:0.9rem;'>{L['stat3_t']}</p></div>", unsafe_allow_html=True)

# --- 7. PLANES ---
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='card-wrapper free-card'><div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'><div class='feature-list'>{L['desc1']}<span class='info-icon i-free' data-tooltip='{L['t1_1']}'>i</span><br>{L['desc2']}<span class='info-icon i-free' data-tooltip='{L['t1_2']}'>i</span><br>{L['desc3']}<span class='info-icon i-free' data-tooltip='{L['t1_3']}'>i</span></div></div></div>", unsafe_allow_html=True)
    st.button(L['btn1'], key="btn_f")
with col2:
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'><div class='feature-list'><b>{L['desc4']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_1']}'>i</span><br>{L['desc5']}<span class='info-icon i-pro' data-tooltip='{L['t2_2']}'>i</span><br>{L['desc6']}<span class='info-icon i-pro' data-tooltip='{L['t2_3']}'>i</span><br><b>{L['desc7']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_4']}'>i</span></div></div></div>", unsafe_allow_html=True)
    st.button(L['btn2'], key="btn_p")
with col3:
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'><div class='feature-list'>{L['desc8']}<span class='info-icon i-agency' data-tooltip='{L['t3_1']}'>i</span><br>{L['desc9']}<span class='info-icon i-agency' data-tooltip='{L['t3_2']}'>i</span><br>{L['desc10']}<span class='info-icon i-agency' data-tooltip='{L['t3_3']}'>i</span><br><b>{L['desc11']}</b><span class='info-icon i-agency' data-tooltip='{L['t3_4']}'>i</span></div></div></div>", unsafe_allow_html=True)
    st.button(L['btn3'], key="btn_a")

# --- TESTIMONIOS ---
st.markdown(f"<br><br><h2 style='text-align:center; color:white;'>{L['test_title']}</h2>", unsafe_allow_html=True)
ct1, ct2, ct3 = st.columns(3)
ts = "<div style='padding:20px; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); height:180px;'><p style='font-style:italic; color:#ddd; font-size:0.9rem;'>\"{texto}\"</p><p style='color:#00d2ff; font-weight:bold; margin-top:15px;'>- {autor}</p></div>"
with ct1: st.markdown(ts.format(texto=L['test1_txt'], autor=L['test1_aut']), unsafe_allow_html=True)
with ct2: st.markdown(ts.format(texto=L['test2_txt'], autor=L['test2_aut']), unsafe_allow_html=True)
with ct3: st.markdown(ts.format(texto=L['test3_txt'], autor=L['test3_aut']), unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <br><br><br>
    <div style="border-top: 1px solid rgba(255,255,255,0.1); padding: 40px 0px; text-align: center;">
        <div style="font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom:10px;">🏢 AI REALTY PRO</div>
        <p style="color:#666; font-size:0.8rem;">© 2026 AI Realty Pro - {L['footer_txt']}<br>Términos de Servicio | Política de Privacidad | Soporte</p>
    </div>
""", unsafe_allow_html=True)
