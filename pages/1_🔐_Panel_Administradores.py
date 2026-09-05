import streamlit as st
from utils.auth import (
    hay_administradores, crear_administrador, verificar_login,
    esta_logueado, cerrar_sesion, listar_administradores, existe_administrador,
)
from utils.data import (
    crear_serie, listar_series, eliminar_serie,
    crear_leccion, listar_lecciones, eliminar_leccion,
    agregar_material_archivo, agregar_material_enlace,
    listar_materiales, eliminar_material,
    ArchivoDemasiadoGrandeError, LIMITE_ARCHIVO_BYTES,
)

st.set_page_config(page_title="Panel de administradores", page_icon="🔐", layout="wide")
st.title("🔐 Panel de administradores")

if "admin_logueado" not in st.session_state:
    st.session_state["admin_logueado"] = None


# ---------- BLOQUE: primer administrador (solo si no existe ninguno) ----------
if not hay_administradores():
    st.warning("Todavía no hay ningún administrador registrado. Crea el primero para continuar.")
    with st.form("crear_primer_admin"):
        nombre = st.text_input("Tu nombre")
        username = st.text_input("Usuario (sin espacios, ej: jheremy)")
        password = st.text_input("Contraseña", type="password")
        enviado = st.form_submit_button("Crear primer administrador")
        if enviado:
            if not nombre or not username or not password:
                st.error("Completa todos los campos.")
            else:
                crear_administrador(username, nombre, password)
                st.success("Administrador creado. Ahora inicia sesión abajo.")
                st.rerun()
    st.stop()


# ---------- BLOQUE: login ----------
if not esta_logueado():
    st.write("Inicia sesión para gestionar series, lecciones y materiales.")
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        entrar = st.form_submit_button("Entrar")
        if entrar:
            admin = verificar_login(username, password)
            if admin:
                st.session_state["admin_logueado"] = admin
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
    st.stop()


# ---------- A PARTIR DE AQUÍ: usuario logueado ----------
admin = st.session_state["admin_logueado"]
col_a, col_b = st.columns([4, 1])
with col_a:
    st.success(f"Sesión iniciada como **{admin['nombre']}**")
with col_b:
    if st.button("Cerrar sesión"):
        cerrar_sesion()
        st.rerun()

tab_series, tab_lecciones, tab_admins = st.tabs(
    ["📚 Series", "📝 Lecciones y materiales", "👥 Administradores"]
)

# ---------- TAB: SERIES ----------
with tab_series:
    st.subheader("Crear nueva serie")
    with st.form("form_nueva_serie", clear_on_submit=True):
        nombre_serie = st.text_input("Nombre de la serie (ej: Amistad con Dios)")
        desc_serie = st.text_area("Descripción breve", height=80)
        crear = st.form_submit_button("Crear serie")
        if crear:
            if nombre_serie.strip():
                crear_serie(nombre_serie, desc_serie, admin["username"])
                st.success("Serie creada.")
                st.rerun()
            else:
                st.error("Ponle un nombre a la serie.")

    st.divider()
    st.subheader("Series existentes")
    series = listar_series()
    if not series:
        st.caption("Todavía no hay series creadas.")
    for serie in series:
        with st.expander(f"📚 {serie['nombre']}"):
            st.write(serie.get("descripcion", ""))
            if st.button("🗑️ Eliminar esta serie y sus lecciones", key=f"del_serie_{serie['id']}"):
                eliminar_serie(serie["id"])
                st.success("Serie eliminada.")
                st.rerun()

# ---------- TAB: LECCIONES ----------
with tab_lecciones:
    series = listar_series()
    if not series:
        st.info("Primero crea una serie en la pestaña anterior.")
    else:
        nombres_series = {s["nombre"]: s["id"] for s in series}
        serie_sel_nombre = st.selectbox("Selecciona una serie", list(nombres_series.keys()))
        serie_sel_id = nombres_series[serie_sel_nombre]

        st.subheader(f"Nueva lección en: {serie_sel_nombre}")
        with st.form("form_nueva_leccion", clear_on_submit=True):
            nombre_leccion = st.text_input("Nombre de la lección")
            fecha_leccion = st.date_input("Fecha programada")
            desc_leccion = st.text_area("Descripción", height=80)
            crear_lec = st.form_submit_button("Crear lección")
            if crear_lec:
                if nombre_leccion.strip():
                    crear_leccion(
                        serie_sel_id, nombre_leccion, fecha_leccion.isoformat(),
                        desc_leccion, admin["username"],
                    )
                    st.success("Lección creada.")
                    st.rerun()
                else:
                    st.error("Ponle un nombre a la lección.")

        st.divider()
        st.subheader("Lecciones de esta serie")
        lecciones = listar_lecciones(serie_sel_id)
        if not lecciones:
            st.caption("Todavía no hay lecciones en esta serie.")

        limite_kb = LIMITE_ARCHIVO_BYTES // 1024

        for leccion in lecciones:
            with st.expander(f"📝 {leccion['nombre']}  ·  {leccion.get('fecha', 'sin fecha')}"):
                st.write(leccion.get("descripcion", ""))

                st.write(f"**Subir archivo** (PDF, imagen, presentación — máximo {limite_kb} KB):")
                archivo = st.file_uploader(
                    "Selecciona un archivo",
                    key=f"upload_{leccion['id']}",
                    label_visibility="collapsed",
                )
                if archivo is not None:
                    if st.button("Subir archivo", key=f"btn_subir_{leccion['id']}"):
                        try:
                            agregar_material_archivo(leccion["id"], archivo.name, archivo.getvalue())
                            st.success("Archivo subido.")
                            st.rerun()
                        except ArchivoDemasiadoGrandeError as e:
                            st.error(str(e))

                st.write("**O agregar un enlace** (video, audio, Google Drive, YouTube, o un PDF grande):")
                col1, col2 = st.columns(2)
                with col1:
                    nombre_enlace = st.text_input("Nombre del enlace", key=f"nombre_enlace_{leccion['id']}")
                with col2:
                    url_enlace = st.text_input("URL", key=f"url_enlace_{leccion['id']}")
                if st.button("Agregar enlace", key=f"btn_enlace_{leccion['id']}"):
                    if nombre_enlace.strip() and url_enlace.strip():
                        agregar_material_enlace(leccion["id"], nombre_enlace, url_enlace)
                        st.success("Enlace agregado.")
                        st.rerun()
                    else:
                        st.error("Completa el nombre y la URL del enlace.")

                materiales = listar_materiales(leccion["id"])
                if materiales:
                    st.write("**Materiales actuales:**")
                    for mat in materiales:
                        colm1, colm2 = st.columns([5, 1])
                        with colm1:
                            icono = "🔗" if mat["tipo"] == "enlace" else "📎"
                            st.write(f"{icono} {mat['nombre']}")
                        with colm2:
                            if st.button("Eliminar", key=f"del_mat_{mat['id']}"):
                                eliminar_material(mat["id"])
                                st.rerun()

                st.markdown("---")
                if st.button("🗑️ Eliminar esta lección", key=f"del_leccion_{leccion['id']}"):
                    eliminar_leccion(leccion["id"])
                    st.success("Lección eliminada.")
                    st.rerun()

# ---------- TAB: ADMINISTRADORES ----------
with tab_admins:
    st.subheader("Agregar nuevo administrador")
    with st.form("form_nuevo_admin", clear_on_submit=True):
        nuevo_nombre = st.text_input("Nombre completo")
        nuevo_username = st.text_input("Usuario (sin espacios)")
        nueva_password = st.text_input("Contraseña", type="password")
        agregar = st.form_submit_button("Agregar administrador")
        if agregar:
            if not nuevo_nombre or not nuevo_username or not nueva_password:
                st.error("Completa todos los campos.")
            elif existe_administrador(nuevo_username):
                st.error("Ese usuario ya existe.")
            else:
                crear_administrador(nuevo_username, nuevo_nombre, nueva_password)
                st.success("Administrador agregado.")
                st.rerun()

    st.divider()
    st.subheader("Administradores actuales")
    for a in listar_administradores():
        st.write(f"👤 {a['nombre']}  ·  usuario: `{a['username']}`")
