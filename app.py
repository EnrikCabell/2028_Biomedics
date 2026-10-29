import os
import sqlite3
from contextlib import closing
from datetime import date, datetime, time

import pandas as pd
import psycopg
import streamlit as st

st.set_page_config(page_title="BIOMEDICS | Gestión de clientes", page_icon="🦻", layout="wide")

st.sidebar.markdown(
    """<div style="width:100%;display:flex;flex-direction:column;align-items:center;padding:10px 0 24px;overflow:visible;">
    <img src="data:image/png;base64,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" style="width:180px !important;height:180px !important;max-width:100% !important;max-height:none !important;object-fit:contain !important;object-position:center;display:block;flex:none;margin:0 auto 12px;">
    <div style="font-size:25px;font-weight:800;letter-spacing:.4px;color:#C8102E !important;text-align:center;line-height:1.2;">BIOMEDICS</div>
    </div>""",
    unsafe_allow_html=True,
)

def obtener_url():
    url = os.getenv("DATABASE_URL")
    if not url:
        try:
            url = st.secrets.get("DATABASE_URL")
        except Exception:
            url = None
    return url

DATABASE_URL = obtener_url()
MODO_DEMO = not bool(DATABASE_URL)
DB_LOCAL = "biomedics_demo.db"

def conectar():
    if MODO_DEMO:
        con = sqlite3.connect(DB_LOCAL, check_same_thread=False)
        con.execute("PRAGMA foreign_keys = ON")
        return con
    return psycopg.connect(DATABASE_URL)

def inicializar():
    with closing(conectar()) as con:
        cur = con.cursor()
        if MODO_DEMO:
            cur.execute("""CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL, telefono TEXT, correo TEXT, direccion TEXT,
                notas TEXT, creado TEXT NOT NULL
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS estudios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
                fecha TEXT NOT NULL, tipo TEXT NOT NULL, resultado TEXT, observaciones TEXT
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
                fecha TEXT NOT NULL, hora TEXT NOT NULL, motivo TEXT,
                estado TEXT NOT NULL DEFAULT 'Pendiente', notas TEXT
            )""")
        else:
            cur.execute("""CREATE TABLE IF NOT EXISTS clientes (
                id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                nombre TEXT NOT NULL, telefono TEXT, correo TEXT, direccion TEXT,
                notas TEXT, creado TEXT NOT NULL
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS estudios (
                id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                cliente_id BIGINT NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
                fecha TEXT NOT NULL, tipo TEXT NOT NULL, resultado TEXT, observaciones TEXT
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS citas (
                id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                cliente_id BIGINT NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
                fecha TEXT NOT NULL, hora TEXT NOT NULL, motivo TEXT,
                estado TEXT NOT NULL DEFAULT 'Pendiente', notas TEXT
            )""")
        con.commit()

def consultar(sql, params=()):
    with closing(conectar()) as con:
        if MODO_DEMO:
            return pd.read_sql_query(sql, con, params=params)
        with con.cursor() as cur:
            cur.execute(sql.replace("?", "%s"), params)
            filas = cur.fetchall()
            columnas = [d.name for d in cur.description] if cur.description else []
            return pd.DataFrame(filas, columns=columnas)

def ejecutar(sql, params=()):
    with closing(conectar()) as con:
        cur = con.cursor()
        if MODO_DEMO:
            cur.execute(sql, params)
            nuevo_id = cur.lastrowid
        else:
            cur.execute(sql.replace("?", "%s"), params)
            nuevo_id = None
            if sql.lstrip().upper().startswith("INSERT"):
                cur.execute("SELECT LASTVAL()")
                nuevo_id = cur.fetchone()[0]
        con.commit()
        return nuevo_id

try:
    inicializar()
except Exception as exc:
    st.error("No fue posible iniciar la base de datos. Revisa la conexión y la configuración.")
    st.exception(exc)
    st.stop()

st.title("BIOMEDICS")
st.caption("Gestión de clientes, estudios y citas")
if MODO_DEMO:
    st.warning("SISTEMA DE PRUEBA: los registros se guardan temporalmente en el archivo local de la aplicación. Configura PostgreSQL para conservarlos de forma permanente.")

menu = st.sidebar.radio("Panel", ["Panel", "Clientes", "Estudios", "Citas", "Buscar"])
clientes = consultar("SELECT id, nombre, telefono, correo FROM clientes ORDER BY nombre")

if menu == "Panel":
    a, b, c = st.columns(3)
    a.metric("Clientes registrados", int(consultar("SELECT COUNT(*) n FROM clientes").iloc[0,0]))
    b.metric("Estudios registrados", int(consultar("SELECT COUNT(*) n FROM estudios").iloc[0,0]))
    c.metric("Citas registradas", int(consultar("SELECT COUNT(*) n FROM citas").iloc[0,0]))
    st.subheader("Citas registradas")
    citas = consultar("""SELECT c.id, cl.nombre AS Cliente, c.fecha AS Fecha, c.hora AS Hora,
        c.motivo AS Motivo, c.estado AS Estado
        FROM citas c JOIN clientes cl ON cl.id=c.cliente_id
        ORDER BY c.fecha, c.hora""")
    st.dataframe(citas, use_container_width=True, hide_index=True)
    st.subheader("Clientes recientes")
    st.dataframe(consultar("SELECT id, nombre, telefono, correo FROM clientes ORDER BY id DESC LIMIT 8"),
                 use_container_width=True, hide_index=True)

elif menu == "Clientes":
    st.subheader("Registrar cliente")
    with st.form("nuevo_cliente", clear_on_submit=True):
        nombre = st.text_input("Nombre completo *")
        col1, col2 = st.columns(2)
        telefono = col1.text_input("Teléfono")
        correo = col2.text_input("Correo electrónico")
        direccion = st.text_area("Dirección")
        notas = st.text_area("Notas")
        guardar = st.form_submit_button("Guardar cliente", type="primary")
        if guardar:
            if not nombre.strip():
                st.error("Escribe el nombre del cliente.")
            else:
                ejecutar("INSERT INTO clientes(nombre,telefono,correo,direccion,notas,creado) VALUES(?,?,?,?,?,?)",
                         (nombre.strip(), telefono.strip(), correo.strip(), direccion.strip(), notas.strip(), datetime.now().isoformat(timespec="seconds")))
                st.success("Cliente guardado.")
                st.rerun()
    st.subheader("Directorio de clientes")
    st.dataframe(consultar("SELECT id, nombre, telefono, correo, direccion, notas FROM clientes ORDER BY nombre"),
                 use_container_width=True, hide_index=True)
    if not clientes.empty:
        with st.expander("Editar o eliminar cliente"):
            elegido = st.selectbox("Cliente", clientes.itertuples(index=False), format_func=lambda x: f"{x.nombre} · ID {x.id}")
            datos = consultar("SELECT nombre,telefono,correo,direccion,notas FROM clientes WHERE id=?", (int(elegido.id),)).iloc[0]
            with st.form("editar_cliente"):
                n = st.text_input("Nombre", datos["nombre"])
                t = st.text_input("Teléfono", datos["telefono"] or "")
                e = st.text_input("Correo", datos["correo"] or "")
                d = st.text_area("Dirección", datos["direccion"] or "")
                no = st.text_area("Notas", datos["notas"] or "")
                x1, x2 = st.columns(2)
                actualizar = x1.form_submit_button("Guardar cambios")
                eliminar = x2.form_submit_button("Eliminar cliente")
                if actualizar:
                    ejecutar("UPDATE clientes SET nombre=?,telefono=?,correo=?,direccion=?,notas=? WHERE id=?",
                             (n.strip(),t.strip(),e.strip(),d.strip(),no.strip(),int(elegido.id)))
                    st.success("Cambios guardados.")
                    st.rerun()
                if eliminar:
                    ejecutar("DELETE FROM clientes WHERE id=?", (int(elegido.id),))
                    st.success("Cliente eliminado junto con sus registros.")
                    st.rerun()

elif menu == "Estudios":
    st.subheader("Registrar estudio")
    if clientes.empty:
        st.info("Primero registra un cliente.")
    else:
        with st.form("nuevo_estudio", clear_on_submit=True):
            cli = st.selectbox("Cliente", clientes.itertuples(index=False), format_func=lambda x: x.nombre)
            fecha = st.date_input("Fecha del estudio", value=date.today())
            tipo = st.selectbox("Tipo de estudio", ["Audiometría", "Logoaudiometría", "Impedanciometría", "Timpanometría", "Emisiones otoacústicas", "Potenciales evocados", "Otro"])
            resultado = st.text_area("Resultados")
            observaciones = st.text_area("Observaciones")
            guardar = st.form_submit_button("Guardar estudio", type="primary")
            if guardar:
                ejecutar("INSERT INTO estudios(cliente_id,fecha,tipo,resultado,observaciones) VALUES(?,?,?,?,?)",
                         (int(cli.id), fecha.isoformat(), tipo.strip(), resultado.strip(), observaciones.strip()))
                st.success("Estudio guardado.")
                st.rerun()
    st.subheader("Historial de estudios")
    estudios = consultar("""SELECT e.id, cl.nombre AS Cliente, e.fecha AS Fecha, e.tipo AS Estudio,
        e.resultado AS Resultados, e.observaciones AS Observaciones
        FROM estudios e JOIN clientes cl ON cl.id=e.cliente_id ORDER BY e.fecha DESC, e.id DESC""")
    st.dataframe(estudios, use_container_width=True, hide_index=True)

elif menu == "Citas":
    st.subheader("Agendar cita")
    if clientes.empty:
        st.info("Primero registra un cliente.")
    else:
        with st.form("nueva_cita", clear_on_submit=True):
            cli = st.selectbox("Cliente", clientes.itertuples(index=False), format_func=lambda x: x.nombre)
            col1, col2 = st.columns(2)
            fecha = col1.date_input("Fecha", value=date.today())
            hora = col2.time_input("Hora", value=time(10,0), step=900)
            motivo = st.text_input("Motivo de la cita")
            estado = st.selectbox("Estado", ["Pendiente", "Confirmada", "Atendida", "Cancelada"])
            notas = st.text_area("Notas")
            guardar = st.form_submit_button("Guardar cita", type="primary")
            if guardar:
                ejecutar("INSERT INTO citas(cliente_id,fecha,hora,motivo,estado,notas) VALUES(?,?,?,?,?,?)",
                         (int(cli.id), fecha.isoformat(), hora.strftime("%H:%M"), motivo.strip(), estado, notas.strip()))
                st.success("Cita guardada.")
                st.rerun()
    st.subheader("Agenda")
    agenda = consultar("""SELECT c.id, cl.nombre AS Cliente, cl.telefono AS Teléfono,
        c.fecha AS Fecha, c.hora AS Hora, c.motivo AS Motivo, c.estado AS Estado, c.notas AS Notas
        FROM citas c JOIN clientes cl ON cl.id=c.cliente_id ORDER BY c.fecha, c.hora""")
    st.dataframe(agenda, use_container_width=True, hide_index=True)
    if not agenda.empty:
        with st.expander("Modificar estado o eliminar cita"):
            cita = st.selectbox("Cita", agenda.itertuples(index=False),
                                format_func=lambda x: f"{x.Fecha} {x.Hora} · {x.Cliente} · {x.Motivo}")
            estado_nuevo = st.selectbox("Estado", ["Pendiente", "Confirmada", "Atendida", "Cancelada"],
                                        index=["Pendiente", "Confirmada", "Atendida", "Cancelada"].index(cita.Estado))
            z1,z2 = st.columns(2)
            if z1.button("Actualizar estado"):
                ejecutar("UPDATE citas SET estado=? WHERE id=?", (estado_nuevo, int(cita.id)))
                st.success("Estado actualizado.")
                st.rerun()
            if z2.button("Eliminar cita"):
                ejecutar("DELETE FROM citas WHERE id=?", (int(cita.id),))
                st.success("Cita eliminada.")
                st.rerun()

elif menu == "Buscar":
    st.subheader("Buscar información")
    termino = st.text_input("Nombre o teléfono del cliente")
    if termino.strip():
        patron = f"%{termino.strip()}%"
        encontrados = consultar("SELECT id,nombre,telefono,correo,direccion,notas FROM clientes WHERE nombre LIKE ? OR telefono LIKE ? ORDER BY nombre", (patron,patron))
        st.dataframe(encontrados, use_container_width=True, hide_index=True)
        if not encontrados.empty:
            ids = tuple(int(x) for x in encontrados["id"].tolist())
            marcas = ",".join("?" for _ in ids)
            st.markdown("**Estudios**")
            st.dataframe(consultar(f"""SELECT cl.nombre AS Cliente,e.fecha AS Fecha,e.tipo AS Estudio,e.resultado AS Resultados,e.observaciones AS Observaciones
                FROM estudios e JOIN clientes cl ON cl.id=e.cliente_id WHERE e.cliente_id IN ({marcas}) ORDER BY e.fecha DESC""", ids),
                use_container_width=True, hide_index=True)
            st.markdown("**Citas**")
            st.dataframe(consultar(f"""SELECT cl.nombre AS Cliente,c.fecha AS Fecha,c.hora AS Hora,c.motivo AS Motivo,c.estado AS Estado,c.notas AS Notas
                FROM citas c JOIN clientes cl ON cl.id=c.cliente_id WHERE c.cliente_id IN ({marcas}) ORDER BY c.fecha,c.hora""", ids),
                use_container_width=True, hide_index=True)
