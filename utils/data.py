import datetime
import uuid
from utils.firebase_config import get_db, get_bucket


# ---------- SERIES ----------

def crear_serie(nombre: str, descripcion: str, creado_por: str):
    db = get_db()
    db.collection("series").add({
        "nombre": nombre.strip(),
        "descripcion": descripcion.strip(),
        "creado_por": creado_por,
        "fecha_creacion": datetime.datetime.utcnow().isoformat(),
    })


def listar_series():
    db = get_db()
    series = []
    for doc in db.collection("series").stream():
        d = doc.to_dict()
        d["id"] = doc.id
        series.append(d)
    series.sort(key=lambda s: s.get("nombre", ""))
    return series


def eliminar_serie(serie_id: str):
    db = get_db()
    # Elimina también las lecciones de esa serie
    lecciones = db.collection("lecciones").where("serie_id", "==", serie_id).stream()
    for lec in lecciones:
        eliminar_leccion(lec.id)
    db.collection("series").document(serie_id).delete()


# ---------- LECCIONES ----------

def crear_leccion(serie_id: str, nombre: str, fecha: str, descripcion: str, creado_por: str):
    db = get_db()
    ref = db.collection("lecciones").add({
        "serie_id": serie_id,
        "nombre": nombre.strip(),
        "fecha": fecha,  # formato ISO: YYYY-MM-DD
        "descripcion": descripcion.strip(),
        "materiales": [],
        "creado_por": creado_por,
        "fecha_creacion": datetime.datetime.utcnow().isoformat(),
    })
    return ref[1].id


def listar_lecciones(serie_id: str = None):
    db = get_db()
    lecciones = []
    query = db.collection("lecciones")
    if serie_id:
        query = query.where("serie_id", "==", serie_id)
    for doc in query.stream():
        d = doc.to_dict()
        d["id"] = doc.id
        lecciones.append(d)
    lecciones.sort(key=lambda l: l.get("fecha", ""))
    return lecciones


def eliminar_leccion(leccion_id: str):
    db = get_db()
    doc = db.collection("lecciones").document(leccion_id).get()
    if doc.exists:
        data = doc.to_dict()
        bucket = get_bucket()
        for mat in data.get("materiales", []):
            if mat.get("tipo") == "archivo" and mat.get("storage_path"):
                try:
                    bucket.blob(mat["storage_path"]).delete()
                except Exception:
                    pass
    db.collection("lecciones").document(leccion_id).delete()


# ---------- MATERIALES ----------

def agregar_material_archivo(leccion_id: str, serie_id: str, nombre_archivo: str, contenido_bytes: bytes):
    bucket = get_bucket()
    ext = nombre_archivo.split(".")[-1] if "." in nombre_archivo else ""
    ruta = f"materiales/{serie_id}/{leccion_id}/{uuid.uuid4().hex}_{nombre_archivo}"
    blob = bucket.blob(ruta)
    blob.upload_from_string(contenido_bytes, content_type=None)

    db = get_db()
    leccion_ref = db.collection("lecciones").document(leccion_id)
    leccion = leccion_ref.get().to_dict()
    materiales = leccion.get("materiales", [])
    materiales.append({
        "nombre": nombre_archivo,
        "tipo": "archivo",
        "storage_path": ruta,
    })
    leccion_ref.update({"materiales": materiales})


def agregar_material_enlace(leccion_id: str, nombre: str, url: str):
    db = get_db()
    leccion_ref = db.collection("lecciones").document(leccion_id)
    leccion = leccion_ref.get().to_dict()
    materiales = leccion.get("materiales", [])
    materiales.append({
        "nombre": nombre.strip(),
        "tipo": "enlace",
        "url": url.strip(),
    })
    leccion_ref.update({"materiales": materiales})


def eliminar_material(leccion_id: str, indice: int):
    db = get_db()
    leccion_ref = db.collection("lecciones").document(leccion_id)
    leccion = leccion_ref.get().to_dict()
    materiales = leccion.get("materiales", [])
    if 0 <= indice < len(materiales):
        mat = materiales.pop(indice)
        if mat.get("tipo") == "archivo" and mat.get("storage_path"):
            try:
                get_bucket().blob(mat["storage_path"]).delete()
            except Exception:
                pass
        leccion_ref.update({"materiales": materiales})


def descargar_material(storage_path: str) -> bytes:
    bucket = get_bucket()
    blob = bucket.blob(storage_path)
    return blob.download_as_bytes()
