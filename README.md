# Multi-Provider Async LLM Manager

**Trabajo Práctico — AI Engineering | Coderhouse**

**Autor:** Fernando Tasín
**Lenguaje:** Python 3.12

---

## 1. Descripción del proyecto

Este proyecto implementa un administrador asíncrono de modelos de lenguaje (LLMs), desarrollado en Python 3.12, que permite interactuar con las APIs de **OpenAI y Anthropic** desde una única interfaz.

La aplicación utiliza una clase centralizada llamada `AsyncLLMManager`, capaz de seleccionar dinámicamente el proveedor de inteligencia artificial mediante variables de entorno.

El sistema incluye validación de parámetros con Pydantic, generación de respuestas mediante streaming y manejo controlado de errores de API.

## 2. Tecnologías utilizadas

- **Python 3.12:** lenguaje de programación.
- **OpenAI SDK:** integración con modelos de OpenAI.
- **Anthropic SDK:** integración con modelos Claude.
- **Pydantic:** validación de parámetros de entrada.
- **python-dotenv:** administración de variables de entorno.
- **asyncio:** ejecución de operaciones asíncronas.
- **Git y GitHub:** control de versiones y publicación del proyecto.

## 3. Funcionalidades principales

- Integración con OpenAI y Anthropic.
- Selección del proveedor mediante `LLM_PROVIDER`.
- Validación de parámetros mediante Pydantic.
- Validación de temperatura entre 0 y 2.
- Validación de `max_tokens` como entero positivo, con máximo de 8192.
- Generación asíncrona de respuestas.
- Streaming de texto mediante `async for` y `yield`.
- Manejo de errores de conexión y rate limiting.
- Captura de excepciones generales de las APIs.
- Configuración mediante variables de entorno.

## 4. Estructura del proyecto

```text
curso-python-ai/
├── config.py
├── llm_manager.py
├── main.py
├── test_config.py
├── requirements.txt
├── README.md
└── .gitignore
```

**Descripción de los archivos:**

| Archivo | Función |
|---|---|
| `config.py` | Define el esquema Pydantic y valida los parámetros. |
| `llm_manager.py` | Implementa `AsyncLLMManager` para OpenAI y Anthropic. |
| `main.py` | Ejecuta las consultas a los modelos. |
| `test_config.py` | Realiza pruebas de validación de parámetros. |
| `requirements.txt` | Registra las dependencias del proyecto. |
| `.gitignore` | Excluye credenciales y archivos locales. |
| `README.md` | Documenta la instalación, configuración y ejecución. |

El archivo `.env` se crea localmente y no se incluye en el repositorio por motivos de seguridad.

## 5. Instalación

### Requisitos previos

- Python 3.12 instalado.
- Git instalado.
- Una API key de OpenAI o Anthropic.
- Créditos disponibles en el proveedor que se desee utilizar.

### Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd curso-python-ai
```

Reemplazar `URL_DEL_REPOSITORIO` por la dirección del repositorio publicado en GitHub.

### Crear el entorno virtual

En Windows:

```powershell
py -3.12 -m venv .venv
```

### Activar el entorno virtual

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

## 6. Configuración de variables de entorno

Crear un archivo llamado `.env` en la raíz del proyecto.

Agregar las siguientes variables:

```dotenv
# API KEYS
OPENAI_API_KEY=tu_api_key_openai
ANTHROPIC_API_KEY=tu_api_key_anthropic

# CONFIGURACION DEL LLM
LLM_PROVIDER=openai

# MODELOS
OPENAI_MODEL=gpt-4o-mini
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
```

Las API keys deben reemplazarse por credenciales válidas.

### Selección del proveedor

Para utilizar OpenAI:

```dotenv
LLM_PROVIDER=openai
```

Para utilizar Anthropic:

```dotenv
LLM_PROVIDER=anthropic
```

El sistema selecciona automáticamente el cliente y el modelo correspondiente.

Los modelos indicados fueron utilizados durante el desarrollo. Su disponibilidad puede variar según la cuenta y el proveedor.

## 7. Ejecución

Con el entorno virtual activado:

```powershell
python main.py
```

El programa carga las variables de entorno, valida los parámetros y ejecuta una consulta al proveedor seleccionado.

La respuesta se muestra progresivamente mediante streaming.

### Ejemplo de ejecución

```text
Proveedor: openai
Modelo: gpt-4o-mini

Respuesta:

AI Engineering es una disciplina que combina...
```

## 8. Validación de parámetros con Pydantic

El proyecto utiliza `BaseModel` y `Field` de Pydantic para definir y validar la configuración del modelo.

Ejemplo:

```python
config = LLMConfig(
    provider="openai",
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=500,
    prompt="Explicá qué es AI Engineering."
)
```

**Reglas de validación:**

| Parámetro | Validación |
|---|---|
| `provider` | `openai` o `anthropic` |
| `temperature` | Número entre 0 y 2 |
| `max_tokens` | Entero entre 1 y 8192 |
| `prompt` | Texto no vacío |
| `model` | Identificador de modelo como texto |

La disponibilidad y compatibilidad de los parámetros también dependen de cada proveedor.

## 9. Streaming asíncrono

La clase `AsyncLLMManager` implementa un método `generate()` que utiliza programación asíncrona.

El método procesa los eventos recibidos desde las APIs y devuelve fragmentos de texto mediante `yield`.

Esto permite mostrar la respuesta mientras se genera, sin esperar a recibirla completamente.

La implementación utiliza:

- `async def`
- `await`
- `async for`
- `yield`

## 10. Manejo de errores

La aplicación incorpora manejo de excepciones para evitar que errores habituales provoquen un cierre inesperado.

**Errores contemplados:**

- Rate limiting.
- Créditos o cuota insuficientes en OpenAI.
- Errores de conexión.
- Errores generales de API.
- Errores inesperados.

Los errores capturados se devuelven como mensajes controlados mediante el generador asíncrono.

## 11. Pruebas y validaciones realizadas

Durante el desarrollo se realizaron las siguientes comprobaciones:

| Prueba | Resultado |
|---|---|
| Conexión con OpenAI (`gpt-4o-mini`) | Exitosa |
| Conexión con Anthropic (`claude-haiku-4-5-20251001`) | Exitosa |
| Generación mediante el método asíncrono | Exitosa |
| Recepción de respuestas mediante streaming | Exitosa |
| Configuración Pydantic válida | Aceptada |
| Temperatura fuera de rango (`5`) | Rechazada |
| `max_tokens` negativo (`-10`) | Rechazado |
| Captura de `RateLimitError` | Error controlado |
| Simulación de error de conexión | Pendiente |

### Ejecutar pruebas de validación

```powershell
python test_config.py
```

Este script comprueba una configuración válida y dos configuraciones incorrectas.

### Probar las APIs

```powershell
python main.py
```

Para probar el otro proveedor, modificar `LLM_PROVIDER` en `.env` y volver a ejecutar el programa.

**Nota:** las pruebas de integración requieren conexión a Internet y pueden consumir créditos de las APIs.

## 12. Seguridad y credenciales

Las API keys se almacenan localmente en el archivo `.env`, excluido del repositorio mediante `.gitignore`.

Cada usuario que descargue el proyecto deberá utilizar sus propias credenciales.

**Medidas de seguridad:**

- No almacenar API keys directamente en el código Python.
