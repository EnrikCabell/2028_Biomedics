# Publicación de BIOMEDICS

## Arquitectura
- Aplicación: Streamlit Community Cloud.
- Datos: PostgreSQL alojado, con almacenamiento persistente.
- La aplicación no solicita usuario ni contraseña para ingresar.
- La dirección web podrá abrirse desde cualquier ubicación y dispositivo.

## 1. Crear la base de datos
Crea una instancia PostgreSQL en un proveedor administrado. Copia la cadena de conexión PostgreSQL (DATABASE_URL) y mantenla privada. No la guardes en el código ni en GitHub.

## 2. Publicar en Streamlit Community Cloud
1. Entra a https://share.streamlit.io/ e inicia sesión con GitHub.
2. Selecciona el repositorio `EnrikCabell/2028_Biomedics`, la rama `main` y el archivo `app.py`.
3. En la configuración de la aplicación, abre **Secrets** y agrega:

```toml
APP_ENV = "production"
DATABASE_URL = "postgresql://usuario:contraseña@servidor:5432/base_datos?sslmode=require"
```

4. Sustituye DATABASE_URL por la cadena real de tu base de datos y guarda los Secrets.
5. Despliega la aplicación. La primera ejecución creará las tablas necesarias en PostgreSQL.
6. Abre la URL asignada y prueba el alta de un cliente, un estudio y una cita. Comprueba que los datos sigan presentes después de reiniciar la aplicación.

## 3. Seguridad y almacenamiento
- No publiques la cadena DATABASE_URL en el repositorio.
- La aplicación no tendrá pantalla de inicio de sesión; cualquier persona que tenga la dirección web podrá entrar y consultar o modificar los registros.
- Configura copias de seguridad automáticas en el proveedor PostgreSQL y limita el acceso administrativo a la base de datos.
- La aplicación conserva un modo local de demostración durante el desarrollo. En producción, si falta DATABASE_URL, se detiene para impedir que los registros queden en almacenamiento temporal.

## 4. Actualizaciones
Los cambios enviados a la rama `main` se pueden desplegar desde Streamlit Community Cloud.
