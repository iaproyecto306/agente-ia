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
    portales_validos = ["infocasas", "mercadolibre", "zillow", "properati", "remax", "fincaraiz", "realtor", "idealista", "fotocasa", "inmuebles24"]
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
    if len(texto_final) > 400:
        return texto_final[:6000], es_portal_conocido
    else:
        # Mensaje amigable explicando la situación al usuario
        return "⚠️ AVISO DE SEGURIDAD: Zillow/MercadoLibre ha bloqueado el acceso automático desde la nube. Esto es normal en versiones gratuitas. Por favor, COPIA Y PEGA la descripción del inmueble manualmente en la caja de abajo.", es_portal_conocido

# ==============================================================================
# 2. CONFIGURACIÓN DE IA Y CONEXIONES SEGURAS
# ==============================================================================

# Verificación de API Key de OpenAI
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("⚠️ ERROR CRÍTICO: No se detectó la OPENAI_API_KEY en los Secrets de Streamlit.")
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
        print(f"Error guardando historial: {e}")

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
                {"role": "system", "content": "Eres un Broker Inmobiliario Senior de Lujo y Copywriter experto en Neuromarketing. Tu objetivo es VENDER."},
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
if "idioma" not in st.session_state: st.session_state.idioma = "Español"
if "last_result" not in st.session_state: st.session_state.last_result = None

# ==============================================================================
# 4. DICCIONARIO MAESTRO 360° (COMPLETO - 6 IDIOMAS)
# ==============================================================================

traducciones = {
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
        "t1_1": "Límite diario prueba.",
        "desc2": "Soporte Básico",
        "t1_2": "Ayuda técnica básica.",
        "desc3": "Marca de Agua",
        "t1_3": "Incluye firma plataforma.",
        "desc4": "Generaciones Ilimitadas",
        "t2_1": "Sin límites mensuales.",
        "desc5": "Pack Redes Sociales",
        "t2_2": "Scripts Insta/TikTok.",
        "desc6": "Optimización SEO",
        "t2_3": "Palabras clave incluidas.",
        "desc7": "Banner Principal",
        "t2_4": "Rotación en home.",
        "desc8": "5 Usuarios",
        "t3_1": "Acceso equipo.",
        "desc9": "Panel de Equipo",
        "t3_2": "Gestión agentes.",
        "desc10": "Acceso API",
        "t3_3": "Próximamente.",
        "desc11": "Prioridad Banner",
        "t3_4": "Doble exposición.",
        "btn1": "REGISTRO GRATIS",
        "btn2": "MEJORAR AHORA",
        "btn3": "CONTACTAR VENTAS",
        "how_title": "¿Cómo funciona?",
        "step1_t": "Pega el Link",
        "step1_d": "O escribe detalles.",
        "step2_t": "IA Analiza",
        "step2_d": "Motor Triple.",
        "step3_t": "Vende",
        "step3_d": "Copia y cierra.",
        "stat1": "Anuncios Optimizados",
        "stat2": "Tiempo Ahorrado",
        "stat3": "Más Consultas",
        "test_title": "Lo que dicen los Expertos",
        "test1_txt": "Ventas subieron 50%.",
        "test1_au": "Carlos R.",
        "test2_txt": "Ahorro horas.",
        "test2_au": "Ana M.",
        "test3_txt": "Vital para agencia.",
        "test3_au": "Luis P.",
        "foot_desc": "Inteligencia Artificial Inmobiliaria.",
        "mail_label": "📧 Email Profesional",
        "limit_msg": "🚫 Límite gratuito alcanzado.",
        "upgrade_msg": "Pásate a PRO para seguir vendiendo.",
        "lbl_tone": "Estilo:",
        "lbl_lang_out": "Idioma Salida:",
        "annual_toggle": "📅 Ahorrar 20% (Anual)",
        "annual_save": "✅ 2 Meses GRATIS",
        "whatsapp": "Enviar a WhatsApp",
        "download": "Descargar Reporte .txt",
        "copy_success": "¡Copiado con éxito!",
        "revoke": "Revocar Acceso",
        "manage_team": "👥 Gestionar Equipo",
        "team_activity": "📈 Actividad",
        "refine_pl": "🔄 Ajuste rápido...",
        "refine_btn": "Refinar Resultado",
        "social_title": "📱 Social Media Pack",
        "char_count": "Caracteres",
        "link_warn": "⚠️ Link no reconocido (Usa copiado manual).",
        "badge_free": "GRATIS",
        "badge_pro": "PRO",
        "badge_agency": "AGENCIA",
        "api_soon": "API (Próximamente)",
        "legal_title": "Términos Legales",
        "logout": "Cerrar Sesión",
        "welcome": "Bienvenido",
        "usage_bar": "Progreso Diario",
        "feedback_lbl": "💡 Soporte / Feedback",
        "feedback_btn": "Enviar Mensaje",
        "support_mail": "Soporte",
        "credits_left": "Créditos hoy:",
        "res_title": "ESTRATEGIA GENERADA",
        "impact_full": "🔥 IMPACTO DE VENTA MAXIMIZADO",
        "analysis_title": "🧠 Análisis: ¿Por qué vende más?",
        "watermark": "Generado por AI Realty Pro (Plan Gratis)",
        "feed_ok": "✅ ¡Mensaje recibido!",
        "tones": ["Storytelling", "Profesional", "Urgencia", "Lujo"],
        "ag_add": "Añadir Agente",
        "ag_ph": "Email del agente...",
        "ag_revoke": "Revocar",
        "morning": "Buenos días",
        "afternoon": "Buenas tardes",
        "night": "Buenas noches",
        "ag_team": "Mi Equipo",
        "ag_act": "Actividad",
        "save_txt": "Ahorra 20%",
        "m_year": "Anual",
        "copy_btn": "COPIAR",
        "down_btn": "DESCARGAR",
        "social_btn": "Pack Redes"
    },
    "English": {
        "title1": "Turn Boring Listings into",
        "title2": "Sales Magnets",
        "sub": "The secret AI tool for top-producing agents in 2026.",
        "placeholder": "🏠 Describe property...",
        "url_placeholder": "🔗 Paste property link...",
        "btn_gen": "✨ GENERATE STRATEGY",
        "p_destacada": "FEATURED LISTING",
        "comunidad": "Real Estate Community",
        "popular": "MOST POPULAR",
        "plan1": "Starter",
        "plan2": "Pro Agent",
        "plan3": "Agency",
        "desc1": "3 descriptions / day",
        "t1_1": "Daily limit.",
        "desc2": "Basic Support",
        "t1_2": "Basic help.",
        "desc3": "Watermark",
        "t1_3": "Platform signature.",
        "desc4": "Unlimited Generations",
        "t2_1": "No limits.",
        "desc5": "Social Media Pack",
        "t2_2": "Insta/TikTok Scripts.",
        "desc6": "SEO Optimization",
        "t2_3": "Keywords included.",
        "desc7": "Main Banner",
        "t2_4": "Rotation.",
        "desc8": "5 Users",
        "t3_1": "Team access.",
        "desc9": "Team Dashboard",
        "t3_2": "Manage agents.",
        "desc10": "API Access",
        "t3_3": "Coming Soon.",
        "desc11": "Banner Priority",
        "t3_4": "Double exposure.",
        "btn1": "FREE SIGNUP",
        "btn2": "UPGRADE NOW",
        "btn3": "CONTACT SALES",
        "how_title": "How it works?",
        "step1_t": "Paste Link",
        "step1_d": "Or write details.",
        "step2_t": "AI Analyzes",
        "step2_d": "Triple Engine.",
        "step3_t": "Sell",
        "step3_d": "Close deals.",
        "stat1": "Optimized Ads",
        "stat2": "Time Saved",
        "stat3": "More Leads",
        "test_title": "Experts Say",
        "test1_txt": "Sales up 50%.",
        "test1_au": "Carlos R.",
        "test2_txt": "Saves hours.",
        "test2_au": "Ana M.",
        "test3_txt": "Vital for agency.",
        "test3_au": "Luis P.",
        "foot_desc": "AI for Real Estate.",
        "mail_label": "📧 Professional Email",
        "limit_msg": "🚫 Free limit reached.",
        "upgrade_msg": "Upgrade to PRO.",
        "lbl_tone": "Style:",
        "lbl_lang_out": "Output Language:",
        "annual_toggle": "📅 Save 20% (Yearly)",
        "annual_save": "✅ 2 Months FREE",
        "whatsapp": "Send to WhatsApp",
        "download": "Download Report .txt",
        "copy_success": "Copied successfully!",
        "revoke": "Revoke Access",
        "manage_team": "👥 Manage Team",
        "team_activity": "📈 Activity",
        "refine_pl": "🔄 Quick adjust...",
        "refine_btn": "Refine Result",
        "social_title": "📱 Social Media Pack",
        "char_count": "Characters",
        "link_warn": "⚠️ Link not recognized.",
        "badge_free": "FREE",
        "badge_pro": "PRO",
        "badge_agency": "AGENCY",
        "api_soon": "API (Coming Soon)",
        "legal_title": "Terms & Privacy",
        "logout": "Log Out",
        "welcome": "Welcome",
        "usage_bar": "Daily Progress",
        "feedback_lbl": "💡 Support / Feedback",
        "feedback_btn": "Send Message",
        "support_mail": "Support",
        "credits_left": "Credits left:",
        "res_title": "GENERATED STRATEGY",
        "impact_full": "🔥 SALES IMPACT MAXIMIZED",
        "analysis_title": "🧠 Analysis: Why does this sell?",
        "watermark": "Generated by AI Realty Pro (Free Plan)",
        "feed_ok": "✅ Message received!",
        "tones": ["Storytelling", "Professional", "Urgency", "Luxury"],
        "ag_add": "Add Agent",
        "ag_ph": "Agent email...",
        "ag_revoke": "Revoke",
        "morning": "Good morning",
        "afternoon": "Good afternoon",
        "night": "Good evening",
        "ag_team": "My Team",
        "ag_act": "Activity",
        "save_txt": "Save 20%",
        "m_year": "Yearly",
        "copy_btn": "COPY",
        "down_btn": "DOWNLOAD",
        "social_btn": "Social Pack"
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
        "t1_2": "Ajuda.",
        "desc3": "Marca d'água",
        "t1_3": "Inclui assinatura.",
        "desc4": "Gerações Ilimitadas",
        "t2_1": "Sem limites.",
        "desc5": "Social Pack",
        "t2_2": "Scripts Insta/TikTok.",
        "desc6": "SEO Otimizado",
        "t2_3": "Palavras-chave.",
        "desc7": "Banner Principal",
        "t2_4": "Rotação na home.",
        "desc8": "5 Usuários",
        "t3_1": "Acesso equipe.",
        "desc9": "Painel Equipe",
        "t3_2": "Gestão.",
        "desc10": "Acesso API",
        "t3_3": "Em breve.",
        "desc11": "Prioridade",
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
        "test1_txt": "Vendas +50%.",
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
        "refine_btn": "Refinar",
        "social_title": "📱 Social Pack",
        "char_count": "Caracteres",
        "link_warn": "⚠️ Link não reconhecido.",
        "badge_free": "GRÁTIS",
        "badge_pro": "PRO",
        "badge_agency": "AGÊNCIA",
        "api_soon": "API (Breve)",
        "legal_title": "Termos e Privacidade",
        "logout": "Sair",
        "welcome": "Bem-vindo",
        "usage_bar": "Progresso",
        "feedback_lbl": "💡 Suporte",
        "feedback_btn": "Enviar",
        "support_mail": "Suporte",
        "credits_left": "Créditos hoje:",
        "res_title": "ESTRATÉGIA GERADA",
        "impact_full": "🔥 IMPACTO MÁXIMO",
        "analysis_title": "🧠 Análise: Por que vende?",
        "watermark": "Gerado por AI Realty Pro",
        "feed_ok": "✅ Recebido!",
        "tones": ["Storytelling", "Profissional", "Urgência", "Luxo"],
        "ag_add": "Adicionar",
        "ag_ph": "Email do agente...",
        "ag_revoke": "Revogar",
        "morning": "Bom dia",
        "afternoon": "Boa tarde",
        "night": "Boa noite",
        "ag_team": "Minha Equipe",
        "ag_act": "Atividade",
        "save_txt": "Poupe 20%",
        "m_year": "Anual",
        "copy_btn": "COPIAR",
        "down_btn": "BAIXAR",
        "social_btn": "Social Pack"
    },
    "Français": {
        "title1": "Transformez vos Annonces",
        "title2": "en Aimants",
        "sub": "L'outil IA secret des agents top.",
        "placeholder": "🏠 Décrivez la propriété...",
        "url_placeholder": "🔗 Collez le lien...",
        "btn_gen": "✨ GÉNÉRER",
        "p_destacada": "EN VEDETTE",
        "comunidad": "Communauté",
        "popular": "POPULAIRE",
        "plan1": "Initial",
        "plan2": "Pro",
        "plan3": "Agence",
        "desc1": "3 desc./jour",
        "t1_1": "Limite jour.",
        "desc2": "Support",
        "t1_2": "Aide.",
        "desc3": "Filigrane",
        "t1_3": "Signature.",
        "desc4": "Illimité",
        "t2_1": "Sans limites.",
        "desc5": "Pack Social",
        "t2_2": "Scripts.",
        "desc6": "SEO",
        "t2_3": "Mots-clés.",
        "desc7": "Bannière",
        "t2_4": "Rotation.",
        "desc8": "5 Utilisateurs",
        "t3_1": "Équipe.",
        "desc9": "Dashboard",
        "t3_2": "Gestion.",
        "desc10": "API",
        "t3_3": "Bientôt.",
        "desc11": "Priorité",
        "t3_4": "Double expo.",
        "btn1": "GRATUIT",
        "btn2": "UPGRADE",
        "btn3": "CONTACT",
        "how_title": "Comment ça marche?",
        "step1_t": "Lien",
        "step1_d": "Détails.",
        "step2_t": "Analyse",
        "step2_d": "Moteur.",
        "step3_t": "Vente",
        "step3_d": "Publiez.",
        "stat1": "Optimisés",
        "stat2": "Temps",
        "stat3": "Conversion",
        "test_title": "Avis",
        "test1_txt": "Ventes +50%.",
        "test1_au": "Carlos",
        "test2_txt": "Gain temps.",
        "test2_au": "Ana",
        "test3_txt": "Vital.",
        "test3_au": "Luis",
        "foot_desc": "IA Immo.",
        "mail_label": "📧 Email",
        "limit_msg": "🚫 Limite atteinte.",
        "upgrade_msg": "Passez PRO.",
        "lbl_tone": "Ton:",
        "lbl_lang_out": "Langue:",
        "annual_toggle": "📅 -20% Annuel",
        "annual_save": "✅ 2 Mois Gratuits",
        "whatsapp": "WhatsApp",
        "download": "Télécharger",
        "copy_success": "Copié!",
        "revoke": "Révoquer",
        "manage_team": "👥 Équipe",
        "team_activity": "📈 Activité",
        "refine_pl": "🔄 Ajuster...",
        "refine_btn": "Raffiner",
        "social_title": "📱 Social Pack",
        "char_count": "Caractères",
        "link_warn": "⚠️ Lien inconnu.",
        "badge_free": "GRATUIT",
        "badge_pro": "PRO",
        "badge_agency": "AGENCE",
        "api_soon": "API",
        "legal_title": "Mentions",
        "logout": "Sortir",
        "welcome": "Bienvenue",
        "usage_bar": "Progrès",
        "feedback_lbl": "Support",
        "feedback_btn": "Envoyer",
        "support_mail": "Support",
        "credits_left": "Crédits:",
        "res_title": "STRATÉGIE",
        "impact_full": "🔥 IMPACT MAXIMUM",
        "analysis_title": "🧠 Analyse",
        "watermark": "Généré par AI Realty Pro",
        "feed_ok": "✅ Reçu!",
        "tones": ["Storytelling", "Professionnel", "Urgence", "Luxe"],
        "ag_add": "Ajouter",
        "ag_ph": "Email...",
        "ag_revoke": "Révoquer",
        "morning": "Bonjour",
        "afternoon": "Bon après-midi",
        "night": "Bonsoir",
        "ag_team": "Équipe",
        "ag_act": "Activité",
        "save_txt": "-20%",
        "m_year": "Annuel",
        "copy_btn": "COPIER",
        "down_btn": "TÉLÉCHARGER",
        "social_btn": "Social Pack"
    },
    "Deutsch": {
        "title1": "Verwandeln Sie Anzeigen",
        "title2": "in Magnete",
        "sub": "Das geheime KI-Tool.",
        "placeholder": "🏠 Beschreibung...",
        "url_placeholder": "🔗 Link einfügen...",
        "btn_gen": "✨ GENERIEREN",
        "p_destacada": "HIGHLIGHT",
        "comunidad": "Community",
        "popular": "BELIEBT",
        "plan1": "Start",
        "plan2": "Pro",
        "plan3": "Agentur",
        "desc1": "3 Texte/Tag",
        "t1_1": "Limit.",
        "desc2": "Support",
        "t1_2": "Hilfe.",
        "desc3": "Wasserzeichen",
        "t1_3": "Signatur.",
        "desc4": "Unbegrenzt",
        "t2_1": "Kein Limit.",
        "desc5": "Social Pack",
        "t2_2": "Skripte.",
        "desc6": "SEO",
        "t2_3": "Keywords.",
        "desc7": "Banner",
        "t2_4": "Rotation.",
        "desc8": "5 Nutzer",
        "t3_1": "Team.",
        "desc9": "Dashboard",
        "t3_2": "Verwaltung.",
        "desc10": "API",
        "t3_3": "Bald.",
        "desc11": "Priorität",
        "t3_4": "Sichtbarkeit.",
        "btn1": "GRATIS",
        "btn2": "UPGRADE",
        "btn3": "KONTAKT",
        "how_title": "Wie?",
        "step1_t": "Link",
        "step1_d": "Text.",
        "step2_t": "Analyse",
        "step2_d": "Engine.",
        "step3_t": "Verkauf",
        "step3_d": "Fertig.",
        "stat1": "Optimiert",
        "stat2": "Zeit",
        "stat3": "Mehr",
        "test_title": "Experten",
        "test1_txt": "+50%.",
        "test1_au": "C.", "test2_txt": "Zeit.", "test2_au": "A.", "test3_txt": "Wichtig.", "test3_au": "L.",
        "foot_desc": "Immo-KI.",
        "mail_label": "📧 E-Mail",
        "limit_msg": "🚫 Limit.",
        "upgrade_msg": "Upgrade.",
        "lbl_tone": "Ton:",
        "lbl_lang_out": "Sprache:",
        "annual_toggle": "📅 -20% Jährlich",
        "annual_save": "✅ 2 Monate GRATIS",
        "whatsapp": "WhatsApp",
        "download": "Download",
        "copy_success": "Kopiert!",
        "revoke": "Widerrufen",
        "manage_team": "👥 Team",
        "team_activity": "📈 Aktivität",
        "refine_pl": "🔄 Anpassen...",
        "refine_btn": "Verfeinern",
        "social_title": "📱 Social Pack",
        "char_count": "Zeichen",
        "link_warn": "⚠️ Fehler.",
        "badge_free": "GRATIS",
        "badge_pro": "PRO",
        "badge_agency": "AGENTUR",
        "api_soon": "API",
        "legal_title": "Recht",
        "logout": "Abmelden",
        "welcome": "Hallo",
        "usage_bar": "Fortschritt",
        "feedback_lbl": "Support",
        "feedback_btn": "Senden",
        "support_mail": "Support",
        "credits_left": "Credits:",
        "res_title": "STRATEGIE",
        "impact_full": "🔥 MAXIMALER IMPACT",
        "analysis_title": "🧠 Analyse",
        "watermark": "Generiert von AI Realty Pro",
        "feed_ok": "✅ Erhalten!",
        "tones": ["Storytelling", "Professionell", "Dringend", "Luxus"],
        "ag_add": "Add",
        "ag_ph": "E-Mail...",
        "ag_revoke": "Widerrufen",
        "morning": "Guten Morgen",
        "afternoon": "Guten Tag",
        "night": "Guten Abend",
        "ag_team": "Team",
        "ag_act": "Aktivität",
        "save_txt": "Sparen",
        "m_year": "Jahr",
        "copy_btn": "KOPIEREN",
        "down_btn": "LADEN",
        "social_btn": "Social Pack"
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
        "t1_1": "限制。",
        "desc2": "支持",
        "t1_2": "基础。",
        "desc3": "水印",
        "t1_3": "签名。",
        "desc4": "无限",
        "t2_1": "无限制。",
        "desc5": "社交包",
        "t2_2": "脚本。",
        "desc6": "SEO",
        "t2_3": "关键词。",
        "desc7": "横幅",
        "t2_4": "轮播。",
        "desc8": "5用户",
        "t3_1": "团队。",
        "desc9": "面板",
        "t3_2": "管理。",
        "desc10": "API",
        "t3_3": "即将。",
        "desc11": "优先",
        "t3_4": "曝光。",
        "btn1": "免费",
        "btn2": "升级",
        "btn3": "联系",
        "how_title": "如何运作?",
        "step1_t": "链接",
        "step1_d": "详情。",
        "step2_t": "分析",
        "step2_d": "引擎。",
        "step3_t": "销售",
        "step3_d": "发布。",
        "stat1": "优化",
        "stat2": "时间",
        "stat3": "转化",
        "test_title": "评价",
        "test1_txt": "+50%", "test1_au": "C.", "test2_txt": "时间。", "test2_au": "A.", "test3_txt": "重要。", "test3_au": "L.",
        "foot_desc": "AI房产。", "mail_label": "📧 邮箱",
        "limit_msg": "🚫 限制。", "upgrade_msg": "升级。",
        "lbl_tone": "语气:", "lbl_lang_out": "语言:", "annual_toggle": "📅 省20%", "annual_save": "✅ 送2个月",
        "whatsapp": "微信/Whats", "download": "下载", "copy_success": "成功!",
        "revoke": "撤销", "manage_team": "👥 团队", "team_activity": "📈 活动",
        "refine_pl": "🔄 调整...", "refine_btn": "优化", "social_title": "📱 社交包", "char_count": "字数",
        "link_warn": "⚠️ 错误。", "badge_free": "免费", "badge_pro": "专业", "badge_agency": "机构",
        "api_soon": "API", "legal_title": "条款", "logout": "退出", "welcome": "欢迎",
        "usage_bar": "进度", "feedback_lbl": "反馈", "feedback_btn": "提交",
        "support_mail": "支持", "credits_left": "剩余:",
        "res_title": "策略生成",
        "impact_full": "🔥 销售影响力最大化",
        "analysis_title": "🧠 分析", "watermark": "AI生成",
        "feed_ok": "✅ 收到!",
        "tones": ["故事", "专业", "紧迫", "奢华"],
        "ag_add": "添加", "ag_ph": "邮箱...", "ag_revoke": "撤销",
        "morning": "早安", "afternoon": "午安", "night": "晚安",
        "ag_team": "团队", "ag_act": "活动",
        "save_txt": "省钱", "m_year": "年付",
        "copy_btn": "复制", "down_btn": "下载", "social_btn": "社交包"
    }
}
# Fallback
if st.session_state.idioma not in traducciones: st.session_state.idioma = "Español"
L = traducciones[st.session_state.idioma]
# ==============================================================================
# 6. SIDEBAR PROFESIONAL Y NAVEGACIÓN
# ==============================================================================

with st.sidebar:
    st.markdown('<div style="text-align:center; font-size: 1.6rem; font-weight: 800; color: #fff; letter-spacing: 1px;">🏢 AI REALTY</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # --- SELECTOR DE IDIOMA SINCRONIZADO ---
    # Busca el índice del idioma actual para mantener la selección
    try:
        idx_idioma = list(traducciones.keys()).index(st.session_state.idioma)
    except:
        idx_idioma = 0
        
    idioma_selec = st.selectbox("🌐 Language", list(traducciones.keys()), index=idx_idioma)
    
    # Actualizar estado si cambia
    if idioma_selec != st.session_state.idioma:
        st.session_state.idioma = idioma_selec
        st.rerun()
    
    # Cargar diccionario activo
    L = traducciones[st.session_state.idioma]

    # --- PERFIL DE USUARIO (SI ESTÁ LOGUEADO) ---
    if st.session_state.email_usuario:
        st.markdown(f"### {L.get('nav_welcome', 'Bienvenido')}")
        st.markdown(f"**{st.session_state.email_usuario}**")
        
        # Cálculo de créditos
        usos = st.session_state.usos
        es_pro_local = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite = 99999 if es_pro_local else 3
        
        # Color del contador: Dorado (Pro), Rojo (Poco saldo), Azul (Normal)
        color_cred = "#d4af37" if es_pro_local else ("#ff4b4b" if (3 - usos) <= 1 else "#00d2ff")
        restantes = "∞" if es_pro_local else str(3 - usos)
        credits_label = L.get('nav_credits', 'Créditos:')
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; border: 1px solid {color_cred}; margin-bottom: 10px;">
            <div style="font-size: 0.85rem; color: #aaa;">{credits_label}</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: {color_cred};">{restantes}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Barra de progreso visual
        if limite < 100:
            progreso = min(usos / limite, 1.0)
            st.progress(progreso)
        else:
            st.progress(1.0) # Barra llena para ilimitados
            
        st.markdown("---")
        
        # Botón de Logout
        if st.button(f"🚪 {L.get('nav_logout', 'Cerrar Sesión')}"):
            try:
                cookie_manager.delete("user_email")
            except:
                pass 
            st.session_state.email_usuario = ""
            st.session_state.usos = 0
            st.session_state.plan_usuario = "Gratis"
            st.rerun()

    # --- ZONA DE FEEDBACK ---
    st.markdown("---")
    st.subheader(L.get("feed_title", "Soporte"))
    st.markdown(f"📧 **{L.get('support_mail', 'Soporte')}: support@airealtypro.com**")
    
    fb_text = st.text_area("", placeholder=L.get("feed_ph", "Escribe aquí..."), height=100, label_visibility="collapsed", key="fb_input")
    
    if st.button(L.get("feed_btn", "Enviar"), use_container_width=True):
        if fb_text:
            with st.spinner("..."):
                ok = guardar_feedback(st.session_state.email_usuario, fb_text)
                if ok:
                    st.toast(L.get("feed_ok", "Enviado"))
                else:
                    st.error("Error DB")
        else:
            st.warning("...")
            
    st.markdown("---")
    st.markdown(f"<div style='text-align:center; color:#666; font-size:0.8rem;'>v7.0 Platinum Final</div>", unsafe_allow_html=True)

# ==============================================================================
# 7. INTERFAZ: CABECERA Y HUD DE IDENTIDAD
# ==============================================================================

col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo:
    st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 AI REALTY PRO</div>', unsafe_allow_html=True)

# --- HUD SUPERIOR (BADGE DE PLAN) ---
if st.session_state.email_usuario:
    # Intento silencioso de actualizar plan desde DB por si hubo cambios externos
    try:
        df_check = obtener_datos_db()
        if not df_check.empty and st.session_state.email_usuario in df_check['email'].values:
            user_row = df_check[df_check['email'] == st.session_state.email_usuario].iloc[0]
            real_plan = user_row['plan'] if 'plan' in user_row else 'Gratis'
            st.session_state.plan_usuario = str(real_plan).title()
            st.session_state.usos = int(user_row['usos'])
    except Exception as e:
        pass 

    # Saludo según hora
    hora = datetime.now().hour
    if "morning" in L:
        saludo_txt = L["morning"] if 5 <= hora < 12 else L["afternoon"] if 12 <= hora < 20 else L["night"]
    else:
        saludo_txt = "Hola"

    p_name = str(st.session_state.plan_usuario).lower()
    
    # Asignación de estilos de Badge
    if "agencia" in p_name: 
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
            <div>👋 <b>{saludo_txt}</b>, <span style="color:#00d2ff;">{st.session_state.email_usuario}</span></div>
            <div class="badge-neon {badge_cls}">{badge_txt}</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown(f"<h1 class='neon-title'>{L['title1']} <br><span class='neon-highlight'>{L['title2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)

# --- BANNER CENTRAL ---
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    st.markdown(f'''
        <div class="video-placeholder">
            <div class="dynamic-tag">{L["p_destacada"]}</div>
            <div style="background:rgba(0,0,0,0.6);width:100%;text-align:center;padding:10px;">{L["comunidad"]}</div>
        </div>
    ''', unsafe_allow_html=True)

# ==============================================================================
# 8. LÓGICA DE NEGOCIO PRINCIPAL (LOGIN & CHECK EMPLEADOS)
# ==============================================================================

# Verificación inicial de Cookie
if not st.session_state.email_usuario:
    cookie_val = cookie_manager.get("user_email")
    if cookie_val:
        st.session_state.email_usuario = cookie_val
        st.rerun()

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    # --- PANTALLA DE LOGIN ---
    if not st.session_state.email_usuario:
        st.markdown('<div class="glass-container" style="height:auto; box-shadow: 0 0 30px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
        
        email_input = st.text_input(L["mail_label"], placeholder="email@ejemplo.com", key="user_email")
        if st.button("COMENZAR / START", type="primary"):
            if email_input and "@" in email_input:
                email_limpio = email_input.strip().lower()
                st.session_state.email_usuario = email_limpio
                
                # Guardar Cookie
                try:
                    cookie_manager.set("user_email", email_limpio, expires_at=datetime.now().replace(year=datetime.now().year + 1))
                except:
                    pass
                
                # --- FIX EMPLEADOS: PRIORIDAD AL EMPLEADO ---
                df_u = obtener_datos_db()
                df_e = obtener_empleados_db()
                
                es_empleado_confirmado = False
                
                # 1. Buscamos primero en la lista de empleados
                if 'employeeemail' in df_e.columns and email_limpio in df_e['employeeemail'].values:
                    # Encontrar al jefe
                    boss_email = df_e[df_e['employeeemail'] == email_limpio].iloc[0]['bossemail']
                    
                    # Verificar plan del jefe
                    if boss_email in df_u['email'].values:
                        boss_data = df_u[df_u['email'] == boss_email].iloc[0]
                        boss_plan = str(boss_data['plan']).title()
                        
                        # Si el jefe es Agencia, el empleado es Pro
                        if boss_plan == "Agencia":
                            st.session_state.plan_usuario = "Pro"
                            st.session_state.es_empleado = True
                            st.session_state.usos = 0 # Ilimitado
                            es_empleado_confirmado = True
                
                # 2. Si no es empleado confirmado, buscamos su cuenta personal
                if not es_empleado_confirmado:
                    if email_limpio in df_u['email'].values:
                        usuario = df_u[df_u['email'] == email_limpio].iloc[0]
                        st.session_state.usos = int(usuario['usos'])
                        st.session_state.plan_usuario = str(usuario['plan']).title() if 'plan' in usuario else 'Gratis'
                        st.session_state.es_empleado = False
                    else:
                        # Usuario nuevo
                        st.session_state.usos = 0
                        st.session_state.plan_usuario = "Gratis"
                        st.session_state.es_empleado = False
                
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Email inválido.")
        st.markdown('</div>', unsafe_allow_html=True)
        # --- MOTOR DE GENERACIÓN IA (SI HAY SESIÓN ACTIVA) ---
    elif st.session_state.email_usuario:
        es_pro = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite = 99999 if es_pro else 3
        
        # Panel Principal (Centrado)
        # Usamos columnas para dar un margen y centrar el contenido visualmente
        col_main = st.columns([1, 2, 1])[1]
        
        with col_main:
            if st.session_state.usos < limite:
                st.markdown('<div class="glass-container" style="height:auto;">', unsafe_allow_html=True)
                
                # --- FILTROS DE ENTRADA ---
                ct1, ct2 = st.columns(2)
                with ct1: 
                    # Mapeo de Tonos: Mostramos el traducido, pero internamente sabemos cuál es
                    tonos_display = L["tones"] # Lista traducida del diccionario actual
                    # Mapeo interno para consistencia en el prompt (o usamos el seleccionado directo)
                    sel_idx = st.selectbox(L["lbl_tone"], range(len(tonos_display)), format_func=lambda x: tonos_display[x])
                    sel_tone = tonos_display[sel_idx] 
                
                with ct2: 
                    # Selector de idioma de SALIDA del texto (puede ser distinto al de la interfaz)
                    idioma_salida = st.selectbox(L["lbl_lang_out"], list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma))

                # Inputs de datos
                url_input = st.text_input("", placeholder=L["url_placeholder"], label_visibility="collapsed")
                user_input = st.text_area("", placeholder=L["placeholder"], key="input_ia", label_visibility="collapsed", height=150)
                
                # Contador de caracteres
                st.caption(f"{L['char_count']}: {len(user_input)}")

                # --- BOTÓN DE GENERAR ---
                if st.button(L['btn_gen'], key="main_gen", type="primary"):
                    if user_input or url_input: 
                        with st.spinner("🚀 AI Realty Pro..."):
                            
                            # 1. Scraping (Llamada a la función del Bloque 1)
                            datos_web, es_valido = extraer_datos_inmueble(url_input) if url_input else ("", True)
                            
                            # Aviso si el link es raro, pero intentamos igual
                            if not es_valido:
                                st.toast(L["link_warn"], icon="⚠️")
                            
                            # 2. Construcción del Prompt
                            # Define la estructura según el plan
                            if es_pro:
                                estructura = "ESTRATEGIA COMPLETA: 1. Título Gancho, 2. Descripción Emocional, 3. Ficha Técnica (Bullets), 4. Copy para WhatsApp, 5. SEO (Keywords)."
                            else:
                                estructura = "DESCRIPCIÓN ESTÁNDAR (Máximo 2 párrafos). Agrega al final: 'Generado por AI Realty Pro - Versión Gratuita'."

                            prompt_base = f"""
                            ACTÚA COMO: El mejor Copywriter Inmobiliario del mundo.
                            IDIOMA DE SALIDA: {idioma_salida}.
                            ESTILO: {sel_tone}.
                            
                            DATOS DEL INMUEBLE (WEB): {datos_web}
                            DATOS MANUALES: {user_input}
                            
                            INSTRUCCIONES CRÍTICAS:
                            1. Si 'DATOS DEL INMUEBLE' dice 'ERROR_LECTURA' y no hay 'DATOS MANUALES', responde ÚNICAMENTE con un mensaje de error traducido al {idioma_salida} pidiendo que ingrese datos manuales. No inventes nada.
                            2. Si tienes datos, genera una descripción de venta inmobiliaria de alto impacto.
                            3. FORMATO: Markdown con negritas en palabras clave.
                            
                            ESTRUCTURA SOLICITADA:
                            {estructura}
                            """
                            
                            # 3. Llamada a OpenAI (Función del Bloque 1)
                            resultado = generar_texto(prompt_base)
                            
                            if "ERROR_IA" not in resultado:
                                st.session_state.last_result = resultado
                                st.session_state.usos += 1
                                
                                # 4. Actualizar BD 
                                # (Si es empleado, no descontamos o actualizamos al jefe, aquí actualizamos el uso del usuario logueado 
                                # para llevar registro, aunque sea ilimitado por ser Pro/Agencia)
                                if not st.session_state.es_empleado:
                                    update_usage(st.session_state.email_usuario, st.session_state.usos, st.session_state.plan_usuario)
                                
                                # 5. Guardar Historial
                                save_log(st.session_state.email_usuario, f"{url_input} {user_input}", resultado)
                                
                                # Recargar para mostrar resultados
                                st.rerun()
                    else:
                        st.warning("Input required") # Mensaje simple si está vacío
                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- VISUALIZACIÓN DE RESULTADOS (DISEÑO PREMIUM) ---
                if st.session_state.last_result:
                    # Barra de Impacto Dorada (Animada por CSS)
                    st.markdown(f"""
                    <div class="meter-container">
                        <div class="meter-fill"></div>
                        <div class="meter-text">{L['impact_full']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Caja de Texto Dark Glass
                    st.markdown(f'''
                        <div class="result-container">
                            <div style="color: #d4af37; font-weight: 800; margin-bottom: 15px; letter-spacing: 1px; text-transform: uppercase;">
                                {L['res_title']} | {sel_tone.upper()}
                            </div>
                            <div style="font-size: 1.05rem;">
                                {st.session_state.last_result.replace(chr(10), "<br>")}
                            </div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    # Marca de Agua (Solo para usuarios Gratis)
                    if not es_pro:
                        st.caption(f"🔒 {L['watermark']}")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Botones de Acción
                    b1, b2, b3 = st.columns(3)
                    
                    with b1:
                        if st.button(f"📋 {L['copy_btn']}"):
                            # Intento de copiado visual + toast
                            st.code(st.session_state.last_result)
                            st.toast(L["copy_success"])
                    
                    with b2:
                        # Codificar mensaje para URL de WhatsApp
                        wa_msg = urllib.parse.quote(st.session_state.last_result[:900])
                        st.link_button(f"📲 {L['whatsapp']}", f"https://wa.me/?text={wa_msg}", use_container_width=True)
                    
                    with b3:
                        st.download_button(f"💾 {L['down_btn']}", st.session_state.last_result, file_name=f"Listing_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)

                    # --- EXTRAS PRO (Solo visibles para Pro/Agencia) ---
                    if es_pro:
                        st.markdown("---")
                        # Pack Redes Sociales
                        with st.expander(f"📱 {L['social_title']}"):
                            with st.spinner("..."):
                                res_social = generar_texto(f"Crea 1 Post de Instagram (con hashtags) y 1 Guion de TikTok para este texto. Idioma: {idioma_salida}. Texto: {st.session_state.last_result}")
                                st.markdown(res_social)
                    
                    # Análisis Educativo (Para todos, muestra el valor de la IA)
                    with st.expander(f"🧠 {L['analysis_title']}"):
                        with st.spinner("..."):
                            analisis = generar_texto(f"Analiza brevemente (3 puntos) por qué este texto es efectivo para vender. Idioma: {idioma_salida}. Texto: {st.session_state.last_result[:500]}")
                            st.write(analisis)

                    # Herramienta de Refinamiento Rápido
                    st.divider()
                    refine = st.text_input("", placeholder=L["refine_pl"])
                    if st.button(L["refine_btn"]):
                        with st.spinner("..."):
                            nuevo_res = generar_texto(f"Reescribe el siguiente texto aplicando este cambio: '{refine}'. Idioma: {idioma_salida}. Texto: {st.session_state.last_result}")
                            st.session_state.last_result = nuevo_res
                            st.rerun()

            else:
                # Bloqueo de Pago (Paywall) - Si se acabaron los usos
                st.error(L["limit_msg"])
                st.markdown(f"#### {L['upgrade_msg']}")
                # Placeholder visual del botón de pago (los reales están abajo)
                components.html(f'<div style="background:#0e1117; color:#888; padding:10px; text-align:center; border:1px dashed #444; border-radius:10px;">Upgrade below to unlock infinite generations</div>', height=50)
                # ==============================================================================
# 9. CONSOLA DE AGENCIA (PANEL DE CONTROL DE EQUIPO)
# ==============================================================================

# Solo se muestra si el usuario es "Agencia" y es el jefe (no un empleado)
if st.session_state.plan_usuario == "Agencia" and not st.session_state.es_empleado:
    st.divider()
    st.subheader(f"🏢 {L.get('manage_team', 'Gestión de Equipo')}")
    
    # Pestañas de Navegación dentro del Panel (Traducidas)
    tab_equipo, tab_monitor = st.tabs([L.get("ag_team", "Equipo"), L.get("ag_act", "Actividad")])
    
    # Cargar datos actuales
    df_emp = obtener_empleados_db()
    
    # Filtro: Buscar empleados donde el BossEmail sea el usuario actual
    if 'bossemail' in df_emp.columns and 'employeeemail' in df_emp.columns:
        mis_empleados = df_emp[df_emp['bossemail'] == st.session_state.email_usuario]['employeeemail'].tolist()
    else:
        mis_empleados = []
    
    # --- PESTAÑA 1: GESTIÓN DE MIEMBROS ---
    with tab_equipo:
        c_add1, c_add2 = st.columns([3, 1])
        
        # Input para añadir nuevo agente (Traducido)
        with c_add1: 
            new_emp = st.text_input("Email", placeholder=L.get("ag_ph", "email@agente.com"), label_visibility="collapsed", key="in_new_ag")
        
        # Botón de añadir con validaciones
        with c_add2:
            if st.button(L.get("ag_add", "Añadir"), use_container_width=True):
                # Validación: Máximo 5 usuarios (1 jefe + 4 empleados) y formato email
                if len(mis_empleados) < 5 and "@" in new_emp:
                    # Crear nueva fila normalizada
                    nr = pd.DataFrame({
                        "bossemail": [st.session_state.email_usuario], 
                        "employeeemail": [new_emp.strip().lower()]
                    })
                    # Guardar en Google Sheets
                    conn.update(worksheet="Employees", data=pd.concat([df_emp, nr], ignore_index=True))
                    st.rerun()
                elif len(mis_empleados) >= 5:
                    st.warning("Límite de equipo alcanzado (Máx 5).")
                else:
                    st.warning("Email inválido.")
        
        st.write("---")
        st.markdown(f"**Miembros Activos ({len(mis_empleados)}/5):**")
        
        # Listado de empleados con opción de revocar
        if mis_empleados:
            for emp in mis_empleados:
                ce1, ce2 = st.columns([4, 1])
                with ce1:
                    st.success(f"👤 {emp}")
                with ce2:
                    if st.button(L.get("ag_revoke", "Revocar"), key=f"del_{emp}"):
                        # Lógica de borrado: Filtramos todo MENOS el que queremos borrar
                        clean_df = df_emp[~((df_emp['bossemail'] == st.session_state.email_usuario) & (df_emp['employeeemail'] == emp))]
                        conn.update(worksheet="Employees", data=clean_df)
                        st.toast(f"Acceso revocado a {emp}")
                        st.rerun()
        else:
            st.info("Aún no tienes equipo.")

    # --- PESTAÑA 2: MONITOR DE ACTIVIDAD ---
    with tab_monitor:
        if mis_empleados:
            df_usuarios = obtener_datos_db()
            # Filtramos de la base de datos general solo los emails de mis empleados
            if not df_usuarios.empty and 'email' in df_usuarios.columns:
                stats = df_usuarios[df_usuarios['email'].isin(mis_empleados)][['email', 'usos']]
                st.dataframe(stats, use_container_width=True, hide_index=True)
            else:
                st.warning("No hay datos.")
        else:
            st.warning("...")

# ==============================================================================
# 10. SECCIÓN INFORMATIVA (MARKETING VISUAL)
# ==============================================================================

st.markdown(f"<br><br><h2 style='text-align:center; color:white;'>{L.get('how_title', '¿Cómo funciona?')}</h2>", unsafe_allow_html=True)

# Pasos de funcionamiento (Traducidos)
ch1, ch2, ch3 = st.columns(3)
with ch1: 
    st.markdown(f"<div style='text-align:center; padding:20px;'><h1 style='color:#00d2ff; font-size:3rem;'>1</h1><p style='font-size:1.1rem;'><b>{L.get('step1_t', 'Pega el Link')}</b><br>{L.get('step1_d', '...')}</p></div>", unsafe_allow_html=True)
with ch2: 
    st.markdown(f"<div style='text-align:center; padding:20px;'><h1 style='color:#00d2ff; font-size:3rem;'>2</h1><p style='font-size:1.1rem;'><b>{L.get('step2_t', 'IA Analiza')}</b><br>{L.get('step2_d', '...')}</p></div>", unsafe_allow_html=True)
with ch3: 
    st.markdown(f"<div style='text-align:center; padding:20px;'><h1 style='color:#00d2ff; font-size:3rem;'>3</h1><p style='font-size:1.1rem;'><b>{L.get('step3_t', 'Vende')}</b><br>{L.get('step3_d', '...')}</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Estadísticas de Impacto (Traducidas)
col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1: 
    st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">+10k</h2><p style="color:#aaa; font-size:0.9rem;">{L.get("stat1", "Listings")}</p></div>', unsafe_allow_html=True)
with col_stat2: 
    st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">-80%</h2><p style="color:#aaa; font-size:0.9rem;">{L.get("stat2", "Tiempo")}</p></div>', unsafe_allow_html=True)
with col_stat3: 
    st.markdown(f'<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);"><h2 style="color:#00d2ff; margin:0;">+45%</h2><p style="color:#aaa; font-size:0.9rem;">{L.get("stat3", "Conversión")}</p></div>', unsafe_allow_html=True)

# ==============================================================================
# 11. PLANES DE SUSCRIPCIÓN Y PAYPAL
# ==============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center;'>{L.get('plan_title', 'Planes')}</h2>", unsafe_allow_html=True)

# Switch Anual
col_sw1, col_sw2, col_sw3 = st.columns([1, 2, 1])
with col_sw2:
    es_anual = st.toggle(f"📅 {L.get('annual_toggle', 'Anual')}", value=False)

# Variables de Precio
precio_pro = "490" if es_anual else "49"
precio_age = "1,990" if es_anual else "199"
ahorro_txt = L.get("annual_save", "") if es_anual else ""

# IDs PayPal Reales
id_pro = "P-2PU023636P1209345NFQ7TMY" if es_anual else "P-3P2657040E401734NNFQQ5TY"
id_age = "P-87X83840151393810NFQ7X6Q" if es_anual else "P-0S451470G5041550ENFQRB4I"

# Tarjetas
c1, c2, c3 = st.columns(3)

# GRATIS
with c1:
    desc_f = f"<div class='feature-list'>{L.get('desc1', '')}<br>{L.get('desc2', '')}<br>{L.get('desc3', '')}</div>"
    st.markdown(f"<div class='card-wrapper free-card'><div class='glass-container'><h3>{L.get('plan1', 'Free')}</h3><h1>$0</h1><hr style='opacity:0.2;'>{desc_f}</div></div>", unsafe_allow_html=True)
    if not st.session_state.email_usuario:
        st.button(L.get('btn1', 'Registro'), key="btn_free_signup", use_container_width=True)

# PRO
with c2:
    desc_p = f"<div class='feature-list'><b>{L.get('desc4', '')}</b><br>{L.get('desc5', '')}<br>{L.get('desc6', '')}<br>{L.get('desc7', '')}</div>"
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L.get('popular', 'POPULAR')}</div><h3 style='color:#00d2ff;'>{L.get('plan2', 'Pro')}</h3><h1>${precio_pro}</h1><p style='color:#00d2ff; font-weight:bold; font-size:0.9rem;'>{ahorro_txt}</p><hr style='border-color:#00d2ff;opacity:0.3;'>{desc_p}</div></div>", unsafe_allow_html=True)
    
    # Botón PayPal Pro
    components.html(f'<div id="p_pro"></div><script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script><script>paypal.Buttons({{style:{{shape:"rect",color:"blue",layout:"vertical",label:"subscribe"}},createSubscription:function(d,a){{return a.subscription.create({{plan_id:"{id_pro}",custom_id:"{st.session_state.email_usuario}"}});}}}}).render("#p_pro");</script>', height=160)

# AGENCIA
with c3:
    desc_a = f"<div class='feature-list'><b>{L.get('desc8', '')}</b><br>{L.get('desc9', '')}<br>{L.get('desc10', '')}<br>{L.get('desc11', '')}</div>"
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#d4af37;'>{L.get('plan3', 'Agencia')}</h3><h1>${precio_age}</h1><p style='color:#d4af37; font-weight:bold; font-size:0.9rem;'>{ahorro_txt}</p><hr style='border-color:#d4af37;opacity:0.3;'>{desc_a}</div></div>", unsafe_allow_html=True)
    
    # Botón PayPal Agencia
    components.html(f'<div id="p_age"></div><script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script><script>paypal.Buttons({{style:{{shape:"rect",color:"blue",layout:"vertical",label:"subscribe"}},createSubscription:function(d,a){{return a.subscription.create({{plan_id:"{id_age}",custom_id:"{st.session_state.email_usuario}"}});}}}}).render("#p_age");</script>', height=160)

# --- FOOTER LEGAL ---
st.markdown("---")
st.markdown(f"""
<div style='text-align:center; color:#666; padding: 40px;'>
    <div style="font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom:10px;">🏢 AI REALTY PRO</div>
    <p>© 2026 AI Realty Pro - {L.get('foot_desc', 'AI Real Estate')}</p>
</div>
""", unsafe_allow_html=True)

with st.expander(f"⚖️ {L.get('legal_title', 'Legales')}"):
    st.write("1. No guardamos datos de tarjeta (PayPal procesa todo).")
    st.write("2. Verifique siempre el contenido generado por IA.")
    st.write("3. Garantía de 7 días solo en planes anuales.")
