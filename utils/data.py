import base64
import datetime
from utils.firebase_config import get_db

# Límite de tamaño de archivo. Firestore permite documentos de hasta 1 MiB,
# y guardar el archivo en base64 le agrega ~33% de peso, así que dejamos
# margen de seguridad.
LIMITE_ARCHIVO_BYTES = 700 * 1024  # 700 KB


class ArchivoDemasiadoGrandeError(Exception):
    pass


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
    materiales = db.collection("materiales").where("leccion_id", "==", leccion_id).stream()
    for mat in materiales:
        mat.reference.delete()
    db.collection("lecciones").document(leccion_id).delete()


# ---------- MATERIALES ----------
# Se guardan en su propia colección "materiales" (no dentro de la lección)
# para no exceder el límite de tamaño de un documento de Firestore.

def agregar_material_archivo(leccion_id: str, nombre_archivo: str, contenido_bytes: bytes):
    if len(contenido_bytes) > LIMITE_ARCHIVO_BYTES:
        raise ArchivoDemasiadoGrandeError(
            f"El archivo pesa {len(contenido_bytes) / 1024:.0f} KB. "
            f"El límite es {LIMITE_ARCHIVO_BYTES // 1024} KB. "
            "Para archivos más grandes (o videos), usa un enlace de Google Drive o YouTube."
        )
    contenido_b64 = base64.b64encode(contenido_bytes).decode("utf-8")
    db = get_db()
    db.collection("materiales").add({
        "leccion_id": leccion_id,
        "nombre": nombre_archivo,
        "tipo": "archivo",
        "contenido_b64": contenido_b64,
        "fecha_creacion": datetime.datetime.utcnow().isoformat(),
    })


def agregar_material_enlace(leccion_id: str, nombre: str, url: str):
    db = get_db()
    db.collection("materiales").add({
        "leccion_id": leccion_id,
        "nombre": nombre.strip(),
        "tipo": "enlace",
        "url": url.strip(),
        "fecha_creacion": datetime.datetime.utcnow().isoformat(),
    })


def listar_materiales(leccion_id: str):
    db = get_db()
    materiales = []
    for doc in db.collection("materiales").where("leccion_id", "==", leccion_id).stream():
        d = doc.to_dict()
        d["id"] = doc.id
        materiales.append(d)
    materiales.sort(key=lambda m: m.get("fecha_creacion", ""))
    return materiales


def eliminar_material(material_id: str):
    db = get_db()
    db.collection("materiales").document(material_id).delete()


def obtener_contenido_material(material_id: str) -> bytes:
    db = get_db()
    doc = db.collection("materiales").document(material_id).get()
    data = doc.to_dict()
    return base64.b64decode(data["contenido_b64"])
