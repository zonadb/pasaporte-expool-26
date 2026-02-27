import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import os
import pytz

# 1. CONFIGURACIÓN TOP
st.set_page_config(
    page_title="EXPOOL 2026 - Pasaporte MZB", 
    layout="wide", 
    page_icon="logo_mzb.jpg" if os.path.exists("logo_mzb.jpg") else "💧"
)

# --- CSS ESTILO ULTRA TOP (NEGRO Y NARANJA) ---
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
        color: #FF8C00; text-align: center; margin-bottom: 10px; border: 2px solid #FF8C00;
    }
    .asamblea-card {
        background-color: #111; padding: 15px; border-radius: 10px; 
        border-left: 4px solid #FF8C00; color: white; margin-bottom: 10px;
    }
    .stDownloadButton button, .stLinkButton a {
        background-color: #FF8C00 !important; color: black !important;
        font-weight: bold !important; width: 100% !important; border-radius: 10px;
        text-decoration: none; display: inline-block; text-align: center; padding: 12px 0;
        border: none;
    }
    [data-testid="stTable"] { width: 100% !important; color: white !important; background-color: #111; }
    th { background-color: #FF8C00 !important; color: black !important; }
    .alergia-box {
        background-color: #330000; color: #FF4B4B; padding: 15px; 
        border-radius: 10px; border: 1px solid #FF4B4B; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENSAJE DE BIENVENIDA ---
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

# --- LISTADOS OFICIALES ---
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

# --- GENERADOR DE DATOS ---
def generar_datos_feria(dia):
    es_d1 = (dia == "Día 1 (3 Marzo)")
    filas = []
    t_count = 0
    if es_d1:
        curr = datetime.strptime("09:00", "%H:%M")
        while curr < datetime.strptime("13:00", "%H:%M"):
            f = {"HORA": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado): f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f); curr += timedelta(minutes=20); t_count += 1
        filas.append({"HORA": "13:00", "TIPO": "EVENTO", **{s: "🏁 INAUGURACIÓN" for s in mzb_listado}})
        curr = datetime.strptime("15:00", "%H:%M")
        while curr < datetime.strptime("19:00", "%H:%M"):
            f = {"HORA": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado): f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f); curr += timedelta(minutes=20); t_count += 1
    else:
        curr = datetime.strptime("09:30", "%H:%M")
        t_count = 15
        while curr < datetime.strptime("14:00", "%H:%M"):
            f = {"HORA": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado): f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f); curr += timedelta(minutes=20); t_count += 1
        filas.append({"HORA": "14:00", "TIPO": "EVENTO", **{s: "🍽️ COMIDA GRUPAL" for s in mzb_listado}})
        curr = datetime.strptime("16:00", "%H:%M")
        while curr < datetime.strptime("17:00", "%H:%M"):
            f = {"HORA": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado): f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f); curr += timedelta(minutes=20); t_count += 1
        filas.append({"HORA": "17:00", "TIPO": "EVENTO", **{s: "🎰 SORTEO PROVEEDORES" for s in mzb_listado}})
    return pd.DataFrame(filas)

# --- TIEMPO REAL ---
tz = pytz.timezone('Europe/Madrid')
ahora = datetime.now(tz)
hora_str = ahora.strftime("%H:%M")
hoy_str = ahora.strftime("%d/%m")

def obtener_estado_actual(nombre, es_mzb):
    if hoy_str == "03/03": df_hoy = generar_datos_feria("Día 1 (3 Marzo)")
    elif hoy_str == "04/03": df_hoy = generar_datos_feria("Día 2 (4 Marzo)")
    else: return "⏳ PRÓXIMAMENTE: EXPOOL 2026 (3-4 MARZO)"
    
    for i in range(len(df_hoy)-1):
        if df_hoy.iloc[i]["HORA"] <= hora_str < df_hoy.iloc[i+1]["HORA"]:
            if df_hoy.iloc[i]["TIPO"] == "EVENTO": return f"📍 EVENTO: {df_hoy.iloc[i][mzb_listado[0]]}"
            if es_mzb: return f"📍 AHORA EN STAND: {df_hoy.iloc[i][nombre]}"
            else:
                visita = next((s for s in mzb_listado if df_hoy.iloc[i][s] == nombre), "☕ LIBRE")
                return f"📍 RECIBIENDO A: {visita}"
    return "😴 FERIA CERRADA POR HOY"

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo_mzb.jpg"): st.image("logo_mzb.jpg", use_container_width=True)
    vista = st.radio("🔍 MENÚ:", ["AGENDA GENERAL", "MZB", "Proveedor / Stand", "🏛️ ASAMBLEA", "🗺️ PLANO FERIA", "🎉 MENÚS Y OCIO", "🆘 AYUDA ZB"])
    
    if vista in ["AGENDA GENERAL", "MZB", "Proveedor / Stand"]:
        dia_sel = st.selectbox("📅 JORNADA:", ["Día 1 (3 Marzo)", "Día 2 (4 Marzo)"])
        if vista != "AGENDA GENERAL":
            sel = st.selectbox("👤 SELECCIONA NOMBRE:", mzb_listado if vista == "MZB" else prov_listado)

    # --- ZONA ADMIN ---
    with st.expander("🔐 ACCESO ORGANIZACIÓN"):
        pwd_admin = st.text_input("Clave Admin:", type="password")
        if pwd_admin == "cipoteboys":
            st.success("✅ Acceso Concedido")
            def excel_proveedores():
                output = io.BytesIO()
                d1, d2 = generar_datos_feria("Día 1 (3 Marzo)"), generar_datos_feria("Día 2 (4 Marzo)")
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    for p in prov_listado:
                        ag = []
                        for h in d1["HORA"].unique():
                            s1 = next((s for s in mzb_listado if d1.loc[d1["HORA"]==h, s].iloc[0] == p), "-")
                            s2 = next((s for s in mzb_listado if d2.loc[d2["HORA"]==h, s].iloc[0] == p), "-")
                            ag.append({'HORA': h, 'DÍA 1': s1, 'HORA ': h, 'DÍA 2': s2})
                        pd.DataFrame(ag).to_excel(writer, sheet_name=str(p)[:30].strip().replace('/','-'), index=False)
                return output.getvalue()
            st.download_button("📥 EXCEL PROVEEDORES", excel_proveedores(), "PLANING_PROV.xlsx", use_container_width=True)

# --- VISTAS ---
if vista == "AGENDA GENERAL":
    st.markdown('<div class="socio-card"><h2>📅 CUADRANTE GENERAL</h2></div>', unsafe_allow_html=True)
    df = generar_datos_feria(dia_sel)
    for _, r in df.iterrows():
        with st.expander(f"⏰ {r['HORA']}"):
            if r["TIPO"] == "EVENTO": st.warning(r[mzb_listado[0]])
            else:
                for m in mzb_listado: st.write(f"🔹 {m} ➔ {r[m]}")

elif vista == "MZB":
    estado = obtener_estado_actual(sel, True)
    st.markdown(f'<div class="status-box">{estado}</div>', unsafe_allow_html=True)
    df = generar_datos_feria(dia_sel)
    st.table(df[["HORA", sel]].rename(columns={sel: "VISITA A:"}))

elif vista == "Proveedor / Stand":
    estado = obtener_estado_actual(sel, False)
    st.markdown(f'<div class="status-box">{estado}</div>', unsafe_allow_html=True)
    df = generar_datos_feria(dia_sel)
    v = []
    for _, r in df.iterrows():
        vis = r[mzb_listado[0]] if r["TIPO"]=="EVENTO" else next((s for s in mzb_listado if r[s]==sel), "☕ LIBRE")
        v.append({"HORA": r["HORA"], "VISITA DE:": vis})
    st.table(pd.DataFrame(v))

elif vista == "🏛️ ASAMBLEA":
    st.markdown('<div class="socio-card"><h1>🏛️ ASAMBLEA GENERAL</h1></div>', unsafe_allow_html=True)
    password = st.text_input("Introduce la clave de Socio:", type="password")
    if password == "ZB2026":
        st.success("✅ Acceso concedido")
        st.markdown('<div class="asamblea-card">📍 UBICACIÓN: Edificio Multiusos de Amposta</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div class="asamblea-card">
                <h3 style="color: #FF8C00;">📅 SESIÓN 1</h3>
                <p><b>Lunes 2 de Marzo</b></p>
                <ul style="font-size: 14px;">
                    <li>1. Bienvenida Presidente y Consejo.</li>
                    <li>2. ALTAS y BAJAS Grupo ZB 2026.</li>
                    <li>3. Actividades FERIA EXPOOL 2026.</li>
                    <li>4. COMPRAS a PROVEEDORES 2025.</li>
                    <li>5. PROVEEDORES 2026 y ZB AQUANATUR.</li>
                </ul></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class="asamblea-card">
                <h3 style="color: #FF8C00;">📅 SESIÓN 2</h3>
                <p><b>Jueves 5 de Marzo</b></p>
                <ul style="font-size: 14px;">
                    <li>6. FIGURA SOCIO Y RAPPEL 2025.</li>
                    <li>7. PROGRAMA ZB PLATINUM 2026.</li>
                    <li>8. MARKETING, WEB y RR.SS.</li>
                    <li>9. NUEVO CATÁLOGO ZB 2026-27.</li>
                    <li>10. Ruegos y Preguntas.</li>
                </ul></div>""", unsafe_allow_html=True)
    elif password != "": st.error("❌ Clave incorrecta.")

elif vista == "🗺️ PLANO FERIA":
    if os.path.exists("plano.jpg"): st.image("plano.jpg", use_container_width=True)
elif vista == "🎉 MENÚS Y OCIO":
    if os.path.exists("ocio.jpg"): st.image("ocio.jpg", use_container_width=True)
    st.markdown('<div class="alergia-box">⚠️ Avisa de alergias a Claudia.</div>', unsafe_allow_html=True)
elif vista == "🆘 AYUDA ZB":
    st.markdown('<div class="socio-card"><h2>🆘 AYUDA EXPOOL</h2></div>', unsafe_allow_html=True)
    st.link_button("💬 WHATSAPP ORGANIZACIÓN", "https://wa.me/34670379925")
