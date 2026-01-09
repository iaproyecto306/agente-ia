import streamlit as st
from openai import OpenAI
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. CONFIGURACIÓN DE IA Y DB ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.warning("⚠️ Configuración pendiente: Añade la API Key en los Secrets.")
    st.stop()

conn = st.connection("gsheets", type=GSheetsConnection)

def obtener_datos_db():
    try:
        return conn.read(worksheet="Sheet1", ttl=0)
    except:
        return pd.DataFrame(columns=['email', 'usos', 'plan'])

def actualizar_usos_db(email, nuevos_usos, plan_actual):
    df = obtener_datos_db()
    email = str(email).strip().lower()
    if email in df['email'].str.strip().str.lower().values:
        idx = df[df['email'].str.strip().str.lower() == email].index
        df.loc[idx, 'usos'] = nuevos_usos
        df.loc[idx, 'plan'] = plan_actual
    else:
        nueva_fila = pd.DataFrame({"email": [email], "usos": [nuevos_usos], "plan": [plan_actual]})
        df = pd.concat([df, nueva_fila], ignore_index=True)
    conn.update(worksheet="Sheet1", data=df)

# --- 2. EL NUEVO "CEREBRO" (SYSTEM PROMPT JERÁRQUICO) ---
def generar_contenido_ia(user_input, plan_usuario, idioma):
    es_premium = plan_usuario in ["Pro", "Agencia"]
    
    if es_premium:
        instrucciones = f"""
        Eres un experto en Marketing Inmobiliario de Lujo. Genera una respuesta en {idioma} estructurada EXACTAMENTE así:

        [DESCRIPCION_WEB]
        Escribe un título gancho, una descripción emocional de alto impacto y una lista de características clave.

        [PACK_REDES]
        1. Instagram/Facebook: Un post con estructura AIDA (Atención, Interés, Deseo, Acción).
        2. TikTok/Reels: Un guion de 30 segundos con un Hook inicial potente.

        [ESTRATEGIA_SEO]
        Escribe 5 etiquetas (hashtags/keywords) y un mensaje corto de WhatsApp para calentar prospectos.
        """
    else:
        instrucciones = f"Genera únicamente una descripción de lujo en {idioma} para portales inmobiliarios basada en los datos proporcionados."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": instrucciones},
                {"role": "user", "content": f"Datos de la propiedad: {user_input}"}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR_TECNICO: {str(e)}"

# --- 3. CONFIGURACIÓN DE PÁGINA Y ESTILOS (PRESERVADOS) ---
st.set_page_config(page_title="AI Realty Pro", page_icon="🏢", layout="wide")

if "usos" not in st.session_state: st.session_state.usos = 0
if "email_usuario" not in st.session_state: st.session_state.email_usuario = ""
if "plan" not in st.session_state: st.session_state.plan = "Gratis"
if "idioma" not in st.session_state: st.session_state.idioma = "Español"

st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Arial, sans-serif; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }
    
    /* AURAS Y CARDS PRESERVADAS */
    .card-wrapper { transition: transform 0.6s cubic-bezier(0.165, 0.84, 0.44, 1); border-radius: 12px; margin-bottom: 20px; }
    .card-wrapper:hover { transform: translateY(-15px); }
    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; height: 100%; }
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.6) !important; box-shadow: 0 0 30px rgba(0, 210, 255, 0.3); }
    .agency-card { border: 1px solid rgba(221, 160, 221, 0.6) !important; box-shadow: 0 0 30px rgba(221, 160, 221, 0.3); }
    
    /* ANIMACIÓN CARRUSEL */
    .video-placeholder {
        border-radius: 12px; height: 230px; margin-bottom: 25px; position: relative; overflow: hidden; background-size: cover; background-position: center;
        animation: float 5s ease-in-out infinite, adCarousel 20s infinite alternate; border: 1px solid rgba(255,255,255,0.1);
    }
    @keyframes adCarousel { 
        0%, 33% { background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=800'); }
        34%, 66% { background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=800'); }
        67%, 100% { background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=800'); }
    }
    @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
</style>
""", unsafe_allow_html=True)

# --- 4. DICCIONARIO MULTI-IDIOMA COMPLETO ---
traducciones = {
    "Español": {
        "t1": "Convierte Anuncios en", "t2": "Imanes de Ventas", "sub": "La herramienta IA secreta de los agentes top.",
        "placeholder": "🏠 Pega el link o describe la propiedad...", "btn_gen": "✨ GENERAR ESTRATEGIA",
        "mail_label": "📧 Email para comenzar", "limit_msg": "🚫 Límite gratuito alcanzado.", "upgrade_msg": "Pásate a PRO.",
        "p1": "Inicial", "p2": "Agente Pro", "p3": "Agencia", "stat1": "Anuncios Listos", "stat2": "Tiempo Ahorrado", "stat3": "Más Consultas"
    },
    "English": {
        "t1": "Turn Listings into", "t2": "Sales Magnets", "sub": "The secret AI tool for top producing agents.",
        "placeholder": "🏠 Paste link or describe property...", "btn_gen": "✨ GENERATE STRATEGY",
        "mail_label": "📧 Email to start", "limit_msg": "🚫 Free limit reached.", "upgrade_msg": "Upgrade to PRO.",
        "p1": "Starter", "p2": "Pro Agent", "p3": "Agency", "stat1": "Optimized Ads", "stat2": "Time Saved", "stat3": "More Leads"
    },
    "Português": {
        "t1": "Converta Anúncios em", "t2": "Ímãs de Vendas", "sub": "A ferramenta de IA secreta dos principais agentes.",
        "placeholder": "🏠 Cole o link ou descreva...", "btn_gen": "✨ GERAR ESTRATÉGIA",
        "mail_label": "📧 E-mail para começar", "limit_msg": "🚫 Limite atingido.", "upgrade_msg": "Mude para PRO.",
        "p1": "Inicial", "p2": "Agente Pro", "p3": "Agência", "stat1": "Anúncios Prontos", "stat2": "Tempo Salvo", "stat3": "Mais Leads"
    },
    "Français": {
        "t1": "Transformez vos Annonces", "t2": "en Aimants", "sub": "L'outil IA secret des meilleurs agents.",
        "placeholder": "🏠 Collez le lien ou décrivez...", "btn_gen": "✨ GÉNÉRER STRATÉGIE",
        "mail_label": "📧 Email pour commencer", "limit_msg": "🚫 Limite atteinte.", "upgrade_msg": "Passez au PRO.",
        "p1": "Initial", "p2": "Agent Pro", "p3": "Agence", "stat1": "Annonces Prêtes", "stat2": "Temps Gagné", "stat3": "Plus de Leads"
    }
}

# --- 5. INTERFAZ ---
col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_lang:
    st.session_state.idioma = st.selectbox("", list(traducciones.keys()), label_visibility="collapsed")

L = traducciones[st.session_state.idioma]

st.markdown(f"<h1 class='neon-title'>{L['t1']} <br><span class='neon-highlight'>{L['t2']}</span></h1>", unsafe_allow_html=True)
st.markdown(f"<p class='subtitle'>{L['sub']}</p>", unsafe_allow_html=True)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown('<div class="video-placeholder"></div>', unsafe_allow_html=True)
    
    if not st.session_state.email_usuario:
        email_in = st.text_input(L["mail_label"])
        if st.button("ACCEDER / LOGIN", type="primary"):
            if email_in and "@" in email_in:
                df = obtener_datos_db()
                user_match = df[df['email'].str.strip().str.lower() == email_in.strip().lower()]
                if not user_match.empty:
                    st.session_state.usos = int(pd.to_numeric(user_match['usos'].values[0], errors='coerce'))
                    st.session_state.plan = str(user_match['plan'].values[0])
                else:
                    st.session_state.usos, st.session_state.plan = 0, "Gratis"
                st.session_state.email_usuario = email_in.strip().lower()
                st.rerun()
    else:
        # LÓGICA DE GENERACIÓN Y TABS
        if st.session_state.usos < 3 or st.session_state.plan in ["Pro", "Agencia"]:
            u_input = st.text_area("", placeholder=L["placeholder"], height=120, label_visibility="collapsed")
            if st.button(L["btn_gen"], type="primary"):
                with st.spinner("IA procesando estrategia..."):
                    raw_res = generar_contenido_ia(u_input, st.session_state.plan, st.session_state.idioma)
                    st.session_state.usos += 1
                    actualizar_usos_db(st.session_state.email_usuario, st.session_state.usos, st.session_state.plan)
                    
                    if st.session_state.plan in ["Pro", "Agencia"]:
                        # Separación por secciones para los Tabs
                        desc = raw_res.split("[PACK_RED_ES]")[0].replace("[DESCRIPCION_WEB]", "")
                        redes = raw_res.split("[PACK_REDES]")[-1].split("[ESTRATEGIA_SEO]")[0] if "[PACK_REDES]" in raw_res else ""
                        seo = raw_res.split("[ESTRATEGIA_SEO]")[-1] if "[ESTRATEGIA_SEO]" in raw_res else ""
                        
                        t1, t2, t3 = st.tabs(["🏠 Descripción Web", "📱 Pack Redes", "📊 Estrategia SEO"])
                        with t1: st.write(desc)
                        with t2: st.info(redes)
                        with t3: st.success(seo)
                    else:
                        st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #00d2ff;'>{raw_res}</div>", unsafe_allow_html=True)
                        st.warning("⚠️ Pásate a PRO para desbloquear Redes Sociales y SEO.")
        else:
            st.error(L["limit_msg"])
            st.info(L["upgrade_msg"])

# --- 6. ESTADÍSTICAS ---
st.markdown("<br>", unsafe_allow_html=True)
s1, s2, s3 = st.columns(3)
with s1: st.markdown(f'<div style="text-align:center;"><h3>+10k</h3><p>{L["stat1"]}</p></div>', unsafe_allow_html=True)
with s2: st.markdown(f'<div style="text-align:center;"><h3>-80%</h3><p>{L["stat2"]}</p></div>', unsafe_allow_html=True)
with s3: st.markdown(f'<div style="text-align:center;"><h3>+45%</h3><p>{L["stat3"]}</p></div>', unsafe_allow_html=True)

# --- 7. PLANES CON AURAS Y PAYPAL (PRESERVADOS) ---
st.markdown("<br><br>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(f"<div class='card-wrapper'><div class='glass-container'><h3>{L['p1']}</h3><h1>$0</h1><p>3 usos/día</p></div></div>", unsafe_allow_html=True)

with p2:
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><h3 style='color:#00d2ff;'>{L['p2']}</h3><h1>$49</h1><p>Ilimitado + Pack Redes</p></div></div>", unsafe_allow_html=True)
    components.html("""
    <div id="pp-pro"></div>
    <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
    <script>
        paypal.Buttons({
            style: {shape: 'pill', color: 'blue', layout: 'horizontal', label: 'subscribe'},
            createSubscription: function(data, actions) { return actions.subscription.create({'plan_id': 'P-3P2657040E401734NNFQQ5TY'}); }
        }).render('#pp-pro');
    </script>""", height=70)

with p3:
    st.markdown(f"<div class='card-wrapper agency-card'><div class='glass-container'><h3 style='color:#DDA0DD;'>{L['p3']}</h3><h1>$199</h1><p>5 Cuentas + Panel Equipo</p></div></div>", unsafe_allow_html=True)
    components.html("""
    <div id="pp-ag"></div>
    <script src="https://www.paypal.com/sdk/js?client-id=AYaVEtIjq5MpcAfeqGxyicDqPTUooERvDGAObJyJcB-UAQU4FWqyvmFNPigHn6Xwv30kN0el5dWPBxnj&vault=true&intent=subscription"></script>
    <script>
        paypal.Buttons({
            style: {shape: 'pill', color: 'blue', layout: 'horizontal', label: 'subscribe'},
            createSubscription: function(data, actions) { return actions.subscription.create({'plan_id': 'P-0S451470G5041550ENFQRB4I'}); }
        }).render('#pp-ag');
    </script>""", height=70)
