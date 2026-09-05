# Príncipe de Paz Jóvenes — Plataforma de capacitación

Esta versión funciona **solo con Firestore** (gratis, plan Spark), sin necesitar
Firebase Storage ni tarjeta de crédito.

- **Página pública** (`app.py`): calendario de series y lecciones, con descarga de materiales. Esta es la que compartes por link.
- **Panel de administradores** (`pages/1_🔐_Panel_Administradores.py`): login, crear series, crear lecciones, subir materiales (archivos pequeños o enlaces), y agregar más administradores.

## Cómo se manejan los materiales

- **Archivos pequeños** (PDF, imágenes, documentos, presentaciones de hasta ~700 KB) se guardan directo en la base de datos (Firestore), sin costo.
- **Archivos grandes o videos/audios**: se agregan como un **enlace** (por ejemplo, subes el archivo a Google Drive o el video a YouTube, y pegas el link en la plataforma). Esto no tiene límite de tamaño y sigue siendo gratis.

Si en el futuro el grupo crece mucho y quieres subir archivos pesados directo (sin usar enlaces), se puede activar Firebase Storage más adelante — eso sí requeriría el plan Blaze de Firebase (pago por uso, con capa gratuita).

## Paso 1 — Subir estos archivos a GitHub

1. Ve a tu repositorio: `https://github.com/jheremymerida123-lab/MNJPRINCIPEDEPAZ`
2. Sube (o reemplaza) todos los archivos y carpetas de este proyecto, manteniendo la misma estructura (`pages/`, `utils/`)
3. **IMPORTANTE:** no subas el archivo `.streamlit/secrets.toml.example` con datos reales — es solo un ejemplo. Las credenciales reales se configuran directo en Streamlit Cloud (paso 3), nunca en GitHub.

## Paso 2 — Activar Firestore en Firebase

Si ya lo activaste anteriormente, sáltate este paso.

1. En tu proyecto de Firebase (MNJ-principe-de-paz), entra a **"Bases de datos y almacenamiento" → "Firestore Database"**
2. Haz clic en **"Crear base de datos"**, modo **"Producción"**, elige la ubicación más cercana
3. Espera a que termine de crearse

No necesitas activar Storage.

## Paso 3 — Obtener las credenciales y configurarlas en Streamlit

1. En Firebase, ve al ícono de engranaje ⚙️ > **"Configuración del proyecto"**
2. Ve a la pestaña **"Cuentas de servicio"**
3. Haz clic en **"Generar nueva clave privada"** → se descarga un archivo `.json`. Guárdalo, contiene información sensible.
4. Ve a **share.streamlit.io**, haz clic en **"Create app"**, y selecciona tu repositorio `MNJPRINCIPEDEPAZ`, rama `main`, archivo principal `app.py`
5. En **Settings > Secrets** de la app, pega esto, reemplazando cada valor con el del archivo JSON descargado:

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
- **Material** = archivos pequeños que subes directo, o enlaces (para videos/audios o archivos grandes)

## Siguientes mejoras posibles

- Vista de calendario visual (mes por mes)
- Notificaciones o recordatorios
- Categorías por edad
- Buscador de lecciones
- Activar Firebase Storage más adelante si se necesita subir archivos pesados directo
