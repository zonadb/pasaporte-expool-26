import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import io
import os

st.set_page_config(page_title="EXPOOL 2026 - Pasaporte MZB", layout="wide", page_icon="💧")

# --- CSS ESTILO NEGRO Y NARANJA ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .titulo-principal {
        color: #FF8C00; font-size: 42px !important; font-weight: 900 !important;
        line-height: 1.1; text-transform: uppercase; text-align: center;
    }
    th { background-color: #000000 !important; color: #FF8C00 !important; }
    .socio-card {
        background-color: #000000; padding: 20px; border-radius: 10px;
        color: #FF8C00; text-align: center; margin-bottom: 15px; border-bottom: 6px solid #FF8C00;
    }
    .asamblea-card {
        background-color: #000; padding: 15px; border-radius: 10px; 
        border-left: 5px solid #FF8C00; height: 100%; color: white;
    }
    [data-testid="stTable"] { width: 100% !important; font-size: 12px !important; }
    .stDownloadButton button {
        background-color: #FF8C00 !important;
        color: black !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS MAESTROS (ACTUALIZADOS CON IDEOS) ---
socios_nombres = ["AIGUANET GARDEN", "AISLAMAX", "ALELLA PISCINAS", "AQUAINDESA", "AQUASERVEIS", "AZ PISCINAS", "CIPAGUA", "OCIO JARDIN", "AIT", "CALDARIUM", "CONSAN", "COSTA PISCINAS", "GRIFONSUR", "GUADALOPE", "AGUA CLARA", "IPOOL CENTER", "JUBERT I VILA", "KAU PISCINAS", "MANEIG", "NEW CHEM", "NAVARRO ATH", "PISCIBLUE", "DE LA FLOR", "LOS BALCONES", "PILIO", "PISCINES CENTER", "PISCINES GELMI", "PISCINES PIERA", "PISCISALUD", "POOLMARK", "SHOP LINER POOL", "SILLERO E HIJOS", "PISCINAS JESUS", "TECNODRY"]

# Hemos quitado los descansos específicos y añadido IDEOS. El Simulador ahora incluye el Bar.
stands_nombres = ["KITPOOL", "BAEZA", "SINED", "G4PRO", "POOLSTAR", "BSLIGHT", "IBERCOVER", "INSOL", "HAYWARD", "GCL ELECTRIC", "DOSIM", "SPECK", "SCP", "IDEOS", "CUPOSOL", "VIDREPUR", "BEHQ", "POOLTIGER", "SPACE POOLS", "HAGENPLAST", "ETATRON", "TRYPOOL", "AQA CHEMICAL", "EZARRI", "BWT", "🎮 OCIO / ☕ BAR", "ZB", "VYP VALVULAS Y PROCESOS", "FLUIDRA", "HIDROTEN", "IASO", "PSH BOMBES", "BAYROL", "PRODUCTOS QP", "RENOLIT", "SAS", "BS POOL", "PS GROUP", "MAYTRONICS"]

def generar_datos_feria(dia):
    es_d1 = (dia == "Día 1 (3 Marzo)")
    franjas = []
    if es_d1:
        curr = datetime.strptime("09:00", "%H:%M")
        while curr + timedelta(minutes=20) <= datetime.strptime("14:00", "%H:%M"):
            franjas.append(curr.strftime("%H:%M")); curr += timedelta(minutes=20)
        franjas.append("14:00-16:00")
        curr = datetime.strptime("16:00", "%H:%M")
        while curr + timedelta(minutes=20) <= datetime.strptime("19:00", "%H:%M"):
            franjas.append(curr.strftime("%H:%M")); curr += timedelta(minutes=20)
        offset = 0
    else:
        curr = datetime.strptime("09:30", "%H:%M")
        while curr + timedelta(minutes=20) <= datetime.strptime("14:00", "%H:%M"):
            franjas.append(curr.strftime("%H:%M")); curr += timedelta(minutes=20)
        franjas.append("14:00-16:00")
        curr = datetime.strptime("16:00", "%H:%M")
        for _ in range(3):
            franjas.append(curr.strftime("%H:%M")); curr += timedelta(minutes=20)
        franjas.append("17:00-18:00")
        offset = 24
    
    filas = []
    t_count = 0
    for h in franjas:
        if h == "14:00-16:00":
            txt = "🎉 INAGURACIÓN Y PICOTEO 🎉" if es_d1 else "🍽️ COMIDA GRUPAL 🍽️"
            filas.append({"Hora": h, "TIPO": "EVENTO", **{s: txt for s in socios_nombres}})
        elif h == "17:00-18:00":
            txt = "🎰 SORTEO PROVEEDORES 🎰"
            filas.append({"Hora": h, "TIPO": "EVENTO", **{s: txt for s in socios_nombres}})
        else:
            f = {"Hora": h, "TIPO": "ROTACION"}
            for i, s in enumerate(socios_nombres):
                # Se asignan los stands de la lista stands_nombres
                f[s] = stands_nombres[(i + offset + t_count) % len(stands_nombres)]
            filas.append(f); t_count += 1
    return pd.DataFrame(filas)

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo_mzb.jpg"): st.image("logo_mzb.jpg", use_container_width=True)
    tipo_vista = st.radio("🔍 MENÚ PRINCIPAL:", ["AGENDA GENERAL", "Socio MZB", "Proveedor / Stand", "🏛️ ASAMBLEA"])
    
    if tipo_vista != "🏛️ ASAMBLEA":
        dia_seleccionado = st.selectbox("📅 JORNADA:", ["Día 1 (3 Marzo)", "Día 2 (4 Marzo)"])
        if tipo_vista == "Socio MZB": seleccion = st.selectbox("👤 SELECCIONAR SOCIO:", socios_nombres)
        elif tipo_vista == "Proveedor / Stand": seleccion = st.selectbox("🏢 SELECCIONAR STAND:", stands_nombres)
        else: seleccion = "CUADRANTE COMPLETO"

# --- CABECERA ---
col_izq, col_cen, col_der = st.columns([1, 4, 1])
with col_izq: 
    if os.path.exists("logo_expool.png"): st.image("logo_expool.png", use_container_width=True)
with col_cen:
    st.markdown('<p class="titulo-principal">EXPOOL 2026 · PASAPORTE MZB</p>', unsafe_allow_html=True)
    if os.path.exists("juntos.png"): st.image("juntos.png", use_container_width=True)
with col_der: 
    if os.path.exists("logo_expool.png"): st.image("logo_expool.png", use_container_width=True)

# --- LÓGICA DE VISTAS ---

if tipo_vista == "🏛️ ASAMBLEA":
    st.markdown('<div class="socio-card"><h1 style="margin:0; color: #FF8C00;">🏛️ ASAMBLEA GENERAL</h1><p style="margin:0; color: white;">GRUPO ZONA DE BAÑO S.COOP.</p></div>', unsafe_allow_html=True)
    st.markdown("""<div style="background-color: #000; color: #FF8C00; padding: 10px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #FF8C00; text-align: center;">
        <b>📍 UBICACIÓN:</b> EDIFICIO MULTIUSOS DE AMPOSTA (Frente al Recinto Ferial)</div>""", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="asamblea-card">
            <h3 style="color: #FF8C00;">📅 SESIÓN 1</h3><p><b>Lunes 2 de Marzo</b></p>
            <p style="margin-bottom:2px;"><small>15:30h (1ª convocatoria)</small></p>
            <p style="margin-top:0;"><small>16:00h (2ª convocatoria)</small></p><hr>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><b>1.</b> Bienvenida Presidente y Consejo.</li>
                <li><b>2.</b> ALTAS y BAJAS Grupo ZB 2026.</li>
                <li><b>3.</b> Actividades FERIA EXPOOL 2026.</li>
                <li><b>4.</b> COMPRAS a PROVEEDORES 2025.</li>
                <li><b>5.</b> PROVEEDORES 2026 y ZB AQUANATUR.</li>
            </ul></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="asamblea-card">
            <h3 style="color: #FF8C00;">📅 SESIÓN 2</h3><p><b>Jueves 5 de Marzo</b></p>
            <p style="margin-bottom:2px;"><small>09:30h (1ª convocatoria)</small></p>
            <p style="margin-top:0;"><small>10:00h (2ª convocatoria)</small></p><hr>
            <ul style="list-style-type: none; padding-left: 0;">
                <li><b>6.</b> FIGURA SOCIO Y RAPPEL 2025.</li>
                <li><b>7.</b> PROGRAMA ZB PLATINUM 2026.</li>
                <li><b>8.</b> MARKETING, WEB y RR.SS.</li>
                <li><b>9.</b> NUEVO CATÁLOGO ZB 2026-27.</li>
                <li><b>10.</b> Actualidad ASOFAP 2026.</li>
                <li><b>11.</b> Ruegos y Preguntas.</li>
            </ul></div>""", unsafe_allow_html=True)

else:
    df_base = generar_datos_feria(dia_seleccionado)
    
    if tipo_vista == "Socio MZB":
        df_descarga = df_base[["Hora", seleccion]].rename(columns={seleccion: "UBICACIÓN"})
        titulo_excel = f"Agenda_Socio_{seleccion}"
    elif tipo_vista == "Proveedor / Stand":
        visitas = []
        contador_zb = 0
        for idx_fila, fila in df_base.iterrows():
            if fila["TIPO"] == "EVENTO":
                visitas.append({"Hora": fila["Hora"], "ACTIVIDAD / VISITA": f"--- {fila[socios_nombres[0]]} ---"})
            else:
                visitante = next((s for s in socios_nombres if fila[s] == seleccion), None)
                if visitante:
                    visitas.append({"Hora": fila["Hora"], "ACTIVIDAD / VISITA": f"SOCIO: {visitante}"})
                else:
                    if contador_zb < 2:
                        visitas.append({"Hora": fila["Hora"], "ACTIVIDAD / VISITA": "VISITA STAND ZB"})
                        contador_zb += 1
                    else:
                        visitas.append({"Hora": fila["Hora"], "ACTIVIDAD / VISITA": "☕ BAR (Descanso)"})
        df_descarga = pd.DataFrame(visitas)
        titulo_excel = f"Agenda_Stand_{seleccion}"
    else:
        df_descarga = df_base.drop(columns=["TIPO"])
        titulo_excel = "Agenda_General_Completa"

    # --- BOTÓN EXCEL ---
    buffer = io.BytesIO()
    try:
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_descarga.to_excel(writer, index=False, sheet_name='Agenda', startrow=2)
            workbook, worksheet = writer.book, writer.sheets['Agenda']
            header_format = workbook.add_format({'bold': True, 'font_color': '#FF8C00', 'bg_color': '#000000', 'font_size': 12})
            worksheet.write(0, 0, f"EXPOOL 2026 - {dia_seleccionado}", header_format)
            worksheet.write(1, 0, f"Agenda para: {seleccion}", workbook.add_format({'bold': True}))
        st.download_button(label=f"📥 Descargar Excel: {seleccion}", data=buffer.getvalue(), file_name=f"{titulo_excel}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except:
        st.download_button(label="📥 Descargar CSV", data=df_descarga.to_csv(index=False).encode('utf-8-sig'), file_name="agenda.csv", mime='text/csv')

    st.markdown(f'<div class="socio-card"><h1 style="margin:0; color: #FF8C00;">{seleccion}</h1><p style="margin:0; color: white;">{dia_seleccionado}</p></div>', unsafe_allow_html=True)
    
    if tipo_vista == "AGENDA GENERAL":
        st.dataframe(df_descarga, use_container_width=True)
    else:
        mitad = len(df_descarga) // 2 + 1
        c1, c2 = st.columns(2)
        with c1: st.table(df_descarga.head(mitad))
        with c2: st.table(df_descarga.tail(len(df_descarga)-mitad))