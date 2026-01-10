import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import urllib.parse
import time

# --- 1. CONFIGURACIÓN INICIAL Y SECRETS ---
st.set_page_config(
    page_title="AI Realty Pro | Platinum Edition",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuración de OpenAI
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.warning("⚠️ Configuración pendiente: Por favor, añade la API Key en los Secrets de Streamlit.")
    st.stop()

# --- 2. CONEXIÓN A BASE DE DATOS Y FUNCIONES CORE ---
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

# FUNCIÓN NUEVA: REVOCACIÓN FÍSICA (Panel Agencia)
def eliminar_empleado_db(boss_email, employee_email_to_remove):
    try:
        df = obtener_empleados_db()
        # Filtramos para excluir la fila exacta que coincide
        df_nuevo = df[~((df['BossEmail'] == boss_email) & (df['EmployeeEmail'] == employee_email_to_remove))]
        conn.update(worksheet="Employees", data=df_nuevo)
        return True
    except Exception as e:
        return False

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
    except Exception as e:
        print(f"Error guardando historial: {e}")

# FUNCIÓN DE SCRAPING CON BLINDAJE
def extraer_datos_inmueble(url):
    # Blindaje: Validador de URL básico
    if not re.match(r'^https?://', url):
        return "Error: Link inválido. Debe comenzar con http:// o https://"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup(['script', 'style', 'header', 'footer', 'nav']):
                element.decompose()
            texto = soup.get_text(separator=' ', strip=True)
            return texto[:3500]
        else:
            return "Error: No se pudo acceder a la página (Status Code)."
    except Exception as e:
        return f"Error al leer el link: {str(e)}"

# CEREBRO DE IA TRIPLE (Storytelling, Ficha, Copy, SEO)
def generar_texto_triple(prompt_base, modelo="gpt-4o"):
    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Eres un estratega inmobiliario de élite. Tu respuesta debe estar estrictamente estructurada en 4 secciones claras usando Markdown."},
                {"role": "user", "content": prompt_base}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR_TECNICO: {str(e)}"

# --- 3. DICCIONARIO MAESTRO (IDIOMA TOTAL) ---
traducciones = {
    "Español": {
        "hud_greet_m": "Buenos días", "hud_greet_a": "Buenas tardes", "hud_greet_n": "Buenas noches",
        "badge_pro": "MIEMBRO PRO", "badge_agency": "PARTNER AGENCIA", "badge_free": "INVITADO",
        "api_item": "Acceso vía API (Próximamente)",
        "save_msg": "Ahorra 20% con pago Anual",
        "title1": "Convierte Anuncios Aburridos en", "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores.",
        "placeholder": "🏠 Describe la propiedad o escribe instrucciones extra...",
        "btn_gen": "✨ GENERAR PACK PLATINUM", "p_destacada": "PROPIEDAD DESTACADA",
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
        "desc10": "Acceso vía API (Próximamente)", "t3_3": "Conecta nuestra IA directamente con tu propio software o CRM.",
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
        "lbl_tone": "Tono:", "lbl_lang_out": "Idioma de Salida:",
        "lbl_emoji": "Densidad Emojis:", "lbl_quick": "Ajuste Rápido:",
        "btn_whatsapp": "Enviar a WhatsApp", "btn_download": "Descargar .txt",
        "revoke_btn": "Revocar Acceso", "agency_tab1": "Gestión Equipo", "agency_tab2": "Actividad"
    },
    "English": {
        "hud_greet_m": "Good morning", "hud_greet_a": "Good afternoon", "hud_greet_n": "Good evening",
        "badge_pro": "PRO MEMBER", "badge_agency": "AGENCY PARTNER", "badge_free": "GUEST",
        "api_item": "API Access (Coming Soon)",
        "save_msg": "Save 20% with Annual billing",
        "title1": "Turn Boring Listings into", "title2": "Sales Magnets",
        "sub": "The secret AI tool used by top producing agents.",
        "placeholder": "🏠 Describe the property or add extra instructions...",
        "btn_gen": "✨ GENERATE PLATINUM PACK", "p_destacada": "FEATURED PROPERTY",
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
        "desc10": "API Access (Coming Soon)", "t3_3": "Connect our AI directly with your own software or CRM.",
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
        "lbl_tone": "Tone:", "lbl_lang_out": "Output Language:",
        "lbl_emoji": "Emoji Density:", "lbl_quick": "Quick Adjust:",
        "btn_whatsapp": "Send to WhatsApp", "btn_download": "Download .txt",
        "revoke_btn": "Revoke Access", "agency_tab1": "Team Mgmt", "agency_tab2": "Activity"
    },
    "Português": {
        "hud_greet_m": "Bom dia", "hud_greet_a": "Boa tarde", "hud_greet_n": "Boa noite",
        "badge_pro": "MEMBRO PRO", "badge_agency": "PARCEIRO AGÊNCIA", "badge_free": "VISITANTE",
        "api_item": "Acesso via API (Em breve)",
        "save_msg": "Economize 20% no plano Anual",
        "title1": "Transforme Anúncios Tediosos em", "title2": "Ímãs de Vendas",
        "sub": "A ferramenta de IA secreta dos agentes de alto desempenho.",
        "placeholder": "🏠 Descreva o imóvel ou adicione instruções...",
        "btn_gen": "✨ GERAR PACOTE PLATINUM", "p_destacada": "IMÓVEL EM DESTAQUE",
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
        "desc10": "Acesso via API (Em breve)", "t3_3": "Conecte nossa IA diretamente com seu próprio software o CRM.",
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
        "lbl_tone": "Tom:", "lbl_lang_out": "Idioma de saída:",
        "lbl_emoji": "Densidade Emojis:", "lbl_quick": "Ajuste Rápido:",
        "btn_whatsapp": "Enviar para WhatsApp", "btn_download": "Baixar .txt",
        "revoke_btn": "Revogar Acesso", "agency_tab1": "Gestão Equipe", "agency_tab2": "Atividade"
    }
}

# --- 4. ESTILOS CSS PLATINUM (Sin Ghost Links, Scrollbar Custom, Glassmorphism) ---
st.markdown("""
<style>
    /* RESET & BASE */
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    
    /* GHOST LINKS KILLER */
    .css-15zrgzn {display: none}
    .css-1dp5vir {display: none}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    a.anchor-link {display: none !important;}

    /* SCROLLBAR ULTRA-FINA */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #0e1117; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #555; }

    /* SELECCIÓN DE TEXTO NEÓN */
    ::selection { background: #00d2ff; color: #000; }

    /* TYPOGRAPHY */
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }

    /* HUD (HEAD UP DISPLAY) */
    .hud-container {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(20, 20, 20, 0.8); backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(0, 210, 255, 0.2);
        padding: 10px 20px; margin-top: -50px; margin-left: -20px; margin-right: -20px; margin-bottom: 30px;
    }
    .hud-user { font-size: 0.9rem; color: #fff; font-weight: 500; }
    .hud-badge { padding: 4px 12px; border-radius: 12px; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px; margin-left: 10px; }
    .badge-pro { background: rgba(0, 210, 255, 0.15); color: #00d2ff; border: 1px solid rgba(0, 210, 255, 0.5); box-shadow: 0 0 10px rgba(0,210,255,0.3); }
    .badge-agency { background: rgba(221, 160, 221, 0.15); color: #DDA0DD; border: 1px solid rgba(221, 160, 221, 0.5); box-shadow: 0 0 10px rgba(221,160,221,0.3); }
    .badge-free { background: rgba(255, 255, 255, 0.1); color: #aaa; border: 1px solid #555; }

    /* CAJA DE RESULTADO ELEGANTE */
    .result-container {
        background-color: #f8f9fa; color: #1a1a1a; padding: 25px; border-radius: 12px;
        border-left: 5px solid #00d2ff; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 1.05rem; line-height: 1.6; margin-top: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* BOTONES */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; border: none !important; 
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4) !important; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important; 
        color: white !important; font-weight: 700 !important; height: 3.5rem !important; width: 100% !important;
    }
    div.stButton > button[kind="primary"]:hover { 
        background: #000000 !important; color: #ffffff !important;
        transform: scale(1.02) !important;
        box-shadow: 0 0 40px rgba(0, 210, 255, 0.8) !important; 
        border: 2px solid #00d2ff !important;
    }

    /* TARJETAS DE PRECIOS GLASSMORPHISM */
    .card-wrapper { transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1); border-radius: 12px; height: 550px; margin-bottom: 20px;}
    .card-wrapper:hover { transform: translateY(-10px); }
    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; height: 100%; backdrop-filter: blur(10px); }
    
    .free-card { box-shadow: 0 0 20px rgba(255, 255, 255, 0.03); }
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.4) !important; box-shadow: 0 0 25px rgba(0, 210, 255, 0.15); }
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.4) !important; box-shadow: 0 0 25px rgba(221, 160, 221, 0.15); }

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
</style>
""", unsafe_allow_html=True)

# --- 5. ESTADO DE SESIÓN ---
if "usos" not in st.session_state: st.session_state.usos = 0
if "email_usuario" not in st.session_state: st.session_state.email_usuario = ""
if "plan_usuario" not in st.session_state: st.session_state.plan_usuario = "Gratis"
if "es_empleado" not in st.session_state: st.session_state.es_empleado = False
if "idioma" not in st.session_state: st.session_state.idioma = "Español"
if "last_click" not in st.session_state: st.session_state.last_click = 0 # Para doble click protection

# --- 6. INTERFAZ PRINCIPAL ---

# Selector de Idioma (Sidebar/Esquina)
col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo: 
    st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 AI REALTY PRO</div>', unsafe_allow_html=True)
with col_lang:
    idioma_selec = st.selectbox("", list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma), label_visibility="collapsed")
    st.session_state.idioma = idioma_selec

L = traducciones[st.session_state.idioma]

# --- UX & SMART LOGIN: HUD BAR ---
if st.session_state.email_usuario:
    hora_actual = datetime.now().hour
    if 5 <= hora_actual < 12: saludo = L["hud_greet_m"]
    elif 12 <= hora_actual < 19: saludo = L["hud_greet_a"]
    else: saludo = L["hud_greet_n"]

    badge_class = "badge-free"
    badge_text = L["badge_free"]
    if st.session_state.plan_usuario == "Pro": 
        badge_class = "badge-pro"; badge_text = L["badge_pro"]
    elif st.session_state.plan_usuario == "Agencia": 
        badge_class = "badge-agency"; badge_text = L["badge_agency"]

    st.markdown(f"""
    <div class="hud-container">
        <div class="hud-user">👋 {saludo}, {st.session_state.email_usuario} <span class="hud-badge {badge_class}">{badge_text}</span></div>
        <div style="color:#666; font-size:0.8rem;">Credit Usage: {st.session_state.usos}</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Título Principal si no está logueado
    st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)


# --- 7. BLOQUE DE CAPTURA Y GENERACIÓN ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="glass-container" style="height:auto; box-shadow: 0 0 30px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
    
    # --- LÓGICA DE LOGIN CON HERENCIA ---
    if not st.session_state.email_usuario:
        email_input = st.text_input(L["mail_label"], placeholder="email@ejemplo.com", key="user_email")
        if st.button("COMENZAR / START", type="primary"):
            if email_input and "@" in email_input:
                df_actual = obtener_datos_db()
                df_emp = obtener_empleados_db()
                
                # CASO 1: ES DUEÑO
                if email_input in df_actual['email'].values:
                    usuario = df_actual[df_actual['email'] == email_input].iloc[0]
                    st.session_state.usos = int(usuario['usos'])
                    st.session_state.plan_usuario = usuario['plan'] if 'plan' in usuario else 'Gratis'
                    st.session_state.es_empleado = False
                    st.session_state.email_usuario = email_input
                    st.rerun()
                
                # CASO 2: ES EMPLEADO (HERENCIA)
                elif email_input in df_emp['EmployeeEmail'].values:
                    jefe_email = df_emp[df_emp['EmployeeEmail'] == email_input].iloc[0]['BossEmail']
                    datos_jefe = df_actual[df_actual['email'] == jefe_email].iloc[0]
                    
                    st.session_state.usos = 0 # Usos propios del empleado
                    
                    # Lógica de Herencia
                    if datos_jefe['plan'] == "Agencia":
                        st.session_state.plan_usuario = "Pro" # Hereda Pro
                    else:
                        st.session_state.plan_usuario = datos_jefe['plan'] # Hereda lo que tenga el jefe
                    
                    st.session_state.es_empleado = True
                    st.session_state.email_usuario = email_input
                    st.session_state.boss_ref = jefe_email
                    st.rerun()
                
                # CASO 3: NUEVO
                else:
                    st.session_state.usos = 0
                    st.session_state.plan_usuario = "Gratis"
                    st.session_state.email_usuario = email_input
                    st.rerun()
            else:
                st.error("Email inválido.")

    # --- MOTOR DE GENERACIÓN PLATINUM ---
    elif st.session_state.email_usuario:
        
        # Check Límite
        es_pro = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite_usos = 99999 if es_pro else 3
        
        if st.session_state.usos < limite_usos:
            # Inputs Avanzados
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                tono = st.selectbox(L.get("lbl_tone", "Tono:"), ["Storytelling Emocional", "Técnico Profesional", "Urgencia/Inversión", "Lujo Exclusivo"])
            with col_t2:
                idioma_salida = st.selectbox(L.get("lbl_lang_out", "Idioma Salida:"), list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma))
            
            # Selector de Densidad Emoji y Ajuste Rápido
            col_d1, col_d2 = st.columns([1, 2])
            with col_d1:
                densidad_emoji = st.select_slider(L.get("lbl_emoji", "Emojis:"), options=["0%", "20%", "50%", "100%"], value="20%")
            with col_d2:
                ajuste_rapido = st.text_input(L.get("lbl_quick", "Ajuste:"), placeholder="Ej: Mencionar piscina climatizada...")

            url_input = st.text_input("", placeholder="🔗 Link (http/https)...", label_visibility="collapsed")
            user_input = st.text_area("", placeholder=L['placeholder'], key="input_ia", label_visibility="collapsed")
            
            # BLINDAJE DOBLE CLICK
            now = time.time()
            click_boton = st.button(L['btn_gen'], key="main_gen", type="primary")
            
            if click_boton:
                if now - st.session_state.last_click > 2: # Anti-Spam de 2 seg
                    st.session_state.last_click = now
                    
                    if user_input or url_input: 
                        with st.spinner("🧠 Activando Cerebro Triple IA..."):
                            
                            # 1. Scraping
                            datos_web = ""
                            if url_input:
                                datos_web = extraer_datos_inmueble(url_input)

                            # 2. Prompt Triple (Obliga estructura)
                            prompt_completo = f"""
                            Actúa como un equipo de marketing inmobiliario. Necesito 4 piezas de contenido distintas.
                            
                            CONTEXTO:
                            Datos Link: {datos_web}
                            Datos Usuario: {user_input}
                            Ajuste Extra: {ajuste_rapido}
                            
                            CONFIGURACIÓN:
                            Idioma: {idioma_salida}
                            Tono: {tono}
                            Densidad Emojis: {densidad_emoji} (Si es 0% no usar ninguno).
                            
                            SALIDA REQUERIDA (Usa Headers Markdown exactos):
                            ### STORYTELLING
                            (Una descripción narrativa, seductora y visual del inmueble).

                            ### FICHA TÉCNICA
                            (Lista con bullets de características clave, m2, baños, etc).

                            ### WHATSAPP COPY
                            (Un mensaje corto, directo y con emojis optimizado para enviar por mensajería).

                            ### SEO META-PACK
                            (Título SEO, Meta Descripción y 10 Keywords de cola larga).
                            """
                            
                            resultado = generar_texto_triple(prompt_completo)
                            
                            if "ERROR_TECNICO" not in resultado:
                                st.session_state.usos += 1
                                actualizar_usos_db(st.session_state.email_usuario, st.session_state.usos, st.session_state.plan_usuario)
                                guardar_historial(st.session_state.email_usuario, f"{url_input} {user_input}", resultado)
                                st.success("✅ Pack Platinum Generado")
                                
                                # VISUALIZACIÓN DE RESULTADOS
                                st.markdown(f'<div class="result-container">{resultado.replace("###", "<br><h3 style=\'color:#00d2ff;\'>").replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                                
                                # BOTONES DE PRODUCTIVIDAD
                                cp1, cp2, cp3 = st.columns(3)
                                with cp1:
                                    # Copy Feedback Visual
                                    if st.button("📋 COPY TEXT"):
                                        st.toast("Texto copiado al portapapeles", icon="📋")
                                        st.write(f"<script>navigator.clipboard.writeText(`{resultado}`)</script>", unsafe_allow_html=True)
                                with cp2:
                                    # Generar Link WhatsApp
                                    try:
                                        # Extraemos el bloque de WhatsApp
                                        bloque_wa = resultado.split("### WHATSAPP COPY")[1].split("###")[0].strip()
                                        wa_encoded = urllib.parse.quote(bloque_wa)
                                        st.link_button(f"📱 {L['btn_whatsapp']}", f"https://wa.me/?text={wa_encoded}")
                                    except:
                                        st.link_button(f"📱 {L['btn_whatsapp']}", "https://wa.me/")
                                with cp3:
                                    st.download_button(f"💾 {L['btn_download']}", resultado, file_name="inmueble_platinum.txt")

                                if not es_pro:
                                    st.info(f"Usos restantes: {3 - st.session_state.usos}")
                            else:
                                st.error("Error en conexión IA.")
                    else:
                        st.warning("Ingresa datos.")
            
            # --- PANEL DE AGENCIA (SEGURIDAD Y GESTIÓN) ---
            if st.session_state.plan_usuario == "Agencia" and not st.session_state.es_empleado:
                st.divider()
                st.subheader("🛡️ Agency Command Center")
                tab_team, tab_activity = st.tabs([L["agency_tab1"], L["agency_tab2"]])
                
                with tab_team:
                    df_employees = obtener_empleados_db()
                    current_team = df_employees[df_employees['BossEmail'] == st.session_state.email_usuario]['EmployeeEmail'].tolist()
                    
                    c_add1, c_add2 = st.columns([3, 1])
                    with c_add1: new_e = st.text_input("Email Agente", key="new_emp")
                    with c_add2: 
                        st.write(" ")
                        if st.button("➕ ADD"):
                            if len(current_team) < 4 and "@" in new_e:
                                new_row = pd.DataFrame({"BossEmail": [st.session_state.email_usuario], "EmployeeEmail": [new_e]})
                                conn.update(worksheet="Employees", data=pd.concat([df_employees, new_row], ignore_index=True))
                                st.rerun()
                    
                    st.write("---")
                    for emp in current_team:
                        col_e1, col_e2 = st.columns([4, 1])
                        col_e1.write(f"👤 {emp}")
                        # BOTÓN REVOCAR (Eliminación Física)
                        if col_e2.button(f"{L['revoke_btn']}", key=f"del_{emp}"):
                            eliminar_empleado_db(st.session_state.email_usuario, emp)
                            st.rerun()

                with tab_activity:
                    try:
                        df_h = conn.read(worksheet="Historial", ttl=0)
                        team_full = current_team + [st.session_state.email_usuario]
                        st.dataframe(df_h[df_h['email'].isin(team_full)].sort_values('fecha', ascending=False), use_container_width=True)
                    except: st.write("No data.")

        else:
            # PAYWALL
            st.error(L["limit_msg"])
            st.markdown(f"#### {L['upgrade_msg']}")
            # Paypal Bloqueo
            components.html(f"""
            <div id="paypal-bloqueo"></div>
            <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'pill', color: 'blue', layout: 'horizontal', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{
                    return actions.subscription.create({{ 'plan_id': 'P-3P2657040E401734NNFQQ5TY', 'custom_id': '{st.session_state.email_usuario}' }});
                  }}
              }}).render('#paypal-bloqueo');
            </script>
            """, height=100)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 8. PLANES CON SWITCH ANUAL Y RESPONSIVE CARDS ---
st.markdown("<br><br>", unsafe_allow_html=True)
col_sw1, col_sw2, col_sw3 = st.columns([1,2,1])
with col_sw2:
    modo_anual = st.toggle(f"📅 {L['save_msg']}", value=False)

if modo_anual:
    p_pro, p_agencia = "490", "1,990"
    id_pro, id_agencia = "P-ID_ANUAL_PRO", "P-ID_ANUAL_AGENCY"
    txt_ahorro = "✅ 2 Months FREE"
else:
    p_pro, p_agencia = "49", "199"
    id_pro, id_agencia = "P-3P2657040E401734NNFQQ5TY", "P-0S451470G5041550ENFQRB4I"
    txt_ahorro = ""

col1, col2, col3 = st.columns(3)

# GRATIS
with col1:
    desc_f = f"<div class='feature-list'>{L['desc1']}<span class='info-icon i-free' data-tooltip='{L['t1_1']}'>i</span><br>{L['desc2']}<span class='info-icon i-free' data-tooltip='{L['t1_2']}'>i</span><br>{L['desc3']}<span class='info-icon i-free' data-tooltip='{L['t1_3']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper free-card'><div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'>{desc_f}</div></div>", unsafe_allow_html=True)

# PRO
with col2:
    desc_p = f"<div class='feature-list'><b>{L['desc4']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_1']}'>i</span><br>{L['desc5']}<span class='info-icon i-pro' data-tooltip='{L['t2_2']}'>i</span><br>{L['desc6']}<span class='info-icon i-pro' data-tooltip='{L['t2_3']}'>i</span><br><b>{L['desc7']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>${p_pro}</h1><p style='color:#00d2ff; font-weight:bold; font-size:0.9rem;'>{txt_ahorro}</p><hr style='border-color:#00d2ff;opacity:0.3;'>{desc_p}</div></div>", unsafe_allow_html=True)
    components.html(f"""<script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script><div id="pp-pro"></div><script>paypal.Buttons({{style:{{shape:'pill',color:'blue',layout:'vertical',label:'subscribe'}},createSubscription:function(d,a){{return a.subscription.create({{'plan_id':'{id_pro}','custom_id':'{st.session_state.email_usuario}'}});}}}}).render('#pp-pro');</script>""", height=150)

# AGENCIA
with col3:
    desc_a = f"<div class='feature-list'>{L['desc8']}<span class='info-icon i-agency' data-tooltip='{L['t3_1']}'>i</span><br>{L['desc9']}<span class='info-icon i-agency' data-tooltip='{L['t3_2']}'>i</span><br>{L['desc10']}<span class='info-icon i-agency' data-tooltip='{L['t3_3']}'>i</span><br><b>{L['desc11']}</b><span class='info-icon i-agency' data-tooltip='{L['t3_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>${p_agencia}</h1><p style='color:#DDA0DD; font-weight:bold; font-size:0.9rem;'>{txt_ahorro}</p><hr style='border-color:#DDA0DD;opacity:0.3;'>{desc_a}</div></div>", unsafe_allow_html=True)
    components.html(f"""<script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script><div id="pp-agency"></div><script>paypal.Buttons({{style:{{shape:'pill',color:'blue',layout:'vertical',label:'subscribe'}},createSubscription:function(d,a){{return a.subscription.create({{'plan_id':'{id_agencia}','custom_id':'{st.session_state.email_usuario}'}});}}}}).render('#pp-agency');</script>""", height=150)

# --- FOOTER ---
st.markdown(f'<div style="border-top: 1px solid rgba(255,255,255,0.1); padding: 40px 0px; text-align: center;"><div style="font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom:10px;">🏢 AI REALTY PRO</div><p style="color:#666; font-size:0.8rem;">© 2026 IA Realty Pro - {L["foot_desc"]}</p></div>', unsafe_allow_html=True)
