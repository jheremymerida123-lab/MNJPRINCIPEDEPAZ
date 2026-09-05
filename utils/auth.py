import hashlib
import datetime
import streamlit as st
from utils.firebase_config import get_db


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hay_administradores() -> bool:
    db = get_db()
    docs = db.collection("admins").limit(1).stream()
    return len(list(docs)) > 0


def crear_administrador(username: str, nombre: str, password: str):
    db = get_db()
    username = username.strip().lower()
    db.collection("admins").document(username).set({
        "nombre": nombre.strip(),
        "password_hash": hash_password(password),
        "fecha_creacion": datetime.datetime.utcnow().isoformat(),
    })


def existe_administrador(username: str) -> bool:
    db = get_db()
    username = username.strip().lower()
    doc = db.collection("admins").document(username).get()
    return doc.exists


def verificar_login(username: str, password: str):
    """Devuelve el dict del admin si las credenciales son correctas, si no None."""
    db = get_db()
    username = username.strip().lower()
    doc = db.collection("admins").document(username).get()
    if not doc.exists:
        return None
    data = doc.to_dict()
    if data.get("password_hash") == hash_password(password):
        data["username"] = username
        return data
    return None


def listar_administradores():
    db = get_db()
    admins = []
    for doc in db.collection("admins").stream():
        d = doc.to_dict()
        admins.append({"username": doc.id, "nombre": d.get("nombre", "")})
    return admins


def esta_logueado() -> bool:
    return st.session_state.get("admin_logueado") is not None


def cerrar_sesion():
    st.session_state["admin_logueado"] = None
