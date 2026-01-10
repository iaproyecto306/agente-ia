import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import io
import time
import urllib.parse

# ==========================================
# 1. MOTOR DE EXTRACCIÓN (SCRAPING)
# ==========================================
def extraer_datos_inmueble(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Limpieza profunda de etiquetas innecesarias
            for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
                element.decompose()
            texto = soup.get_text(separator=' ', strip=True)
            return texto[:3500] 
        else:
            return "Error: No se pudo acceder a la página del inmueble."
    except Exception as e:
        return f"Error crítico al leer el link: {str(e)}"

# ==========================================
# 2. CONFIGURACIÓN DE IA (OPENAI)
# ==========================================
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.warning("⚠️ API Key no detectada en Secrets de Streamlit.")
    st.stop()

# ==========================================
# 3. GESTIÓN DE BASE DE DATOS (GSHEETS)
# ==========================================
conn = st.connection("gsheets", type=GSheetsConnection)

def obtener_datos_db():
    try:
        return conn.read(worksheet="Sheet1", ttl=0)
    except:
        return pd.DataFrame(columns=['email', 'usos', 'plan'])

def obtener_empleados_db():
    try:
        return conn.read(worksheet="Employees", ttl=0)
    except:
        return pd.DataFrame(columns=['BossEmail', 'EmployeeEmail'])

def actualizar_usos_db(email, nuevos_usos, plan_actual):
    df = obtener_datos_db()
    if 'plan' not in df.columns:
        df['plan'] = 'Gratis'
    if email in df['email'].values:
        df.loc[df['email'] == email, 'usos'] = nuevos_usos
        if pd.isna(df.loc[df['email'] == email, 'plan']).any():
             df.loc[df['email'] == email, 'plan'] = plan_actual
    else:
        nueva_fila = pd.DataFrame({"email": [email], "usos": [nuevos_usos], "plan": [plan_actual]})
        df = pd.concat([df, nueva_fila], ignore_index=True)
    conn.update(worksheet="Sheet1", data=df)

def guardar_historial(email, input_user, output_ia):
    try:
        try:
            df_hist = conn.read(worksheet="Historial", ttl=0)
        except:
            df_hist = pd.DataFrame(columns=['fecha', 'email', 'input', 'output'])
        nueva_fila = pd.DataFrame({
            "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")],
            "email": [email],
            "input": [input_user[:500]],
            "output": [output_ia]
        })
        df_final = pd.concat([df_hist, nueva_fila], ignore_index=True)
        conn.update(worksheet="Historial", data=df_final)
    except:
        pass

def generar_texto(prompt, modelo="gpt-4o"):
    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un copywriter inmobiliario de élite especializado en ventas de lujo."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR_IA: {str(e)}" 
# ==========================================
# 4. CONFIGURACIÓN DE PÁGINA Y ESTADOS
# ==========================================
st.set_page_config(
    page_title="AI Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Variables de Estado Persistentes
if "usos" not in st.session_state: st.session_state.usos = 0
if "email_usuario" not in st.session_state: st.session_state.email_usuario = ""
if "plan_usuario" not in st.session_state: st.session_state.plan_usuario = "Gratis"
if "es_empleado" not in st.session_state: st.session_state.es_empleado = False
if "idioma" not in st.session_state: st.session_state.idioma = "Español"
if "last_result" not in st.session_state: st.session_state.last_result = None

# ==========================================
# 5. DICCIONARIO MAESTRO PLATINUM (360°)
# ==========================================
traducciones = {
    "Español": {
        "hi": "Buenos días", "hi_after": "Buenas tardes", "hi_night": "Buenas noches",
        "badge_free": "USUARIO GRATIS", "badge_pro": "MIEMBRO PRO", "badge_agency": "SOCIO AGENCIA",
        "title1": "Convierte Anuncios Aburridos en", "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores.",
        "placeholder": "🏠 Describe la propiedad o escribe instrucciones extra...",
        "url_placeholder": "🔗 Pega aquí el link (InfoCasas, MercadoLibre, Zillow...)",
        "btn_gen": "✨ GENERAR ESTRATEGIA DE VENTA", "btn_refine": "🔄 Ajustar texto generado...",
        "p_destacada": "PROPIEDAD DESTACADA", "comunidad": "Comunidad Real Estate", "popular": "MÁS POPULAR",
        "plan_title": "Selecciona tu Plan", "annual_toggle": "📅 Ahorrar 20% con Pago Anual (Save 20% Yearly)",
        "annual_save": "✅ 2 Meses GRATIS incluidos",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agencia",
        "desc1": "• 3 descripciones / día", "t1_1": "Límite diario de generaciones para nuevos usuarios.",
        "desc2": "• Soporte Básico", "t1_2": "Ayuda técnica vía email con respuesta en menos de 48hs.",
        "desc3": "• Marca de Agua", "t1_3": "Los textos incluyen una pequeña mención a nuestra plataforma.",
        "desc4": "• Generaciones Ilimitadas", "t2_1": "Crea tantas descripciones como necesites sin restricciones.",
        "desc5": "• Pack Redes Sociales", "t2_2": "Genera automáticamente posts para Instagram, Facebook y TikTok con hashtags.",
        "desc6": "• Optimización SEO", "t2_3": "Textos estructurados para aparecer primero en los buscadores.",
        "desc7": "• Banner Principal", "t2_4": "Tus propiedades destacadas rotarán en nuestra página de inicio.",
        "desc8": "• 5 Usuarios / Cuentas", "t3_1": "Acceso individual para hasta 5 miembros de tu equipo inmobiliario.",
        "desc9": "• Panel de Equipo", "t3_2": "Supervisa y gestiona las descripciones creadas por tus agentes.",
        "desc10": "• Acceso vía API (Próximamente)", "t3_3": "Conecta nuestra IA directamente con tu propio software o CRM.",
        "desc11": "• Prioridad en Banner", "t3_4": "Tus anuncios aparecerán con el doble de frecuencia en la home.",
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
        "lbl_tone": "Tono:", "lbl_lang_out": "Idioma de Salida:", "lbl_emoji": "Emojis:",
        "emoji_low": "Pocos", "emoji_med": "Medios", "emoji_high": "Muchos",
        "agency_console": "📊 Panel de Control de Agencia", "manage_team": "👥 Gestionar Equipo", "team_activity": "📈 Actividad del Equipo",
        "revoke": "Revocar Acceso", "copy_success": "¡Copiado!", "whatsapp": "WhatsApp", "download": "Descargar", "char_count": "Caracteres",
        "leg_title": "⚖️ Términos Legales & Privacidad", "leg1": "Uso de IA", "leg1_t": "Contenido generado por IA; el agente debe verificar la precisión legal.",
        "leg2": "Suscripciones", "leg2_t": "Pagos vía PayPal. Cancelación en cualquier momento.", "leg3": "Privacidad", "leg3_t": "No compartimos sus datos con terceros."
    },
    "English": {
        "hi": "Good morning", "hi_after": "Good afternoon", "hi_night": "Good evening",
        "badge_free": "FREE USER", "badge_pro": "PRO MEMBER", "badge_agency": "AGENCY PARTNER",
        "title1": "Turn Boring Listings into", "title2": "Sales Magnets",
        "sub": "The secret AI tool for top producing agents.",
        "placeholder": "🏠 Describe the property or add instructions...",
        "url_placeholder": "🔗 Paste property link (Zillow, InfoCasas, MLS...)",
        "btn_gen": "✨ GENERATE SALES STRATEGY", "btn_refine": "🔄 Refine text...",
        "p_destacada": "FEATURED LISTING", "comunidad": "Real Estate Community", "popular": "MOST POPULAR",
        "plan_title": "Select Your Plan", "annual_toggle": "📅 Save 20% with Yearly Payment",
        "annual_save": "✅ 2 Months FREE included",
        "plan1": "Starter", "plan2": "Pro Agent", "plan3": "Agency",
        "desc1": "• 3 descriptions / day", "t1_1": "Daily limit for new free users.",
        "desc2": "• Basic Support", "t1_2": "Email support with 48h response time.",
        "desc3": "• Watermark", "t1_3": "Texts include a small platform mention.",
        "desc4": "• Unlimited Generations", "t2_1": "Create as many listings as you need.",
        "desc5": "• Social Media Pack", "t2_2": "Auto-generate Instagram, FB, and TikTok posts with hashtags.",
        "desc6": "• SEO Optimization", "t2_3": "Structured copy for better search engine ranking.",
        "desc7": "• Main Banner", "t2_4": "Your listings rotate on our homepage.",
        "desc8": "• 5 Users / Accounts", "t3_1": "Access for up to 5 members of your agency.",
        "desc9": "• Team Dashboard", "t3_2": "Monitor and manage your team's content.",
        "desc10": "• API Access (Coming Soon)", "t3_3": "Connect our AI to your CRM or website.",
        "desc11": "• Banner Priority", "t3_4": "Double visibility on the homepage.",
        "btn1": "FREE SIGNUP", "btn2": "UPGRADE NOW", "btn3": "CONTACT SALES",
        "how_title": "How does IA Realty Pro work?",
        "step1_t": "Paste Link", "step1_d": "Or write a brief description.",
        "step2_t": "AI Analyzes", "step2_d": "We optimize for SEO and sales.",
        "step3_t": "Publish", "step3_d": "Copy text and attract leads.",
        "stat1": "Optimized Ads", "stat2": "Time Saved", "stat3": "More Inquiries",
        "test_title": "What Experts Say",
        "test1_txt": "Instagram sales went up 50% since using AI for my captions.", "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "Amazing how it summarizes web links. Saves me hours.", "test2_au": "Ana M. (Century 21)",
        "test3_txt": "Best investment this year. Pro plan is worth every penny.", "test3_au": "Luis P. (Independent)",
        "foot_desc": "Artificial Intelligence Tools for Real Estate.",
        "foot_links": "Terms of Service | Privacy Policy | Support",
        "mail_label": "📧 Enter your Email to start", "limit_msg": "🚫 Free limit reached.", "upgrade_msg": "Go PRO to keep selling.",
        "lbl_tone": "Tone:", "lbl_lang_out": "Output Language:", "lbl_emoji": "Emojis:",
        "emoji_low": "Low", "emoji_med": "Medium", "emoji_high": "High",
        "agency_console": "📊 Agency Dashboard", "manage_team": "👥 Manage Team", "team_activity": "📈 Team Activity",
        "revoke": "Revoke Access", "copy_success": "Copied!", "whatsapp": "WhatsApp", "download": "Download", "char_count": "Characters",
        "leg_title": "⚖️ Terms & Privacy", "leg1": "AI Usage", "leg1_t": "AI-generated content; verify accuracy.",
        "leg2": "Subscriptions", "leg2_t": "PayPal payments. Cancel anytime.", "leg3": "Privacy", "leg3_t": "Data is encrypted and private."
    },
    "Português": {
        "hi": "Bom dia", "hi_after": "Boa tarde", "hi_night": "Boa noite",
        "badge_free": "GRÁTIS", "badge_pro": "MEMBRO PRO", "badge_agency": "AGÊNCIA",
        "title1": "Transforme Anúncios em", "title2": "Ímãs de Vendas",
        "sub": "A ferramenta de IA secreta dos agentes top.",
        "placeholder": "🏠 Descreva o imóvel ou adicione instruções...",
        "url_placeholder": "🔗 Cole o link (Zap, Viva Real, MLS...)",
        "btn_gen": "✨ GERAR ESTRATÉGIA DE VENDAS", "btn_refine": "🔄 Refinar texto...",
        "p_destacada": "DESTAQUE", "comunidad": "Comunidade Imobiliária", "popular": "MAIS POPULAR",
        "plan_title": "Selecione seu Plano", "annual_toggle": "📅 Economize 20% no Plano Anual",
        "annual_save": "✅ 2 Meses GRÁTIS incluídos",
        "plan1": "Inicial", "plan2": "Agente Pro", "plan3": "Agência",
        "desc1": "• 3 descrições / día", "t1_1": "Limite diário para novos usuários.",
        "desc2": "• Suporte Básico", "t1_2": "Resposta em até 48 horas.",
        "desc3": "• Marca d'Água", "t1_3": "Os textos incluem menção à plataforma.",
        "desc4": "• Gerações Ilimitadas", "t2_1": "Crie quantos anúncios precisar.",
        "desc5": "• Redes Sociais", "t2_2": "Posts para Instagram, FB e TikTok com hashtags.",
        "desc6": "• Otimização SEO", "t2_3": "Textos otimizados para buscas.",
        "desc7": "• Banner Principal", "t2_4": "Seus imóveis na página inicial.",
        "desc8": "• 5 Usuários / Contas", "t3_1": "Acesso para 5 membros da equipe.",
        "desc9": "• Painel de Equipe", "t3_2": "Gerencie o conteúdo do seu time.",
        "desc10": "• API (Em breve)", "t3_3": "Conecte ao seu CRM.",
        "desc11": "• Prioridade no Banner", "t3_4": "Dobro de visibilidade.",
        "btn1": "REGISTRO GRÁTIS", "btn2": "MELHORAR AGORA", "btn3": "CONTATO VENDAS",
        "how_title": "Como funciona?",
        "stat1": "Anúncios Otimizados", "stat2": "Tempo Economizado", "stat3": "Mais Leads",
        "test_title": "Depoimentos",
        "test1_txt": "Minhas vendas subiram 50% com IA.", "test1_au": "Carlos R. (RE/MAX)",
        "mail_label": "📧 Email para começar", "limit_msg": "🚫 Limite atingido.", "upgrade_msg": "Atualize para PRO.",
        "lbl_tone": "Tom:", "lbl_lang_out": "Idioma:", "lbl_emoji": "Emojis:",
        "emoji_low": "Poucos", "emoji_med": "Médios", "emoji_high": "Muitos",
        "agency_console": "📊 Painel da Agência", "manage_team": "👥 Gerenciar Equipe", "team_activity": "📈 Atividade",
        "revoke": "Revogar Acesso", "copy_success": "Copiado!", "whatsapp": "WhatsApp", "download": "Baixar", "char_count": "Caracteres",
        "leg_title": "⚖️ Termos e Privacidade", "leg1": "Uso de IA", "leg1_t": "Verifique a precisão legal.",
        "leg2": "Assinatura", "leg2_t": "PayPal. Cancele quando quiser.", "leg3": "Privacidade", "leg3_t": "Dados protegidos."
    },
    "Français": {
        "hi": "Bonjour", "hi_after": "Bon après-midi", "hi_night": "Bonsoir",
        "badge_free": "GRATUIT", "badge_pro": "MEMBRE PRO", "badge_agency": "AGENCE",
        "title1": "Annonces en", "title2": "Aimants à Ventes",
        "sub": "L'IA secrète des agents immobiliers performants.",
        "placeholder": "🏠 Décrivez la propriété...",
        "url_placeholder": "🔗 Collez le lien ici...",
        "btn_gen": "✨ GÉNÉRER LA STRATÉGIE", "btn_refine": "🔄 Affiner le texte",
        "p_destacada": "À LA UNE", "comunidad": "Communauté Immo", "popular": "LE PLUS POPULAIRE",
        "plan_title": "Forfaits", "annual_toggle": "📅 Économisez 20% (Annuel)",
        "annual_save": "✅ 2 mois GRATUITS inclus",
        "plan1": "Initial", "plan2": "Pro", "plan3": "Agence",
        "desc1": "• 3 descriptions / jour", "t1_1": "Limite quotidienne gratuite.",
        "desc10": "• API (Bientôt)", "t3_3": "Connectez à votre CRM.",
        "btn1": "S'INSCRIRE", "btn2": "UPGRADE", "btn3": "CONTACT",
        "how_title": "Comment ça marche ?", "stat1": "Ventes Boostées", "stat2": "Temps Gagné", "stat3": "Leads",
        "test_title": "Avis Experts", "mail_label": "📧 Email Pro",
        "limit_msg": "🚫 Limite atteinte.", "upgrade_msg": "Passez en PRO.",
        "lbl_tone": "Ton:", "lbl_lang_out": "Langue:", "lbl_emoji": "Émojis:",
        "emoji_low": "Peu", "emoji_med": "Moyen", "emoji_high": "Beaucoup",
        "agency_console": "📊 Console Agence", "manage_team": "👥 Équipe", "team_activity": "📈 Audit",
        "revoke": "Révoquer", "copy_success": "Copié !", "whatsapp": "WhatsApp", "download": "Télécharger", "char_count": "Caractères",
        "leg_title": "⚖️ Mentions Légales", "leg1": "IA", "leg1_t": "Vérifiez l'exactitude.",
        "leg2": "Abonnement", "leg2_t": "PayPal. Annulez à tout moment.", "leg3": "Confidentialité", "leg3_t": "Données sécurisées."
    },
    "Deutsch": {
        "hi": "Guten Morgen", "hi_after": "Guten Tag", "hi_night": "Guten Abend",
        "badge_free": "GRATIS", "badge_pro": "PRO", "badge_agency": "AGENTUR",
        "title1": "Anzeigen in", "title2": "Verkaufsmagnete",
        "sub": "Das KI-Tool für Top-Makler.",
        "placeholder": "🏠 Beschreiben Sie die Immobilie...",
        "url_placeholder": "🔗 Link hier einfügen...",
        "btn_gen": "✨ STRATEGIE GENERIEREN", "btn_refine": "🔄 Text anpassen",
        "p_destacada": "TOP-OBJEKT", "comunidad": "Immobilien-Community", "popular": "BELIEBTEST",
        "plan_title": "Wählen Sie Ihren Plan", "annual_toggle": "📅 20% sparen (Jährlich)",
        "annual_save": "✅ 2 Monate GRATIS",
        "plan1": "Basis", "plan2": "Pro", "plan3": "Agentur",
        "desc1": "• 3 Beschreibungen / Tag", "t1_1": "Gratis-Limit.",
        "desc10": "• API (Demnächst)", "t3_3": "CRM-Anbindung.",
        "btn1": "REGISTRIEREN", "btn2": "UPGRADE", "btn3": "KONTAKT",
        "how_title": "Wie funktioniert es?", "stat1": "Anzeigen", "stat2": "Zeit", "stat3": "Leads",
        "test_title": "Expertenstimmen", "mail_label": "📧 E-Mail",
        "limit_msg": "🚫 Limit erreicht.", "upgrade_msg": "Auf PRO upgraden.",
        "lbl_tone": "Tonfall:", "lbl_lang_out": "Sprache:", "lbl_emoji": "Emojis:",
        "emoji_low": "Wenig", "emoji_med": "Mittel", "emoji_high": "Viel",
        "agency_console": "📊 Agentur-Konsole", "manage_team": "👥 Team", "team_activity": "📈 Audit",
        "revoke": "Zugriff entziehen", "copy_success": "Kopiert!", "whatsapp": "WhatsApp", "download": "Herunterladen", "char_count": "Zeichen",
        "leg_title": "⚖️ Rechtliches", "leg1": "KI", "leg1_t": "KI-generiert; prüfen Sie Richtigkeit.",
        "leg2": "Abos", "leg2_t": "PayPal. Kündbar.", "leg3": "Datenschutz", "leg3_t": "Sicher."
    },
    "中文": {
        "hi": "早上好", "hi_after": "下午好", "hi_night": "晚上好",
        "badge_free": "免费用户", "badge_pro": "专业会员", "badge_agency": "机构伙伴",
        "title1": "将广告转化为", "title2": "销售磁铁",
        "sub": "顶级经纪人的人工智能工具。",
        "placeholder": "🏠 描述您的房产...",
        "url_placeholder": "🔗 在此粘贴链接...",
        "btn_gen": "✨ 生成销售策略", "btn_refine": "🔄 调整文本",
        "p_destacada": "精选房产", "comunidad": "房产社区", "popular": "最受欢迎",
        "plan_title": "选择您的方案", "annual_toggle": "📅 年度付款节省 20%",
        "annual_save": "✅ 包含 2 个月免费",
        "plan1": "基础版", "plan2": "专业版", "plan3": "机构版",
        "desc1": "• 每天 3 条描述", "t1_1": "免费额度。",
        "desc10": "• API (即将推出)", "t3_3": "连接您的 CRM。",
        "btn1": "免费注册", "btn2": "立即升级", "btn3": "联系销售",
        "how_title": "如何运作？", "stat1": "已优化广告", "stat2": "节省时间", "stat3": "更多潜在客户",
        "test_title": "专家评价", "mail_label": "📧 商务邮箱",
        "limit_msg": "🚫 已达到免费限制。", "upgrade_msg": "升级到专业版继续。",
        "lbl_tone": "语气:", "lbl_lang_out": "语言:", "lbl_emoji": "表情密度:",
        "emoji_low": "少", "emoji_med": "中", "emoji_high": "多",
        "agency_console": "📊 机构后台", "manage_team": "👥 团队管理", "team_activity": "📈 活动审计",
        "revoke": "撤销权限", "copy_success": "已复制!", "whatsapp": "微信", "download": "下载报告", "char_count": "字数",
        "leg_title": "⚖️ 法律条款", "leg1": "AI 使用", "leg1_t": "AI生成内容；经纪人需核实。",
        "leg2": "订阅", "leg2_t": "PayPal 支付。随时取消。", "leg3": "隐私", "leg3_t": "数据加密。"
    }
}
# ==========================================
# 6. ESTILOS CSS PLATINUM (BLINDAJE VISUAL)
# ==========================================
st.markdown("""
<style>
    /* 1. RESET Y FONDO BASE */
    .stApp { 
        background-color: #0e1117; 
        color: #FFFFFF; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }
    
    /* 2. ELIMINACIÓN DE LINKS INVISIBLES EN ENCABEZADOS */
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a, 
    .stMarkdown h4 a, .stMarkdown h5 a, .stMarkdown h6 a {
        display: none !important;
    }
    [data-testid="stHeaderActionElements"] { display: none !important; }

    /* 3. SCROLLBAR Y SELECCIÓN NEÓN */
    ::selection { background: rgba(0, 210, 255, 0.9); color: #000; }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0e1117; }
    ::-webkit-scrollbar-thumb { 
        background: #1a1c23; 
        border-radius: 10px; 
        border: 1px solid rgba(0, 210, 255, 0.2); 
    }

    /* 4. TIPOGRAFÍA NEÓN */
    .neon-title { 
        font-size: 3.5rem; 
        font-weight: 800; 
        text-align: center; 
        margin-top: 20px; 
        color: white; 
        text-shadow: 0 0 25px rgba(0, 210, 255, 0.4); 
    }
    .neon-highlight { color: #00d2ff; }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }

    /* 5. HUD: BARRA DE ESTADO SUPERIOR */
    .hud-container { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 12px 25px; 
        background: rgba(255, 255, 255, 0.03); 
        border-bottom: 1px solid rgba(0, 210, 255, 0.1); 
        margin-bottom: 30px; 
        border-radius: 12px;
    }
    .badge { 
        padding: 5px 15px; 
        border-radius: 20px; 
        font-size: 0.75rem; 
        font-weight: 800; 
        border: 1px solid; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .badge-pro { color: #00d2ff; border-color: #00d2ff; box-shadow: 0 0 10px rgba(0, 210, 255, 0.3); }
    .badge-agency { color: #DDA0DD; border-color: #DDA0DD; box-shadow: 0 0 10px rgba(221, 160, 221, 0.3); }

    /* 6. CONTENEDOR DE RESULTADO IA */
    .result-container { 
        background-color: #1a1c23; 
        color: #e0e0e0; 
        padding: 30px; 
        border-radius: 15px; 
        border: 1px solid rgba(0, 210, 255, 0.2); 
        font-size: 1.1rem; 
        line-height: 1.7; 
        margin-top: 25px; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.6); 
    }
    .char-badge { font-size: 0.8rem; color: #555; text-align: right; margin-top: 10px; font-weight: 600; }

    /* 7. BOTONES PRINCIPALES */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; 
        border: none !important; 
        color: white !important; 
        font-weight: 700 !important; 
        height: 3.8rem !important; 
        width: 100% !important; 
        border-radius: 10px !important;
        transition: all 0.4s ease !important;
    }
    div.stButton > button[kind="primary"]:hover { 
        transform: translateY(-3px) scale(1.01) !important; 
        box-shadow: 0 0 40px rgba(0, 210, 255, 0.7) !important; 
    }

    /* 8. CARDS DE PRECIOS Y PLANES */
    .card-wrapper { 
        transition: all 0.5s cubic-bezier(0.165, 0.84, 0.44, 1); 
        border-radius: 15px; 
        height: 580px; 
        margin-bottom: 25px; 
    }
    .card-wrapper:hover { transform: translateY(-15px); }
    .glass-container { 
        background: rgba(38, 39, 48, 0.6); 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-radius: 15px; 
        padding: 35px; 
        text-align: center; 
        position: relative; 
        height: 100%; 
    }
    .popular-badge { 
        position: absolute; 
        top: -15px; 
        left: 50%; 
        transform: translateX(-50%); 
        background: #00d2ff; 
        color: black; 
        padding: 7px 22px; 
        border-radius: 25px; 
        font-weight: 900; 
        font-size: 0.85rem; 
        box-shadow: 0 5px 15px rgba(0, 210, 255, 0.4);
    }
    .feature-list { 
        text-align: left; 
        margin: 25px auto; 
        display: inline-block; 
        font-size: 0.95rem; 
        color: #ccc; 
        line-height: 2.3; 
    }

    /* 9. VIDEO PLACEHOLDER / BANNER */
    .video-placeholder {
        border-radius: 15px; 
        height: 230px; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: flex-end;
        margin-bottom: 25px; 
        position: relative; 
        overflow: hidden; 
        background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80');
        background-size: cover; 
        background-position: center;
        border: 1px solid rgba(0, 210, 255, 0.3);
    }
    .dynamic-tag { 
        position: absolute; 
        top: 15px; 
        left: 15px; 
        background: #00d2ff; 
        color: black; 
        padding: 5px 14px; 
        border-radius: 4px; 
        font-size: 0.75rem; 
        font-weight: 900; 
    }
</style>
""", unsafe_allow_html=True)
# ==========================================
# 7. IDENTIDAD Y HUD (HEADS-UP DISPLAY)
# ==========================================
# Selector de idioma (Actualiza la variable L globalmente)
col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo: 
    st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 AI REALTY PRO</div>', unsafe_allow_html=True)

with col_lang:
    idioma_selec = st.selectbox("", list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma), label_visibility="collapsed")
    st.session_state.idioma = idioma_selec

L = traducciones[st.session_state.idioma]

# Renderizado del HUD (Saludo dinámico y Badge de Rango)
if st.session_state.email_usuario:
    hora_actual = datetime.now().hour
    if hora_actual < 12: saludo = L["hi"]
    elif hora_actual < 19: saludo = L["hi_after"]
    else: saludo = L["hi_night"]
    
    plan_n = str(st.session_state.plan_usuario).strip().capitalize()
    badge_style = "badge-pro" if plan_n == "Pro" else ("badge-agency" if plan_n == "Agencia" else "")
    badge_label = L.get(f"badge_{plan_n.lower()}", "USER")
    
    st.markdown(f'''
        <div class="hud-container">
            <div><b>{saludo}</b>, {st.session_state.email_usuario}</div>
            <div class="badge {badge_style}">{badge_label}</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)

# ==========================================
# 8. PANEL CENTRAL: LOGIN Y GENERADOR
# ==========================================
c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    # Banner Visual con Aura Neón
    st.markdown(f'''
        <div class="video-placeholder">
            <div class="dynamic-tag">{L["p_destacada"]}</div>
            <div style="position: absolute; bottom: 15px; width: 100%; text-align: center; color: white; font-weight: bold; background: rgba(0,0,0,0.4); padding: 5px 0;">{L["comunidad"]}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container" style="height:auto; box-shadow: 0 0 40px rgba(0,0,0,0.5); padding-top: 40px;">', unsafe_allow_html=True)
    
    # --- PASO 1: LOGIN MULTI-CUENTA ---
    if not st.session_state.email_usuario:
        email_input = st.text_input(L["mail_label"], placeholder="agente@ejemplo.com", key="main_login")
        if st.button(L["btn1"], type="primary", use_container_width=True):
            if email_input and "@" in email_input:
                df_u = obtener_datos_db()
                df_e = obtener_empleados_db()
                
                # Verificación: ¿Es un Jefe/Titular?
                if email_input in df_u['email'].values:
                    u_data = df_u[df_u['email'] == email_input].iloc[0]
                    st.session_state.usos = int(u_data['usos'])
                    st.session_state.plan_usuario = str(u_data['plan']).strip().capitalize()
                    st.session_state.es_empleado = False
                # Verificación: ¿Es un Empleado Invitado?
                elif email_input in df_e['EmployeeEmail'].values:
                    boss_email = df_e[df_e['EmployeeEmail'] == email_input].iloc[0]['BossEmail']
                    boss_data = df_u[df_u['email'] == boss_email].iloc[0]
                    st.session_state.usos = 0
                    # Si el jefe es Agencia, el empleado hereda privilegios PRO
                    st.session_state.plan_usuario = "Pro" if str(boss_data['plan']).capitalize() == "Agencia" else "Gratis"
                    st.session_state.es_empleado = True
                    st.session_state.boss_ref = boss_email
                else:
                    st.session_state.usos, st.session_state.plan_usuario, st.session_state.es_empleado = 0, "Gratis", False
                
                st.session_state.email_usuario = email_input
                st.rerun()
    
    # --- PASO 2: MOTOR IA PLATINUM ---
    else:
        # Lógica de límites
        p_act = str(st.session_state.plan_usuario).strip().capitalize()
        es_premium = p_act in ["Pro", "Agencia"]
        limite_usos = 99999 if es_premium else 3
        
        if st.session_state.usos < limite_usos:
            # Selectores de Configuración de IA
            col_ia1, col_ia2, col_ia3 = st.columns(3)
            with col_ia1:
                tono = st.selectbox(L["lbl_tone"], ["Storytelling", "Persuasivo", "Técnico", "Lujo"])
            with col_ia2:
                o_lang = st.selectbox(L["lbl_lang_out"], list(traducciones.keys()))
            with col_ia3:
                emojis = st.select_slider(L["lbl_emoji"], options=[L["emoji_low"], L["emoji_med"], L["emoji_high"]], value=L["emoji_med"])

            # Inputs de Datos
            url_in = st.text_input("", placeholder=L["url_placeholder"], label_visibility="collapsed")
            text_in = st.text_area("", placeholder=L["placeholder"], key="prop_desc", label_visibility="collapsed")
            st.markdown(f'<div class="char-badge">{L["char_count"]}: {len(text_in)}</div>', unsafe_allow_html=True)

            # EJECUCIÓN DE GENERACIÓN
            if st.button(L["btn_gen"], type="primary", use_container_width=True):
                if url_in or text_in:
                    with st.spinner("🚀 IA Realty Pro está analizando y redactando..."):
                        scraped_data = extraer_datos_inmueble(url_in) if url_in else ""
                        
                        # CONSTRUCCIÓN DEL PROMPT MAESTRO (3 VERSIONES + SEO)
                        prompt_ia = f"""
                        Actúa como un Broker Inmobiliario de lujo y experto en SEO.
                        TONO: {tono}. IDIOMA: {o_lang}. EMOJIS: {emojis}.
                        
                        PROPORCIONA:
                        1. VERSIÓN STORYTELLING: Enfocada en la experiencia de vivir allí.
                        2. VERSIÓN TÉCNICA: Enfocada en metros, calidades y datos duros.
                        3. VERSIÓN EJECUTIVA: Muy breve para WhatsApp.
                        4. SEO PACK: Título SEO optimizado y Meta-Descripción.
                        
                        DATOS: {scraped_data} {text_in}
                        """
                        
                        res_ia = generar_texto(prompt_ia)
                        if "ERROR_IA" not in res_ia:
                            st.session_state.last_result = res_ia
                            st.session_state.usos += 1
                            actualizar_usos_db(st.session_state.email_usuario, st.session_state.usos, st.session_state.plan_usuario)
                            guardar_historial(st.session_state.email_usuario, f"{url_in} {text_in}", res_ia)
                            st.rerun()
                else:
                    st.warning("Ingresa un link o describe la propiedad.")

            # DESPLIEGUE DE RESULTADOS Y HERRAMIENTAS
            if st.session_state.last_result:
                final_res = st.session_state.last_result
                st.markdown(f'<div class="result-container">{final_res.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
                
                # Toolbar de Acciones
                t_col1, t_col2, t_col3 = st.columns(3)
                with t_col1:
                    if st.button("📋 " + L["copy_success"]):
                        st.copy_to_clipboard(final_res); st.toast(L["copy_success"])
                with t_col2:
                    wa_link = urllib.parse.quote(final_res[:900] + "...")
                    st.link_button(f"📲 {L['whatsapp']}", f"https://wa.me/?text={wa_link}")
                with t_col3:
                    st.download_button(f"💾 {L['download']}", final_res, file_name=f"Estrategia_{datetime.now().strftime('%d%m')}.txt")
                
                # Herramienta de Refinamiento
                st.divider()
                refine_q = st.text_input(L["btn_refine"], placeholder="Ej: Haz la versión técnica más detallada...")
                if st.button("Refinar / Adjust"):
                    with st.spinner("Ajustando texto..."):
                        new_res = generar_texto(f"Basado en: {final_res}. Aplica este ajuste: {refine_q}")
                        st.session_state.last_result = new_res
                        st.rerun()
        else:
            st.error(L["limit_msg"])
            st.markdown(f"### {L['upgrade_msg']}")
            # (El botón de PayPal se incluye en el módulo final de planes)
            
    st.markdown('</div>', unsafe_allow_html=True)
    # ==========================================
# 9. PANEL DE CONTROL AGENCIA (ADMIN)
# ==========================================
if st.session_state.plan_usuario == "Agencia" and not st.session_state.es_empleado:
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    st.subheader(L["agency_console"])
    
    tab_team, tab_activity = st.tabs([L["manage_team"], L["team_activity"]])
    
    with tab_team:
        st.write(f"Invite agents to your organization (Plan: {st.session_state.plan_usuario}):")
        df_employees = obtener_empleados_db()
        # Filtramos equipo actual
        team_data = df_employees[df_employees['BossEmail'] == st.session_state.email_usuario]
        team_list = team_data['EmployeeEmail'].tolist()
        
        # UI para agregar miembros
        e_col1, e_col2 = st.columns([3, 1])
        with e_col1:
            new_emp = st.text_input("Agent Email", key="add_emp_field", placeholder="name@agency.com")
        with e_col2:
            st.write(" ") # Alineación con el input
            if st.button("ADD AGENT", use_container_width=True):
                if len(team_list) < 4:
                    if new_emp and "@" in new_emp and new_emp not in team_list:
                        new_entry = pd.DataFrame({"BossEmail": [st.session_state.email_usuario], "EmployeeEmail": [new_emp]})
                        conn.update(worksheet="Employees", data=pd.concat([df_employees, new_entry], ignore_index=True))
                        st.success(f"{new_emp} added to team!")
                        st.rerun()
                else:
                    st.warning("Agency Plan limit: 4 agents + Owner.")

        # LISTA DE GESTIÓN CON BOTÓN DE ELIMINACIÓN QUIRÚRGICA
        if team_list:
            st.write("---")
            for emp in team_list:
                m_c1, m_c2 = st.columns([3, 1])
                m_c1.markdown(f"👤 **{emp}**")
                # El botón de Revocar Acceso elimina la fila de la DB
                if m_c2.button(L["revoke"], key=f"del_{emp}", use_container_width=True):
                    updated_df = df_employees[~( (df_employees['BossEmail'] == st.session_state.email_usuario) & 
                                                 (df_employees['EmployeeEmail'] == emp) )]
                    conn.update(worksheet="Employees", data=updated_df)
                    st.toast(f"Access revoked: {emp}")
                    st.rerun()

    with tab_activity:
        st.write("Audit trail for your team's generations:")
        try:
            df_hist = conn.read(worksheet="Historial", ttl=0)
            full_team = team_list + [st.session_state.email_usuario]
            # Filtramos historial por los emails de este equipo
            team_hist = df_hist[df_hist['email'].isin(full_team)]
            if not team_hist.empty:
                st.dataframe(
                    team_hist.sort_values(by='fecha', ascending=False),
                    use_container_width=True,
                    column_order=("fecha", "email", "input", "output")
                )
            else:
                st.info("No records found for this team.")
        except:
            st.warning("Audit log inaccessible (Historial sheet missing).")

# ==========================================
# 10. SECCIÓN INFORMATIVA Y ESTADÍSTICAS
# ==========================================
st.markdown(f"<br><br><h2 style='text-align:center;'>{L['how_title']}</h2>", unsafe_allow_html=True)
h_c1, h_c2, h_c3 = st.columns(3)
with h_c1: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>1</h1><b>{L['step1_t']}</b><br>{L['step1_d']}</div>", unsafe_allow_html=True)
with h_c2: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>2</h1><b>{L['step2_t']}</b><br>{L['step2_d']}</div>", unsafe_allow_html=True)
with h_c3: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>3</h1><b>{L['step3_t']}</b><br>{L['step3_d']}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
s_c1, s_c2, s_c3 = st.columns(3)
card_st = '<div style="text-align:center; padding:25px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">{v}</h2><p style="color:#aaa; font-size:0.9rem;">{t}</p></div>'
with s_c1: st.markdown(card_st.format(v="+10k", t=L["stat1"]), unsafe_allow_html=True)
with s_c2: st.markdown(card_st.format(v="-80%", t=L["stat2"]), unsafe_allow_html=True)
with s_c3: st.markdown(card_st.format(v="+45%", t=L["stat3"]), unsafe_allow_html=True)

# ==========================================
# 11. PLANES CON SWITCH ANUAL Y PAYPAL
# ==========================================
st.markdown(f"<br><br><h2 style='text-align:center;'>{L['plan_title']}</h2>", unsafe_allow_html=True)
_, toggle_col, _ = st.columns([1,2,1])
with toggle_col:
    is_yearly = st.toggle(L["annual_toggle"], value=False)

# Precios dinámicos e IDs de PayPal
if is_yearly:
    price_pro, price_age = "490", "1,990"
    id_p_pro, id_p_age = "P-PON_AQUI_ID_ANUAL_PRO", "P-PON_AQUI_ID_ANUAL_AGE"
    saving = L["annual_save"]
else:
    price_pro, price_age = "49", "199"
    id_p_pro, id_p_age = "P-3P2657040E401734NNFQQ5TY", "P-0S451470G5041550ENFQRB4I"
    saving = ""

plan_col1, plan_col2, plan_col3 = st.columns(3)

with plan_col1:
    f_list_free = f"{L['desc1']}<br>{L['desc2']}<br>{L['desc3']}"
    st.markdown(f"<div class='card-wrapper'><div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.1;'>{f_list_free}</div></div>", unsafe_allow_html=True)
    st.button(L["btn1"], key="f_free_btn", use_container_width=True)

with plan_col2:
    f_list_pro = f"<b>{L['desc4']}</b><br>{L['desc5']}<br>{L['desc6']}<br><b>{L['desc7']}</b>"
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>${price_pro}</h1><p style='color:#00d2ff; font-size:0.8rem;'>{saving}</p><hr style='border-color:#00d2ff;opacity:0.2;'>{f_list_pro}</div></div>", unsafe_allow_html=True)
    paypal_pro_html = f'''
        <div id="paypal-pro-btn"></div>
        <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
        <script>
            paypal.Buttons({{
                style: {{ shape: 'pill', color: 'blue', layout: 'vertical', label: 'subscribe' }},
                createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{id_p_pro}', 'custom_id': '{st.session_state.email_usuario}' }});
                }}
            }}).render('#paypal-pro-btn');
        </script>
    '''
    components.html(paypal_pro_html, height=180)

with plan_col3:
    f_list_age = f"{L['desc8']}<br>{L['desc9']}<br>{L['desc10']}<br><b>{L['desc11']}</b>"
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>${price_age}</h1><p style='color:#DDA0DD; font-size:0.8rem;'>{saving}</p><hr style='border-color:#DDA0DD;opacity:0.2;'>{f_list_age}</div></div>", unsafe_allow_html=True)
    paypal_age_html = f'''
        <div id="paypal-age-btn"></div>
        <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
        <script>
            paypal.Buttons({{
                style: {{ shape: 'pill', color: 'blue', layout: 'vertical', label: 'subscribe' }},
                createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': '{id_p_age}', 'custom_id': '{st.session_state.email_usuario}' }});
                }}
            }}).render('#paypal-age-btn');
        </script>
    '''
    components.html(paypal_age_html, height=180)

# ==========================================
# 12. TESTIMONIOS Y FOOTER FINAL
# ==========================================
st.markdown(f"<br><br><h2 style='text-align:center;'>{L['test_title']}</h2>", unsafe_allow_html=True)
t_c1, t_c2, t_c3 = st.columns(3)
test_st = '<div style="padding:25px; border-radius:12px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); height:180px;"><p style="font-style:italic; color:#ddd; font-size:0.85rem;">"{txt}"</p><p style="color:#00d2ff; font-weight:bold; margin-top:15px;">- {aut}</p></div>'
with t_c1: st.markdown(test_st.format(txt=L["test1_txt"], aut=L["test1_au"]), unsafe_allow_html=True)
with t_c2: st.markdown(test_st.format(txt=L["test2_txt"], aut=L["test2_au"]), unsafe_allow_html=True)
with t_c3: st.markdown(test_st.format(txt=L["test3_txt"], aut=L["test3_au"]), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander(L["leg_title"]):
    l_c1, l_c2, l_c3 = st.columns(3)
    with l_c1: st.write(f"**{L['leg1']}**"); st.caption(L['leg1_t'])
    with l_c2: st.write(f"**{L['leg2']}**"); st.caption(L['leg2_t'])
    with l_c3: st.write(f"**{L['leg3']}**"); st.caption(L['leg3_t'])

st.markdown(f'<div style="text-align:center; padding:60px; color:#444; border-top:1px solid rgba(255,255,255,0.05);">© 2026 AI REALTY PRO - {L["foot_desc"]}</div>', unsafe_allow_html=True)
