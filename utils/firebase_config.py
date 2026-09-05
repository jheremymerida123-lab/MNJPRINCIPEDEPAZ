import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage


@st.cache_resource
def init_firebase():
    """Inicializa la conexión con Firebase (Firestore y Storage).

    Lee las credenciales desde st.secrets["firebase"], que debe
    contener el contenido del archivo JSON de la cuenta de servicio
    de Firebase, más el campo storage_bucket.
    """
    if not firebase_admin._apps:
        secrets = dict(st.secrets["firebase"])
        storage_bucket = secrets.pop("storage_bucket")

        cred = credentials.Certificate(secrets)
        firebase_admin.initialize_app(cred, {
            "storageBucket": storage_bucket
        })

    db = firestore.client()
    bucket = storage.bucket()
    return db, bucket


def get_db():
    db, _ = init_firebase()
    return db


def get_bucket():
    _, bucket = init_firebase()
    return bucket
