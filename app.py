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
    page_title="IA Realty Pro",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
        "desc1": "3 descrições / día", "t1_1": "Limite diário de gerações para nuevos usuários.",
        "desc2": "Suporte Básico", "t1_2": "Ajuda técnica por e-mail com resposta em menos de 48 horas.",
        "desc3": "Marca d'Água", "t1_3": "Os textos incluem uma pequena menção à nossa plataforma.",
        "desc4": "Gerações Ilimitadas", "t2_1": "Crie quantas descrições precisar, sem restrições.",
        "desc5": "Pack Redes Sociais", "t2_2": "Gere automaticamente posts para Instagram, Facebook e TikTok com hashtags.",
        "desc6": "Optimización SEO", "t2_3": "Textos estruturados para aparecer primeiro nos motores de busca.",
        "desc7": "Banner Principal", "t2_4": "Seus imóveis de destaque rodarão em nossa página inicial.",
        "desc8": "5 Usuários / Contas", "t3_1": "Acesso individual para até 5 membros da sua equipe imobiliária.",
        "desc9": "Painel de Equipe", "t3_2": "Supervisione e gerencie as descrições criadas por seus agentes.",
        "desc10": "Acesso via API", "t3_3": "Conecte nossa IA diretamente com seu próprio software ou CRM.",
        "desc11": "Prioridade no Banner", "t3_4": "Seus anúncios aparecerão com o dobro de frequência na home.",
        "btn1": "REGISTRO GRÁTIS", "btn2": "MELHORAR AGORA", "btn3": "CONTATO VENDAS"
    }
}

# --- 4. ESTILOS CSS (Arreglado el error de letras GitHub) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #FFFFFF; font-family: 'Helvetica Neue', Arial, sans-serif; }
    .neon-title { font-size: 3.5rem; font-weight: 800; text-align: center; margin-top: 20px; color: white; text-shadow: 0 0 25px rgba(0, 210, 255, 0.5); }
    .neon-highlight { color: #00d2ff; text-shadow: 0 0 40px rgba(0, 210, 255, 0.8); }
    .subtitle { text-align: center; font-size: 1.2rem; color: #aaa; margin-bottom: 40px; }

    /* BOTÓN GENERAR */
    div.stButton > button[kind="primary"] { 
        background: linear-gradient(90deg, #00d2ff 0%, #0099ff 100%) !important; border: none !important; 
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.4) !important; transition: 0.4s !important; 
        color: white !important; font-weight: 700 !important; height: 3.5rem !important; width: 100% !important;
    }

    /* PLANES */
    .card-wrapper { transition: 0.4s; border-radius: 12px; height: 480px; margin-bottom: 20px; }
    .card-wrapper:hover { transform: translateY(-10px); }
    .glass-container { background: rgba(38, 39, 48, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 30px; text-align: center; position: relative; height: 100%; }
    
    .pro-card { border: 1px solid rgba(0, 210, 255, 0.4) !important; }
    .popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background-color: #00d2ff; color: black; padding: 6px 18px; border-radius: 20px; font-weight: 900; font-size: 0.85rem; }

    /* CONTENEDOR DE IMAGEN (Sin errores de texto) */
    .video-placeholder {
        border-radius: 12px; 
        height: 230px; 
        background: linear-gradient(45deg, #1e293b, #0f172a);
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 25px; border: 1px solid rgba(0, 210, 255, 0.3);
        box-shadow: 0 0 30px rgba(0, 210, 255, 0.2);
    }
    
    .feature-list { text-align: left; margin: 25px auto; font-size: 0.95rem; color: #ddd; line-height: 2.2; }
    .info-icon { display: inline-block; width: 16px; height: 16px; border-radius: 50%; text-align: center; font-size: 11px; margin-left: 8px; cursor: help; background: rgba(255,255,255,0.1); font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 5. INTERFAZ ---
if "idioma" not in st.session_state: st.session_state.idioma = "Español"

col_logo, _, col_lang = st.columns([2.5, 4, 1.5])
with col_logo: st.markdown('<div style="font-size: 1.6rem; font-weight: 800; color: #fff; margin-top:10px;">🏢 IA REALTY PRO</div>', unsafe_allow_html=True)
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
            <div style="text-align: center;">
                <h2 style="color:#00d2ff; margin:0;">{L["p_destacada"]}</h2>
                <p style="color:#aaa;">{L["comunidad"]}</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container" style="height:auto;">', unsafe_allow_html=True)
    user_input = st.text_area("", placeholder=L['placeholder'], key="input_ia", label_visibility="collapsed")
    
    if st.button(L['btn_gen'], key="main_gen", type="primary"):
        if user_input:
            with st.spinner("Generando..."):
                prompt = f"Actúa como un experto inmobiliario. Crea un anuncio persuasivo en {st.session_state.idioma} para: {user_input}"
                resultado = generar_texto(prompt)
                st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:10px; border:1px solid #00d2ff; margin-top:20px; color:white;'>{resultado}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. PLANES ---
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='card-wrapper'><div class='glass-container'><h3>{L['plan1']}</h3><h1>$0</h1><hr style='opacity:0.2;'><div class='feature-list'>{L['desc1']}<br>{L['desc2']}<br>{L['desc3']}</div></div></div>", unsafe_allow_html=True)
    st.button(L['btn1'], key="btn_f")

with col2:
    st.markdown(f"<div class='card-wrapper pro-card'><div class='glass-container'><div class='popular-badge'>{L['popular']}</div><h3 style='color:#00d2ff;'>{L['plan2']}</h3><h1>$49</h1><hr style='border-color:#00d2ff;opacity:0.3;'><div class='feature-list'><b>{L['desc4']}</b><br>{L['desc5']}<br>{L['desc6']}<br><b>{L['desc7']}</b></div></div></div>", unsafe_allow_html=True)
    st.button(L['btn2'], key="btn_p")

with col3:
    st.markdown(f"<div class='card-wrapper'><div class='glass-container'><h3>{L['plan3']}</h3><h1>$199</h1><hr style='opacity:0.2;'><div class='feature-list'>{L['desc8']}<br>{L['desc9']}<br>{L['desc10']}<br><b>{L['desc11']}</b></div></div></div>", unsafe_allow_html=True)
    st.button(L['btn3'], key="btn_a")
