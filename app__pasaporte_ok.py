import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import os
import pytz

# 1. CONFIGURACIÓN TOP (Logo en la pestaña)
st.set_page_config(
    page_title="EXPOOL 2026 - Pasaporte MZB", 
    layout="wide", 
    page_icon="logo_mzb.jpg" if os.path.exists("logo_mzb.jpg") else "💧"
)

# --- CSS ESTILO ULTRA TOP ---
st.markdown("""
    <style>
    .main { background-color: #000000; }
    body { background-color: #000000; color: white; }
    .titulo-principal {
        color: #FF8C00; font-size: 28px !important; font-weight: 900 !important;
        line-height: 1.1; text-transform: uppercase; text-align: center; margin-bottom: 10px;
    }
    .status-box {
        background: linear-gradient(90deg, #FF8C00, #FF4500);
        color: black; padding: 15px; border-radius: 12px;
        text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 20px;
    }
    .socio-card {
        background-color: #111; padding: 12px; border-radius: 10px;
        color: #FF8C00; text-align: center; margin-bottom: 10px; border: 1px solid #FF8C00;
    }
    .asamblea-card {
        background-color: #111; padding: 15px; border-radius: 10px; 
        border-left: 4px solid #FF8C00; color: white; margin-bottom: 10px;
    }
    .stDownloadButton button, .stLinkButton a {
        background-color: #FF8C00 !important; color: black !important;
        font-weight: bold !important; width: 100% !important; border-radius: 10px;
        text-decoration: none; display: inline-block; text-align: center; padding: 12px 0;
    }
    [data-testid="stTable"] { width: 100% !important; color: white !important; }
    th { background-color: #FF8C00 !important; color: black !important; }
    .alergia-box {
        background-color: #330000; color: #FF4B4B; padding: 15px; 
        border-radius: 10px; border: 1px solid #FF4B4B; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENSAJE DE BIENVENIDA DEFINITIVO (SIN LA PALABRA INSTALAR) ---
@st.dialog("💧 BIENVENIDO A EXPOOL 2026")
def bienvenida():
    st.markdown("""
    <div style="text-align: center;">
        <p style="font-size: 18px;"><b>¡Tu Pasaporte MZB ya está listo!</b></p>
        <p>Para llevar la agenda siempre a mano en tu móvil:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    1. Pulsa los **3 puntos** (Android) o el botón **Compartir** (iPhone).
    2. Selecciona la opción **'Añadir a pantalla de inicio'**.
    3. ¡Listo! Tendrás el icono de la App junto a tus otras aplicaciones.
    """)
    
    if st.button("CONFIGURAR MÁS TARDE", use_container_width=True):
        st.session_state.visto = True
        st.rerun()
if 'visto' not in st.session_state:
    bienvenida()

# --- LISTADOS ---
mzb_listado = [
    "AIGUANET GARDEN AND POOL", "AISLANTES AISLAMAX", "AIT", "AZ PISCINAS", "CIPAGUA",
    "OCIO JARDIN CARRETERO S.L.", "AQUAINDESA", "CALDARIUM", "CONSAN PISCINAS", "COSTA PISCINAS",
    "GRIFONSUR", "GUADALOPE PISCINAS", "HERMONT", "HIDRAULICA AGUA CLARA", "IPOOL CENTER",
    "JUBERT & VILA", "KAU PISCINAS", "MANEIG PISCINES", "NAVARRO A.T.H", "ALELLA PISCINAS",
    "NEW CHEM", "AQUASERVEIS", "AQUASERVEIS REUS", "PISCIBLUE", "PISCINAS DE LA FLOR",
    "PISCINAS JESUS", "INSTALACIONES PISCINAS JESUS", "PISCINAS LOS BALCONES S.L.U.", "PISCINAS PILIO",
    "PISCINES CENTER", "PISCINES GELMI", "PISCINES PIERA", "PISCISALUD", "POOLMARK",
    "SHOP LINER POOL", "SILLERO E HIJOS SL", "TECNODRY"
]

prov_listado = [
    "KITPOOL", "BAEZA S.A.", "SINED", "G4PRO", "POOLSTAR", "BSLIGHT SL", "IBERCOVERPOOL",
    "INSOL - PWG", "HAYWARD", "GCL ELECT.", "DOSIM", "SPECK", "SCP POOL", "CUPOSOL S.L.",
    "VIDREPUR", "BEHQ", "POOLTIGER", "SPACE POOLS", "HAOGENPLAST", "ETATRON",
    "A.Q.A. CHEM.", "TRYPOOL", "IDEOS", "EZARRI", "BWT - ATH", "🎮 SIMULADOR (☕ OCIO/CAFÉ)",
    "ZB", "VYP", "FLUIDRA", "HIDROTEN S.A.", "IASO S.L.", "BOMBES PSH", "BAYROL",
    "PRODUCTOS QP", "RENOLIT", "SAS", "BSPOOL", "PS GROUP", "MAYTRONICS"
]

def generar_datos_feria(dia):
    es_d1 = (dia == "Día 1 (3 Marzo)")
    filas = []
    t_count = 0
    if es_d1:
        curr = datetime.strptime("09:00", "%H:%M")
        while curr < datetime.strptime("13:00", "%H:%M"):
            f = {"Hora": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado): f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f); curr += timedelta(minutes=20); t_count += 1
        filas.append({"Hora": "13:00", "TIPO": "EVENTO", **{s: "🏁 INAUGURACIÓN" for s in mzb_listado}})
        curr = datetime.strptime("15:00", "%H:%M")
        while curr < datetime.strptime("19:00", "%H:%M"):
            f = {"Hora": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado): f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f); curr += timedelta(minutes=20); t_count += 1
    else:
        curr = datetime.strptime("09:30", "%H:%M")
        t_count = 15
        while curr < datetime.strptime("14:00", "%H:%M"):
            f = {"Hora": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado): f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f); curr += timedelta(minutes=20); t_count += 1
        filas.append({"Hora": "14:00", "TIPO": "EVENTO", **{s: "🍽️ COMIDA GRUPAL" for s in mzb_listado}})
        curr = datetime.strptime("16:00", "%H:%M")
        while curr < datetime.strptime("17:00", "%H:%M"):
            f = {"Hora": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado): f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f); curr += timedelta(minutes=20); t_count += 1
        filas.append({"Hora": "17:00", "TIPO": "EVENTO", **{s: "🎰 SORTEO PROVEEDORES" for s in mzb_listado}})
    return pd.DataFrame(filas)

# --- LÓGICA DE TIEMPO REAL (ZONA MADRID) ---
tz = pytz.timezone('Europe/Madrid')
ahora = datetime.now(tz)
hora_str = ahora.strftime("%H:%M")
hoy_str = ahora.strftime("%d/%m")

def obtener_estado_actual(nombre, es_mzb):
    if hoy_str == "03/03": df_hoy = generar_datos_feria("Día 1 (3 Marzo)")
    elif hoy_str == "04/03": df_hoy = generar_datos_feria("Día 2 (4 Marzo)")
    else: return "⏳ PRÓXIMAMENTE: EXPOOL 2026 (3-4 MARZO)"
    for i in range(len(df_hoy)-1):
        h_actual = df_hoy.iloc[i]["Hora"]
        h_siguiente = df_hoy.iloc[i+1]["Hora"]
        if h_actual <= hora_str < h_siguiente:
            if df_hoy.iloc[i]["TIPO"] == "EVENTO": return f"📍 EVENTO: {df_hoy.iloc[i][mzb_listado[0]]}"
            if es_mzb: return f"📍 AHORA EN STAND: {df_hoy.iloc[i][nombre]}"
            else:
                visita = next((s for s in mzb_listado if df_hoy.iloc[i][s] == nombre), "☕ TIEMPO LIBRE")
                return f"📍 RECIBIENDO A: {visita}"
    return "😴 FERIA CERRADA POR HOY"

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo_mzb.jpg"): st.image("logo_mzb.jpg", use_container_width=True)
    vista = st.radio("🔍 MENÚ:", ["AGENDA GENERAL", "MZB", "Proveedor / Stand", "🏛️ ASAMBLEA", "🗺️ PLANO FERIA", "🎉 MENÚS Y OCIO", "🆘 AYUDA ZB"])
    if vista not in ["🏛️ ASAMBLEA", "🗺️ PLANO FERIA", "🎉 MENÚS Y OCIO", "🆘 AYUDA ZB"]:
        dia_sel = st.selectbox("📅 JORNADA:", ["Día 1 (3 Marzo)", "Día 2 (4 Marzo)"])
        sel = st.selectbox("👤 SELECCIONA NOMBRE:", mzb_listado if vista == "MZB" else prov_listado)

# --- CABECERA ---
c1, c2, c3 = st.columns([1, 4, 1])
with c1: 
    if os.path.exists("portada.jpg"): st.image("portada.jpg", use_container_width=True)
with c2: 
    st.markdown('<p class="titulo-principal">EXPOOL 2026<br>PASAPORTE MZB</p>', unsafe_allow_html=True)
    if os.path.exists("juntos.png"): st.image("juntos.png", use_container_width=True)
with c3: 
    if os.path.exists("planing_mzb.jpg"): st.image("planing_mzb.jpg", use_container_width=True)

# --- VISTAS ---
if vista == "🆘 AYUDA ZB":
    st.markdown('<div class="socio-card"><h2>🆘 AYUDA EXPOOL</h2></div>', unsafe_allow_html=True)
    st.link_button("💬 WHATSAPP ORGANIZACIÓN", "https://wa.me/34670379925?text=Hola%20Claudia,%20necesito%20ayuda...")

elif vista == "🗺️ PLANO FERIA":
    if os.path.exists("plano.jpg"): st.image("plano.jpg", use_container_width=True)

elif vista == "🎉 MENÚS Y OCIO":
    if os.path.exists("ocio.jpg"): st.image("ocio.jpg", use_container_width=True)
    st.markdown('<div class="alergia-box">⚠️ Avisa de alergias a Claudia.</div>', unsafe_allow_html=True)
    st.link_button("📲 AVISAR ALERGIAS", "https://wa.me/34670379925?text=Tengo%20una%20alergia...")

elif vista == "🏛️ ASAMBLEA":
    st.markdown('<div class="socio-card"><h1 style="margin:0; font-size: 32px;">🏛️ ASAMBLEA GENERAL</h1><p style="margin:0; color: white; font-size: 18px;">ACCESO RESTRINGIDO A SOCIOS</p></div>', unsafe_allow_html=True)
    
    # Sistema de protección
    password = st.text_input("Introduce la clave de Socio para ver el orden del día:", type="password")
    
    if password == "ZB2026":
        st.success("✅ Acceso concedido")
        st.markdown('<div style="background-color: #111; padding: 15px; border-radius: 10px; border: 1px solid #FF8C00; color: #FF8C00; font-size: 20px; text-align: center; font-weight: bold;">📍 UBICACIÓN: Edificio Multiusos de Amposta</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div class="asamblea-card" style="padding: 20px;">
                <h2 style="color: #FF8C00; font-size: 28px; margin-bottom: 5px;">📅 SESIÓN 1</h2>
                <p style="font-size: 20px; margin-bottom: 2px;"><b>Lunes 2 de Marzo</b></p>
                <p style="color: #bbb; font-size: 16px;">15:30h (1ª conv.) | 16:00h (2ª conv.)</p>
                <hr style="border-color: #444;">
                <ul style="list-style-type: none; padding-left: 0; font-size: 18px; line-height: 1.8;">
                    <li><b style="color: #FF8C00;">1.</b> Bienvenida Presidente y Consejo.</li>
                    <li><b style="color: #FF8C00;">2.</b> ALTAS y BAJAS Grupo ZB 2026.</li>
                    <li><b style="color: #FF8C00;">3.</b> Actividades FERIA EXPOOL 2026.</li>
                    <li><b style="color: #FF8C00;">4.</b> COMPRAS a PROVEEDORES 2025.</li>
                    <li><b style="color: #FF8C00;">5.</b> PROVEEDORES 2026 y ZB AQUANATUR.</li>
                </ul></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class="asamblea-card" style="padding: 20px;">
                <h2 style="color: #FF8C00; font-size: 28px; margin-bottom: 5px;">📅 SESIÓN 2</h2>
                <p style="font-size: 20px; margin-bottom: 2px;"><b>Jueves 5 de Marzo</b></p>
                <p style="color: #bbb; font-size: 16px;">09:30h (1ª conv.) | 10:00h (2ª conv.)</p>
                <hr style="border-color: #444;">
                <ul style="list-style-type: none; padding-left: 0; font-size: 18px; line-height: 1.8;">
                    <li><b style="color: #FF8C00;">6.</b> FIGURA SOCIO Y RAPPEL 2025.</li>
                    <li><b style="color: #FF8C00;">7.</b> PROGRAMA ZB PLATINUM 2026.</li>
                    <li><b style="color: #FF8C00;">8.</b> MARKETING, WEB y RR.SS.</li>
                    <li><b style="color: #FF8C00;">9.</b> NUEVO CATÁLOGO ZB 2026-27.</li>
                    <li><b style="color: #FF8C00;">10.</b> Ruegos y Preguntas.</li>
                </ul></div>""", unsafe_allow_html=True)
    elif password == "":
        st.warning("Por favor, introduce la clave para continuar.")
    else:
        st.error("❌ Clave incorrecta.")

elif vista == "AGENDA GENERAL":
    df = generar_datos_feria(dia_sel)
    for _, fila in df.iterrows():
        with st.expander(f"⏰ {fila['Hora']}"):
            if fila["TIPO"] == "EVENTO": st.warning(fila[mzb_listado[0]])
            else:
                for mzb in mzb_listado: st.write(f"🔹 {mzb} ➔ {fila[mzb]}")

else: # MZB o Proveedor
    estado = obtener_estado_actual(sel, vista == "MZB")
    st.markdown(f'<div class="status-box">{estado}</div>', unsafe_allow_html=True)
    df = generar_datos_feria(dia_sel)
    if vista == "MZB": res = df[["Hora", sel]].rename(columns={sel: "VISITA A:"})
    else:
        v = []
        for _, r in df.iterrows():
            if r["TIPO"] == "EVENTO": v.append({"Hora": r["Hora"], "ESTADO": r[mzb_listado[0]]})
            else: v.append({"Hora": r["Hora"], "ESTADO": next((s for s in mzb_listado if r[s] == sel), "☕ LIBRE")})
        res = pd.DataFrame(v)
    st.table(res)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr: res.to_excel(wr, index=False)
    st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), f"{sel}.xlsx")




