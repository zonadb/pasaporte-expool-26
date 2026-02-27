import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import os

# Configuración con Icono de Gota
st.set_page_config(page_title="EXPOOL 2026 - Pasaporte MZB", layout="wide", page_icon="💧")

# --- CSS ESTILO "ULTRA TOP" ---
st.markdown("""
    <style>
    .main { background-color: #000000; }
    body { background-color: #000000; color: white; }
    .titulo-principal {
        color: #FF8C00; font-size: 28px !important; font-weight: 900 !important;
        line-height: 1.1; text-transform: uppercase; text-align: center; margin-bottom: 10px;
        text-shadow: 2px 2px #333;
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
        border: none;
    }
    [data-testid="stTable"] { width: 100% !important; color: white !important; }
    th { background-color: #FF8C00 !important; color: black !important; }
    .alergia-box {
        background-color: #330000; color: #FF4B4B; padding: 15px; 
        border-radius: 10px; border: 1px solid #FF4B4B; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LISTADOS ---
mzb_listado = [
    "AIGUANET GARDEN AND POOL", "AISLANTES AISLAMAX", "AIT", "AZ PISCINAS", "CIPAGUA",
    "OCIO JARDIN CARRETERO S.L.", "AQUAINDESA", "CALDARIUM", "CONSAN PISCINAS", "COSTA PISCINAS",
    "GRIFONSUR", "GUADALOPE PISCINAS", "HERMONT", "HIDRAULICA AGUA CLARA", "IPOOL CENTER",
    "JUBERT & VILA", "KAU PISCINAS", "MANEIG PISCINES", "NAVARRO A.T.H", "ALELLA PISCINAS",
    "NEW CHEM", "NEO SWIMMING", "AQUASERVEIS REUS", "PISCIBLUE", "PISCINAS DE LA FLOR",
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

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo_mzb.jpg"): st.image("logo_mzb.jpg", use_container_width=True)
    vista = st.radio("🔍 MENÚ:", ["AGENDA GENERAL", "MZB", "Proveedor / Stand", "🏛️ ASAMBLEA", "🗺️ PLANO FERIA", "🎉 MENÚS Y OCIO", "🆘 AYUDA ZB"])
    if vista not in ["🏛️ ASAMBLEA", "🗺️ PLANO FERIA", "🎉 MENÚS Y OCIO", "🆘 AYUDA ZB"]:
        dia_sel = st.selectbox("📅 JORNADA:", ["Día 1 (3 Marzo)", "Día 2 (4 Marzo)"])
        sel = st.selectbox("👤 SELECCIONA NOMBRE:", mzb_listado if vista == "MZB" else prov_listado)

# --- CABECERA ---
c1, c2, c3 = st.columns([1, 4, 1])
with c1: st.image("portada.jpg", use_container_width=True)
with c2: 
    st.markdown('<p class="titulo-principal">EXPOOL 2026<br>PASAPORTE MZB</p>', unsafe_allow_html=True)
    st.image("juntos.png", use_container_width=True)
with c3: st.image("planing_mzb.jpg", use_container_width=True)

# --- LÓGICA DE TIEMPO REAL ---
ahora = datetime.now()
hora_str = ahora.strftime("%H:%M")

def obtener_estado_actual(df, nombre, es_mzb):
    for i in range(len(df)-1):
        h_actual = df.iloc[i]["Hora"]
        h_siguiente = df.iloc[i+1]["Hora"]
        if h_actual <= hora_str < h_siguiente:
            if df.iloc[i]["TIPO"] == "EVENTO": return f"📍 EVENTO: {df.iloc[i][mzb_listado[0]]}"
            if es_mzb: return f"📍 AHORA EN STAND: {df.iloc[i][nombre]}"
            else:
                visita = next((s for s in mzb_listado if df.iloc[i][s] == nombre), "☕ TIEMPO LIBRE")
                return f"📍 RECIBIENDO A: {visita}"
    return "😴 FUERA DE HORARIO DE FERIA"

# --- VISTAS ---
if vista == "🆘 AYUDA ZB":
    st.markdown('<div class="socio-card"><h2>🆘 AYUDA EXPOOL</h2></div>', unsafe_allow_html=True)
    st.link_button("💬 WHATSAPP ORGANIZACIÓN", "https://wa.me/34670379925?text=Hola%20Claudia,%20necesito%20ayuda...")

elif vista == "🗺️ PLANO FERIA":
    st.image("plano.jpg", use_container_width=True)

elif vista == "🎉 MENÚS Y OCIO":
    st.image("ocio.jpg", use_container_width=True)
    st.markdown('<div class="alergia-box">⚠️ Avisa de alergias a Claudia.</div>', unsafe_allow_html=True)
    st.link_button("📲 AVISAR ALERGIAS", "https://wa.me/34670379925?text=Tengo%20una%20alergia...")

elif vista == "🏛️ ASAMBLEA":
    st.markdown('<div class="socio-card"><h3>Lunes 2 - 16:00h | Jueves 5 - 10:00h</h3></div>', unsafe_allow_html=True)
    st.markdown("📍 Ubicación: Edificio Multiusos Amposta")

elif vista == "AGENDA GENERAL":
    meta = datetime(2026, 3, 4, 17, 0)
    faltan = meta - ahora
    if faltan.total_seconds() > 0:
        st.markdown(f'<div class="status-box">🎰 SORTEO EN: {str(faltan).split(".")[0]}</div>', unsafe_allow_html=True)
    df = generar_datos_feria(dia_sel)
    for _, fila in df.iterrows():
        with st.expander(f"⏰ {fila['Hora']}"):
            if fila["TIPO"] == "EVENTO": st.warning(fila[mzb_listado[0]])
            else:
                for mzb in mzb_listado: st.write(f"🔹 {mzb} ➔ {fila[mzb]}")

else: # MZB o Proveedor
    df = generar_datos_feria(dia_sel)
    estado = obtener_estado_actual(df, sel, vista == "MZB")
    st.markdown(f'<div class="status-box">{estado}</div>', unsafe_allow_html=True)
    
    if vista == "MZB":
        res = df[["Hora", sel]].rename(columns={sel: "VISITA A:"})
    else:
        v = []
        for _, r in df.iterrows():
            if r["TIPO"] == "EVENTO":
                v.append({"Hora": r["Hora"], "ESTADO": r[mzb_listado[0]]})
            else:
                visitante = next((s for s in mzb_listado if r[s] == sel), "☕ LIBRE")
                v.append({"Hora": r["Hora"], "ESTADO": visitante})
        res = pd.DataFrame(v)
    
    st.table(res)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        res.to_excel(wr, index=False)
    st.download_button("📥 DESCARGAR AGENDA EXCEL", buf.getvalue(), f"{sel}.xlsx")

