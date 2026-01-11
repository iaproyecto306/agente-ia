import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import urllib.parse
import time
import io
import extra_streamlit_components as stx
import random

# ==============================================================================
#
#    0. GESTOR DE COOKIES (MEMORIA PERMANENTE)
#
# ==============================================================================

if "cookie_manager" not in st.session_state:
    st.session_state.cookie_manager = stx.CookieManager()

cookie_manager = st.session_state.cookie_manager

# ==============================================================================
#
#    1. MOTOR DE EXTRACCIÓN (NINJA V6.0)
#
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
    
    # --- CAPA 1: JINA AI ---
    try:
        url_jina = f"https://r.jina.ai/{url}"
        
        headers_jina = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Return-Format": "text"
        }
        
        response = requests.get(
            url_jina, 
            headers=headers_jina, 
            timeout=25
        )
        
        if response.status_code == 200 and "Just a moment" not in response.text:
            texto_final = response.text
    except:
        pass

    # --- CAPA 2: NAVEGADOR PC ---
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
            
            response = requests.get(
                url, 
                headers=headers_pc, 
                timeout=15
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(
                    response.text, 
                    'html.parser'
                )
                
                for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'svg', 'button']):
                    element.decompose()
                    
                texto_final = soup.get_text(separator=' ', strip=True)
        except:
            pass

    # --- CAPA 3: MÓVIL ---
    if not texto_final or len(texto_final) < 500:
        try:
            headers_movil = {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1"
            }
            
            response = requests.get(
                url, 
                headers=headers_movil, 
                timeout=15
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(
                    response.text, 
                    'html.parser'
                )
                
                for element in soup(['script', 'style', 'nav', 'footer']):
                    element.decompose()
                    
                texto_final = soup.get_text(separator=' ', strip=True)
        except:
            pass

    # --- VEREDICTO FINAL ---
    if len(texto_final) > 400:
        return texto_final[:6000], es_portal_conocido
    else:
        return "⚠️ SECURITY ALERT: Automated access blocked. Please copy description manually.", es_portal_conocido

# ==============================================================================
#
#    2. CONFIGURACIÓN DE IA, CONEXIONES Y WEBHOOKS (MAKE)
#
# ==============================================================================

try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("⚠️ CRITICAL ERROR: OPENAI_API_KEY not found.")
    st.stop()

conn = st.connection("gsheets", type=GSheetsConnection)

# ----------------------------------------------------------------------
#  AQUÍ PEGA TU URL DE MAKE (INTEGROMAT)
# ----------------------------------------------------------------------
# Esta URL única manejará tanto Pro como Agencia.
WEBHOOK_MAKE_GENERAL = "PEGAR_TU_WEBHOOK_AQUI" 

# ==============================================================================
#
#    3. FUNCIONES DE BASE DE DATOS
#
# ==============================================================================

def obtener_datos_db():
    try:
        df = conn.read(worksheet="Sheet1", ttl=0)
        df['email'] = df['email'].astype(str).str.strip().str.lower()
        
        if 'plan' in df.columns:
            df['plan'] = df['plan'].astype(str).str.strip().str.title()
            
        if 'vencimiento' not in df.columns:
            df['vencimiento'] = ""
            
        if 'ultima_fecha' not in df.columns:
            df['ultima_fecha'] = ""

        if 'password' not in df.columns:
            df['password'] = ""
            
        return df
    except:
        return pd.DataFrame(
            columns=['email', 'usos', 'plan', 'vencimiento', 'ultima_fecha', 'password']
        )

def obtener_empleados_db():
    try:
        df = conn.read(worksheet="Employees", ttl=0)
        df['BossEmail'] = df['BossEmail'].astype(str).str.strip().str.lower()
        df['EmployeeEmail'] = df['EmployeeEmail'].astype(str).str.strip().str.lower()
        return df
    except:
        return pd.DataFrame(columns=['BossEmail', 'EmployeeEmail'])

def obtener_historial_db():
    try:
        df = conn.read(worksheet="Historial", ttl=0)
        return df
    except:
        return pd.DataFrame(columns=['fecha', 'email', 'input', 'output'])

def actualizar_usos_db(email, nuevos_usos, plan_actual):
    email = email.strip().lower() 
    df = obtener_datos_db()
    hoy_str = datetime.now().strftime("%Y-%m-%d")
    
    if 'plan' not in df.columns:
        df['plan'] = 'Gratis'

    if email in df['email'].values:
        df.loc[df['email'] == email, 'usos'] = nuevos_usos
        df.loc[df['email'] == email, 'ultima_fecha'] = hoy_str
        
        if plan_actual and plan_actual.lower() in ["pro", "agencia", "agency"]:
             df.loc[df['email'] == email, 'plan'] = "Pro"
    else:
        nueva_fila = pd.DataFrame({
            "email": [email], 
            "usos": [nuevos_usos], 
            "plan": [plan_actual.title() if plan_actual else "Gratis"],
            "vencimiento": [""],
            "ultima_fecha": [hoy_str],
            "password": [""]
        })
        df = pd.concat([df, nueva_fila], ignore_index=True)
    
    conn.update(worksheet="Sheet1", data=df)

def verificar_reseteo_diario(email):
    df = obtener_datos_db()
    if email in df['email'].values:
        row = df[df['email'] == email].iloc[0]
        ultima = str(row['ultima_fecha']).strip()
        hoy = datetime.now().strftime("%Y-%m-%d")
        
        if ultima != hoy:
            df.loc[df['email'] == email, 'usos'] = 0
            df.loc[df['email'] == email, 'ultima_fecha'] = hoy
            conn.update(worksheet="Sheet1", data=df)
            return 0
        else:
            return int(row['usos'])
    return 0

def verificar_vencimiento(email, plan_actual):
    if plan_actual == "Gratis":
        return "Gratis"
    
    df = obtener_datos_db()
    if email in df['email'].values:
        row = df[df['email'] == email].iloc[0]
        fecha_str = str(row['vencimiento']).strip()
        
        if fecha_str and fecha_str.lower() != "nan" and fecha_str != "":
            try:
                fecha_venc = datetime.strptime(fecha_str, "%Y-%m-%d")
                if datetime.now() > fecha_venc:
                    df.loc[df['email'] == email, 'plan'] = 'Gratis'
                    conn.update(worksheet="Sheet1", data=df)
                    return "Gratis"
            except:
                pass 
    return plan_actual

def procesar_login_registro(email, input_pass):
    email = email.strip().lower()
    input_pass = input_pass.strip()
    
    df_users = obtener_datos_db()
    
    # 1. USUARIO EXISTENTE
    if email in df_users['email'].values:
        row = df_users[df_users['email'] == email].iloc[0]
        stored_pass = str(row['password']).strip()
        
        if stored_pass and stored_pass.lower() != "nan" and stored_pass != "":
            # Si hay contraseña guardada, verificarla
            if input_pass != stored_pass:
                return False, "❌ Incorrect Password / Contraseña Incorrecta.", False
            else:
                return True, "✅ Login Success.", False
        else:
            # Si no hay pass, pasa directo
            return True, "✅ Login Success.", False
            
    # 2. USUARIO NUEVO (AUTO-REGISTRO)
    else:
        hoy_str = datetime.now().strftime("%Y-%m-%d")
        
        nueva_fila = pd.DataFrame({
            "email": [email], 
            "usos": [0], 
            "plan": ["Gratis"],
            "vencimiento": [""],
            "ultima_fecha": [hoy_str],
            "password": [input_pass]
        })
        
        try:
            df_updated = pd.concat([df_users, nueva_fila], ignore_index=True)
            conn.update(worksheet="Sheet1", data=df_updated)
            return True, "✨ Account Created Successfully.", True
        except Exception as e:
            return False, f"Error creating user: {e}", False

def guardar_historial(email, input_user, output_ia):
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
    except:
        pass

def guardar_feedback(email, mensaje):
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
    except:
        return False

def generar_texto(prompt, modelo="gpt-4o"):
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
# 4. CONFIGURACIÓN DE PÁGINA Y VARIABLES DE ESTADO
# ==============================================================================

st.set_page_config(
    page_title="AI Realty Pro Platinum", 
    page_icon="🏢", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

if "usos" not in st.session_state: st.session_state.usos = 0
if "email_usuario" not in st.session_state: st.session_state.email_usuario = ""
if "plan_usuario" not in st.session_state: st.session_state.plan_usuario = "Gratis"
if "es_empleado" not in st.session_state: st.session_state.es_empleado = False
if "idioma" not in st.session_state: st.session_state.idioma = "English"
if "last_result" not in st.session_state: st.session_state.last_result = None

# ==============================================================================
# 5. DICCIONARIO MAESTRO
# ==============================================================================

traducciones = {
    "English": {
        "title1": "Turn Boring Listings into", 
        "title2": "Sales Magnets", 
        "sub": "The secret AI tool for top-producing agents.",
        "placeholder": "🏠 Describe property...", 
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
        "foot_desc": "AI for Real Estate.",
        "mail_label": "📧 Professional Email", 
        "pass_label": "🔑 Password",
        "limit_msg": "🚫 Free limit reached.", 
        "upgrade_msg": "Upgrade to PRO.",
        "lbl_tone": "Tone:", 
        "lbl_lang_out": "Output Language:", 
        "annual_toggle": "📅 Save 20% Yearly", 
        "annual_save": "✅ 2 Months FREE", 
        "whatsapp": "Send to WhatsApp", 
        "download": "Download Report", 
        "copy_success": "Copied!", 
        "revoke": "Revoke Access", 
        "manage_team": "👥 Manage Team",
        "team_activity": "📈 Activity", 
        "refine_pl": "🔄 Quick adjust...", 
        "social_title": "📱 Social Media Pack",
        "char_count": "Characters", 
        "link_warn": "⚠️ Link not recognized.", 
        "badge_free": "FREE USER", 
        "badge_pro": "PRO MEMBER", 
        "badge_agency": "AGENCY PARTNER", 
        "legal_title": "Terms", 
        "logout": "Log Out", 
        "welcome": "Welcome",
        "usage_bar": "Daily Progress", 
        "feedback_lbl": "💡 Feedback", 
        "feedback_btn": "Send", 
        "support_mail": "Support", 
        "credits_left": "Credits:", 
        "welcome_morn": "Good morning", 
        "welcome_aft": "Good afternoon", 
        "welcome_eve": "Good evening", 
        "impact_text": "SALES IMPACT BOOSTED", 
        "strategy_gen": "GENERATED STRATEGY", 
        "desc_luxury": "LUXURY DESCRIPTION", 
        "btn_refine": "Refine", 
        "analyzing_msg": "ANALYZING...", 
        "feedback_success": "✅ Saved.", 
        "tone_lux": "Luxury", 
        "tone_prof": "Professional", 
        "tone_urg": "Urgency", 
        "tone_story": "Storytelling", 
        "emp_email_lbl": "Agent Email", 
        "emp_add_btn": "ADD", 
        "pass_error": "Incorrect Password", 
        "sec_1": "SECTION 1: MAIN DESCRIPTION", 
        "sec_2": "SECTION 2: TECHNICAL SPECS", 
        "sec_3": "SECTION 3: WHATSAPP", 
        "sec_4": "SECTION 4: SEO", 
        "sec_short": "SHORT DESCRIPTION", 
        "tab_team": "👥 My Team", 
        "tab_monitor": "📊 Activity Monitor", 
        "monitor_desc": "Team usage.", 
        "monitor_empty": "No data yet.", 
        "expired_msg": "⚠️ Expired.", 
        "test_title": "What Experts Say", 
        "test1_txt": "Sales +50%.", 
        "test1_au": "Carlos R.", 
        "test2_txt": "Saves hours.", 
        "test2_au": "Ana M.", 
        "test3_txt": "Key tool.", 
        "test3_au": "Luis P." 
    },
    "Español": {
        "title1": "Convierte Anuncios Aburridos en", 
        "title2": "Imanes de Ventas", 
        "sub": "Herramienta IA para agentes top.",
        "placeholder": "🏠 Describe la propiedad...", 
        "url_placeholder": "🔗 Pega el link...", 
        "btn_gen": "✨ GENERAR ESTRATEGIA", 
        "p_destacada": "DESTACADO", 
        "comunidad": "Comunidad", 
        "popular": "MÁS POPULAR", 
        "plan1": "Inicial", 
        "plan2": "Agente Pro", 
        "plan3": "Agencia", 
        "desc1": "3 descripciones / día", 
        "t1_1": "Límite diario prueba.", 
        "desc2": "Soporte Básico", 
        "t1_2": "Ayuda básica.", 
        "desc3": "Marca de Agua", 
        "t1_3": "Texto con firma.", 
        "desc4": "Generaciones Ilimitadas", 
        "t2_1": "Sin límites.", 
        "desc5": "Pack Redes Sociales", 
        "t2_2": "Scripts para Instagram, TikTok y Reels.", 
        "desc6": "Optimización SEO", 
        "t2_3": "Palabras clave.", 
        "desc7": "Banner Principal", 
        "t2_4": "Rotación en home.", 
        "desc8": "5 Usuarios / Cuentas", 
        "t3_1": "Acceso equipo.", 
        "desc9": "Panel de Equipo", 
        "t3_2": "Gestiona agentes.", 
        "desc10": "Acceso API", 
        "t3_3": "Próximamente.", 
        "desc11": "Prioridad en Banner", 
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
        "step3_d": "Cierra tratos.", 
        "stat1": "Optimizado", 
        "stat2": "Ahorro", 
        "stat3": "Conversión", 
        "foot_desc": "IA Inmobiliaria.", 
        "mail_label": "📧 Email", 
        "pass_label": "🔑 Contraseña", 
        "limit_msg": "🚫 Límite.", 
        "upgrade_msg": "Pásate a PRO.", 
        "lbl_tone": "Tono:", 
        "lbl_lang_out": "Idioma:", 
        "annual_toggle": "📅 Ahorro Anual", 
        "annual_save": "✅ 2 Meses GRATIS", 
        "whatsapp": "WhatsApp", 
        "download": "Descargar", 
        "copy_success": "¡Copiado!", 
        "revoke": "Revocar", 
        "manage_team": "👥 Equipo", 
        "team_activity": "📈 Actividad", 
        "refine_pl": "🔄 Ajuste...", 
        "social_title": "📱 Redes", 
        "char_count": "Caracteres", 
        "link_warn": "⚠️ Error.", 
        "badge_free": "GRATIS", 
        "badge_pro": "PRO", 
        "badge_agency": "AGENCIA", 
        "legal_title": "Legales", 
        "logout": "Salir", 
        "welcome": "Hola", 
        "usage_bar": "Progreso", 
        "feedback_lbl": "💡 Ayuda", 
        "feedback_btn": "Enviar", 
        "support_mail": "Soporte", 
        "credits_left": "Créditos:", 
        "welcome_morn": "Buenos días", 
        "welcome_aft": "Buenas tardes", 
        "welcome_eve": "Buenas noches", 
        "impact_text": "IMPACTO AUMENTADO", 
        "strategy_gen": "ESTRATEGIA", 
        "desc_luxury": "LUJO", 
        "btn_refine": "Refinar", 
        "analyzing_msg": "ANALIZANDO...", 
        "feedback_success": "✅ Guardado.", 
        "pass_error": "Contraseña Incorrecta", 
        "tone_lux": "Lujo", 
        "tone_prof": "Profesional", 
        "tone_urg": "Urgencia", 
        "tone_story": "Storytelling", 
        "emp_email_lbl": "Email", 
        "emp_add_btn": "AÑADIR", 
        "sec_1": "SECCIÓN 1", 
        "sec_2": "SECCIÓN 2", 
        "sec_3": "SECCIÓN 3", 
        "sec_4": "SECCIÓN 4", 
        "sec_short": "CORTA", 
        "tab_team": "👥 Equipo", 
        "tab_monitor": "📊 Monitor", 
        "monitor_desc": "Historial.", 
        "monitor_empty": "Sin datos.", 
        "expired_msg": "⚠️ Vencido.", 
        "test_title": "Expertos", 
        "test1_txt": "Ventas +50%.", 
        "test1_au": "Carlos R.", 
        "test2_txt": "Ahorro horas.", 
        "test2_au": "Ana M.", 
        "test3_txt": "Vital.", 
        "test3_au": "Luis P." 
    },
    "Português": {
        "title1": "Transforme Anúncios", 
        "title2": "Ímãs de Vendas", 
        "sub": "Ferramenta secreta.", 
        "placeholder": "🏠 Descreva...", 
        "url_placeholder": "🔗 Link...", 
        "btn_gen": "✨ GERAR", 
        "p_destacada": "DESTAQUE", 
        "comunidad": "Comunidade", 
        "popular": "POPULAR", 
        "plan1": "Inicial", 
        "plan2": "Pro", 
        "plan3": "Agência", 
        "desc1": "3/dia", 
        "desc2": "Suporte", 
        "desc3": "Marca d'água", 
        "desc4": "Ilimitado", 
        "desc5": "Social Pack", 
        "desc6": "SEO", 
        "desc7": "Banner", 
        "desc8": "5 Usuários", 
        "desc9": "Painel", 
        "desc10": "API", 
        "desc11": "Prioridade", 
        "btn1": "GRÁTIS", 
        "btn2": "UPGRADE", 
        "btn3": "CONTATO", 
        "how_title": "Funciona?", 
        "step1_t": "Link", 
        "step1_d": "Detalhes.", 
        "step2_t": "IA Analisa", 
        "step2_d": "Motor.", 
        "step3_t": "Venda", 
        "step3_d": "Publique.", 
        "stat1": "Otimizados", 
        "stat2": "Tempo", 
        "stat3": "Conversão", 
        "foot_desc": "IA Imobiliária.", 
        "mail_label": "📧 Email", 
        "pass_label": "🔑 Senha", 
        "limit_msg": "🚫 Limite.", 
        "upgrade_msg": "Mude para PRO.", 
        "lbl_tone": "Tom:", 
        "lbl_lang_out": "Idioma:", 
        "annual_toggle": "📅 Anual", 
        "annual_save": "✅ 2 Meses", 
        "whatsapp": "WhatsApp", 
        "download": "Baixar", 
        "copy_success": "Copiado!", 
        "revoke": "Revogar", 
        "manage_team": "👥 Equipe", 
        "team_activity": "📈 Atividade", 
        "refine_pl": "🔄 Ajuste...", 
        "social_title": "📱 Social", 
        "char_count": "Caracteres", 
        "link_warn": "⚠️ Erro.", 
        "badge_free": "GRÁTIS", 
        "badge_pro": "PRO", 
        "badge_agency": "AGÊNCIA", 
        "legal_title": "Termos", 
        "logout": "Sair", 
        "welcome": "Olá", 
        "usage_bar": "Progresso", 
        "feedback_lbl": "💡 Suporte", 
        "feedback_btn": "Enviar", 
        "support_mail": "Suporte", 
        "credits_left": "Créditos:", 
        "welcome_morn": "Bom dia", 
        "welcome_aft": "Boa tarde", 
        "welcome_eve": "Boa noite", 
        "impact_text": "IMPACTO AUMENTADO", 
        "strategy_gen": "ESTRATÉGIA", 
        "desc_luxury": "LUXO", 
        "btn_refine": "Refinar", 
        "analyzing_msg": "ANALISANDO...", 
        "feedback_success": "✅ Obrigado!", 
        "tone_lux": "Luxo", 
        "tone_prof": "Pro", 
        "tone_urg": "Urgência", 
        "tone_story": "Story", 
        "pass_error": "Senha Incorreta", 
        "emp_email_lbl": "Email", 
        "emp_add_btn": "ADD", 
        "sec_1": "SEÇÃO 1", 
        "sec_2": "SEÇÃO 2", 
        "sec_3": "SEÇÃO 3", 
        "sec_4": "SEÇÃO 4", 
        "sec_short": "CURTA", 
        "tab_team": "👥 Equipe", 
        "tab_monitor": "📊 Monitor", 
        "monitor_desc": "Histórico.", 
        "monitor_empty": "Sem dados.", 
        "expired_msg": "⚠️ Expirado.", 
        "test_title": "Especialistas", 
        "test1_txt": "Vendas +50%.", 
        "test1_au": "Carlos R.", 
        "test2_txt": "Tempo.", 
        "test2_au": "Ana M.", 
        "test3_txt": "Vital.", 
        "test3_au": "Luis P." 
    },
    "Français": {
        "title1": "Transformez Annonces", 
        "title2": "Aimants Ventes", 
        "sub": "Outil secret.", 
        "placeholder": "🏠 Décrivez...", 
        "url_placeholder": "🔗 Lien...", 
        "btn_gen": "✨ GÉNÉRER", 
        "p_destacada": "VEDETTE", 
        "comunidad": "Communauté", 
        "popular": "POPULAIRE", 
        "plan1": "Initial", 
        "plan2": "Pro", 
        "plan3": "Agence", 
        "desc1": "3/jour", 
        "desc2": "Support", 
        "desc3": "Filigrane", 
        "desc4": "Illimité", 
        "desc5": "Social", 
        "desc6": "SEO", 
        "desc7": "Bannière", 
        "desc8": "5 Utilisateurs", 
        "desc9": "Tableau", 
        "desc10": "API", 
        "desc11": "Priorité", 
        "btn1": "GRATUIT", 
        "btn2": "UPGRADE", 
        "btn3": "CONTACT", 
        "how_title": "Marche?", 
        "step1_t": "Lien", 
        "step1_d": "Détails.", 
        "step2_t": "IA Analyse", 
        "step2_d": "Moteur.", 
        "step3_t": "Vendez", 
        "step3_d": "Publiez.", 
        "stat1": "Optimisés", 
        "stat2": "Temps", 
        "stat3": "Conversion", 
        "foot_desc": "IA Immo.", 
        "mail_label": "📧 Email", 
        "pass_label": "🔑 Mot de passe", 
        "limit_msg": "🚫 Limite.", 
        "upgrade_msg": "Passez PRO.", 
        "lbl_tone": "Ton:", 
        "lbl_lang_out": "Langue:", 
        "annual_toggle": "📅 Annuel", 
        "annual_save": "✅ 2 Mois", 
        "whatsapp": "WhatsApp", 
        "download": "Télécharger", 
        "copy_success": "Copié!", 
        "revoke": "Révoquer", 
        "manage_team": "👥 Équipe", 
        "team_activity": "📈 Activité", 
        "refine_pl": "🔄 Ajustement...", 
        "social_title": "📱 Social", 
        "char_count": "Caractères", 
        "link_warn": "⚠️ Erreur.", 
        "badge_free": "GRATUIT", 
        "badge_pro": "PRO", 
        "badge_agency": "AGENCE", 
        "legal_title": "Mentions", 
        "logout": "Déco", 
        "welcome": "Bienvenue", 
        "usage_bar": "Progrès", 
        "feedback_lbl": "💡 Support", 
        "feedback_btn": "Envoyer", 
        "support_mail": "Support", 
        "credits_left": "Crédits:", 
        "welcome_morn": "Bonjour", 
        "welcome_aft": "Après-midi", 
        "welcome_eve": "Bonsoir", 
        "impact_text": "IMPACT AUGMENTÉ", 
        "strategy_gen": "STRATÉGIE", 
        "desc_luxury": "LUXE", 
        "btn_refine": "Raffiner", 
        "analyzing_msg": "ANALYSE...", 
        "feedback_success": "✅ Merci!", 
        "tone_lux": "Luxe", 
        "tone_prof": "Pro", 
        "tone_urg": "Urgence", 
        "tone_story": "Story", 
        "pass_error": "Erreur mot de passe", 
        "emp_email_lbl": "Email", 
        "emp_add_btn": "AJOUTER", 
        "sec_1": "SECTION 1", 
        "sec_2": "SECTION 2", 
        "sec_3": "SECTION 3", 
        "sec_4": "SECTION 4", 
        "sec_short": "COURTE", 
        "tab_team": "👥 Équipe", 
        "tab_monitor": "📊 Moniteur", 
        "monitor_desc": "Historique.", 
        "monitor_empty": "Pas données.", 
        "expired_msg": "⚠️ Expiré.", 
        "test_title": "Avis", 
        "test1_txt": "Ventes +50%.", 
        "test1_au": "Carlos R.", 
        "test2_txt": "Temps.", 
        "test2_au": "Ana M.", 
        "test3_txt": "Vital.", 
        "test3_au": "Luis P." 
    },
    "Deutsch": {
        "title1": "Anzeigen verwandeln", 
        "title2": "Verkaufsmagnete", 
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
        "desc1": "3/Tag", 
        "desc2": "Support", 
        "desc3": "Wasserzeichen", 
        "desc4": "Unbegrenzt", 
        "desc5": "Social", 
        "desc6": "SEO", 
        "desc7": "Banner", 
        "desc8": "5 Nutzer", 
        "desc9": "Panel", 
        "desc10": "API", 
        "desc11": "Priorität", 
        "btn1": "GRATIS", 
        "btn2": "UPGRADE", 
        "btn3": "KONTAKT", 
        "how_title": "Funktion?", 
        "step1_t": "Link", 
        "step1_d": "Details.", 
        "step2_t": "KI Analyse", 
        "step2_d": "Motor.", 
        "step3_t": "Verkaufen", 
        "step3_d": "Kopieren.", 
        "stat1": "Optimiert", 
        "stat2": "Zeit", 
        "stat3": "Konversion", 
        "foot_desc": "Immo-KI.", 
        "mail_label": "📧 E-Mail", 
        "pass_label": "🔑 Passwort", 
        "limit_msg": "🚫 Limit.", 
        "upgrade_msg": "Upgrade PRO.", 
        "lbl_tone": "Ton:", 
        "lbl_lang_out": "Sprache:", 
        "annual_toggle": "📅 Jährlich", 
        "annual_save": "✅ 2 Monate", 
        "whatsapp": "WhatsApp", 
        "download": "Download", 
        "copy_success": "Kopiert!", 
        "revoke": "Widerrufen", 
        "manage_team": "👥 Team", 
        "team_activity": "📈 Aktivität", 
        "refine_pl": "🔄 Anpassung...", 
        "social_title": "📱 Social", 
        "char_count": "Zeichen", 
        "link_warn": "⚠️ Fehler.", 
        "badge_free": "GRATIS", 
        "badge_pro": "PRO", 
        "badge_agency": "AGENTUR", 
        "legal_title": "Recht", 
        "logout": "Abmelden", 
        "welcome": "Hallo", 
        "usage_bar": "Fortschritt", 
        "feedback_lbl": "💡 Support", 
        "feedback_btn": "Senden", 
        "support_mail": "Support", 
        "credits_left": "Credits:", 
        "welcome_morn": "Morgen", 
        "welcome_aft": "Tag", 
        "welcome_eve": "Abend", 
        "impact_text": "IMPAKT HOCH", 
        "strategy_gen": "STRATEGIE", 
        "desc_luxury": "LUXUS", 
        "btn_refine": "Verfeinern", 
        "analyzing_msg": "ANALYSE...", 
        "feedback_success": "✅ Danke!", 
        "tone_lux": "Luxus", 
        "tone_prof": "Profi", 
        "tone_urg": "Dringend", 
        "tone_story": "Story", 
        "emp_email_lbl": "E-Mail", 
        "emp_add_btn": "NEU", 
        "pass_error": "Falsches Passwort", 
        "sec_1": "TEIL 1", 
        "sec_2": "TEIL 2", 
        "sec_3": "TEIL 3", 
        "sec_4": "TEIL 4", 
        "sec_short": "KURZ", 
        "tab_team": "👥 Team", 
        "tab_monitor": "📊 Monitor", 
        "monitor_desc": "Verlauf.", 
        "monitor_empty": "Keine Daten.", 
        "expired_msg": "⚠️ Abgelaufen.", 
        "test_title": "Experten", 
        "test1_txt": "Umsatz +50%.", 
        "test1_au": "Carlos R.", 
        "test2_txt": "Zeit.", 
        "test2_au": "Ana M.", 
        "test3_txt": "Wichtig.", 
        "test3_au": "Luis P." 
    },
    "中文": {
        "title1": "广告转化", 
        "title2": "销售磁铁", 
        "sub": "秘密工具。", 
        "placeholder": "🏠 描述...", 
        "url_placeholder": "🔗 链接...", 
        "btn_gen": "✨ 生成", 
        "p_destacada": "精选", 
        "comunidad": "社区", 
        "popular": "热门", 
        "plan1": "基础", 
        "plan2": "专业", 
        "plan3": "机构", 
        "desc1": "3条/天", 
        "desc2": "支持", 
        "desc3": "水印", 
        "desc4": "无限", 
        "desc5": "社交", 
        "desc6": "SEO", 
        "desc7": "横幅", 
        "desc8": "5用户", 
        "desc9": "面板", 
        "desc10": "API", 
        "desc11": "优先", 
        "btn1": "免费", 
        "btn2": "升级", 
        "btn3": "联系", 
        "how_title": "如何?", 
        "step1_t": "链接", 
        "step1_d": "详情。", 
        "step2_t": "AI分析", 
        "step2_d": "引擎。", 
        "step3_t": "销售", 
        "step3_d": "发布。", 
        "stat1": "优化", 
        "stat2": "时间", 
        "stat3": "转化", 
        "foot_desc": "房产AI。", 
        "mail_label": "📧 邮箱", 
        "pass_label": "🔑 密码", 
        "limit_msg": "🚫 限制。", 
        "upgrade_msg": "升级PRO。", 
        "lbl_tone": "语气:", 
        "lbl_lang_out": "语言:", 
        "annual_toggle": "📅 年付", 
        "annual_save": "✅ 送2月", 
        "whatsapp": "WhatsApp", 
        "download": "下载", 
        "copy_success": "已复制!", 
        "revoke": "撤销", 
        "manage_team": "👥 团队", 
        "team_activity": "📈 活动", 
        "refine_pl": "🔄 调整...", 
        "social_title": "📱 社交", 
        "char_count": "字数", 
        "link_warn": "⚠️ 错误。", 
        "badge_free": "免费", 
        "badge_pro": "专业", 
        "badge_agency": "机构", 
        "legal_title": "条款", 
        "logout": "退出", 
        "welcome": "欢迎", 
        "usage_bar": "进度", 
        "feedback_lbl": "💡 反馈", 
        "feedback_btn": "发送", 
        "support_mail": "支持", 
        "credits_left": "额度:", 
        "welcome_morn": "早安", 
        "welcome_aft": "午安", 
        "welcome_eve": "晚安", 
        "impact_text": "影响力提升", 
        "strategy_gen": "策略", 
        "desc_luxury": "豪华", 
        "btn_refine": "完善", 
        "analyzing_msg": "分析中...", 
        "feedback_success": "✅ 谢谢!", 
        "tone_lux": "豪华", 
        "tone_prof": "专业", 
        "tone_urg": "紧迫", 
        "tone_story": "故事", 
        "emp_email_lbl": "邮箱", 
        "emp_add_btn": "添加", 
        "pass_error": "密码错误", 
        "sec_1": "第1部分", 
        "sec_2": "第2部分", 
        "sec_3": "第3部分", 
        "sec_4": "第4部分", 
        "sec_short": "简短", 
        "tab_team": "👥 团队", 
        "tab_monitor": "📊 监控", 
        "monitor_desc": "历史。", 
        "monitor_empty": "无数据。", 
        "expired_msg": "⚠️ 过期.", 
        "test_title": "专家", 
        "test1_txt": "销售+50%.", 
        "test1_au": "Carlos R.", 
        "test2_txt": "省时.", 
        "test2_au": "Ana M.", 
        "test3_txt": "必备.", 
        "test3_au": "Luis P." 
    }
}

# ==============================================================================
# 5. ESTILOS CSS PLATINUM
# ==============================================================================

st.markdown("""
<style>
    /* CSS CORE */
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 5rem !important; 
    }
    .stApp { 
        background-color: #0e1117; 
        color: #FFFFFF; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }
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
    
    /* SCROLLBAR */
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
    
    /* UI ELEMENTS */
    ::selection { 
        background: rgba(0, 210, 255, 0.25); 
        color: #00d2ff; 
    }
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
    
    /* HUD */
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
    .badge-agency { 
        border-color: #DDA0DD; 
        color: #DDA0DD; 
        box-shadow: 0 0 15px rgba(221, 160, 221, 0.4); 
    }
    
    /* RESULTS */
    .result-container { 
        background: rgba(20, 20, 20, 0.95); 
        color: #f0f0f0; 
        padding: 30px; 
        border-radius: 15px; 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        font-size: 1.1rem; 
        line-height: 1.6; 
        margin-top: 25px; 
        box-shadow: 0 15px 40px rgba(0,0,0,0.8); 
        backdrop-filter: blur(10px); 
    }
    
    /* BUTTONS */
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
    
    /* CARDS */
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
        box-shadow: 0 10px 20px rgba(255, 255, 255, 0.2); 
        border-color: rgba(255,255,255,0.4); 
    }
    .pro-card { 
        border: 1px solid rgba(0, 210, 255, 0.3) !important; 
    }
    .pro-card:hover { 
        border: 1px solid rgba(0, 210, 255, 0.6) !important; 
        box-shadow: 0 10px 30px rgba(0, 210, 255, 0.3); 
    }
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
    }
    .glass-container h3 { 
        margin-top: 15px !important; 
    }

    /* TOOLTIPS */
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
        width: 220px; 
        z-index: 999; 
        box-shadow: 0 10px 40px rgba(0,0,0,0.9); 
        border: 1px solid rgba(255,255,255,0.1); 
        line-height: 1.4; 
        text-align: center; 
    }
    .feature-list { 
        text-align: left; 
        margin: 10px auto; 
        display: inline-block; 
        font-size: 0.95rem; 
        color: #ddd; 
        line-height: 1.8; 
    }
    
    /* ANIMATIONS */
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
        50% { transform: translateY(-12px); 
        100% { transform: translateY(0px); } 
    }

    /* METER */
    .meter-container { 
        background: rgba(255, 255, 255, 0.05); 
        border-radius: 4px; 
        height: 3px; 
        width: 100%; 
        position: relative; 
        overflow: hidden; 
        margin-top: 15px; 
        border: none; 
    }
    .meter-fill { 
        height: 100%; 
        background: linear-gradient(90deg, #D4AF37, #FFD700, #F2D06B); 
        width: 0%; 
        animation: fillMeter 2s ease-out forwards; 
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.6); 
    }
    .meter-text { 
        width: 100%; 
        text-align: left; 
        margin-bottom: 5px; 
        font-weight: 700; 
        color: #D4AF37; 
        text-transform: uppercase; 
        font-size: 0.8rem; 
        letter-spacing: 2px; 
    }
    @keyframes fillMeter { 
        from { width: 0%; } 
        to { width: 100%; } 
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 6. SIDEBAR
# ==============================================================================

with st.sidebar:
    st.markdown('<div style="text-align:center; font-size: 1.6rem; font-weight: 800; color: #fff; letter-spacing: 1px;">🏢 AI REALTY</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    idioma_selec = st.selectbox("🌐 Idioma / Language", list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma))
    st.session_state.idioma = idioma_selec
    L = traducciones[st.session_state.idioma]

    if st.session_state.email_usuario:
        st.markdown(f"### {L.get('welcome', 'Bienvenido')}")
        st.markdown(f"**{st.session_state.email_usuario}**")
        
        usos = st.session_state.usos
        es_pro_local = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite = 99999 if es_pro_local else 3
        color_cred = "#ff4b4b" if (not es_pro_local and 3-usos <= 1) else "#00d2ff"
        restantes = "∞" if es_pro_local else str(3 - usos)
        
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; border: 1px solid {color_cred}; margin-bottom: 10px;">
            <div style="font-size: 0.85rem; color: #aaa;">{L.get('credits_left', 'Créditos:')}</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: {color_cred};">{restantes}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if limite < 100: 
            st.progress(min(usos / limite, 1.0))
        else: 
            st.progress(1.0)
            
        st.markdown("---")
        if st.button(f"🚪 {L.get('logout', 'Salir')}"):
            try: 
                cookie_manager.delete("user_email")
            except: 
                pass
            st.session_state.email_usuario = ""
            st.session_state.usos = 0
            st.rerun()

    st.markdown("---")
    st.subheader(L.get("feedback_lbl", "💡 Ayuda"))
    st.markdown(f"📧 **{L.get('support_mail', 'Soporte')}: support@airealtypro.com**")
    fb_text = st.text_area("", placeholder=L.get("feedback_lbl", "..."), height=100, label_visibility="collapsed", key="fb_input")
    
    if st.button(L.get("feedback_btn", "Enviar"), use_container_width=True):
        if fb_text:
            with st.spinner("Enviando..."):
                ok = guardar_feedback(st.session_state.email_usuario, fb_text)
                if ok: 
                    st.toast(L["feedback_success"])
                else: 
                    st.error("Error.")
    st.markdown("---")
    st.markdown(f"<div style='text-align:center; color:#666; font-size:0.8rem;'>v2.7 Final Build</div>", unsafe_allow_html=True)

# ==============================================================================
# 7. INTERFAZ
# ==============================================================================

col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo:
    st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px; letter-spacing: 1px;">🏢 AI REALTY PRO</div>', unsafe_allow_html=True)

if st.session_state.email_usuario:
    try:
        df_check = obtener_datos_db()
        if st.session_state.email_usuario in df_check['email'].values:
            user_row = df_check[df_check['email'] == st.session_state.email_usuario].iloc[0]
            real_plan = user_row['plan'] if 'plan' in user_row else 'Gratis'
            st.session_state.plan_usuario = real_plan.title() if real_plan else "Gratis"
            st.session_state.usos = int(user_row['usos'])
    except: 
        pass

    hora = datetime.now().hour
    saludo = L["welcome_morn"] if hora < 12 else L["welcome_aft"] if hora < 19 else L["welcome_eve"]
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

col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    st.markdown(f'''
        <div class="video-placeholder">
            <div class="dynamic-tag">{L["p_destacada"]}</div>
            <div style="background:rgba(0,0,0,0.6);width:100%;text-align:center;padding:10px;">{L["comunidad"]}</div>
        </div>
    ''', unsafe_allow_html=True)
 
# ==============================================================================
# 8. LÓGICA PRINCIPAL
# ==============================================================================

if not st.session_state.email_usuario:
    cookie_val = cookie_manager.get("user_email")
    if cookie_val:
        st.session_state.email_usuario = cookie_val
        df_actual = obtener_datos_db()
        df_emp = obtener_empleados_db()
        
        if cookie_val in df_emp['EmployeeEmail'].values:
            jefe_email = df_emp[df_emp['EmployeeEmail'] == cookie_val].iloc[0]['BossEmail']
            if jefe_email in df_actual['email'].values:
                datos_jefe = df_actual[df_actual['email'] == jefe_email].iloc[0]
                plan_jefe_raw = str(datos_jefe['plan']).strip()
                if any(p.lower() in plan_jefe_raw.lower() for p in ["agencia", "agency", "partner"]):
                    st.session_state.plan_usuario = "Pro"
                else:
                    st.session_state.plan_usuario = plan_jefe_raw.title()
                st.session_state.es_empleado = True
                st.session_state.boss_ref = jefe_email
                st.session_state.usos = 0
        
        elif cookie_val in df_actual['email'].values:
            plan_verificado = verificar_vencimiento(cookie_val, df_actual[df_actual['email'] == cookie_val].iloc[0]['plan'])
            st.session_state.plan_usuario = plan_verificado
            usos_reales = verificar_reseteo_diario(cookie_val)
            st.session_state.usos = usos_reales
            usuario = df_actual[df_actual['email'] == cookie_val].iloc[0]
        st.rerun()

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if not st.session_state.email_usuario:
        st.markdown('<div class="glass-container" style="height:auto; box-shadow: 0 0 30px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
        email_input = st.text_input(L["mail_label"], placeholder="email@example.com", key="user_email")
        password_input = st.text_input(L.get("pass_label", "Password"), type="password", key="user_pass")
        
        if st.button("START / ENTRAR", type="primary"):
            if email_input and "@" in email_input:
                exito, mensaje, es_nuevo = procesar_login_registro(email_input, password_input)
                if not exito: 
                    st.error(mensaje)
                else:
                    if es_nuevo: 
                        st.toast("🎉 Account Created!")
                    
                    st.session_state.email_usuario = email_input.strip().lower()
                    try: 
                        cookie_manager.set("user_email", st.session_state.email_usuario, expires_at=datetime.now().replace(year=datetime.now().year + 1))
                    except: 
                        pass
                    
                    df_actual = obtener_datos_db()
                    df_emp = obtener_empleados_db()
                    
                    if st.session_state.email_usuario in df_emp['EmployeeEmail'].values:
                        jefe_email = df_emp[df_emp['EmployeeEmail'] == st.session_state.email_usuario].iloc[0]['BossEmail']
                        if jefe_email in df_actual['email'].values:
                            datos_jefe = df_actual[df_actual['email'] == jefe_email].iloc[0]
                            st.session_state.usos = 0
                            plan_jefe_raw = str(datos_jefe['plan']).strip()
                            if any(p.lower() in plan_jefe_raw.lower() for p in ["agencia", "agency", "partner"]):
                                st.session_state.plan_usuario = "Pro"
                            else:
                                st.session_state.plan_usuario = plan_jefe_raw.title()
                            st.session_state.es_empleado = True
                            st.session_state.boss_ref = jefe_email
                        else:
                            st.session_state.plan_usuario = "Gratis"
                    elif st.session_state.email_usuario in df_actual['email'].values:
                        usuario = df_actual[df_actual['email'] == st.session_state.email_usuario].iloc[0]
                        plan_verificado = verificar_vencimiento(st.session_state.email_usuario, usuario['plan'])
                        st.session_state.plan_usuario = plan_verificado
                        if plan_verificado == "Gratis" and usuario['plan'] != "Gratis":
                            st.toast(L["expired_msg"], icon="⚠️")
                        usos_reales = verificar_reseteo_diario(st.session_state.email_usuario)
                        st.session_state.usos = usos_reales
                        st.session_state.es_empleado = False
                    time.sleep(0.5)
                    st.rerun()
            else: 
                st.error("Invalid Email.")
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.email_usuario:
        es_pro = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite_usos = 99999 if es_pro else 3
        
        if st.session_state.usos < limite_usos:
            st.markdown('<div class="glass-container" style="height:auto;">', unsafe_allow_html=True)
            col_t1, col_t2 = st.columns(2)
            with col_t1: 
                tono_display = st.selectbox(L.get("lbl_tone", "Tone:"), [L["tone_story"], L["tone_prof"], L["tone_urg"], L["tone_lux"]])
                mapa_tonos = {L["tone_story"]: "Storytelling", L["tone_prof"]: "Profesional", L["tone_urg"]: "Urgencia", L["tone_lux"]: "Lujo"}
                tono = mapa_tonos.get(tono_display, "Lujo")
            with col_t2: 
                idioma_salida = st.selectbox(L.get("lbl_lang_out", "Lang:"), list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma))

            url_input = st.text_input("", placeholder=L["url_placeholder"], label_visibility="collapsed")
            user_input = st.text_area("", placeholder=L['placeholder'], key="input_ia", label_visibility="collapsed", height=150)
            st.caption(f"{L.get('char_count', 'Chars')}: {len(user_input)}")

            if st.button(L['btn_gen'], key="main_gen", type="primary"):
                if user_input or url_input: 
                    with st.spinner(f"🚀 {L['analyzing_msg']}"):
                        datos_web, es_valido = extraer_datos_inmueble(url_input) if url_input else ("", True)
                        if not es_valido: 
                            st.toast(L["link_warn"], icon="⚠️")
                        
                        if tono == "Profesional": 
                            instr_estilo = "STYLE: Corporate, direct, data-driven."
                        elif tono == "Storytelling": 
                            instr_estilo = "STYLE: Narrative, emotional, sensory. Describe smells, light."
                        elif tono == "Urgencia": 
                            instr_estilo = "STYLE: Scarcity triggers, short sentences."
                        else: 
                            instr_estilo = "STYLE: Exclusive, sophisticated, high-ticket vocabulary."

                        sec1, sec2, sec3, sec4 = L["sec_1"], L["sec_2"], L["sec_3"], L["sec_4"]
                        
                        if es_pro:
                            instrucciones_plan = f"""
                            GENERATE FULL STRATEGY:
                            {sec_1} ({tono.upper()})
                            {sec_2} (Technical Bullets)
                            {sec_3} (Persuasive w/ emojis)
                            {sec_4} (Title <60 chars, Meta <160 chars)
                            """
                        else:
                            instrucciones_plan = f'GENERATE ONLY: {L["sec_short"]}. Append at the end: "{L["desc3"]}"'

                        prompt_base = f"""
                        ACT AS: Expert Real Estate Copywriter. 
                        OUTPUT LANGUAGE: {idioma_salida}. 
                        {instr_estilo}. 
                        WEB DATA: {datos_web}. 
                        MANUAL DATA: {user_input}. 
                        {instrucciones_plan}. 
                        FORMAT: Markdown.
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
                    st.warning("Input required.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.session_state.last_result:
                p_u = st.session_state.plan_usuario.lower()
                res_color = "#DDA0DD" if ("agencia" in p_u or "agency" in p_u) else "#00d2ff" if "pro" in p_u else "#cccccc"
                
                st.markdown(f"""
                <div class="meter-text">{L['impact_text']}</div>
                <div class="meter-container"><div class="meter-fill"></div></div>
                <style>
                    @keyframes shine {{ 0% {{ background-position: -200% center; }} 100% {{ background-position: 200% center; }} }}
                    .shine-text {{ background: linear-gradient(to right, {res_color} 0%, #ffffff 50%, {res_color} 100%); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 3s linear infinite; font-weight: 900; }}
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown(f'''
                    <div class="result-container" style="border-top: 4px solid {res_color}; border-left: 1px solid {res_color}40; border-right: 1px solid {res_color}40; box-shadow: 0 0 20px {res_color}20;">
                        <div class="shine-text" style="margin-bottom: 15px; letter-spacing: 1.5px; font-size: 1.1rem;">
                            {L['strategy_gen']} ({st.session_state.plan_usuario.upper()})
                        </div>
                        <div style="font-size: 1.05rem;">
                            {st.session_state.last_result.replace("\n", "<br>")}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                b1, b2, b3 = st.columns(3)
                with b1:
                    if st.button(f"📋 COPY"):
                        st.code(st.session_state.last_result)
                        st.toast(L["copy_success"])
                with b2:
                    wa_msg = urllib.parse.quote(st.session_state.last_result[:900])
                    st.link_button(f"📲 {L['whatsapp']}", f"https://wa.me/?text={wa_msg}", use_container_width=True)
                with b3:
                    st.download_button(f"💾 {L['download']}", st.session_state.last_result, file_name=f"Strategy_{datetime.now().strftime('%Y%m%d')}.txt", use_container_width=True)

                if es_pro:
                    st.markdown("---")
                    with st.expander(f"📱 {L.get('social_title', 'Social Pack')}"):
                        with st.spinner("Generating..."):
                            res_social = generar_texto(f"Create IG Post with hashtags and TikTok Script (15s) for: {st.session_state.last_result}")
                            st.markdown(res_social)
                
                st.divider()
                refine = st.text_input("", placeholder=L.get("refine_pl", "..."))
                if st.button(L["btn_refine"]):
                    with st.spinner("Refining..."):
                        nuevo_res = generar_texto(f"Adjust this: {st.session_state.last_result}. User: {refine}")
                        st.session_state.last_result = nuevo_res
                        st.rerun()

        else:
            # Usamos la misma variable para ambos casos
            WEBHOOK_TARGET = WEBHOOK_MAKE_GENERAL
            
            st.error(L["limit_msg"])
            st.markdown(f"#### {L['upgrade_msg']}")
            
            paypal_bloqueo = f"""
            <div id="pb"></div>
            <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
            <script>
            paypal.Buttons({{
                style: {{
                    shape: 'pill',
                    color: 'blue',
                    layout: 'horizontal',
                    label: 'subscribe'
                }},
                createSubscription: function(d, a) {{
                    return a.subscription.create({{
                        'plan_id': 'P-3P2657040E401734NNFQQ5TY',
                        'custom_id': '{st.session_state.email_usuario}'
                    }});
                }},
                onApprove: function(data, actions) {{
                    fetch('{WEBHOOK_TARGET}', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            email: '{st.session_state.email_usuario}',
                            plan: 'Pro',
                            sub_id: data.subscriptionID
                        }})
                    }});
                    alert('Subscription Successful! Your account is being upgraded...');
                }}
            }}).render('#pb');
            </script>
            """
            components.html(paypal_bloqueo, height=100)

# ==============================================================================
# 9. CONSOLA DE AGENCIA
# ==============================================================================

if st.session_state.plan_usuario == "Agencia" and not st.session_state.es_empleado:
    st.divider()
    st.subheader(L["manage_team"])
    tab_equipo, tab_monitor = st.tabs([L["tab_team"], L["tab_monitor"]])
    df_emp = obtener_empleados_db()
    mi_equipo = df_emp[df_emp['BossEmail'] == st.session_state.email_usuario]['EmployeeEmail'].tolist()
    
    with tab_equipo:
        c_add1, c_add2 = st.columns([3, 1])
        with c_add1: 
            nuevo_e = st.text_input(L["emp_email_lbl"], key="new_ag_in", placeholder="agent@agency.com")
        with c_add2:
            st.write(" ")
            if st.button(L["emp_add_btn"]):
                if len(mi_equipo) < 4 and "@" in nuevo_e:
                    new_row_emp = pd.DataFrame({"BossEmail": [st.session_state.email_usuario], "EmployeeEmail": [nuevo_e.strip().lower()]})
                    conn.update(worksheet="Employees", data=pd.concat([df_emp, new_row_emp], ignore_index=True))
                    
                    df_main = obtener_datos_db()
                    if nuevo_e.strip().lower() not in df_main['email'].values:
                        new_row_main = pd.DataFrame({"email": [nuevo_e.strip().lower()], "usos": [0], "plan": ["Pro"], "vencimiento": [""], "ultima_fecha": [""]})
                        conn.update(worksheet="Sheet1", data=pd.concat([df_main, new_row_main], ignore_index=True))
                    st.rerun()
                elif len(mi_equipo) >= 4: 
                    st.warning("Full Team.")
        if mi_equipo:
            st.write("---")
            # --- CORRECCIÓN DE INDENTACIÓN AQUÍ ---
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
            df_hist = obtener_historial_db()
            if not df_hist.empty:
                team_history = df_hist[df_hist['email'].isin(mi_equipo)]
                if not team_history.empty:
                    st.dataframe(team_history.sort_values(by="fecha", ascending=False), use_container_width=True)
                else: 
                    st.write(L["monitor_empty"])
            else: 
                st.write(L["monitor_empty"])

# ==============================================================================
# 10. SECCIÓN INFORMATIVA Y PLANES DE SUSCRIPCIÓN
# ==============================================================================

# 1. ESTADÍSTICAS (PRIMERO)
st.markdown("<br><br>", unsafe_allow_html=True)
col_stat1, col_stat2, col_stat3 = st.columns(3)

with col_stat1: 
    st.markdown(f'''
<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);">
<h2 style="color:#00d2ff; margin:0;">+10k</h2>
<p style="color:#aaa; font-size:0.9rem;">{L["stat1"]}</p>
</div>
''', unsafe_allow_html=True)

with col_stat2: 
    st.markdown(f'''
<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);">
<h2 style="color:#00d2ff; margin:0;">-80%</h2>
<p style="color:#aaa; font-size:0.9rem;">{L["stat2"]}</p>
</div>
''', unsafe_allow_html=True)

with col_stat3: 
    st.markdown(f'''
<div style="text-align:center; padding:20px; border-radius:15px; background:rgba(255,255,255,0.03); border:1px solid rgba(0,210,255,0.2);">
<h2 style="color:#00d2ff; margin:0;">+45%</h2>
<p style="color:#aaa; font-size:0.9rem;">{L["stat3"]}</p>
</div>
''', unsafe_allow_html=True)

# 2. PLANES (SEGUNDO)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center;'>Plans</h3>", unsafe_allow_html=True)

# Switch Anual
col_sw1, col_sw2, col_sw3 = st.columns([1,2,1])
with col_sw2:
    es_anual = st.toggle(L["annual_toggle"], value=False)

# Variables de Precio
precio_pro = "490" if es_anual else "49"
precio_age = "1,990" if es_anual else "199"
id_pro = "P-2PU023636P1209345NFQ7TMY" if es_anual else "P-3P2657040E401734NNFQQ5TY"
id_age = "P-87X83840151393810NFQ7X6Q" if es_anual else "P-0S451470G5041550ENFQRB4I"
ahorro_txt = L["annual_save"] if es_anual else ""

col1, col2, col3 = st.columns(3)

# WEBHOOK ÚNICO (Usamos la variable definida arriba)
WEBHOOK_TARGET = WEBHOOK_MAKE_GENERAL

# --- CARD GRATIS ---
with col1:
    # Tooltips para Gratis
    tt_limite = "Tus 3 créditos se recargan automáticamente cada 24hs. Ideal para probar."
    tt_soporte = "Soporte básico por email en horario comercial."
    
    # HTML STRING FLATTENED TO AVOID </div> ERROR
    desc_f = f"""<div class='feature-list'>
{L['desc1']} <span class='info-icon i-free' data-tooltip='{tt_limite}'>i</span><br>
{L['desc2']} <span class='info-icon i-free' data-tooltip='{tt_soporte}'>i</span><br>
{L['desc3']}
</div>"""
    
    st.markdown(f'''
<div class='card-wrapper free-card'>
<div class='glass-container'>
<h3 style="margin-top:10px;">{L['plan1']}</h3>
<h1>$0</h1>
<hr style='opacity:0.2;'>
{desc_f}
</div>
</div>
''', unsafe_allow_html=True)
    
    if not st.session_state.email_usuario:
        if st.button(L['btn1'], key="btn_f"):
            st.toast("Register above.")

# --- CARD PRO ---
with col2:
    # Tooltips para Pro
    tt_unlimited = "Genera, reescribe y ajusta descripciones infinitas. Nunca te quedas sin saldo."
    tt_social = "Incluye scripts virales para TikTok/Reels y textos de cierre para WhatsApp."
    tt_seo = "Posicionamiento en portales con palabras clave de alto tráfico."
    
    # HTML STRING FLATTENED TO AVOID </div> ERROR
    desc_p = f"""<div class='feature-list'>
<b>{L['desc4']}</b> <span class='info-icon i-pro' data-tooltip='{tt_unlimited}'>i</span><br>
{L['desc5']} + WhatsApp <span class='info-icon i-pro' data-tooltip='{tt_social}'>i</span><br>
{L['desc6']} <span class='info-icon i-pro' data-tooltip='{tt_seo}'>i</span><br>
<b>{L['desc7']}</b>
</div>"""
    
    st.markdown(f'''
<div class='card-wrapper pro-card'>
<div class='glass-container'>
<div class='popular-badge'>{L['popular']}</div>
<h3 style='color:#00d2ff; margin-top:15px;'>{L['plan2']}</h3>
<h1>${precio_pro}</h1>
<p style='color:#00d2ff; font-weight:bold;'>{ahorro_txt}</p>
<hr style='opacity:0.3;'>
{desc_p}
</div>
</div>
''', unsafe_allow_html=True)
    
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
            fetch('{WEBHOOK_TARGET}', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    email: '{st.session_state.email_usuario}',
                    plan: 'Pro',
                    sub_id: data.subscriptionID
                }})
            }});
            alert('Subscription Successful! Activating Pro Plan...');
        }}
      }}).render('#paypal-button-container-pro');
    </script>
    """
    components.html(pay_pro, height=150)

# --- CARD AGENCIA ---
with col3:
    # Tooltips para Agencia
    tt_team = "Gestiona hasta 5 agentes bajo una sola facturación centralizada."
    tt_dash = "Audita el historial y uso de cada agente en tiempo real."
    
    # HTML STRING FLATTENED TO AVOID </div> ERROR
    desc_a = f"""<div class='feature-list'>
{L['desc8']} <span class='info-icon i-agency' data-tooltip='{tt_team}'>i</span><br>
{L['desc9']} <span class='info-icon i-agency' data-tooltip='{tt_dash}'>i</span><br>
{L['desc10']}<br>
<b>{L['desc11']}</b>
</div>"""
    
    st.markdown(f'''
<div class='card-wrapper agency-card'>
<div class='glass-container'>
<h3 style='color:#DDA0DD; margin-top:10px;'>{L['plan3']}</h3>
<h1>${precio_age}</h1>
<p style='color:#DDA0DD; font-weight:bold;'>{ahorro_txt}</p>
<hr style='opacity:0.3;'>
{desc_a}
</div>
</div>
''', unsafe_allow_html=True)
    
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
            fetch('{WEBHOOK_TARGET}', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{
                    email: '{st.session_state.email_usuario}',
                    plan: 'Agency',
                    sub_id: data.subscriptionID
                }})
            }});
            alert('Subscription Successful! Activating Agency Plan...');
        }}
      }}).render('#paypal-button-container-age');
    </script>
    """
    components.html(pay_age, height=150)

# 3. CÓMO FUNCIONA (TERCERO)
st.markdown(f"<br><br><h2 style='text-align:center; color:white;'>{L['how_title']}</h2>", unsafe_allow_html=True)
ch1, ch2, ch3 = st.columns(3)

with ch1: 
    st.markdown(f'''
        <div style='text-align:center;'>
            <h1 style='color:#00d2ff;'>1</h1>
            <p><b>{L['step1_t']}</b><br>{L['step1_d']}</p>
        </div>
    ''', unsafe_allow_html=True)

with ch2: 
    st.markdown(f'''
        <div style='text-align:center;'>
            <h1 style='color:#00d2ff;'>2</h1>
            <p><b>{L['step2_t']}</b><br>{L['step2_d']}</p>
        </div>
    ''', unsafe_allow_html=True)

with ch3: 
    st.markdown(f'''
        <div style='text-align:center;'>
            <h1 style='color:#00d2ff;'>3</h1>
            <p><b>{L['step3_t']}</b><br>{L['step3_d']}</p>
        </div>
    ''', unsafe_allow_html=True)

# 4. RESEÑAS / TESTIMONIOS (CUARTO)
st.markdown(f"<br><br><h3 style='text-align:center; color:white;'>{L.get('test_title', 'Expert Reviews')}</h3>", unsafe_allow_html=True)
t1, t2, t3 = st.columns(3)

with t1:
    st.markdown(f'''
        <div style='padding:15px; border:1px solid #333; border-radius:10px; text-align:center;'>
            <i>"{L['test1_txt']}"</i><br><br>
            <b>{L['test1_au']}</b>
        </div>
    ''', unsafe_allow_html=True)

with t2:
    st.markdown(f'''
        <div style='padding:15px; border:1px solid #333; border-radius:10px; text-align:center;'>
            <i>"{L['test2_txt']}"</i><br><br>
            <b>{L['test2_au']}</b>
        </div>
    ''', unsafe_allow_html=True)

with t3:
    st.markdown(f'''
        <div style='padding:15px; border:1px solid #333; border-radius:10px; text-align:center;'>
            <i>"{L['test3_txt']}"</i><br><br>
            <b>{L['test3_au']}</b>
        </div>
    ''', unsafe_allow_html=True)

# --- FOOTER LEGAL ---
st.markdown(f'''
    <div style="border-top: 1px solid rgba(255,255,255,0.1); padding: 40px 0px; text-align: center;">
        <div style="font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom:10px;">🏢 AI REALTY PRO</div>
        <p style="color:#666; font-size:0.8rem;">© 2026 AI Realty Pro - {L["foot_desc"]}</p>
    </div>
''', unsafe_allow_html=True)

with st.expander(f"⚖️ {L.get('legal_title', 'Términos Legales')}"):
    st.write("1. No credit card data stored (PayPal).")
    st.write("2. AI generated descriptions require review.")
    st.write("3. No refunds on monthly plans.")
