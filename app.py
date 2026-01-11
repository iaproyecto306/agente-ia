import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
import time
import io
import extra_streamlit_components as stx 
import random

# ==============================================================================
# 0. GESTOR DE COOKIES (MEMORIA PERMANENTE - ARQUITECTURA SEGURA)
# ==============================================================================
# Esta sección maneja la persistencia para que el usuario no tenga que loguearse
# cada vez que recarga la página. Se usa session_state como puente.

if "cookie_manager" not in st.session_state:
    st.session_state.cookie_manager = stx.CookieManager()

cookie_manager = st.session_state.cookie_manager

# ==============================================================================
# 1. MOTOR DE EXTRACCIÓN (NINJA V6.0 - ANTI-BLOQUEO)
# ==============================================================================

def extraer_datos_inmueble(url):
    """
    Función Ninja v6.0.
    Estrategia de 3 capas para intentar saltar el bloqueo de IP de servidor.
    """
    # 1. Validación básica de dominio
    portales_validos = [
        "infocasas", 
        "mercadolibre", 
        "zillow", 
        "properati", 
        "remax", 
        "fincaraiz", 
        "realtor", 
        "idealista", 
        "fotocasa", 
        "inmuebles24"
    ]
    es_portal_conocido = any(portal in url.lower() for portal in portales_validos)
    texto_final = ""
    
    # --- MÉTODO A: PUENTE JINA AI (Mejor opción para texto limpio) ---
    try:
        # Añadimos un timestamp para evitar caché
        url_jina = f"https://r.jina.ai/{url}"
        headers_jina = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Return-Format": "text"
        }
        response = requests.get(url_jina, headers=headers_jina, timeout=25)
        if response.status_code == 200 and "Just a moment" not in response.text:
            texto_final = response.text
    except:
        pass

    # --- MÉTODO B: IMITACIÓN NAVEGADOR PC (Si Jina falla) ---
    if not texto_final or len(texto_final) < 500:
        try:
            headers_pc = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1"
            }
            response = requests.get(url, headers=headers_pc, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Eliminamos basura
                for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'svg', 'button']):
                    element.decompose()
                texto_final = soup.get_text(separator=' ', strip=True)
        except:
            pass

    # --- MÉTODO C: IMITACIÓN MÓVIL (A veces los sitios móviles son menos estrictos) ---
    if not texto_final or len(texto_final) < 500:
        try:
            headers_movil = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1"
            }
            response = requests.get(url, headers=headers_movil, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for element in soup(['script', 'style', 'nav', 'footer']):
                    element.decompose()
                texto_final = soup.get_text(separator=' ', strip=True)
        except:
            pass

    # --- VEREDICTO FINAL ---
    # Si logramos sacar más de 400 caracteres, consideramos éxito
    if len(texto_final) > 400:
        return texto_final[:6000], es_portal_conocido
    else:
        # Mensaje amigable explicando la situación al usuario
        return "⚠️ SECURITY ALERT: Automated access blocked by portal. Please COPY AND PASTE the property description manually below.", es_portal_conocido

# ==============================================================================
# 2. CONFIGURACIÓN DE IA Y CONEXIONES SEGURAS
# ==============================================================================

# Verificación de API Key de OpenAI
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("⚠️ CRITICAL ERROR: OPENAI_API_KEY not found in Streamlit Secrets.")
    st.stop()

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNCIONES DE BASE DE DATOS (CON FIX DE NORMALIZACIÓN) ---

def obtener_datos_db():
    """Obtiene la base de datos de usuarios principales con lectura en tiempo real."""
    try:
        # ttl=0 OBLIGATORIO para ver cambios manuales en el Excel al instante
        df = conn.read(worksheet="Sheet1", ttl=0)
        # Normalizamos: todo minúscula y sin espacios para evitar errores de tipeo en Excel
        df['email'] = df['email'].astype(str).str.strip().str.lower()
        if 'plan' in df.columns:
            df['plan'] = df['plan'].astype(str).str.strip().str.title() # Convierte "pro" a "Pro"
        return df
    except:
        return pd.DataFrame(columns=['email', 'usos', 'plan'])

def obtener_empleados_db():
    """Obtiene la base de datos de empleados/equipos en tiempo real."""
    try:
        df = conn.read(worksheet="Employees", ttl=0)
        df['BossEmail'] = df['BossEmail'].astype(str).str.strip().str.lower()
        df['EmployeeEmail'] = df['EmployeeEmail'].astype(str).str.strip().str.lower()
        return df
    except:
        return pd.DataFrame(columns=['BossEmail', 'EmployeeEmail'])

def actualizar_usos_db(email, nuevos_usos, plan_actual):
    """Actualiza el consumo de usos y verifica el plan."""
    email = email.strip().lower() 
    df = obtener_datos_db()
    
    if 'plan' not in df.columns:
        df['plan'] = 'Gratis'

    if email in df['email'].values:
        df.loc[df['email'] == email, 'usos'] = nuevos_usos
        if plan_actual and plan_actual != "Gratis":
             df.loc[df['email'] == email, 'plan'] = plan_actual.title()
    else:
        nueva_fila = pd.DataFrame({
            "email": [email], 
            "usos": [nuevos_usos], 
            "plan": [plan_actual.title() if plan_actual else "Gratis"]
        })
        df = pd.concat([df, nueva_fila], ignore_index=True)
    
    conn.update(worksheet="Sheet1", data=df)

def guardar_historial(email, input_user, output_ia):
    """Guarda cada generación en la hoja Historial para auditoría."""
    try:
        try:
            df_hist = conn.read(worksheet="Historial", ttl=0)
        except:
            df_hist = pd.DataFrame(columns=['fecha', 'email', 'input', 'output'])
        
        nueva_fila = pd.DataFrame({
            "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")],
            "email": [email],
            "input": [input_user[:600]], 
            "output": [output_ia]
        })
        
        df_final = pd.concat([df_hist, nueva_fila], ignore_index=True)
        conn.update(worksheet="Historial", data=df_final)
    except Exception as e:
        print(f"Error saving history: {e}")

def guardar_feedback(email, mensaje):
    """Guarda los mensajes de soporte en una hoja nueva."""
    try:
        try:
            df_feed = conn.read(worksheet="Feedback", ttl=0)
        except:
            df_feed = pd.DataFrame(columns=['fecha', 'email', 'mensaje'])
        
        nueva_fila = pd.DataFrame({
            "fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")],
            "email": [email if email else "Anonimo"],
            "mensaje": [mensaje]
        })
        
        df_final = pd.concat([df_feed, nueva_fila], ignore_index=True)
        conn.update(worksheet="Feedback", data=df_final)
        return True
    except Exception as e:
        print(f"Error feedback: {e}")
        return False

def generar_texto(prompt, modelo="gpt-4o"):
    """
    Motor de generación de texto.
    """
    try:
        response = client.chat.completions.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "You are a Senior Luxury Real Estate Broker and Expert Copywriter. Your goal is to SELL."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.75 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR_IA: {str(e)}"

# ==============================================================================
# 3. CONFIGURACIÓN DE PÁGINA Y VARIABLES DE ESTADO
# ==============================================================================

st.set_page_config(
    page_title="AI Realty Pro Platinum",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# Inicialización de variables de sesión
if "usos" not in st.session_state: st.session_state.usos = 0
if "email_usuario" not in st.session_state: st.session_state.email_usuario = ""
if "plan_usuario" not in st.session_state: st.session_state.plan_usuario = "Gratis"
if "es_empleado" not in st.session_state: st.session_state.es_empleado = False
# FIX: IDIOMA POR DEFECTO INGLÉS
if "idioma" not in st.session_state: st.session_state.idioma = "English"
if "last_result" not in st.session_state: st.session_state.last_result = None

# ==============================================================================
# 4. DICCIONARIO MAESTRO 360° (COMPLETO Y EXPANDIDO)
# ==============================================================================

traducciones = {
    "English": {
        "title1": "Turn Boring Listings into",
        "title2": "Sales Magnets",
        "sub": "The secret AI tool for top-producing agents in 2026.",
        "placeholder": "🏠 Describe property (beds, pool, view) or add instructions...",
        "url_placeholder": "🔗 Paste property link...",
        "btn_gen": "✨ GENERATE TRIPLE STRATEGY",
        "p_destacada": "FEATURED LISTING",
        "comunidad": "Real Estate Community",
        "popular": "MOST POPULAR",
        "plan1": "Starter",
        "plan2": "Pro Agent",
        "plan3": "Agency",
        "desc1": "3 descriptions / day",
        "t1_1": "Daily limit for free trial.",
        "desc2": "Basic Support",
        "t1_2": "Basic technical help.",
        "desc3": "Watermark",
        "t1_3": "Text includes platform signature.",
        "desc4": "Unlimited Generations",
        "t2_1": "No monthly limits.",
        "desc5": "Social Media Pack",
        "t2_2": "Instagram & TikTok Scripts.",
        "desc6": "SEO Optimization",
        "t2_3": "Keywords & meta-tags.",
        "desc7": "Main Banner",
        "t2_4": "Homepage rotation.",
        "desc8": "5 Users / Accounts",
        "t3_1": "Team access.",
        "desc9": "Team Dashboard",
        "t3_2": "Audit and manage agents.",
        "desc10": "API Access",
        "t3_3": "CRM Integration (Coming Soon).",
        "desc11": "Banner Priority",
        "t3_4": "Double exposure.",
        "btn1": "FREE SIGNUP",
        "btn2": "UPGRADE NOW",
        "btn3": "CONTACT SALES",
        "how_title": "How it works?",
        "step1_t": "Paste Link",
        "step1_d": "Or write details.",
        "step2_t": "AI Analyzes",
        "step2_d": "Triple Generation Engine.",
        "step3_t": "Sell",
        "step3_d": "Publish and close.",
        "stat1": "Optimized Ads",
        "stat2": "Time Saved",
        "stat3": "Conversion",
        "test_title": "What Experts Say",
        "test1_txt": "Sales went up 50%.",
        "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "Saves hours of writing.",
        "test2_au": "Ana M. (Century 21)",
        "test3_txt": "Agency plan is vital.",
        "test3_au": "Luis P. (Independent)",
        "foot_desc": "AI for Real Estate.",
        "mail_label": "📧 Professional Email",
        "limit_msg": "🚫 Free limit reached.",
        "upgrade_msg": "Upgrade to PRO to keep selling.",
        "lbl_tone": "Tone:",
        "lbl_lang_out": "Output Language:",
        "annual_toggle": "📅 Save 20% with Yearly Payment",
        "annual_save": "✅ 2 Months FREE included",
        "whatsapp": "Send to WhatsApp",
        "download": "Download Report .txt",
        "copy_success": "Copied successfully!",
        "revoke": "Revoke Access",
        "manage_team": "👥 Manage Team",
        "team_activity": "📈 Activity",
        "refine_pl": "🔄 Quick adjust (e.g., shorter)...",
        "social_title": "📱 Social Media Pack",
        "char_count": "Characters",
        "link_warn": "⚠️ Link not recognized.",
        "badge_free": "FREE USER",
        "badge_pro": "PRO MEMBER",
        "badge_agency": "AGENCY PARTNER",
        "api_soon": "API Access (Coming Soon)",
        "legal_title": "Terms & Privacy",
        "logout": "Log Out",
        "welcome": "Welcome",
        "usage_bar": "Daily Progress",
        "feedback_lbl": "💡 Feedback / Support",
        "feedback_btn": "Send Feedback",
        "support_mail": "Support",
        "credits_left": "Credits left:",
        "welcome_morn": "Good morning",
        "welcome_aft": "Good afternoon",
        "welcome_eve": "Good evening",
        "impact_text": "SALES IMPACT BOOSTED",
        "strategy_gen": "GENERATED STRATEGY",
        "desc_luxury": "LUXURY DESCRIPTION",
        "btn_refine": "Refine / Adjust",
        "analyzing_msg": "ANALYZING PROPERTY AND WRITING STRATEGY...",
        "feedback_success": "✅ Thanks! Your feedback has been saved.",
        "tone_lux": "Luxury",
        "tone_prof": "Professional",
        "tone_urg": "Urgency",
        "tone_story": "Storytelling",
        "emp_email_lbl": "Agent Email",
        "emp_add_btn": "ADD",
        # KEYS DE SECCIÓN AGREGADAS
        "sec_1": "SECTION 1: MAIN DESCRIPTION",
        "sec_2": "SECTION 2: TECHNICAL SPECS",
        "sec_3": "SECTION 3: WHATSAPP COPY",
        "sec_4": "SECTION 4: SEO PACK",
        "sec_short": "SHORT DESCRIPTION",
        "tab_team": "👥 My Team",
        "tab_monitor": "📊 Activity Monitor",
        "monitor_desc": "Here you can see your agents' usage in real time.",
        "monitor_empty": "Your employees haven't generated content yet."
    },
    "Español": {
        "title1": "Convierte Anuncios Aburridos en",
        "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores en 2026.",
        "placeholder": "🏠 Describe la propiedad (ej: 3 dorm, piscina, vista al mar) o añade instrucciones...",
        "url_placeholder": "🔗 Pega el link de la propiedad...",
        "btn_gen": "✨ GENERAR ESTRATEGIA TRIPLE",
        "p_destacada": "PROPIEDAD DESTACADA",
        "comunidad": "Comunidad Real Estate",
        "popular": "MÁS POPULAR",
        "plan1": "Inicial",
        "plan2": "Agente Pro",
        "plan3": "Agencia",
        "desc1": "3 descripciones / día",
        "t1_1": "Límite diario para prueba gratuita.",
        "desc2": "Soporte Básico",
        "t1_2": "Ayuda técnica básica vía email.",
        "desc3": "Marca de Agua",
        "t1_3": "El texto incluye firma de la plataforma.",
        "desc4": "Generaciones Ilimitadas",
        "t2_1": "Sin límites mensuales de uso.",
        "desc5": "Pack Redes Sociales",
        "t2_2": "Scripts para Instagram, TikTok y Reels.",
        "desc6": "Optimización SEO",
        "t2_3": "Palabras clave y meta-tags incluidos.",
        "desc7": "Banner Principal",
        "t2_4": "Rotación de propiedades en home.",
        "desc8": "5 Usuarios / Cuentas",
        "t3_1": "Acceso para todo tu equipo.",
        "desc9": "Panel de Equipo",
        "t3_2": "Audita y gestiona a tus agentes.",
        "desc10": "Acceso vía API",
        "t3_3": "Integración CRM (Próximamente).",
        "desc11": "Prioridad en Banner",
        "t3_4": "Doble exposición en portada.",
        "btn1": "REGISTRO GRATIS",
        "btn2": "MEJORAR AHORA",
        "btn3": "CONTACTAR VENTAS",
        "how_title": "¿Cómo funciona?",
        "step1_t": "Pega el Link",
        "step1_d": "O escribe los detalles.",
        "step2_t": "IA Analiza",
        "step2_d": "Motor Triple Generación.",
        "step3_t": "Vende",
        "step3_d": "Copia y cierra tratos.",
        "stat1": "Anuncios Optimizados",
        "stat2": "Tiempo Ahorrado",
        "stat3": "Más Consultas",
        "test_title": "Lo que dicen los Expertos",
        "test1_txt": "Mis ventas subieron 50%.",
        "test1_au": "Carlos R. (RE/MAX)",
        "test2_txt": "Ahorro horas de redacción.",
        "test2_au": "Ana M. (Century 21)",
        "test3_txt": "El plan Agencia es vital.",
        "test3_au": "Luis P. (Independiente)",
        "foot_desc": "Inteligencia Artificial Inmobiliaria.",
        "mail_label": "📧 Email Profesional",
        "limit_msg": "🚫 Límite gratuito alcanzado.",
        "upgrade_msg": "Pásate a PRO para seguir vendiendo.",
        "lbl_tone": "Tono:",
        "lbl_lang_out": "Idioma Salida:",
        "annual_toggle": "📅 Ahorrar 20% con Pago Anual",
        "annual_save": "✅ 2 Meses GRATIS incluidos",
        "whatsapp": "Enviar a WhatsApp",
        "download": "Descargar Reporte .txt",
        "copy_success": "¡Copiado con éxito!",
        "revoke": "Revocar Acceso",
        "manage_team": "👥 Gestionar Equipo",
        "team_activity": "📈 Actividad",
        "refine_pl": "🔄 Ajuste rápido (ej: hazlo más corto)...",
        "social_title": "📱 Social Media Pack",
        "char_count": "Caracteres",
        "link_warn": "⚠️ Este link no parece ser de un portal conocido.",
        "badge_free": "USUARIO GRATIS",
        "badge_pro": "MIEMBRO PRO",
        "badge_agency": "SOCIO AGENCIA",
        "api_soon": "Acceso API (Próximamente)",
        "legal_title": "Términos Legales & Privacidad",
        "logout": "Cerrar Sesión",
        "welcome": "Bienvenido",
        "usage_bar": "Progreso Diario",
        "feedback_lbl": "💡 Sugerencias / Soporte",
        "feedback_btn": "Enviar Comentario",
        "support_mail": "Soporte",
        "credits_left": "Créditos hoy:",
        "welcome_morn": "Buenos días",
        "welcome_aft": "Buenas tardes",
        "welcome_eve": "Buenas noches",
        "impact_text": "IMPACTO DE VENTA AUMENTADO",
        "strategy_gen": "ESTRATEGIA GENERADA",
        "desc_luxury": "DESCRIPCIÓN LUJO",
        "btn_refine": "Refinar / Ajustar",
        "analyzing_msg": "ANALIZANDO PROPIEDAD Y REDACTANDO ESTRATEGIA...",
        "feedback_success": "✅ ¡Gracias! Tu comentario ha sido guardado.",
        "tone_lux": "Lujo",
        "tone_prof": "Profesional",
        "tone_urg": "Urgencia",
        "tone_story": "Storytelling",
        "emp_email_lbl": "Email Agente",
        "emp_add_btn": "AÑADIR",
        # KEYS AGREGADAS ESPAÑOL
        "sec_1": "SECCIÓN 1: DESCRIPCIÓN PRINCIPAL",
        "sec_2": "SECCIÓN 2: FICHA TÉCNICA",
        "sec_3": "SECCIÓN 3: COPY WHATSAPP",
        "sec_4": "SECCIÓN 4: PACK SEO",
        "sec_short": "DESCRIPCIÓN CORTA",
        "tab_team": "👥 Mi Equipo",
        "tab_monitor": "📊 Monitor de Actividad",
        "monitor_desc": "Aquí puedes ver el consumo de tus agentes en tiempo real.",
        "monitor_empty": "Tus empleados aún no han generado contenido."
    },
    "Português": {
        "title1": "Transforme Anúncios em",
        "title2": "Ímãs de Vendas",
        "sub": "A ferramenta secreta dos top produtores.",
        "placeholder": "🏠 Descreva o imóvel...",
        "url_placeholder": "🔗 Cole o link...",
        "btn_gen": "✨ GERAR ESTRATÉGIA",
        "p_destacada": "DESTAQUE",
        "comunidad": "Comunidade",
        "popular": "POPULAR",
        "plan1": "Inicial",
        "plan2": "Pro",
        "plan3": "Agência",
        "desc1": "3 descrições/dia",
        "t1_1": "Limite diário.",
        "desc2": "Suporte Básico",
        "t1_2": "Ajuda por email.",
        "desc3": "Marca d'água",
        "t1_3": "Inclui assinatura.",
        "desc4": "Gerações Ilimitadas",
        "t2_1": "Sem limites.",
        "desc5": "Social Media Pack",
        "t2_2": "Scripts Insta/TikTok.",
        "desc6": "SEO Otimizado",
        "t2_3": "Palavras-chave.",
        "desc7": "Banner Principal",
        "t2_4": "Rotação na home.",
        "desc8": "5 Usuários",
        "t3_1": "Acesso equipe.",
        "desc9": "Painel Equipe",
        "t3_2": "Gestão de agentes.",
        "desc10": "Acesso API",
        "t3_3": "Em breve.",
        "desc11": "Prioridade Banner",
        "t3_4": "Dupla exposição.",
        "btn1": "REGISTRO GRÁTIS",
        "btn2": "MELHORAR AGORA",
        "btn3": "CONTATO",
        "how_title": "Como funciona?",
        "step1_t": "Cole o Link",
        "step1_d": "Ou escreva.",
        "step2_t": "IA Analisa",
        "step2_d": "Motor Triplo.",
        "step3_t": "Venda",
        "step3_d": "Copie e publique.",
        "stat1": "Otimizados",
        "stat2": "Tempo",
        "stat3": "Conversão",
        "test_title": "Especialistas",
        "test1_txt": "Vendas subiram 50%.",
        "test1_au": "Carlos R.",
        "test2_txt": "Economizo horas.",
        "test2_au": "Ana M.",
        "test3_txt": "Vital para agência.",
        "test3_au": "Luis P.",
        "foot_desc": "IA Imobiliária.",
        "mail_label": "📧 Email Profissional",
        "limit_msg": "🚫 Limite atingido.",
        "upgrade_msg": "Mude para PRO.",
        "lbl_tone": "Tom:",
        "lbl_lang_out": "Idioma:",
        "annual_toggle": "📅 Economize 20%",
        "annual_save": "✅ 2 Meses Grátis",
        "whatsapp": "Enviar WhatsApp",
        "download": "Baixar .txt",
        "copy_success": "Copiado!",
        "revoke": "Revogar",
        "manage_team": "👥 Equipe",
        "team_activity": "📈 Atividade",
        "refine_pl": "🔄 Ajuste rápido...",
        "social_title": "📱 Social Pack",
        "char_count": "Caracteres",
        "link_warn": "⚠️ Link não reconhecido.",
        "badge_free": "GRÁTIS",
        "badge_pro": "MEMBRO PRO",
        "badge_agency": "PARCEIRO AGÊNCIA",
        "api_soon": "API (Em breve)",
        "legal_title": "Termos e Privacidade",
        "logout": "Sair",
        "welcome": "Bem-vindo",
        "usage_bar": "Progresso Diário",
        "feedback_lbl": "💡 Sugestões / Suporte",
        "feedback_btn": "Enviar",
        "support_mail": "Suporte",
        "credits_left": "Créditos hoje:",
        "welcome_morn": "Bom dia",
        "welcome_aft": "Boa tarde",
        "welcome_eve": "Boa noite",
        "impact_text": "IMPACTO DE VENDAS AUMENTADO",
        "strategy_gen": "ESTRATÉGIA GERADA",
        "desc_luxury": "DESCRIÇÃO DE LUXO",
        "btn_refine": "Refinar",
        "analyzing_msg": "ANALISANDO PROPRIEDADE...",
        "feedback_success": "✅ Obrigado pelo feedback!",
        "tone_lux": "Luxo",
        "tone_prof": "Profissional",
        "tone_urg": "Urgência",
        "tone_story": "Storytelling",
        "emp_email_lbl": "Email do Agente",
        "emp_add_btn": "ADICIONAR",
        "sec_1": "SEÇÃO 1: DESCRIÇÃO PRINCIPAL",
        "sec_2": "SEÇÃO 2: FICHA TÉCNICA",
        "sec_3": "SEÇÃO 3: COPY WHATSAPP",
        "sec_4": "SEÇÃO 4: PACK SEO",
        "sec_short": "DESCRIÇÃO CURTA",
        "tab_team": "👥 Minha Equipe",
        "tab_monitor": "📊 Monitor",
        "monitor_desc": "Veja o consumo em tempo real.",
        "monitor_empty": "Sem dados ainda."
    },
    "Français": {
        "title1": "Transformez vos Annonces",
        "title2": "en Aimants",
        "sub": "L'outil IA secret des agents top.",
        "placeholder": "🏠 Décrivez la propriété...",
        "url_placeholder": "🔗 Collez le lien...",
        "btn_gen": "✨ GÉNÉRER STRATÉGIE",
        "p_destacada": "EN VEDETTE",
        "comunidad": "Communauté",
        "popular": "POPULAIRE",
        "plan1": "Initial",
        "plan2": "Pro",
        "plan3": "Agence",
        "desc1": "3 descriptions/jour",
        "t1_1": "Limite journalière.",
        "desc2": "Support De Base",
        "t1_2": "Aide par email.",
        "desc3": "Filigrane",
        "t1_3": "Inclut signature.",
        "desc4": "Illimité",
        "t2_1": "Sans limites.",
        "desc5": "Pack Social",
        "t2_2": "Scripts Insta/TikTok.",
        "desc6": "SEO Optimisé",
        "t2_3": "Mots-clés.",
        "desc7": "Bannière",
        "t2_4": "Rotation home.",
        "desc8": "5 Utilisateurs",
        "t3_1": "Accès équipe.",
        "desc9": "Tableau de Bord",
        "t3_2": "Gestion agents.",
        "desc10": "Accès API",
        "t3_3": "Bientôt.",
        "desc11": "Priorité",
        "t3_4": "Double exposition.",
        "btn1": "GRATUIT",
        "btn2": "UPGRADE",
        "btn3": "CONTACT",
        "how_title": "Comment ça marche?",
        "step1_t": "Lien",
        "step1_d": "Ou écrire.",
        "step2_t": "IA Analyse",
        "step2_d": "Moteur Triple.",
        "step3_t": "Vendez",
        "step3_d": "Copiez et publiez.",
        "stat1": "Optimisés",
        "stat2": "Temps",
        "stat3": "Conversion",
        "test_title": "Avis Experts",
        "test1_txt": "Ventes +50%.",
        "test1_au": "Carlos R.",
        "test2_txt": "Gain de temps.",
        "test2_au": "Ana M.",
        "test3_txt": "Vital pour agence.",
        "test3_au": "Luis P.",
        "foot_desc": "IA Immobilier.",
        "mail_label": "📧 Email Pro",
        "limit_msg": "🚫 Limite atteinte.",
        "upgrade_msg": "Passez PRO.",
        "lbl_tone": "Ton:",
        "lbl_lang_out": "Langue:",
        "annual_toggle": "📅 Économisez 20%",
        "annual_save": "✅ 2 Mois Gratuits",
        "whatsapp": "WhatsApp",
        "download": "Télécharger .txt",
        "copy_success": "Copié!",
        "revoke": "Révoquer",
        "manage_team": "👥 Équipe",
        "team_activity": "📈 Activité",
        "refine_pl": "🔄 Ajustement...",
        "social_title": "📱 Social Pack",
        "char_count": "Caractères",
        "link_warn": "⚠️ Lien non reconnu.",
        "badge_free": "GRATUIT",
        "badge_pro": "MEMBRE PRO",
        "badge_agency": "PARTENAIRE AGENCE",
        "api_soon": "API (Bientôt)",
        "legal_title": "Mentions Légales",
        "logout": "Déconnexion",
        "welcome": "Bienvenue",
        "usage_bar": "Progrès Quotidien",
        "feedback_lbl": "💡 Suggestions / Support",
        "feedback_btn": "Envoyer",
        "support_mail": "Support",
        "credits_left": "Crédits aujourd'hui:",
        "welcome_morn": "Bonjour",
        "welcome_aft": "Bonne après-midi",
        "welcome_eve": "Bonsoir",
        "impact_text": "IMPACT DE VENTE AUGMENTÉ",
        "strategy_gen": "STRATÉGIE GÉNÉRÉE",
        "desc_luxury": "DESCRIPTION DE LUXE",
        "btn_refine": "Raffiner",
        "analyzing_msg": "ANALYSE DE LA PROPRIÉTÉ...",
        "feedback_success": "✅ Merci pour vos commentaires!",
        "tone_lux": "Luxe",
        "tone_prof": "Professionnel",
        "tone_urg": "Urgence",
        "tone_story": "Storytelling",
        "emp_email_lbl": "Email Agent",
        "emp_add_btn": "AJOUTER",
        "sec_1": "SECTION 1: DESCRIPTION PRINCIPALE",
        "sec_2": "SECTION 2: FICHES TECHNIQUES",
        "sec_3": "SECTION 3: COPY WHATSAPP",
        "sec_4": "SECTION 4: PACK SEO",
        "sec_short": "DESCRIPTION COURTE",
        "tab_team": "👥 Mon Équipe",
        "tab_monitor": "📊 Moniteur",
        "monitor_desc": "Suivez la consommation en temps réel.",
        "monitor_empty": "Pas encore de données."
    },
    "Deutsch": {
        "title1": "Verwandeln Sie Anzeigen",
        "title2": "in Magnete",
        "sub": "Das geheime KI-Tool.",
        "placeholder": "🏠 Beschreibung...",
        "url_placeholder": "🔗 Link einfügen...",
        "btn_gen": "✨ STRATEGIE GENERIEREN",
        "p_destacada": "HIGHLIGHT",
        "comunidad": "Community",
        "popular": "BELIEBT",
        "plan1": "Start",
        "plan2": "Pro",
        "plan3": "Agentur",
        "desc1": "3 Texte/Tag",
        "t1_1": "Tageslimit.",
        "desc2": "Basis Support",
        "t1_2": "Hilfe per Mail.",
        "desc3": "Wasserzeichen",
        "t1_3": "Mit Signatur.",
        "desc4": "Unbegrenzt",
        "t2_1": "Keine Limits.",
        "desc5": "Social Pack",
        "t2_2": "Insta/TikTok.",
        "desc6": "SEO",
        "t2_3": "Keywords.",
        "desc7": "Banner",
        "t2_4": "Rotation.",
        "desc8": "5 Nutzer",
        "t3_1": "Team Zugriff.",
        "desc9": "Team Panel",
        "t3_2": "Verwaltung.",
        "desc10": "API",
        "t3_3": "Bald.",
        "desc11": "Priorität",
        "t3_4": "Doppelte Sichtbarkeit.",
        "btn1": "GRATIS",
        "btn2": "UPGRADE",
        "btn3": "KONTAKT",
        "how_title": "Wie funktioniert es?",
        "step1_t": "Link",
        "step1_d": "Oder Text.",
        "step2_t": "KI Analyse",
        "step2_d": "Triple Engine.",
        "step3_t": "Verkaufen",
        "step3_d": "Kopieren.",
        "stat1": "Optimiert",
        "stat2": "Zeit",
        "stat3": "Konversion",
        "test_title": "Experten",
        "test1_txt": "Umsatz +50%.",
        "test1_au": "Carlos R.",
        "test2_txt": "Zeit gespart.",
        "test2_au": "Ana M.",
        "test3_txt": "Wichtig für Agentur.",
        "test3_au": "Luis P.",
        "foot_desc": "Immo-KI.",
        "mail_label": "📧 E-Mail",
        "limit_msg": "🚫 Limit erreicht.",
        "upgrade_msg": "Upgrade auf PRO.",
        "lbl_tone": "Ton:",
        "lbl_lang_out": "Sprache:",
        "annual_toggle": "📅 Sparen Sie 20%",
        "annual_save": "✅ 2 Monate Gratis",
        "whatsapp": "WhatsApp",
        "download": "Download .txt",
        "copy_success": "Kopiert!",
        "revoke": "Widerrufen",
        "manage_team": "👥 Team",
        "team_activity": "📈 Aktivität",
        "refine_pl": "🔄 Anpassung...",
        "social_title": "📱 Social Pack",
        "char_count": "Zeichen",
        "link_warn": "⚠️ Link Fehler.",
        "badge_free": "GRATIS",
        "badge_pro": "PRO MITGLIED",
        "badge_agency": "AGENTUR PARTNER",
        "api_soon": "API (Bald)",
        "legal_title": "Rechtliches",
        "logout": "Abmelden",
        "welcome": "Willkommen",
        "usage_bar": "Täglicher Fortschritt",
        "feedback_lbl": "💡 Vorschläge / Support",
        "feedback_btn": "Senden",
        "support_mail": "Support",
        "credits_left": "Credits heute:",
        "welcome_morn": "Guten Morgen",
        "welcome_aft": "Guten Tag",
        "welcome_eve": "Guten Abend",
        "impact_text": "VERKAUFSIMPAKT GESTEIGERT",
        "strategy_gen": "STRATEGIE GENERIERT",
        "desc_luxury": "LUXUS BESCHREIBUNG",
        "btn_refine": "Verfeinern",
        "analyzing_msg": "IMMOBILIE WIRD ANALYSIERT...",
        "feedback_success": "✅ Danke für Ihr Feedback!",
        "tone_lux": "Luxus",
        "tone_prof": "Professionell",
        "tone_urg": "Dringlichkeit",
        "tone_story": "Storytelling",
        "emp_email_lbl": "Agent E-Mail",
        "emp_add_btn": "HINZUFÜGEN",
        "sec_1": "TEIL 1: HAUPTBESCHREIBUNG",
        "sec_2": "TEIL 2: TECHNISCHE DATEN",
        "sec_3": "TEIL 3: WHATSAPP COPY",
        "sec_4": "TEIL 4: SEO PACK",
        "sec_short": "KURZE BESCHREIBUNG",
        "tab_team": "👥 Mein Team",
        "tab_monitor": "📊 Monitor",
        "monitor_desc": "Echtzeit-Verbrauch.",
        "monitor_empty": "Keine Daten."
    },
    "中文": {
        "title1": "将枯燥的广告",
        "title2": "转化为销售磁铁",
        "sub": "顶级经纪人的秘密工具。",
        "placeholder": "🏠 描述...",
        "url_placeholder": "🔗 粘贴链接...",
        "btn_gen": "✨ 生成策略",
        "p_destacada": "精选",
        "comunidad": "社区",
        "popular": "最受欢迎",
        "plan1": "基础",
        "plan2": "专业",
        "plan3": "机构",
        "desc1": "每天3条",
        "t1_1": "每日限制。",
        "desc2": "基础支持",
        "t1_2": "邮件帮助。",
        "desc3": "水印",
        "t1_3": "包含签名。",
        "desc4": "无限生成",
        "t2_1": "无限制。",
        "desc5": "社交包",
        "t2_2": "Insta/TikTok。",
        "desc6": "SEO优化",
        "t2_3": "关键词。",
        "desc7": "横幅",
        "t2_4": "主页轮播。",
        "desc8": "5个用户",
        "t3_1": "团队访问。",
        "desc9": "团队面板",
        "t3_2": "管理。",
        "desc10": "API",
        "t3_3": "即将推出。",
        "desc11": "优先展示",
        "t3_4": "双倍曝光。",
        "btn1": "免费注册",
        "btn2": "升级",
        "btn3": "联系",
        "how_title": "如何运作?",
        "step1_t": "链接",
        "step1_d": "或文字。",
        "step2_t": "AI分析",
        "step2_d": "三重引擎。",
        "step3_t": "销售",
        "step3_d": "复制发布。",
        "stat1": "已优化",
        "stat2": "时间",
        "stat3": "转化",
        "test_title": "专家评价",
        "test1_txt": "销售额+50%。",
        "test1_au": "Carlos R.",
        "test2_txt": "节省时间。",
        "test2_au": "Ana M.",
        "test3_txt": "机构必备。",
        "test3_au": "Luis P.",
        "foot_desc": "房地产AI。",
        "mail_label": "📧 邮箱",
        "limit_msg": "🚫 限制已达。",
        "upgrade_msg": "升级PRO。",
        "lbl_tone": "语气:",
        "lbl_lang_out": "语言:",
        "annual_toggle": "📅 节省 20%",
        "annual_save": "✅ 免费2个月",
        "whatsapp": "WhatsApp",
        "download": "下载 .txt",
        "copy_success": "已复制!",
        "revoke": "撤销",
        "manage_team": "👥 团队",
        "team_activity": "📈 活动",
        "refine_pl": "🔄 调整...",
        "social_title": "📱 社交媒体",
        "char_count": "字数",
        "link_warn": "⚠️ 链接错误。",
        "badge_free": "免费用户",
        "badge_pro": "专业会员",
        "badge_agency": "机构伙伴",
        "api_soon": "API (即将推出)",
        "legal_title": "条款和隐私",
        "logout": "退出",
        "welcome": "欢迎",
        "usage_bar": "每日进度",
        "feedback_lbl": "💡 反馈 / 支持",
        "feedback_btn": "发送反馈",
        "support_mail": "支持",
        "credits_left": "今日额度:",
        "welcome_morn": "早上好",
        "welcome_aft": "下午好",
        "welcome_eve": "晚上好",
        "impact_text": "销售影响力提升",
        "strategy_gen": "生成策略",
        "desc_luxury": "豪华描述",
        "btn_refine": "完善",
        "analyzing_msg": "正在分析属性...",
        "feedback_success": "✅ 谢谢！您的反馈已保存。",
        "tone_lux": "豪华",
        "tone_prof": "专业",
        "tone_urg": "紧迫感",
        "tone_story": "讲故事",
        "emp_email_lbl": "代理邮箱",
        "emp_add_btn": "添加",
        "sec_1": "第1部分：主要描述",
        "sec_2": "第2部分：技术规格",
        "sec_3": "第3部分：WhatsApp文案",
        "sec_4": "第4部分：SEO包",
        "sec_short": "简短描述",
        "tab_team": "👥 我的团队",
        "tab_monitor": "📊 监控",
        "monitor_desc": "实时查看消耗。",
        "monitor_empty": "暂无数据。"
    }
}

# ==============================================================================
# 5. ESTILOS CSS PLATINUM (BLINDAJE VISUAL - CÓDIGO EXTENDIDO)
# ==============================================================================

st.markdown("""
<style>
    /* 1. FIX DEL SCROLL SUPERIOR (PADDING REMOVIDO) */
    .block-container {
        padding-top: 1rem !important; 
        padding-bottom: 5rem !important;
    }

    /* 2. RESET Y FONDO GLOBAL */
    .stApp { 
        background-color: #0e1117; 
        color: #FFFFFF; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }
    
    /* 3. ELIMINAR GHOST LINKS DE STREAMLIT (CRÍTICO) */
    .stMarkdown h1 a, 
    .stMarkdown h2 a, 
    .stMarkdown h3 a, 
    .stMarkdown h4 a { 
        display: none !important; 
    }
    
    .stMarkdown a { 
        text-decoration: none !important; 
        color: inherit !important; 
        pointer-events: none !important; 
    }
    
    [data-testid="stHeader"] { 
        background: rgba(0,0,0,0); 
    }
    
    #MainMenu { 
        visibility: hidden; 
    }
    
    footer { 
        visibility: hidden; 
    }

    /* 4. SCROLLBAR DE LUJO */
    ::-webkit-scrollbar { 
        width: 6px; 
    }
    
    ::-webkit-scrollbar-track { 
        background: #0e1117; 
    }
    
    ::-webkit-scrollbar-thumb { 
        background: #333; 
        border-radius: 10px; 
    }
    
    ::-webkit-scrollbar-thumb:hover { 
        background: #00d2ff; 
    }

    /* 5. SELECCIÓN DE TEXTO NEÓN */
    ::selection { 
        background: rgba(0, 210, 255, 0.25); 
        color: #00d2ff; 
    }

    /* 6. TIPOGRAFÍA Y TÍTULOS */
    .neon-title { 
        font-size: 3.8rem; 
        font-weight: 800; 
        text-align: center; 
        margin-top: 20px; 
        color: white; 
        text-shadow: 0 0 30px rgba(0, 210, 255, 0.5); 
    }
    
    .neon-highlight { 
        color: #00d2ff; 
        text-shadow: 0 0 45px rgba(0, 210, 255, 0.8); 
    }
    
    .subtitle { 
        text-align: center; 
        font-size: 1.2rem; 
        color: #aaa; 
        margin-bottom: 40px; 
    }

    /* 7. HUD SUPERIOR (IDENTIDAD) */
    .hud-bar { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 15px 30px; 
        background: rgba(255,255,255,0.02); 
        border-bottom: 1px solid rgba(0,210,255,0.15); 
        border-radius: 20px; 
        margin-bottom: 35px; 
        backdrop-filter: blur(10px); 
    }
    
    .badge-neon { 
        padding: 6px 18px; 
        border-radius: 25px; 
        font-size: 0.75rem; 
        font-weight: 900; 
        border: 1px solid; 
        text-transform: uppercase; 
        letter-spacing: 1px; 
    }
    
    .badge-free { 
        border-color: #aaa; 
        color: #aaa; 
    }
    
    .badge-pro { 
        border-color: #00d2ff; 
        color: #00d2ff; 
        box-shadow: 0 0 15px rgba(0,210,255,0.3); 
    }
    
    /* FIX: AGENCIA VIOLETA (#DDA0DD) RESTAURADO */
    .badge-agency { 
        border-color: #DDA0DD; 
        color: #DDA0DD; 
        box-shadow: 0 0 15px rgba(221, 160, 221, 0.4); 
    }

    /* 8. CAJA DE RESULTADO ELEGANTE (LUXURY DARK) CON BORDE VIOLETA */
    .result-container {
        background: rgba(20, 20, 20, 0.95);
        color: #f0f0f0;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 4px solid #DDA0DD;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-top: 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.8);
        backdrop-filter: blur(10px);
    }

    /* 9. BOTÓN GENERAR PLATINUM */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; 
        border: none !important; 
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4) !important; 
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important; 
        color: white !important; 
        font-weight: 700 !important; 
        height: 3.8rem !important; 
        width: 100% !important;
        border-radius: 12px !important; 
        text-transform: uppercase;
    }
    
    div.stButton > button[kind="primary"]:hover { 
        background: #000000 !important; 
        color: #ffffff !important; 
        transform: scale(1.03) translateY(-2px) !important; 
        box-shadow: 0 0 50px rgba(0, 210, 255, 1), 0 0 20px rgba(0, 210, 255, 0.6) !important; 
        border: 2px solid #00d2ff !important; 
    }

    /* 10. TARJETAS DE PLANES - ALTO RENDIMIENTO Y FLUIDEZ */
    .card-wrapper { 
        transition: transform 0.3s ease-out, box-shadow 0.3s ease-out; 
        border-radius: 12px; 
        height: 480px; 
        margin-bottom: 25px;
        position: relative;
        will-change: transform;
    }
    
    .card-wrapper:hover { 
        transform: translateY(-10px); 
    }
    
    .glass-container { 
        background: rgba(30, 31, 38, 0.95); 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 12px; 
        padding: 25px; 
        text-align: center; 
        position: relative; 
        height: 100%; 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        gap: 15px; 
    }
    
    .free-card:hover { 
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4); 
    }
    
    .pro-card { 
        border: 1px solid rgba(0, 210, 255, 0.3) !important; 
    }
    
    .pro-card:hover { 
        border: 1px solid rgba(0, 210, 255, 0.6) !important; 
        box-shadow: 0 10px 30px rgba(0, 210, 255, 0.3); 
    }
    
    /* FIX: AGENCIA CARD VIOLETA */
    .agency-card { 
        border: 1px solid rgba(221, 160, 221, 0.3) !important; 
    }
    
    .agency-card:hover { 
        border: 1px solid rgba(221, 160, 221, 0.6) !important; 
        box-shadow: 0 10px 30px rgba(221, 160, 221, 0.3); 
    }

    .popular-badge { 
        position: absolute; 
        top: -12px; 
        left: 50%; 
        transform: translateX(-50%); 
        background-color: #00d2ff; 
        color: black; 
        padding: 6px 18px; 
        border-radius: 20px; 
        font-weight: 900; 
        font-size: 0.85rem; 
        z-index: 10; 
        transition: background 0.2s ease; 
    }

    .card-wrapper:hover .popular-badge {
        background-color: #fff;
    }

    /* 11. TOOLTIPS DE AYUDA */
    .info-icon { 
        display: inline-block; 
        width: 16px; 
        height: 16px; 
        border-radius: 50%; 
        text-align: center; 
        font-size: 11px; 
        line-height: 16px; 
        margin-left: 8px; 
        cursor: help; 
        position: relative; 
        font-weight: bold; 
    }
    
    .i-free { 
        background-color: rgba(255, 255, 255, 0.1); 
        color: #fff; 
        border: 1px solid rgba(255, 255, 255, 0.3); 
    }
    .i-pro { 
        background-color: rgba(0, 210, 255, 0.15); 
        color: #00d2ff; 
        border: 1px solid rgba(0, 210, 255, 0.5); 
    }
    .i-agency { 
        background-color: rgba(221, 160, 221, 0.15); 
        color: #DDA0DD; 
        border: 1px solid rgba(221, 160, 221, 0.5); 
    }
    
    .info-icon:hover::after {
        content: attr(data-tooltip); 
        position: absolute; 
        bottom: 30px; 
        left: 50%; 
        transform: translateX(-50%); 
        background-color: #1a1c23; 
        color: #fff; 
        padding: 12px 16px; 
        border-radius: 8px; 
        font-size: 12px; 
        width: 230px; 
        z-index: 999; 
        box-shadow: 0 10px 40px rgba(0,0,0,0.9); 
        border: 1px solid rgba(255,255,255,0.1); 
        line-height: 1.5; 
        text-align: left; 
        font-weight: normal; 
    }

    .feature-list { 
        text-align: left; 
        margin: 15px auto; 
        display: inline-block; 
        font-size: 0.95rem; 
        color: #ddd; 
        line-height: 2.0; 
    }
    
    /* 12. BANNER ANIMADO DE FONDO */
    .video-placeholder {
        border-radius: 12px; 
        height: 250px; 
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
    }
    
    .dynamic-tag { 
        position: absolute; 
        top: 15px; 
        left: 15px; 
        color: black; 
        padding: 5px 14px; 
        border-radius: 4px; 
        font-size: 0.75rem; 
        font-weight: 900; 
        transition: background-color 0.8s ease; 
        animation: tagColorChange 24s infinite alternate; 
    }

    @keyframes auraChange { 
        0%, 70% { box-shadow: 0 0 45px rgba(0, 210, 255, 0.5); border-color: rgba(0, 210, 255, 0.4); } 
        75%, 100% { box-shadow: 0 0 45px rgba(221, 160, 221, 0.5); border-color: rgba(221, 160, 221, 0.4); } 
    }
    
    @keyframes tagColorChange { 
        0%, 70% { background: rgba(0, 210, 255, 1); } 
        75%, 100% { background: rgba(221, 160, 221, 1); } 
    }
    
    @keyframes adCarousel { 
        0%, 20% { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80'); opacity: 1; } 
        30%, 45% { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80'); opacity: 1; } 
        55%, 70% { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80'); opacity: 1; } 
        80%, 100% { background-image: url('https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?auto=format&fit=crop&w=800&q=80'); opacity: 1; } 
    }
    
    @keyframes float { 
        0% { transform: translateY(0px); } 
        50% { transform: translateY(-12px); } 
        100% { transform: translateY(0px); } 
    }

    /* 13. BARRA DE IMPACTO (DORADA COMPLETA, VIOLETA EN SOMBRA) */
    .meter-container { 
        background: #111; 
        border-radius: 10px; 
        height: 40px; 
        width: 100%; 
        position: relative; 
        overflow: hidden; 
        margin-top: 10px; 
        border: 1px solid #444; 
    }
    
    .meter-fill { 
        height: 100%; 
        background: linear-gradient(90deg, #B8860B, #FFD700, #F0E68C); 
        width: 0%; 
        animation: fillMeter 2s ease-out forwards; 
        box-shadow: 0 0 15px #FFD700;
    }
    
    .meter-text { 
        position: absolute; 
        width: 100%; 
        text-align: center; 
        top: 8px; 
        font-weight: 800; 
        color: #000; 
        text-shadow: 0px 0px 2px rgba(255,255,255,0.7); 
        font-size: 1rem; 
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    @keyframes fillMeter { 
        from { width: 0%; } 
        to { width: 100%; } 
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. SIDEBAR PROFESIONAL Y NAVEGACIÓN
# ==============================================================================

with st.sidebar:
    st.markdown('<div style="text-align:center; font-size: 1.6rem; font-weight: 800; color: #fff; letter-spacing: 1px;">🏢 AI REALTY</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Selector de Idioma en Sidebar
    idioma_selec = st.selectbox("🌐 Idioma / Language", list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma))
    st.session_state.idioma = idioma_selec
    L = traducciones[st.session_state.idioma]

    # Perfil del Usuario y Logout
    if st.session_state.email_usuario:
        st.markdown(f"### {L.get('welcome', 'Bienvenido')}")
        st.markdown(f"**{st.session_state.email_usuario}**")
        
        # --- CONTADOR DE CRÉDITOS VISIBLE ---
        usos = st.session_state.usos
        es_pro_local = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite = 99999 if es_pro_local else 3
        
        # Color rojo si queda poco, verde si hay mucho
        color_cred = "#ff4b4b" if (not es_pro_local and 3-usos <= 1) else "#00d2ff"
        restantes = "∞" if es_pro_local else str(3 - usos)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; border: 1px solid {color_cred}; margin-bottom: 10px;">
            <div style="font-size: 0.85rem; color: #aaa;">{L.get('credits_left', 'Créditos restantes:')}</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: {color_cred};">{restantes}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if limite < 100:
            progreso = min(usos / limite, 1.0)
            st.progress(progreso)
        else:
            st.progress(1.0) 
            
        st.markdown("---")
        
        # BOTÓN LOGOUT (CERRAR SESIÓN)
        if st.button(f"🚪 {L.get('logout', 'Cerrar Sesión')}"):
            try:
                cookie_manager.delete("user_email")
            except:
                pass # Si no existe, no falla
            st.session_state.email_usuario = ""
            st.session_state.usos = 0
            st.rerun()

    # --- ZONA DE SOPORTE & FEEDBACK (NUEVO) ---
    st.markdown("---")
    st.subheader(L.get("feedback_lbl", "💡 Ayuda / Soporte"))
    
    st.markdown(f"📧 **{L.get('support_mail', 'Soporte')}: support@airealtypro.com**")
    
    # Text Area del Feedback
    fb_text = st.text_area("", placeholder=L.get("feedback_lbl", "Escribe tu sugerencia o error..."), height=100, label_visibility="collapsed", key="fb_input")
    
    if st.button(L.get("feedback_btn", "Enviar"), use_container_width=True):
        if fb_text:
            with st.spinner("Enviando..."):
                ok = guardar_feedback(st.session_state.email_usuario, fb_text)
                if ok:
                    st.toast(L["feedback_success"])
                else:
                    st.error("Error al guardar. Verifica la hoja 'Feedback'.")
        else:
            st.warning("El mensaje está vacío.")
            
    st.markdown("---")
    st.markdown(f"<div style='text-align:center; color:#666; font-size:0.8rem;'>v2.7 Final Build</div>", unsafe_allow_html=True)

# ==============================================================================
# 7. INTERFAZ: CABECERA Y HUD DE IDENTIDAD
# ==============================================================================

# RESTAURACIÓN DEL TÍTULO PRINCIPAL EN PANTALLA
col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo:
    st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 AI REALTY PRO</div>', unsafe_allow_html=True)

# HUD DE IDENTIDAD (DINÁMICO SEGÚN PLAN Y HORA)
if st.session_state.email_usuario:
    # --- RE-VERIFICACIÓN SILENCIOSA DE PLAN EN CADA CARGA ---
    try:
        df_check = obtener_datos_db()
        if st.session_state.email_usuario in df_check['email'].values:
            user_row = df_check[df_check['email'] == st.session_state.email_usuario].iloc[0]
            real_plan = user_row['plan'] if 'plan' in user_row else 'Gratis'
            # Normalizamos mayúsculas
            st.session_state.plan_usuario = real_plan.title() if real_plan else "Gratis"
            st.session_state.usos = int(user_row['usos'])
    except Exception as e:
        pass # Si falla la verificación silenciosa, usamos la sesión actual

    hora = datetime.now().hour
    # FIX: TRADUCCIÓN DEL SALUDO
    saludo = L["welcome_morn"]
    if hora >= 12 and hora < 19:
        saludo = L["welcome_aft"]
    elif hora >= 19:
        saludo = L["welcome_eve"]

    p_name = str(st.session_state.plan_usuario).lower()
    
    if "agencia" in p_name or "agency" in p_name: 
        badge_cls = "badge-agency"
        badge_txt = L.get("badge_agency", "AGENCIA")
    elif "pro" in p_name: 
        badge_cls = "badge-pro"
        badge_txt = L.get("badge_pro", "PRO")
    else: 
        badge_cls = "badge-free"
        badge_txt = L.get("badge_free", "GRATIS")
    
    st.markdown(f'''
        <div class="hud-bar">
            <div>👋 <b>{saludo}</b>, <span style="color:#00d2ff;">{st.session_state.email_usuario}</span></div>
            <div class="badge-neon {badge_cls}">{badge_txt}</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)

# --- BANNER DE IMÁGENES GLOBAL (TAMAÑO NORMAL CORREGIDO) ---
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    st.markdown(f'''
        <div class="video-placeholder">
            <div class="dynamic-tag">{L["p_destacada"]}</div>
            <div style="background:rgba(0,0,0,0.6);width:100%;text-align:center;padding:10px;">{L["comunidad"]}</div>
        </div>
    ''', unsafe_allow_html=True)
 
# ==============================================================================
# 8. LÓGICA DE NEGOCIO PRINCIPAL
# ==============================================================================

# --- VERIFICACIÓN DE COOKIE AL INICIO ---
if not st.session_state.email_usuario:
    cookie_val = cookie_manager.get("user_email")
    if cookie_val:
        st.session_state.email_usuario = cookie_val
        df_actual = obtener_datos_db()
        if cookie_val in df_actual['email'].values:
            usuario = df_actual[df_actual['email'] == cookie_val].iloc[0]
            st.session_state.usos = int(usuario['usos'])
            st.session_state.plan_usuario = usuario['plan']
        st.rerun()

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # --- PANTALLA DE LOGIN ---
    if not st.session_state.email_usuario:
        st.markdown('<div class="glass-container" style="height:auto; box-shadow: 0 0 30px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
        
        email_input = st.text_input(L["mail_label"], placeholder="email@ejemplo.com", key="user_email")
        if st.button("START / ENTRAR", type="primary"):
            if email_input and "@" in email_input:
                st.session_state.email_usuario = email_input.strip().lower()
                try:
                    cookie_manager.set("user_email", st.session_state.email_usuario, expires_at=datetime.now().replace(year=datetime.now().year + 1))
                except:
                    pass
                
                df_actual = obtener_datos_db()
                df_emp = obtener_empleados_db()
                
                # CHECK 1: ¿Es un usuario directo?
                if st.session_state.email_usuario in df_actual['email'].values:
                    usuario = df_actual[df_actual['email'] == st.session_state.email_usuario].iloc[0]
                    st.session_state.usos = int(usuario['usos'])
                    st.session_state.plan_usuario = usuario['plan'] if 'plan' in usuario else 'Gratis'
                    st.session_state.es_empleado = False
                
                # CHECK 2: ¿Es un empleado?
                elif st.session_state.email_usuario in df_emp['EmployeeEmail'].values:
                    jefe_email = df_emp[df_emp['EmployeeEmail'] == st.session_state.email_usuario].iloc[0]['BossEmail']
                    datos_jefe = df_actual[df_actual['email'] == jefe_email].iloc[0]
                    st.session_state.usos = 0
                    
                    # FIX CRÍTICO: Lógica de Plan Empleado (Multilenguaje)
                    plan_jefe_raw = str(datos_jefe['plan']).strip()
                    
                    # Lista de valores aceptados para que el empleado sea PRO
                    planes_agencia_validos = ["Agencia", "Agency", "Agency Partner", "Socio Agencia", "Pro Agency"]
                    
                    if any(p.lower() == plan_jefe_raw.lower() for p in planes_agencia_validos):
                        st.session_state.plan_usuario = "Pro"
                    else:
                        # Si no es agencia, hereda el plan tal cual (ej: Pro -> Pro)
                        st.session_state.plan_usuario = plan_jefe_raw.title()
                        
                    st.session_state.es_empleado = True
                    st.session_state.boss_ref = jefe_email
                else:
                    st.session_state.usos = 0
                    st.session_state.plan_usuario = "Gratis"
                
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Please enter a valid email.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MOTOR DE GENERACIÓN IA PLATINUM ---
    elif st.session_state.email_usuario:
        es_pro = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite_usos = 99999 if es_pro else 3
        
        if st.session_state.usos < limite_usos:
            st.markdown('<div class="glass-container" style="height:auto;">', unsafe_allow_html=True)
            col_t1, col_t2 = st.columns(2)
            
            # FIX: Opciones traducidas
            with col_t1: 
                tono_display = st.selectbox(L.get("lbl_tone", "Tono:"), [L["tone_story"], L["tone_prof"], L["tone_urg"], L["tone_lux"]])
                
                # Mapeo inverso para lógica interna
                mapa_tonos = {
                    L["tone_story"]: "Storytelling",
                    L["tone_prof"]: "Profesional",
                    L["tone_urg"]: "Urgencia",
                    L["tone_lux"]: "Lujo"
                }
                tono = mapa_tonos.get(tono_display, "Lujo")
                
            with col_t2: 
                idioma_salida = st.selectbox(L.get("lbl_lang_out", "Idioma:"), list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma))

            url_input = st.text_input("", placeholder=L["placeholder"].split(" ")[0] + " Link...", label_visibility="collapsed")
            user_input = st.text_area("", placeholder=L['placeholder'], key="input_ia", label_visibility="collapsed", height=150)
            
            st.caption(f"{L.get('char_count', 'Caracteres')}: {len(user_input)}")

            if st.button(L['btn_gen'], key="main_gen", type="primary"):
                if user_input or url_input: 
                    # FIX: Cartel de carga traducido
                    with st.spinner(f"🚀 {L['analyzing_msg']}"):
                        
                        datos_web, es_valido = extraer_datos_inmueble(url_input) if url_input else ("", True)
                        if not es_valido:
                            st.toast(L["link_warn"], icon="⚠️")
                        
                        # Ajustes de Tono
                        if tono == "Profesional":
                            instrucciones_estilo = "STYLE: Corporate, direct, serious. Use data, lists."
                        elif tono == "Storytelling":
                            instrucciones_estilo = "STYLE: Narrative, emotional, sensory. Describe smells, light."
                        elif tono == "Urgencia":
                            instrucciones_estilo = "STYLE: Scarcity triggers. Short sentences. 'Unique opportunity'."
                        else: # Lujo
                            instrucciones_estilo = "STYLE: Exclusive, sophisticated, high-ticket vocabulary."

                        instrucciones_variedad = "RULE: Do NOT use clichés like 'Imagine waking up'. Be original."
                        
                        # FIX: Secciones traducidas dinámicamente desde el diccionario L
                        sec_1_txt = L.get("sec_1", "SECTION 1")
                        sec_2_txt = L.get("sec_2", "SECTION 2")
                        sec_3_txt = L.get("sec_3", "SECTION 3")
                        sec_4_txt = L.get("sec_4", "SECTION 4")
                        sec_short = L.get("sec_short", "SHORT DESCRIPTION")

                        if es_pro:
                            instrucciones_plan = f"""
                            GENERATE FULL STRATEGY:
                            {sec_1_txt} ({tono.upper()})
                            {sec_2_txt} (Technical Bullets)
                            {sec_3_txt} (Persuasive w/ emojis)
                            {sec_4_txt} (Title <60 chars, Meta <160 chars)
                            """
                        else:
                            instrucciones_plan = f"""
                            GENERATE ONLY:
                            {sec_short} (Standard style, max 2 paragraphs)
                            At the end append strictly: "{L['desc3']}"
                            """

                        prompt_base = f"""
                        ACT AS: World Class Real Estate Copywriter.
                        OUTPUT LANGUAGE: {idioma_salida}. 
                        
                        {instrucciones_estilo}
                        {instrucciones_variedad}
                        
                        PROPERTY DATA (WEB): {datos_web}
                        MANUAL DATA: {user_input}
                        
                        SAFETY RULE: If WEB DATA says 'ERROR' and no manual data, return an error message only.
                        
                        OUTPUT INSTRUCTIONS:
                        {instrucciones_plan}
                        
                        FORMAT: Markdown with bolding.
                        """
                        
                        resultado = generar_texto(prompt_base)
                        
                        if "ERROR_TECNICO" not in resultado:
                            st.session_state.last_result = resultado
                            st.session_state.usos += 1
                            actualizar_usos_db(st.session_state.email_usuario, st.session_state.usos, st.session_state.plan_usuario)
                            guardar_historial(st.session_state.email_usuario, f"{url_input} {user_input}", resultado)
                            st.cache_data.clear()
                            st.rerun()
                else:
                    st.warning("Please enter a link or description.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # --- VISUALIZACIÓN DE RESULTADOS ---
            if st.session_state.last_result:
                
                # FIX: BARRA DE IMPACTO DORADA Y TRADUCIDA
                st.markdown(f"""
                <div class="meter-container">
                    <div class="meter-fill"></div>
                    <div class="meter-text">{L['impact_text']}</div>
                </div>
                """, unsafe_allow_html=True)

                # FIX: RESULTADO LUXURY DARK
                st.markdown(f'''
                    <div class="result-container">
                        <div style="color: #DDA0DD; font-weight: 800; margin-bottom: 15px; letter-spacing: 1.5px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:10px;">
                            {L['strategy_gen']} ({st.session_state.plan_usuario.upper()})
                        </div>
                        <div style="font-size: 1.05rem;">
                            {st.session_state.last_result.replace("\n", "<br>")}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # COLUMNAS DE ACCIÓN (FIXED ALIGNMENT)
                b1, b2, b3 = st.columns(3)
                
                with b1:
                    if st.button(f"📋 COPY"):
                        if hasattr(st, "copy_to_clipboard"):
                            st.copy_to_clipboard(st.session_state.last_result)
                            st.toast(L["copy_success"])
                        else:
                            st.info("Copy text above")
                            st.code(st.session_state.last_result)
                
                with b2:
                    wa_msg = urllib.parse.quote(st.session_state.last_result[:900])
                    st.link_button(f"📲 {L['whatsapp']}", f"https://wa.me/?text={wa_msg}", use_container_width=True)
                
                with b3:
                    st.download_button(f"💾 {L['download']}", st.session_state.last_result, file_name=f"Strategy_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)

                if es_pro:
                    st.markdown("---")
                    with st.expander(f"📱 {L.get('social_title', 'Social Pack')}"):
                        with st.spinner("Generating viral content..."):
                            res_social = generar_texto(f"Create IG Post with hashtags and TikTok Script (15s) for: {st.session_state.last_result}")
                            st.markdown(res_social)
                
                st.divider()
                refine = st.text_input("", placeholder=L.get("refine_pl", "Quick adjust..."))
                
                # FIX: Botón Refinar traducido
                if st.button(L["btn_refine"]):
                    with st.spinner("Refining..."):
                        nuevo_res = generar_texto(f"Adjust this text: {st.session_state.last_result}. User request: {refine}")
                        st.session_state.last_result = nuevo_res
                        st.rerun()

        else:
            # PAYWALL
            st.error(L["limit_msg"])
            st.markdown(f"#### {L['upgrade_msg']}")
            paypal_bloqueo = f"""<div id="pb"></div><script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script><script>paypal.Buttons({{style:{{shape:'pill',color:'blue',layout:'horizontal',label:'subscribe'}},createSubscription:function(d,a){{return a.subscription.create({{'plan_id':'P-3P2657040E401734NNFQQ5TY','custom_id':'{st.session_state.email_usuario}'}});}}}}).render('#pb');</script>"""
            components.html(paypal_bloqueo, height=100)

# ==============================================================================
# 9. CONSOLA DE AGENCIA
# ==============================================================================

if st.session_state.plan_usuario == "Agencia" and not st.session_state.es_empleado:
    st.divider()
    st.subheader(L["manage_team"])
    
    # FIX: Pestañas traducidas
    tab_equipo, tab_monitor = st.tabs([L["tab_team"], L["tab_monitor"]])
    
    df_emp = obtener_empleados_db()
    mi_equipo = df_emp[df_emp['BossEmail'] == st.session_state.email_usuario]['EmployeeEmail'].tolist()
    
    with tab_equipo:
        c_add1, c_add2 = st.columns([3, 1])
        with c_add1: 
            # FIX: Placeholder traducido
            nuevo_e = st.text_input(L["emp_email_lbl"], key="new_ag_in", placeholder="agent@agency.com")
        with c_add2:
            st.write(" ")
            # FIX: Botón traducido
            if st.button(L["emp_add_btn"]):
                if len(mi_equipo) < 4 and "@" in nuevo_e:
                    new_row = pd.DataFrame({"BossEmail": [st.session_state.email_usuario], "EmployeeEmail": [nuevo_e.strip().lower()]})
                    conn.update(worksheet="Employees", data=pd.concat([df_emp, new_row], ignore_index=True))
                    st.rerun()
                elif len(mi_equipo) >= 4:
                    st.warning("Full Team (Max 4).")
        
        if mi_equipo:
            st.write("---")
            st.write(f"**{L['tab_team']}:**")
            for miembro in mi_equipo:
                cm1, cm2 = st.columns([3, 1])
                cm1.write(f"👤 {miembro}")
                
                if cm2.button(L["revoke"], key=f"del_{miembro}"):
                    df_limpio = df_emp[~((df_emp['BossEmail'] == st.session_state.email_usuario) & (df_emp['EmployeeEmail'] == miembro))]
                    conn.update(worksheet="Employees", data=df_limpio)
                    st.toast(f"Revoked: {miembro}")
                    st.rerun()
    
    with tab_monitor:
        st.info(L["monitor_desc"])
        if mi_equipo:
            df_total = obtener_datos_db()
            empleados_stats = df_total[df_total['email'].isin(mi_equipo)][['email', 'usos']]
            if not empleados_stats.empty:
                st.dataframe(empleados_stats, use_container_width=True)
            else:
                st.write(L["monitor_empty"])

# ==============================================================================
# 10. SECCIÓN INFORMATIVA Y PLANES DE SUSCRIPCIÓN
# ==============================================================================

st.markdown(f"<br><br><h2 style='text-align:center; color:white;'>{L['how_title']}</h2>", unsafe_allow_html=True)

# Pasos de funcionamiento
ch1, ch2, ch3 = st.columns(3)
with ch1: 
    st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>1</h1><p><b>{L['step1_t']}</b><br>{L['step1_d']}</p></div>", unsafe_allow_html=True)
with ch2: 
    st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>2</h1><p><b>{L['step2_t']}</b><br>{L['step2_d']}</p></div>", unsafe_allow_html=True)
with ch3: 
    st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>3</h1><p><b>{L['step3_t']}</b><br>{L['step3_d']}</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Estadísticas
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1: 
    st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">+10k</h2><p style="color:#aaa; font-size:0.9rem;">{L["stat1"]}</p></div>', unsafe_allow_html=True)
with col_stat2: 
    st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">-80%</h2><p style="color:#aaa; font-size:0.9rem;">{L["stat2"]}</p></div>', unsafe_allow_html=True)
with col_stat3: 
    st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">+45%</h2><p style="color:#aaa; font-size:0.9rem;">{L["stat3"]}</p></div>', unsafe_allow_html=True)

# --- SECCIÓN DE PLANES CON SWITCH ANUAL ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Plans</h3>", unsafe_allow_html=True)

# SWITCH ANUAL (Lógica de Descuento)
col_sw1, col_sw2, col_sw3 = st.columns([1,2,1])
with col_sw2:
    es_anual = st.toggle(L["annual_toggle"], value=False)

# VARIABLES DE PRECIO DINÁMICAS
precio_pro = "490" if es_anual else "49"
precio_age = "1,990" if es_anual else "199"

# IDs DE PAYPAL REALES (Configurados Anual vs Mensual)
id_pro = "P-2PU023636P1209345NFQ7TMY" if es_anual else "P-3P2657040E401734NNFQQ5TY"
id_age = "P-87X83840151393810NFQ7X6Q" if es_anual else "P-0S451470G5041550ENFQRB4I"

ahorro_txt = L["annual_save"] if es_anual else ""

col1, col2, col3 = st.columns(3)

# PLAN GRATIS (BOTÓN OCULTO SI YA ESTÁ LOGUEADO)
with col1:
    desc_f = f"<div class='feature-list'>{L['desc1']}<span class='info-icon i-free' data-tooltip='{L['t1_1']}'>i</span><br>{L['desc2']}<span class='info-icon i-free' data-tooltip='{L['t1_2']}'>i</span><br>{L['desc3']}<span class='info-icon i-free' data-tooltip='{L['t1_3']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper free-card'><div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'>{desc_f}</div></div>", unsafe_allow_html=True)
    
    # Condición para ocultar el botón si ya está logueado
    if not st.session_state.email_usuario:
        if st.button(L['btn1'], key="btn_f"):
            st.toast("Register above.")

# PLAN PRO
with col2:
    desc_p = f"<div class='feature-list'><b>{L['desc4']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_1']}'>i</span><br>{L['desc5']}<span class='info-icon i-pro' data-tooltip='{L['t2_2']}'>i</span><br>{L['desc6']}<span class='info-icon i-pro' data-tooltip='{L['t2_3']}'>i</span><br><b>{L['desc7']}</b><span class='info-icon i-pro' data-tooltip='{L['t2_4']}'>i</span></div>"
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>${precio_pro}</h1><p style='color:#00d2ff; font-weight:bold; font-size:0.9rem;'>{ahorro_txt}</p><hr style='border-color:#00d2ff;opacity:0.3;'>{desc_p}</div></div>", unsafe_allow_html=True)
    
    # Botón PayPal Pro (Dinámico ID)
    pay_pro = f"""
    <div id="paypal-button-container-pro"></div>
    <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
    <script>
      paypal.Buttons({{
        style: {{
          shape: 'pill',
          color: 'blue',
          layout: 'vertical',
          label: 'subscribe'
        }},
        createSubscription: function(data, actions) {{
          return actions.subscription.create({{
            'plan_id': '{id_pro}',
            'custom_id': '{st.session_state.email_usuario}'
          }});
        }},
        onApprove: function(data, actions) {{
          alert('Subscription Successful: ' + data.subscriptionID);
        }}
      }}).render('#paypal-button-container-pro');
    </script>
    """
    components.html(pay_pro, height=150)

# PLAN AGENCIA
with col3:
    desc_a = f"<div class='feature-list'>{L['desc8']}<span class='info-icon i-agency' data-tooltip='{L['t3_1']}'>i</span><br>{L['desc9']}<span class='info-icon i-agency' data-tooltip='{L['t3_2']}'>i</span><br>{L['desc10']}<span class='info-icon i-agency' data-tooltip='{L['t3_3']}'>i</span><br><b>{L['desc11']}</b><span class='info-icon i-agency' data-tooltip='{L['t3_4']}'>i</span></div>"
    # FIX: VIOLETA (#DDA0DD) RESTAURADO
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>${precio_age}</h1><p style='color:#DDA0DD; font-weight:bold; font-size:0.9rem;'>{ahorro_txt}</p><hr style='border-color:#DDA0DD;opacity:0.3;'>{desc_a}</div></div>", unsafe_allow_html=True)
    
    # Botón PayPal Agencia (Dinámico ID)
    pay_age = f"""
    <div id="paypal-button-container-age"></div>
    <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
    <script>
      paypal.Buttons({{
        style: {{
          shape: 'pill',
          color: 'blue',
          layout: 'vertical',
          label: 'subscribe'
        }},
        createSubscription: function(data, actions) {{
          return actions.subscription.create({{
            'plan_id': '{id_age}',
            'custom_id': '{st.session_state.email_usuario}'
          }});
        }},
        onApprove: function(data, actions) {{
          alert('Subscription Successful: ' + data.subscriptionID);
        }}
      }}).render('#paypal-button-container-age');
    </script>
    """
    components.html(pay_age, height=150)

# --- FOOTER LEGAL ---
st.markdown(f'<div style="border-top: 1px solid rgba(255,255,255,0.1); padding: 40px 0px; text-align: center;"><div style="font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom:10px;">🏢 AI REALTY PRO</div><p style="color:#666; font-size:0.8rem;">© 2026 AI Realty Pro - {L["foot_desc"]}</p></div>', unsafe_allow_html=True)

with st.expander(f"⚖️ {L.get('legal_title', 'Términos Legales')}"):
    st.write("1. No credit card data stored (PayPal).")
    st.write("2. AI generated descriptions require review.")
    st.write("3. No refunds on monthly plans.")
