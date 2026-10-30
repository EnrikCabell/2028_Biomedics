# Publicación privada de BIOMEDICS

## Arquitectura
- Aplicación: Streamlit Community Cloud.
- Datos: PostgreSQL alojado, con almacenamiento persistente.
- Acceso: una cuenta administradora protegida por contraseña.
- La dirección web podrá abrirse desde cualquier ubicación y dispositivo. La pantalla de acceso seguirá siendo obligatoria.

## 1. Crear la base de datos
Crea una instancia PostgreSQL en un proveedor administrado. Copia la cadena de conexión PostgreSQL (DATABASE_URL) y mantenla privada. No la guardes en el código ni en GitHub.

## 2. Generar las credenciales del administrador
En tu computadora, abre Python y ejecuta:

```python
import hashlib, secrets, getpass
usuario = input("Usuario administrador: ")
password = getpass.getpass("Contraseña nueva: ")
salt = secrets.token_hex(32)
hash_password = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 600000).hex()
print("APP_USERNAME =", usuario)
print("APP_PASSWORD_SALT =", salt)
print("APP_PASSWORD_HASH =", hash_password)
```

Guarda los tres valores generados. No compartas la contraseña ni los valores de configuración.

## 3. Publicar en Streamlit Community Cloud
1. Entra a https://share.streamlit.io/ e inicia sesión con GitHub.
2. Selecciona el repositorio `EnrikCabell/2028_Biomedics`, la rama `main` y el archivo `app.py`.
3. Antes de permitir el acceso a usuarios, abre la configuración de la aplicación y entra a **Secrets**.
4. Agrega las siguientes variables en formato TOML, sustituyendo cada valor por el real:

```toml
APP_ENV = "production"
APP_USERNAME = "usuario_administrador"
APP_PASSWORD_SALT = "sal_generada"
APP_PASSWORD_HASH = "hash_generado"
DATABASE_URL = "postgresql://usuario:contraseña@servidor:5432/base_datos?sslmode=require"
```

5. Guarda los Secrets y despliega la aplicación. La primera ejecución creará las tablas necesarias en PostgreSQL.
6. Abre la URL asignada y prueba el inicio de sesión, el alta de un cliente, un estudio y una cita. Comprueba que los datos sigan presentes después de reiniciar la aplicación.

## 4. Seguridad y alcance
- No publiques credenciales, contraseñas ni la cadena DATABASE_URL en el repositorio.
- El repositorio puede mantenerse privado. La URL de la aplicación será accesible desde internet, pero la aplicación exigirá autenticación.
- Esta versión habilita una sola cuenta administradora. No compartas esa cuenta entre empleados. Si más personal requiere acceso, conviene implementar cuentas individuales y permisos por función antes de habilitarlos.
- Configura copias de seguridad automáticas en el proveedor PostgreSQL y restringe quién puede administrar la base de datos.
- La aplicación conserva un modo local de demostración durante el desarrollo. En producción, si falta DATABASE_URL, se detiene para impedir que los registros queden en almacenamiento temporal.

## 5. Actualizaciones
Los cambios enviados a la rama `main` se pueden desplegar desde Streamlit Community Cloud. Después de cada actualización, revisa el inicio de sesión y las operaciones principales.
