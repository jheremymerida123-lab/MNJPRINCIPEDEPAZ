# Príncipe de Paz Jóvenes — Plataforma de capacitación

Esta es la primera versión del sistema. Incluye:

- **Página pública** (`app.py`): calendario de series y lecciones, con descarga de materiales. Esta es la que compartes por link.
- **Panel de administradores** (`pages/1_🔐_Panel_Administradores.py`): login, crear series, crear lecciones, subir materiales (archivos o enlaces), y agregar más administradores.

## Paso 1 — Subir estos archivos a GitHub

1. Ve a tu repositorio: `https://github.com/jheremymerida123-lab/MNJPRINCIPEDEPAZ`
2. Haz clic en **"uploading an existing file"** (o "Add file" > "Upload files")
3. Sube **todos** los archivos y carpetas de este proyecto, manteniendo la misma estructura de carpetas (`pages/`, `utils/`, `.streamlit/`)
4. **IMPORTANTE:** no subas el archivo `.streamlit/secrets.toml.example` con datos reales — ese es solo un ejemplo. Las credenciales reales se configuran directo en Streamlit Cloud (paso 3), nunca en GitHub.
5. Confirma el commit ("Commit changes")

## Paso 2 — Activar los servicios de Firebase que se usan

En tu proyecto de Firebase (MNJ-principe-de-paz):

1. En el menú izquierdo, entra a **"Bases de datos y almacenamiento"** (o busca "Firestore Database") y haz clic en **"Crear base de datos"**. Elige el modo **"Producción"** y la ubicación más cercana (ej. `us-central`).
2. En el mismo menú, entra a **"Storage"** y haz clic en **"Comenzar"** / "Get started". Acepta las reglas por defecto (las ajustaremos si hace falta).

## Paso 3 — Obtener las credenciales y configurarlas en Streamlit

1. En Firebase, ve al ícono de engranaje ⚙️ (arriba, junto a "Descripción general") > **"Configuración del proyecto"**
2. Ve a la pestaña **"Cuentas de servicio"**
3. Haz clic en **"Generar nueva clave privada"** → se descarga un archivo `.json`. Guárdalo, contiene información sensible.
4. Ve a **share.streamlit.io**, haz clic en **"Create app"** (o "New app"), y selecciona tu repositorio `MNJPRINCIPEDEPAZ`, rama `main`, archivo principal `app.py`
5. Antes de darle "Deploy" (o después, entrando a **Settings > Secrets** de la app ya creada), pega esto, reemplazando cada valor con el del archivo JSON descargado:

```toml
[firebase]
type = "service_account"
project_id = "el-project-id-del-json"
private_key_id = "el-private_key_id-del-json"
private_key = "la-private_key-del-json (incluye los \n tal cual)"
client_email = "el-client_email-del-json"
client_id = "el-client_id-del-json"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "el-client_x509_cert_url-del-json"
storage_bucket = "el-project-id.appspot.com"
```

6. Guarda los secrets. La app se reiniciará sola con la conexión activa.

## Paso 4 — Crear tu primer administrador

1. Entra a tu app publicada (algo como `principe-de-paz-jovenes.streamlit.app`)
2. En el menú lateral, entra a **"Panel de Administradores"**
3. Como todavía no existe ningún administrador, verás un formulario para crear el primero — complétalo con tu nombre, un usuario y una contraseña
4. Con eso ya puedes iniciar sesión y empezar a crear series y lecciones

## Cómo se organiza el contenido

- **Serie** = un tema o unidad (ej. "Amistad con Dios")
- **Lección** = una sesión dentro de una serie, con su fecha programada
- **Material** = archivos (PDF, imágenes, presentaciones, documentos) que se suben directo, o enlaces (para videos/audios que conviene alojar en YouTube o Google Drive)

## Siguientes mejoras posibles

Cuando quieras seguir creciendo la plataforma, se le puede agregar:
- Vista de calendario visual (mes por mes)
- Notificaciones o recordatorios
- Categorías por edad
- Buscador de lecciones
- Historial y estadísticas de descargas
