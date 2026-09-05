import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore


@st.cache_resource
def init_firebase():
    """Inicializa la conexión con Firestore.

    Lee las credenciales desde st.secrets["firebase"], que debe
    contener el contenido del archivo JSON de la cuenta de servicio
    de Firebase.
    """
    if not firebase_admin._apps:
        secrets = dict(st.secrets["firebase"])
        # Por si quedó configurado de una versión anterior, lo ignoramos.
        secrets.pop("storage_bucket", None)

        cred = credentials.Certificate(secrets)
        firebase_admin.initialize_app(cred)

    return firestore.client()


def get_db():
    return init_firebase()
