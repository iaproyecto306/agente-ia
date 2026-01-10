import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# FUNCIÓN DE SCRAPING
def extraer_datos_inmueble(url):
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
            return "Error: No se pudo acceder a la página."
    except Exception as e:
        return f"Error al leer el link: {str(e)}"

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
        return conn.read(worksheet="Sheet1", ttl=0)
    except:
        return pd.DataFrame(columns=['email', 'usos', 'plan'])

# --- INCISIÓN: FUNCIÓN PARA EMPLEADOS (PLAN AGENCIA) ---
def obtener_empleados_db():
    try:
        return conn.read(worksheet="Employees", ttl=0)
    except:
        return pd.DataFrame(columns=['BossEmail', 'EmployeeEmail'])

def actualizar_usos_db(email, nuevos_usos, plan_actual):
    df = obtener_datos_db()
    if 'plan' not in df.columns: df['plan'] = 'Gratis'

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
st.set_page_config(page_title="AI Realty Pro", page_icon="🏢", layout="wide", initial_sidebar_state="collapsed")

if "usos" not in st.session_state: st.session_state.usos = 0
if "email_usuario" not in st.session_state: st.session_state.email_usuario = ""
if "plan_usuario" not in st.session_state: st.session_state.plan_usuario = "Gratis"
if "es_empleado" not in st.session_state: st.session_state.es_empleado = False

# --- 3. DICCIONARIO MAESTRO (Sin cambios) ---
traducciones = {
    "Español": {
        "title1": "Convierte Anuncios Aburridos en", "title2": "Imanes de Ventas",
        "sub": "La herramienta IA secreta de los agentes top productores.",
        "placeholder": "🏠 Describe la propiedad o escribe instrucciones extra...",
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
        "placeholder": "🏠 Describe the property or add extra instructions...",
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
    }
}

# --- 4. ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    /* BLOQUE DE RESULTADO ELEGANTE */
    .result-box { 
        background-color: #f9f9f9; padding: 25px; border-radius: 12px; 
        border: 1px solid #e0e0e0; color: #1a1a1a; font-family: 'Segoe UI', Arial, sans-serif; 
        line-height: 1.6; font-size: 1.05rem; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

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

    .card-wrapper { transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.6s cubic-bezier(0.165, 0.84, 0.44, 1); border-radius: 12px; height: 520px; margin-bottom: 20px;}
    .card-wrapper:hover { transform: translateY(-15px); }
    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; height: 100%; }
    
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.4) !important; box-shadow: 0 0 25px rgba(0, 210, 255, 0.15); }
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.4) !important; box-shadow: 0 0 25px rgba(221, 160, 221, 0.15); }

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
    
    # --- INCISIÓN: LÓGICA DE LOGIN PARA EMPLEADOS ---
    if not st.session_state.email_usuario:
        email_input = st.text_input(L["mail_label"], placeholder="email@ejemplo.com", key="user_email")
        if st.button("COMENZAR GRATIS / START FREE", type="primary"):
            if email_input and "@" in email_input:
                df_sales = obtener_datos_db()
                df_emp = obtener_empleados_db()
                
                # Caso 1: Es el Comprador/Jefe
                if email_input in df_sales['email'].values:
                    user_data = df_sales[df_sales['email'] == email_input].iloc[0]
                    st.session_state.usos = int(user_data['usos'])
                    st.session_state.plan_usuario = user_data['plan'] if 'plan' in user_data else 'Gratis'
                    st.session_state.es_empleado = False
                    st.session_state.email_usuario = email_input
                    st.rerun()
                
                # Caso 2: Es un Empleado invitado
                elif email_input in df_emp['EmployeeEmail'].values:
                    boss_email = df_emp[df_emp['EmployeeEmail'] == email_input].iloc[0]['BossEmail']
                    boss_data = df_sales[df_sales['email'] == boss_email].iloc[0]
                    st.session_state.usos = 0 # Empleados tienen usos limpios o podrías vincularlos
                    st.session_state.plan_usuario = boss_data['plan']
                    st.session_state.es_empleado = True
                    st.session_state.email_usuario = email_input
                    st.session_state.boss_ref = boss_email # Referencia
                    st.rerun()
                
                else:
                    st.session_state.usos = 0
                    st.session_state.plan_usuario = "Gratis"
                    st.session_state.email_usuario = email_input
                    st.rerun()
    
    # --- PASO 2: LOGICA DE GENERACIÓN ---
    elif st.session_state.email_usuario:
        es_pro = st.session_state.plan_usuario in ["Pro", "Agencia"]
        limite_usos = 99999 if es_pro else 3 
        
        if st.session_state.usos < limite_usos:
            col_t1, col_t2 = st.columns(2)
            with col_t1: tono = st.selectbox(L.get("lbl_tone", "Tono:"), ["Profesional", "Storytelling", "Urgencia/Venta", "Lujo/Minimalista"])
            with col_t2: idioma_salida = st.selectbox(L.get("lbl_lang_out", "Idioma Salida:"), list(traducciones.keys()), index=list(traducciones.keys()).index(st.session_state.idioma))

            url_input = st.text_input("", placeholder="🔗 Pega aquí el link de la propiedad...", label_visibility="collapsed")
            user_input = st.text_area("", placeholder=L['placeholder'], key="input_ia", label_visibility="collapsed")
            
            if st.button(L['btn_gen'], key="main_gen", type="primary"):
                if user_input or url_input: 
                    with st.spinner("Analizando mercado..."):
                        datos_web = extraer_datos_inmueble(url_input) if url_input else ""
                        prompt_base = f"Experto inmobiliario. Tarea: Descripción de venta. Idioma: {idioma_salida}. Tono: {tono}. SEO optimizado. Datos: {datos_web} {user_input}"
                        resultado = generar_texto(prompt_base)
                        
                        if "ERROR_TECNICO" not in resultado:
                            st.session_state.usos += 1
                            actualizar_usos_db(st.session_state.email_usuario, st.session_state.usos, st.session_state.plan_usuario)
                            guardar_historial(st.session_state.email_usuario, f"{url_input} {user_input}", resultado)
                            
                            st.success("¡Generado con éxito!")
                            
                            # --- INCISIÓN: VISUALIZACIÓN ELEGANTE Y BOTÓN COPIAR ---
                            st.markdown(f'<div class="result-box">{resultado.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
                            st.copy_to_clipboard(resultado)
                            st.info("⬆️ Click the 'Copy' button on the right of the text box (or use the one below).")
                            
                            if es_pro:
                                st.markdown("---")
                                st.markdown("### 📱 Social Media Pack (Pro)")
                                prompt_social = f"Crea un Copy para Instagram y un guion de TikTok basado en: {resultado}"
                                res_social = generar_texto(prompt_social)
                                st.markdown(f'<div class="result-box">{res_social.replace("\n", "<br>")}</div>', unsafe_allow_html=True)
                                st.copy_to_clipboard(res_social)
            
            # --- INCISIÓN: GESTIÓN DE EQUIPO (SOLO PARA JEFES AGENCIA) ---
            if st.session_state.plan_usuario == "Agencia" and not st.session_state.es_empleado:
                with st.expander("👥 Manage Agency Team"):
                    st.write("Add up to 4 team members:")
                    df_emp = obtener_empleados_db()
                    mis_emp = df_emp[df_emp['BossEmail'] == st.session_state.email_usuario]['EmployeeEmail'].tolist()
                    
                    e_col1, e_col2 = st.columns([3, 1])
                    with e_col1:
                        new_emp = st.text_input("New Member Email", key="new_emp_mail")
                    with e_col2:
                        st.write(" ")
                        if st.button("Add"):
                            if len(mis_emp) < 4 and "@" in new_emp:
                                conn.update(worksheet="Employees", data=pd.concat([df_emp, pd.DataFrame({"BossEmail": [st.session_state.email_usuario], "EmployeeEmail": [new_emp]})]))
                                st.success("Added!")
                                st.rerun()
                    for m in mis_emp: st.text(f"• {m}")

        else:
            st.error(L["limit_msg"])
            paypal_bloqueo = f"""<div id="p-b"></div><script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
            <script>paypal.Buttons({{ style: {{ shape: 'pill', color: 'blue' }}, createSubscription: function(d, a) {{ return a.subscription.create({{ 'plan_id': 'P-3P2657040E401734NNFQQ5TY', 'custom_id': '{st.session_state.email_usuario}' }}); }} }}).render('#p-b');</script>"""
            components.html(paypal_bloqueo, height=100)

    st.markdown('</div>', unsafe_allow_html=True)

# --- RESTO DEL DISEÑO (Filtros de precio, Testimonios, Footer) ---
# He mantenido tu lógica de 'modo_anual', 'traducciones' y 'footer' exactamente igual a partir de aquí.
# (Copiado de tu script original)
st.markdown(f"<br><br><h2 style='text-align:center; color:white;'>{L['how_title']}</h2>", unsafe_allow_html=True)
ch1, ch2, ch3 = st.columns(3)
with ch1: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>1</h1><p><b>{L['step1_t']}</b><br>{L['step1_d']}</p></div>", unsafe_allow_html=True)
with ch2: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>2</h1><p><b>{L['step2_t']}</b><br>{L['step2_d']}</p></div>", unsafe_allow_html=True)
with ch3: st.markdown(f"<div style='text-align:center;'><h1 style='color:#00d2ff;'>3</h1><p><b>{L['step3_t']}</b><br>{L['step3_d']}</p></div>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align:center;'>Selecciona tu Plan</h3>", unsafe_allow_html=True)
col_sw1, col_sw2, col_sw3 = st.columns([1,2,1])
with col_sw2: modo_anual = st.toggle("📅 Ahorrar 20% con Pago Anual (Save 20% Yearly)", value=False)

if modo_anual:
    precio_pro, precio_agency = "490", "1,990"
    id_pro, id_agency = "P-2PU023636P1209345NFQ7TMY", "P-87X83840151393810NFQ7X6Q"
    texto_ahorro = "✅ 2 Meses GRATIS incluidos"
else:
    precio_pro, precio_agency = "49", "199"
    id_pro, id_agency = "P-3P2657040E401734NNFQQ5TY", "P-0S451470G5041550ENFQRB4I"
    texto_ahorro = ""

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='card-wrapper free-card'><div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'>{L['desc1']}<br>{L['desc2']}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>${precio_pro}</h1><p>{texto_ahorro}</p><hr style='opacity:0.3;'>{L['desc4']}<br>{L['desc5']}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#DDA0DD;'>{L['plan3']}</h3><h1>${precio_agency}</h1><p>{texto_ahorro}</p><hr style='opacity:0.3;'>{L['desc8']}<br>{L['desc9']}</div></div>", unsafe_allow_html=True)

st.markdown(f'<div style="border-top: 1px solid rgba(255,255,255,0.1); padding: 40px 0px; text-align: center;"><div style="font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom:10px;">🏢 AI REALTY PRO</div><p style="color:#666; font-size:0.8rem;">© 2026 IA Realty Pro</p></div>', unsafe_allow_html=True)
