import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import os

st.set_page_config(page_title="EXPOOL 2026 - Pasaporte MZB", layout="wide", page_icon="💧")

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #000000; }
    body { background-color: #000000; color: white; }
    .titulo-principal {
        color: #FF8C00; font-size: 28px !important; font-weight: 900 !important;
        line-height: 1.1; text-transform: uppercase; text-align: center; margin-bottom: 10px;
    }
    .socio-card {
        background-color: #111; padding: 15px; border-radius: 10px;
        color: #FF8C00; text-align: center; margin-bottom: 10px; border: 1px solid #FF8C00;
    }
    .asamblea-card {
        background-color: #111; padding: 15px; border-radius: 10px; 
        border-left: 5px solid #FF8C00; color: white; margin-bottom: 10px;
    }
    [data-testid="stTable"] { width: 100% !important; font-size: 13px !important; color: white !important; }
    th { background-color: #FF8C00 !important; color: black !important; }
    .stDownloadButton button {
        background-color: #FF8C00 !important; color: black !important;
        font-weight: bold !important; width: 100% !important; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LISTADOS OFICIALES (38 MZB y 39 PROVEEDORES) ---
mzb_listado = [
    "AIGUANET GARDEN AND POOL", "AISLANTES AISLAMAX", "AIT", "AZ PISCINAS", "CIPAGUA",
    "OCIO JARDIN CARRETERO S.L.", "AQUAINDESA", "CALDARIUM", "CONSAN PISCINAS", "COSTA PISCINAS",
    "GRIFONSUR", "GUADALOPE PISCINAS", "HERMONT", "HIDRAULICA AGUA CLARA", "IPOOL CENTER",
    "JUBERT & VILA", "KAU PISCINAS", "MANEIG PISCINES", "NAVARRO A.T.H", "ALELLA PISCINAS",
    "NEW CHEM", "NEO SWIMMING", "AQUASERVEIS REUS", "PISCIBLUE", "PISCINAS DE LA FLOR",
    "PISCINAS JESUS", "PISCINAS JESUS (2)", "INSTALACIONES PISCINAS JESUS", "PISCINAS LOS BALCONES S.L.U.", "PISCINAS PILIO",
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
        # MAÑANA D1: 09:00 a 13:00
        curr = datetime.strptime("09:00", "%H:%M")
        while curr < datetime.strptime("13:00", "%H:%M"):
            f = {"Hora": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado):
                f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f)
            curr += timedelta(minutes=20); t_count += 1
        
        # EVENTO CENTRAL D1: 13:00 a 15:00
        filas.append({"Hora": "13:00-15:00", "TIPO": "EVENTO", **{s: "🏁 INAUGURACIÓN Y PICOTEO" for s in mzb_listado}})
        
        # TARDE D1: 15:00 a 19:00
        curr = datetime.strptime("15:00", "%H:%M")
        while curr < datetime.strptime("19:00", "%H:%M"):
            f = {"Hora": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado):
                f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f)
            curr += timedelta(minutes=20); t_count += 1
            
    else:
        # MAÑANA D2: 09:30 a 14:00
        curr = datetime.strptime("09:30", "%H:%M")
        t_count = 30 # Offset para no repetir inicio
        while curr < datetime.strptime("14:00", "%H:%M"):
            f = {"Hora": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado):
                f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f)
            curr += timedelta(minutes=20); t_count += 1
            
        filas.append({"Hora": "14:00-16:00", "TIPO": "EVENTO", **{s: "🍽️ COMIDA GRUPAL" for s in mzb_listado}})
        
        # TARDE D2: 16:00 a 17:00
        curr = datetime.strptime("16:00", "%H:%M")
        while curr < datetime.strptime("17:00", "%H:%M"):
            f = {"Hora": curr.strftime("%H:%M"), "TIPO": "ROTACION"}
            for i, s in enumerate(mzb_listado):
                f[s] = prov_listado[(i + t_count) % len(prov_listado)]
            filas.append(f)
            curr += timedelta(minutes=20); t_count += 1
            
        filas.append({"Hora": "17:00-18:00", "TIPO": "EVENTO", **{s: "🎰 SORTEO PROVEEDORES" for s in mzb_listado}})
        filas.append({"Hora": "18:00", "TIPO": "EVENTO", **{s: "🏁 CIERRE" for s in mzb_listado}})

    return pd.DataFrame(filas)

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo_mzb.jpg"): st.image("logo_mzb.jpg", use_container_width=True)
    vista = st.radio("🔍 MENÚ:", ["AGENDA GENERAL", "MZB", "Proveedor / Stand", "🏛️ ASAMBLEA"])
    if vista != "🏛️ ASAMBLEA":
        dia = st.selectbox("📅 JORNADA:", ["Día 1 (3 Marzo)", "Día 2 (4 Marzo)"])
        if vista == "MZB": sel = st.selectbox("👤 SOCIO:", mzb_listado)
        elif vista == "Proveedor / Stand": sel = st.selectbox("🏢 STAND:", prov_listado)
        else: sel = "CUADRANTE COMPLETO"

# --- CABECERA ---
c1, c2, c3 = st.columns([1, 4, 1])
with c1: st.image("logo_expool.png", use_container_width=True)
with c2: 
    st.markdown('<p class="titulo-principal">EXPOOL 2026<br>PASAPORTE MZB</p>', unsafe_allow_html=True)
    st.image("juntos.png", use_container_width=True)
with c3: st.image("logo_expool.png", use_container_width=True)

# --- VISTAS ---
if vista == "🏛️ ASAMBLEA":
    st.markdown('<div class="socio-card"><h2>🏛️ ASAMBLEA GENERAL</h2></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1: st.markdown('<div class="asamblea-card"><h3>SESIÓN 1</h3>Lunes 2 Marzo - 16:00h</div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="asamblea-card"><h3>SESIÓN 2</h3>Jueves 5 Marzo - 10:00h</div>', unsafe_allow_html=True)
else:
    df = generar_datos_feria(dia)
    if vista == "MZB":
        res = df[["Hora", sel]].rename(columns={sel: "VISITA A:"})
    elif vista == "Proveedor / Stand":
        v = []
        for _, r in df.iterrows():
            if r["TIPO"] == "EVENTO": v.append({"Hora": r["Hora"], "ESTADO": r[mzb_listado[0]]})
            else:
                vis = next((s for s in mzb_listado if r[s] == sel), "☕ LIBRE")
                v.append({"Hora": r["Hora"], "ESTADO": vis})
        res = pd.DataFrame(v)
    else: res = df.drop(columns=["TIPO"])

    # EXCEL
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as wr:
        res.to_excel(wr, index=False, startrow=3)
        fmt = wr.book.add_format({'bold': True, 'font_color': '#FF8C00'})
        wr.sheets['Sheet1'].write(0, 0, f"EXPOOL 2026 - {sel}", fmt)
    st.download_button("📥 DESCARGAR EXCEL", buf.getvalue(), f"{sel}.xlsx")
    
    st.markdown(f'<div class="socio-card"><h3>{sel}</h3></div>', unsafe_allow_html=True)
    m = len(res) // 2 + 1
    col1, col2 = st.columns(2)
    with col1: st.table(res.head(m))
    with col2: st.table(res.tail(len(res)-m))
