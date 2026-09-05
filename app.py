import datetime
import streamlit as st
from utils.data import listar_series, listar_lecciones
from utils.data import descargar_material

st.set_page_config(
    page_title="Príncipe de Paz Jóvenes",
    page_icon="🕊️",
    layout="wide",
)

st.title("🕊️ Príncipe de Paz Jóvenes")
st.subheader("Plataforma de capacitación y lecciones bíblicas juveniles")
st.write(
    "Aquí encontrarás las series y lecciones programadas. "
    "Entra a cada lección para descargar el material disponible."
)
st.divider()

try:
    series = listar_series()
except Exception as e:
    st.error(
        "No se pudo conectar con la base de datos. Si eres el administrador, "
        "revisa que las credenciales de Firebase estén bien configuradas en Secrets."
    )
    st.stop()

if not series:
    st.info("Todavía no hay series de lecciones publicadas. Vuelve pronto 🙌")
else:
    hoy = datetime.date.today().isoformat()

    for serie in series:
        lecciones = listar_lecciones(serie["id"])
        with st.expander(f"📚 {serie['nombre']}  ·  {len(lecciones)} lección(es)", expanded=False):
            if serie.get("descripcion"):
                st.write(serie["descripcion"])

            if not lecciones:
                st.caption("Aún no hay lecciones en esta serie.")
                continue

            for leccion in lecciones:
                fecha_str = leccion.get("fecha", "")
                es_futura = fecha_str >= hoy if fecha_str else False
                etiqueta_fecha = f"📅 {fecha_str}" if fecha_str else "Sin fecha"
                if es_futura:
                    etiqueta_fecha += "  🟢 próxima"

                st.markdown(f"### {leccion['nombre']}")
                st.caption(etiqueta_fecha)
                if leccion.get("descripcion"):
                    st.write(leccion["descripcion"])

                materiales = leccion.get("materiales", [])
                if materiales:
                    st.write("**Material disponible:**")
                    cols = st.columns(min(len(materiales), 4) or 1)
                    for i, mat in enumerate(materiales):
                        col = cols[i % len(cols)]
                        with col:
                            if mat.get("tipo") == "enlace":
                                st.link_button(f"🔗 {mat['nombre']}", mat["url"], use_container_width=True)
                            else:
                                try:
                                    contenido = descargar_material(mat["storage_path"])
                                    st.download_button(
                                        f"⬇️ {mat['nombre']}",
                                        data=contenido,
                                        file_name=mat["nombre"],
                                        use_container_width=True,
                                        key=f"dl_{leccion['id']}_{i}",
                                    )
                                except Exception:
                                    st.caption(f"⚠️ No se pudo cargar: {mat['nombre']}")
                else:
                    st.caption("Sin material subido todavía.")

                st.markdown("---")

st.divider()
st.caption("¿Eres administrador? Usa el menú lateral para entrar al panel de administración.")
