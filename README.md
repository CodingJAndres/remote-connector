# Remote Connector

Este proyecto consta de un script en Python que permite conectarse a servidores usando los protocolos SSH y FTP, así como realizar ataques de fuerza bruta para encontrar credenciales válidas.

## Requisitos

- Python 3.x
- [paramiko](https://pypi.org/project/paramiko/) (para la conexión SSH)
- [ftplib](https://docs.python.org/3/library/ftplib.html) (para la conexión FTP)
- [colorama](https://pypi.org/project/colorama/) (para la gestión de colores en la terminal)

## Instalación

1. **Clona o descarga el repositorio:**

    ```bash
    https://github.com/CodingJAndres/remote-connector.git
    ```

2. **Navega al directorio del proyecto:**

    ```bash
    cd remote-connector
    ```

3. **Instala las dependencias necesarias:**

    ```bash
    pip install paramiko colorama
    ```

## Script

### Conector Remoto

Este script permite conectar a un servidor utilizando los protocolos SSH o FTP. Además, puede realizar ataques de fuerza bruta para encontrar credenciales válidas.

#### Uso

1. **Ejecuta el script:**

    ```bash
    python conectar_remoto.py -H <host> -s <service> -m <mode> -U <userfile> -C <passfile>
    ```

    - `-H` : Dirección del servidor.
    - `-s` : Servicio al que conectar (`ssh` o `ftp`).
    - `-m` : Modo de operación (`normal` o `brute`).
    - `-U` : Archivo con posibles nombres de usuario (para el modo de fuerza bruta).
    - `-C` : Archivo con posibles contraseñas (para el modo de fuerza bruta).

2. **En el modo normal:**
    - Se te pedirá que introduzcas el nombre de usuario y la contraseña manualmente.
    
3. **En el modo de fuerza bruta:**
    - El script probará todas las combinaciones posibles de usuarios y contraseñas desde los archivos proporcionados.

#### Descripción de Opciones

- **Dirección del servidor:** La IP o nombre del servidor al que te deseas conectar.
- **Servicio:** El servicio al que deseas conectarte (`ssh` o `ftp`).
- **Modo de operación:** Puede ser `normal` para conexión directa o `brute` para realizar un ataque de fuerza bruta.
- **Archivo de usuarios:** Archivo de texto que contiene posibles nombres de usuario (uno por línea).
- **Archivo de contraseñas:** Archivo de texto que contiene posibles contraseñas (una por línea).

#### Manejo de Errores

- **Error de autenticación SSH/FTP:** Indica que las credenciales proporcionadas no son válidas.
- **Error de conexión:** El puerto del servicio no está accesible o hay problemas de red.
- **FileNotFoundError:** Se muestra si alguno de los archivos proporcionados no se encuentra en la ruta especificada.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

---

Utiliza este script para probar la conexión a servidores y realizar ataques de fuerza bruta de manera segura y controlada.
