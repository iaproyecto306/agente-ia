import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. CONFIGURACIÓN DE IA SEGURA ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.warning("⚠️ Configuración pendiente: Por favor, añade la API Key en los Secrets de Streamlit.")
    st.stop()

# --- CONEXIÓN A BASE DE DATOS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def obtener_datos_db():
    try:
        # Leemos la hoja. Si es la primera vez, el try fallará y creará el DF vacío
        return conn.read(worksheet="Sheet1", ttl=0)
    except:
        return pd.DataFrame(columns=['email', 'usos', 'plan'])

def actualizar_usos_db(email, nuevos_usos, plan_actual):
    df = obtener_datos_db()
    
    # Aseguramos que exista la columna 'plan' si la hoja es vieja
    if 'plan' not in df.columns:
        df['plan'] = 'Gratis'

    if email in df['email'].values:
        df.loc[df['email'] == email, 'usos'] = nuevos_usos
        # No sobrescribimos el plan a menos que cambie, mantenemos el que tiene
        if pd.isna(df.loc[df['email'] == email, 'plan']).any():
             df.loc[df['email'] == email, 'plan'] = plan_actual
    else:
        nueva_fila = pd.DataFrame({"email": [email], "usos": [nuevos_usos], "plan": [plan_actual]})
        df = pd.concat([df, nueva_fila], ignore_index=True)
    
    conn.update(worksheet="Sheet1", data=df)

def generar_texto(prompt, modelo="gpt-4o"):
    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un experto inmobiliario de lujo y copywriter persuasivo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR_TECNICO: {str(e)}"

# --- 2. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="AI Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VARIABLES DE ESTADO ---
if "usos" not in st.session_state: st.session_state.usos = 0
if "email_usuario" not in st.session_state: st.session_state.email_usuario = ""
if "plan_usuario" not in st.session_state: st.session_state.plan_usuario = "Gratis"

# --- 3. DICCIONARIO MAESTRO ---
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
        "btn1": "REGISTRO GRATIS", "btn2": "MEJORAR AHORA", "btn3": "CONTACTAR VENTAS",
        "how_title": "¿Cómo funciona IA Realty Pro?",
        "step1_t": "Pega el Link", "step1_d": "O escribe una descripción breve.",
        "step2_t": "IA Analiza", "step2_d": "Optimizamos para SEO y ventas.",
        "step3_t": "Publica", "step3_d": "Copia el texto y atrae clientes.",
        "stat1": "Anuncios Optimizados", "stat2": "Tiempo Ahorrado", "stat3": "Más Consultas",
        "test_title": "Lo que dicen los Expertos",
        "test1_txt": "Mis ventas en Instagram subieron un 50% desde que uso la IA para los copies.", "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "Increíble cómo resume las características de los links de portales. Ahorro horas.", "test2_au": "Ana M. (Century 21)",
        "test3_txt": "La mejor inversión para mi agencia este año. El plan Pro vale cada centavo.", "test3_au": "Luis P. (Independiente)",
        "foot_desc": "Herramientas de Inteligencia Artificial para Inmuebles.",
        "foot_links": "Términos de Servicio | Política de Privacidad | Soporte",
        "mail_label": "📧 Ingresa tu Email para comenzar", "limit_msg": "🚫 Límite gratuito alcanzado.", "upgrade_msg": "Pásate a PRO para seguir vendiendo.",
        "lbl_tone": "Tono:", "lbl_lang_out": "Idioma de Salida:"
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
        "btn1": "FREE SIGNUP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES",
        "how_title": "How does AI Realty Pro work?",
        "step1_t": "Paste the Link", "step1_d": "Or write a brief description.",
        "step2_t": "AI Analyzes", "step2_d": "We optimize for SEO and sales.",
        "step3_t": "Publish", "step3_d": "Copy text and attract clients.",
        "stat1": "Optimized Listings", "stat2": "Time Saved", "stat3": "More Inquiries",
        "test_title": "What Experts Say",
        "test1_txt": "My Instagram sales went up 50% since using AI for captions.", "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "Incredible how it summarizes portal links. I save hours.", "test2_au": "Ana M. (Century 21)",
        "test3_txt": "Best investment for my agency this year. Pro plan is worth every penny.", "test3_au": "Luis P. (Independent)",
        "foot_desc": "Artificial Intelligence Tools for Real Estate.",
        "foot_links": "Terms of Service | Privacy Policy | Support",
        "mail_label": "📧 Enter your Email to start", "limit_msg": "🚫 Free limit reached.", "upgrade_msg": "Upgrade to PRO to keep selling.",
        "lbl_tone": "Tone:", "lbl_lang_out": "Output Language:"
    },
    "Português": {
        "title1": "Transforme Anúncios Tediosos em", "title2": "Ímãs de Vendas",
        "sub": "A ferramenta de IA secreta dos agentes de alto desempenho.",
        "placeholder": "🏠 Cole o link do imóvel ou descreva brevemente...",
        "btn_gen": "✨ GERAR DESCRIÇÃO", "p_destacada": "IMÓVEL EM DESTAQUE",
        "comunidad": "Propriedades da Comunidade", "popular": "MAIS POPULAR",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agência",
        "desc1": "3 descrições / día", "t1_1": "Limite diário de gerações para novos usuários.",
        "desc2": "Suporte Básico", "t1_2": "Ajuda técnica por e-mail com resposta em menos de 48 horas.",
        "desc3": "Marca d'Água", "t1_3": "Os textos incluyen uma pequena menção à nossa plataforma.",
        "desc4": "Gerações Ilimitadas", "t2_1": "Crie quantas descrições precisar, sem restrições.",
        "desc5": "Pack Redes Sociais", "t2_2": "Gere automaticamente posts para Instagram, Facebook e TikTok com hashtags.",
        "desc6": "Otimização SEO", "t2_3": "Textos estruturados para aparecer primeiro nos motores de busca.",
        "desc7": "Banner Principal", "t2_4": "Seus imóveis de destaque rodarão em nossa página inicial.",
        "desc8": "5 Usuários / Contas", "t3_1": "Acesso individual para até 5 membros da sua equipe imobiliária.",
        "desc9": "Painel de Equipe", "t3_2": "Supervisione e gerencie as descrições criadas por seus agentes.",
        "desc10": "Acesso via API", "t3_3": "Conecte nossa IA diretamente com seu próprio software ou CRM.",
        "desc11": "Prioridade no Banner", "t3_4": "Seus anúncios aparecerão com o dobro de frequência na home.",
        "btn1": "REGISTRO GRÁTIS", "btn2": "MELHORAR AGORA", "btn3": "CONTATO VENDAS",
        "how_title": "Como funciona o AI Realty Pro?",
        "step1_t": "Cole o Link", "step1_d": "Ou escreva uma breve descrição.",
        "step2_t": "IA Analisa", "step2_d": "Otimizamos para SEO e vendas.",
        "step3_t": "Publique", "step3_d": "Copie o texto e atraia clientes.",
        "stat1": "Anúncios Otimizados", "stat2": "Tempo Economizado", "stat3": "Mais Consultas",
        "test_title": "O que dizem os Especialistas",
        "test1_txt": "Minhas vendas no Instagram subiram 50% desde que uso a IA para legendas.", "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "Incrível como resume os links dos portais. Economizo horas.", "test2_au": "Ana M. (Century 21)",
        "test3_txt": "Melhor investimento para minha agência este ano. O plano Pro vale cada centavo.", "test3_au": "Luis P. (Independente)",
        "foot_desc": "Ferramentas de Inteligencia Artificial para Imóveis.",
        "foot_links": "Termos de Servicio | Política de Privacidade | Suporte",
        "mail_label": "📧 Insira seu e-mail para começar", "limit_msg": "🚫 Limite grátis atingido.", "upgrade_msg": "Atualize para PRO para continuar vendendo.",
        "lbl_tone": "Tom:", "lbl_lang_out": "Idioma de saída:"
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
        "btn1": "免费注册", "btn2": "立即升级", "btn3": "联系销售",
        "how_title": "AI Realty Pro 如何运作？",
        "step1_t": "粘贴链接", "step1_d": "或写简短描述。",
        "step2_t": "AI 分析", "step2_d": "我们针对 SEO 和销售进行优化。",
        "step3_t": "发布", "step3_d": "复制文本并吸引客户。",
        "stat1": "已优化广告", "stat2": "节省时间", "stat3": "更多咨询",
        "test_title": "专家怎么说",
        "test1_txt": "自从使用 AI 撰写文案以来，我的 Instagram 销售额增长了 50%。", "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "令人难以置信的是它如何总结门户网站链接。我节省了几个小时。", "test2_au": "Ana M. (Century 21)",
        "test3_txt": "今年我代理机构的最佳投资。专业版物超所值。", "test3_au": "Luis P. (独立)",
        "foot_desc": "房地产人工智能工具。",
        "foot_links": "服务条款 | 隐私政策 | 支持",
        "mail_label": "📧 输入邮箱开始", "limit_msg": "🚫 已达到免费限制。", "upgrade_msg": "升级到专业版继续销售。",
        "lbl_tone": "语气:", "lbl_lang_out": "输出语言:"
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
        "desc6": "Optimización SEO", "t2_3": "Textos estructurados pour apparaître en premier dans les moteurs de recherche.",
        "desc7": "Bannière Principale", "t2_4": "Vos propriétés à la une tourneront sur notre page d'accueil.",
        "desc8": "5 Utilisateurs / Comptes", "t3_1": "Accès individuel pour jusqu'à 5 membres de votre équipe immobilière.",
        "desc9": "Tableau de Bord Équipe", "t3_2": "Supervisez et gérez les descriptions créées par vos agents.",
        "desc10": "Accès via API", "t3_3": "Connectez notre IA directement à votre propre logiciel ou CRM.",
        "desc11": "Priorité Bannière", "t3_4": "Vos annonces apparaîtront deux fois plus souvent sur la page d'accueil.",
        "btn1": "INSCRIPTION GRATUITE", "btn2": "AMÉLIORER MAINTENANT", "btn3": "CONTACTER VENTES",
        "how_title": "Comment fonctionne AI Realty Pro ?",
        "step1_t": "Collez le lien", "step1_d": "Ou écrivez une brève description.",
        "step2_t": "IA Analyse", "step2_d": "Nous optimisons pour le SEO et la vente.",
        "step3_t": "Publiez", "step3_d": "Copiez le texte et attirez des clients.",
        "stat1": "Annonces Optimisées", "stat2": "Temps Gagné", "stat3": "Plus de Demandes",
        "test_title": "Ce que disent les Experts",
        "test1_txt": "Mes ventes sur Instagram ont augmenté de 50% depuis que j'utilise l'IA.", "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "Incroyable comment il résume les liens des portails. Je gagne des heures.", "test2_au": "Ana M. (Century 21)",
        "test3_txt": "Le meilleur investissement pour mon agence cette année. Le plan Pro vaut chaque centime.", "test3_au": "Luis P. (Indépendant)",
        "foot_desc": "Outils d'Intelligence Artificielle pour l'Immobilier.",
        "foot_links": "Conditions d'Utilisation | Politique de Confidentialité | Support",
        "mail_label": "📧 Entrez votre email pour commencer", "limit_msg": "🚫 Limite gratuite atteinte.", "upgrade_msg": "Passez à PRO pour continuer à vendre.",
        "lbl_tone": "Ton:", "lbl_lang_out": "Langue de sortie:"
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
        "btn1": "GRATIS REGISTRIEREN", "btn2": "JETZT UPGRADEN", "btn3": "VERTRIEB KONTAKTIEREN",
        "how_title": "Wie funktioniert AI Realty Pro?",
        "step1_t": "Link einfügen", "step1_d": "Oder kurze Beschreibung schreiben.",
        "step2_t": "KI Analysiert", "step2_d": "Wir optimieren für SEO und Verkauf.",
        "step3_t": "Veröffentlichen", "step3_d": "Text kopieren und Kunden gewinnen.",
        "stat1": "Optimierte Anzeigen", "stat2": "Zeit Gespart", "stat3": "More Inquiries",
        "test_title": "Was Experten sagen",
        "test1_txt": "Meine Instagram-Verkäufe stiegen um 50%, seit ich KI für Captions nutze.", "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "Unglaublich, wie es Portal-Links zusammenfasst. Ich spare Stunden.", "test2_au": "Ana M. (Century 21)",
        "test3_txt": "Die beste Investition für meine Agentur dieses Jahr. Pro-Plan ist jeden Cent wert.", "test3_au": "Luis P. (Unabhängig)",
        "foot_desc": "Künstliche Intelligenz Tools für Immobilien.",
        "foot_links": "Nutzungsbedingungen | Datenschutzrichtlinie | Support",
        "mail_label": "📧 E-Mail eingeben, um zu starten", "limit_msg": "🚫 Gratis-Limit erreicht.", "upgrade_msg": "Upgrade auf PRO, um weiter zu verkaufen.",
        "lbl_tone": "Ton:", "lbl_lang_out": "Ausgabesprache:"
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
    .card-wrapper { transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.6s cubic-bezier(0.165, 0.84, 0.44, 1); border-radius: 12px; height: 520px; margin-bottom: 20px;}
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

    .video-placeholder {
        border-radius: 12px; height: 230px; display: flex; flex-direction: column; align-items: center; justify-content: flex-end;
        margin-bottom: 25px; position: relative; overflow: hidden; background-size: cover; background-position: center;
        transition: all 0.8s ease-in-out; animation: float 5s ease-in-out infinite, adCarousel 24s infinite alternate, auraChange 24s infinite alternate;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .dynamic-tag { position: absolute; top: 15px; left: 15px; color: black; padding: 5px 14px; border-radius: 4px; font-size: 0.75rem; font-weight: 900; transition: background-color 0.8s ease; animation: tagColorChange 24s infinite alternate; }

    @keyframes auraChange { 0%, 70% { box-shadow: 0 0 45px rgba(0, 210, 255, 0.5); border-color: rgba(0, 210, 255, 0.4); } 75%, 100% { box-shadow: 0 0 45px rgba(221, 160, 221, 0.5); border-color: rgba(221, 160, 221, 0.4); } }
    @keyframes tagColorChange { 0%, 70% { background: rgba(0, 210, 255, 1); } 75%, 100% { background: rgba(221, 160, 221, 1); } }
    @keyframes adCarousel { 
        0%, 20% { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'); opacity: 1; }
        30%, 45% { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80'); opacity: 1; }
        55%, 70% { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'); opacity: 1; }
        80%, 100% { background-image: url('https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=800&q=80'); opacity: 1; }
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

# --- 6. SECCIÓN CENTRAL (BLOQUEO DE USOS Y CAPTURA) ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(f'''
        <div class="video-placeholder">
            <div class="dynamic-tag">{L["p_destacada"]}</div>
            <div class="carousel-label">{L["comunidad"]}</div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="glass-container" style="height:auto; box-shadow: 0 0 30px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
    
    # --- PASO 1: LOGIN ---
    if not st.session_state.email_usuario:
        email_input = st.text_input(L["mail_label"], placeholder="email@ejemplo.com", key="user_email")
        if st.button("COMENZAR GRATIS / START FREE", type="primary"):
            if email_input and "@" in email_input:
                df_actual = obtener_datos_db()
                if email_input in df_actual['email'].values:
                    # Usuario existente: cargamos datos
                    usuario = df_actual[df_actual['email'] == email_input].iloc[0]
                    st.session_state.usos = int(usuario['usos'])
                    st.session_state.plan_usuario = usuario['plan'] if 'plan' in usuario else 'Gratis'
                else:
                    # Usuario nuevo
                    st.session_state.usos = 0
                    st.session_state.plan_usuario = "Gratis"
                st.session_state.email_usuario = email_input
                st.rerun()
            else:
                st.error("Por favor ingresa un email válido.")
    
    # --- PASO 2: LOGICA DE GENERACIÓN ---
    elif st.session_state.email_usuario:
        
        # DEFINICIÓN DE LÍMITES POR PLAN
        es_pro = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite_usos = 99999 if es_pro else 3 # Generaciones Ilimitadas para Pro/Agencia
        
        if st.session_state.usos < limite_usos:
            # Inputs adicionales para PRO (SEO y Tono)
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                tono = st.selectbox(L.get("lbl_tone", "Tono:"), ["Profesional", "Storytelling", "Urgencia/Venta", "Lujo/Minimalista"])
            with col_t2:
                idioma_salida = st.selectbox(L.get("lbl_lang_out", "Idioma Salida:"), list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma))

            user_input = st.text_area("", placeholder=L['placeholder'], key="input_ia", label_visibility="collapsed")
            
            if st.button(L['btn_gen'], key="main_gen", type="primary"):
                if user_input:
                    with st.spinner("Analizando mercado y redactando..."):
                        # Construcción del Prompt con Optimización SEO (Cumple promesa SEO)
                        prompt_base = f"""
                        Actúa como un experto inmobiliario de lujo.
                        Tarea: Crear descripción de venta inmobiliaria.
                        Idioma de salida: {idioma_salida}.
                        Tono: {tono}.
                        Objetivo: Optimización SEO para portales inmobiliarios.
                        Datos de la propiedad: {user_input}
                        """
                        
                        resultado = generar_texto(prompt_base)
                        
                        if "ERROR_TECNICO" not in resultado:
                            # Sumar uso
                            st.session_state.usos += 1
                            actualizar_usos_db(st.session_state.email_usuario, st.session_state.usos, st.session_state.plan_usuario)
                            
                            # Mostrar Resultado Principal
                            st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #00d2ff; margin-top:20px; text-align:left; color:white;'>{resultado}</div>", unsafe_allow_html=True)
                            
                            # --- PACK REDES SOCIALES (Solo PRO/AGENCIA) ---
                            if es_pro:
                                st.markdown("---")
                                st.markdown("### 📱 Social Media Pack (Pro)")
                                with st.spinner("Generando contenido para redes..."):
                                    prompt_social = f"""
                                    Basado en esta descripción: "{resultado}".
                                    1. Crea un Copy para Instagram con Emojis y 5 Hashtags virales.
                                    2. Crea un guion de 15 segundos para TikTok/Reels.
                                    Separalos claramente.
                                    """
                                    resultado_social = generar_texto(prompt_social)
                                    st.info(resultado_social)
                            
                            if not es_pro:
                                st.info(f"Usos restantes: {3 - st.session_state.usos}")
                        else:
                            st.error("Error de conexión.")
                else:
                    st.warning("Por favor, ingresa los detalles.")
        else:
            # --- PASO 3: BLOQUEO (PAYWALL) ---
            st.error(L["limit_msg"])
            st.markdown(f"#### {L['upgrade_msg']}")
            
           # Botón de PayPal INTELIGENTE (Envía el email del usuario para la automatización)
            paypal_bloqueo = f"""
            <div id="paypal-bloqueo-container"></div>
            <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'pill', color: 'blue', layout: 'horizontal', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{
                      'plan_id': 'P-3P2657040E401734NNFQQ5TY',
                      'custom_id': '{st.session_state.email_usuario}' // <--- ESTO ES LA CLAVE DE LA AUTOMATIZACIÓN
                    }});
                  }}
              }}).render('#paypal-bloqueo-container');
            </script>
            """
            components.html(paypal_bloqueo, height=100)

    st.markdown('</div>', unsafe_allow_html=True)

# --- CÓMO FUNCIONA ---
st.markdown(f"<br><br><h2 style='text-align:center; color:white;'>{L['how_title']}</h2>", unsafe_allow_html=True)
ch1, ch2, ch3 = st.columns(3)
with ch1: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>1</h1><p><b>{L['step1_t']}</b><br>{L['step1_d']}</p></div>", unsafe_allow_html=True)
with ch2: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>2</h1><p><b>{L['step2_t']}</b><br>{L['step2_d']}</p></div>", unsafe_allow_html=True)
with ch3: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>3</h1><p><b>{L['step3_t']}</b><br>{L['step3_d']}</p></div>", unsafe_allow_html=True)

# --- ESTADÍSTICAS ---
st.markdown("<br>", unsafe_allow_html=True)
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1: st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">+10k</h2><p style="color:#aaa; font-size:0.9rem;">{L["stat1"]}</p></div>', unsafe_allow_html=True)
with col_stat2: st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">-80%</h2><p style="color:#aaa; font-size:0.9rem;">{L["stat2"]}</p></div>', unsafe_allow_html=True)
with col_stat3: st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">+45%</h2><p style="color:#aaa; font-size:0.9rem;">{L["stat3"]}</p></div>', unsafe_allow_html=True)

# --- 7. PLANES INTEGRADOS CON PAYPAL (AUTOMATIZADOS) ---
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

# PLAN GRATIS
with col1:
    desc_f = f"<div class='feature-list'>{L['desc1']}<span class='info-icon i-free' data-tooltip='{L['t1_1']}'>i</span><br>{L['desc2']}<span class='info-icon i-free' data-tooltip='{L['t1_2']}'>i</span><br>{L['desc3']}<span class='info-icon i-free' data-tooltip='{L['t1_3']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper free-card'><div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'>{desc_f}</div></div>", unsafe_allow_html=True)
    st.button(L['btn1'], key="btn_f")

# PLAN PRO ($49) - Con rastreo de email
with col2:
    desc_p = f"<div class='feature-list'><b>{L['desc4']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_1']}'>i</span><br>{L['desc5']}<span class='info-icon i-pro' data-tooltip='{L['t2_2']}'>i</span><br>{L['desc6']}<span class='info-icon i-pro' data-tooltip='{L['t2_3']}'>i</span><br><b>{L['desc7']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'>{desc_p}</div></div>", unsafe_allow_html=True)
    
    # Botón Pro con custom_id
    paypal_html_49 = f"""
    <div id="paypal-button-container-P-3P2657040E401734NNFQQ5TY"></div>
    <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
    <script>
      paypal.Buttons({{
          style: {{ shape: 'pill', color: 'blue', layout: 'vertical', label: 'subscribe' }},
          createSubscription: function(data, actions) {{
            return actions.subscription.create({{
              'plan_id': 'P-3P2657040E401734NNFQQ5TY',
              'custom_id': '{st.session_state.email_usuario}'
            }});
          }}
      }}).render('#paypal-button-container-P-3P2657040E401734NNFQQ5TY');
    </script>
    """
    components.html(paypal_html_49, height=150)

# PLAN AGENCIA ($199) - Con rastreo de email
with col3:
    desc_a = f"<div class='feature-list'>{L['desc8']}<span class='info-icon i-agency' data-tooltip='{L['t3_1']}'>i</span><br>{L['desc9']}<span class='info-icon i-agency' data-tooltip='{L['t3_2']}'>i</span><br>{L['desc10']}<span class='info-icon i-agency' data-tooltip='{L['t3_3']}'>i</span><br><b>{L['desc11']}</b><span class='info-icon i-agency' data-tooltip='{L['t3_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>$199</h1><hr style='border-color:#DDA0DD;opacity:0.3;'>{desc_a}</div></div>", unsafe_allow_html=True)
    
    # Botón Agencia con custom_id
    paypal_html_199 = f"""
    <div id="paypal-button-container-P-0S451470G5041550ENFQRB4I"></div>
    <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
    <script>
      paypal.Buttons({{
          style: {{ shape: 'pill', color: 'blue', layout: 'vertical', label: 'subscribe' }},
          createSubscription: function(data, actions) {{
            return actions.subscription.create({{
              'plan_id': 'P-0S451470G5041550ENFQRB4I',
              'custom_id': '{st.session_state.email_usuario}'
            }});
          }}
      }}).render('#paypal-button-container-P-0S451470G5041550ENFQRB4I');
    </script>
    """
    components.html(paypal_html_199, height=150)

# --- TESTIMONIOS Y FOOTER ---
st.markdown(f"<br><br><h2 style='text-align:center; color:white;'>{L['test_title']}</h2>", unsafe_allow_html=True)
ct1, ct2, ct3 = st.columns(3)
testimonio_style = '<div style="padding:20px; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); height:180px;"><p style="font-style:italic; color:#ddd; font-size:0.9rem;">"{texto}"</p><p style="color:#00d2ff; font-weight:bold; margin-top:15px;">- {autor}</p></div>'
with ct1: st.markdown(testimonio_style.format(texto=L['test1_txt'], autor=L['test1_au']), unsafe_allow_html=True)
with ct2: st.markdown(testimonio_style.format(texto=L['test2_txt'], autor=L['test2_au']), unsafe_allow_html=True)
with ct3: st.markdown(testimonio_style.format(texto=L['test3_txt'], autor=L['test3_au']), unsafe_allow_html=True)

st.markdown(f'<div style="border-top: 1px solid rgba(255,255,255,0.1); padding: 40px 0px; text-align: center;"><div style="font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom:10px;">🏢 AI REALTY PRO</div><p style="color:#666; font-size:0.8rem;">© 2026 IA Realty Pro - {L["foot_desc"]}<br>{L["foot_links"]}</p></div>', unsafe_allow_html=True)
