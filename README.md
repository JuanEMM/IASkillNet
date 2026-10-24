# Plantilla de repositorio base — Especialización en Desarrollo con IA Generativa (Accenture)

Esta es la estructura base que vas a usar como punto de partida para tu proyecto en este programa. Es la misma estructura que vas a ir ampliando bloque a bloque, hasta llegar a la aplicación completa que entregas en el Gate 3.

## Cómo empezar

Estos pasos se completan de forma progresiva a lo largo de la Unidad U1.2, no todos el mismo día:

1. Descarga este archivo comprimido (adjunto en la plataforma) y descomprímelo en tu computador. Inicializa el control de versiones sobre esa carpeta y registra tu primer commit con esta estructura base, tal como llegó, antes de modificar nada.
2. Crea tu entorno virtual de Python (por ejemplo, con `venv`) y actívalo.
3. Instala las dependencias que necesites y regístralas en `requirements.txt` (al inicio puede estar vacío o con muy pocas).
4. Copia `.env.example` a un archivo nuevo llamado `.env`, y completa ahí tus credenciales reales (llaves de API, tokens). El archivo `.env` nunca se sube al repositorio: ya está excluido en `.gitignore`.

## Estructura de carpetas

- `src/` : todo el código fuente de tu proyecto va aquí.
- `docs/` : documentación técnica del proyecto (diagramas, decisiones de arquitectura, notas). 
- `requirements.txt` : dependencias de Python de tu proyecto, para que cualquier otra persona pueda reconstruir tu entorno con un solo comando.
- `.env.example` : plantilla de las variables de entorno que tu proyecto necesita, sin valores reales. Tu archivo `.env` real (con tus credenciales) nunca se commitea.
- `.gitignore` : le dice a Git qué archivos y carpetas ignorar (entre ellos, tu entorno virtual y tu archivo `.env`).

## Instalación y uso

Esta parte es para quien descarga el proyecto y quiere dejarlo funcionando. Todos los comandos se escriben en una terminal, ubicado en la carpeta del proyecto (la que contiene `src/` y `requirements.txt`).

### 1. Tener Python instalado

Hace falta Python 3. El proyecto se desarrolló con la versión 3.14; si usas otra y alguna librería no se instala, prueba con esa. Para ver si ya lo tienes:

| Sistema | Comando |
|---|---|
| Windows | `python --version` |
| macOS / Linux | `python3 --version` |

Si no aparece una versión, hay que instalarlo:

- **Windows:** descarga el instalador desde python.org y marca la casilla "Add python.exe to PATH" antes de instalar. Ya trae `pip`.
- **macOS:** instalador de python.org o, si usas Homebrew, `brew install python`. Ya trae `pip` (se usa como `pip3`).
- **Linux:** en Debian o Ubuntu, `sudo apt install python3 python3-pip python3-venv`. En Fedora, `sudo dnf install python3 python3-pip`.

### 2. Crear el entorno virtual

El entorno virtual deja las librerías del proyecto en una carpeta propia (`venv`) para que no se mezclen con las del resto del computador.

| Sistema | Comando |
|---|---|
| Windows | `python -m venv venv` |
| macOS / Linux | `python3 -m venv venv` |

### 3. Activar el entorno

| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `venv\Scripts\Activate.ps1` |
| Windows (cmd) | `venv\Scripts\activate.bat` |
| macOS / Linux | `source venv/bin/activate` |

Cuando quedó activo, la terminal muestra `(venv)` al comienzo de la línea. En PowerShell, si aparece un error diciendo que la ejecución de scripts está deshabilitada, escribe `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` (vale solo para esa ventana) y vuelve a activar. Para salir del entorno: `deactivate`.

### 4. Instalar las librerías

Con el entorno activado:

| Sistema | Comando |
|---|---|
| Windows | `pip install -r requirements.txt` |
| macOS / Linux | `pip3 install -r requirements.txt` |

Dentro del entorno activo `pip` también funciona en macOS y Linux. Si en cualquier sistema el comando no se reconoce, sirve `python -m pip install -r requirements.txt`.

### 5. Crear el archivo `.env`

El proyecto lee sus claves desde un archivo `.env` en la raíz. No viene en el repositorio, pero sí una plantilla, `.env.example`, que se copia con el nombre `.env`:

| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `Copy-Item .env.example .env` |
| Windows (cmd) | `copy .env.example .env` |
| macOS / Linux | `cp .env.example .env` |

Después abre el `.env` con cualquier editor y reemplaza el valor de ejemplo de cada línea por tu clave:

```
GEMINI_API_KEY=tu_clave_de_gemini
OPENROUTER_API_KEY=tu_clave_de_openrouter
```

- `GEMINI_API_KEY` es obligatoria. Se genera en Google AI Studio (aistudio.google.com/apikey).
- `OPENROUTER_API_KEY` solo se usa en `src/consumir_openrouter.py`. Si no vas a correr ese script, puedes dejarla como está.

Los valores van sin comillas y sin espacios alrededor del `=`. El `.env` no se sube al repositorio (está en `.gitignore`), así que cada persona tiene el suyo con sus propias claves.

### 6. Ejecutar

Desde la raíz del proyecto y con el entorno activo (dentro del entorno `python` funciona igual en los tres sistemas).

Consulta de ejemplo a Gemini:

```
python src/consumir_gemini.py
```

Envía una guía de transporte de ejemplo y muestra el JSON con los datos extraídos (`dateInput` y `items`). Si algo falla, por ejemplo falta la clave o no hay conexión, imprime "No se pudo completar la operación:" y el motivo.

Prueba de consistencia de los prompts:

```
python src/prompts/test_consistencia.py
```

Prueba cada prompt de `src/prompts/banco.py` tres veces e imprime cuántas respuestas fueron válidas, por ejemplo `obtener_datos_guia: 3/3 respuestas válidas`. El resultado también queda guardado en `src/prompts/registro_resultados.json`. Hace 9 llamadas reales a la API (3 prompts por 3 intentos), así que gasta un poco de cuota.

## Reglas que se mantienen durante todo el programa

- Ningún secreto (contraseña, llave de API, token) va escrito directamente en el código ni en ningún archivo que se suba al repositorio.
- Cada proyecto nuevo tiene su propio entorno virtual: no se comparten dependencias entre proyectos distintos.
- Todo el trabajo que se entrega en este programa vive en un repositorio de GitHub, sin excepción.
