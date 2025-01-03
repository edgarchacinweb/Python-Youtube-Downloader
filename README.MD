# Python video downloader

---

Cliente de descarga multimedia construido con la librería pytubefix, FFMPEG y TKinter para descargar vídeos y música de youtube.

## Instalación
1) clona el repositorio para obtener el código fuente (esta acción requiere tener instalado git en tu máquina):

```
git clone https://github.com/edgarchacinweb/Python-youtube-downloader.git
```

2) Instala FFMPEG
    - **Windows (con winget):**

    ```
    winget install --id=Gyan.FFmpeg  -e
    ```

    - **Windows (sin winget):**

    > Ingresa a la siguiente dirección URL: https://www.ffmpeg.org/download.html#build-windows
    > Descarga el archivo comprimido y descomprímelo en cualquier ruta de tu sistema.
    > Copia la ruta del directorio que contiene FFMPEG y crea una variable de entorno con la dirección del directorio.

    - **Linux (apt):**

    ```
    sudo apt update
    sudo apt install ffmpeg
    ```

    - **Linux (yum):**
    
    ```
    sudo yum install epel-release
    sudo yum localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
    sudo yum install ffmpeg ffmpeg-devel
    ```

    - **MacOS:**

    > Ingresa a la siguiente dirección URL: https://evermeet.cx/ffmpeg/
    > Sigue los pasos de instalación.

3) Crea un entorno virtual
    - **Linux y MacOS:**
    ```
    python3 -m venv .venv
    ```

    - **Windows:**
    ```
    python -m venv .venv
    ```

4) Accede al entorno virtual
    - **Linux y MacOS:**
    ```
    . .venv/bin/activate
    ```

    - **Windows:**
    ```
    . .venv/Scripts/activate
    ```

4) Instala las dependencias

```
pip install -r requirements.txt
```

5) Ejecuta la aplicación
    - **Linux y MacOS:**
    ```
    python3 main.py
    ```

    - **Windows:**
    ```
    py main.py
    ```