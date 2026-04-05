# RAG-Lovable: Retrieval-Augmented Generation with Gemini

Un sistema de Retrieval-Augmented Generation (RAG) diseñado para analizar reportes financieros en español. Extrae texto de documentos PDF, crea embeddings semánticos y utiliza un LLM para responder preguntas basadas en fragmentos relevantes del documento.

## 🎯 Características

- **Extracción de PDF**: Utiliza `pdfplumber` para extraer texto de documentos
- **Chunking inteligente**: Divide el texto en fragmentos superpuestos (900 caracteres, overlap 200)
- **Embeddings con Gemini**: Genera vectores semánticos usando Google's embedding model
- **Recuperación semántica**: Busca los fragmentos más relevantes usando similitud coseno
- **LLM Gemini 2.5 Flash**: Genera respuestas contextuales limitadas a 80 palabras
- **Almacenamiento en Supabase**: Persiste documentos y embeddings en base de datos vectorial

## 📋 Requisitos

- Python 3.8+
- Variables de entorno configuradas (.env):
  - `GEMINI_API_KEY`: API key de Google Generative AI
  - `SUPABASE_URL`: URL de tu proyecto Supabase
  - `SUPABASE_KEY`: API key de Supabase

## 🚀 Instalación

### Crear entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### Instalar dependencias
```bash
pip install langchain langchain-google-genai langchain-text-splitters langchain-core pdfplumber python-dotenv google-generativeai numpy supabase
```

## 📁 Estructura del Proyecto

```
RAG-Lovable/
├── data/
│   └── rag.pdf                    # Documento PDF para análisis
├── notebooks/
│   ├── RAG-Lovable-OpenAI.ipynb   # Notebook con OpenAI (referencia)
│   └── RAG-Lovable-Gemini.ipynb   # Notebook completo con Gemini
├── embeddings.py                   # Módulo de embeddings con Gemini
├── pdf_utils.py                    # Utilidades para extracción de PDF
├── ingest.py                       # Script para ingestar PDFs a Supabase
├── agente1.py                      # Agente RAG interactivo
├── retriever.py                    # Funciones de recuperación de chunks
├── supabase_client.py              # Cliente de Supabase
├── CLAUDE.md                       # Documentación para Claude Code
├── .env.example                    # Template de variables de entorno
└── README.md                       # Este archivo
```

## 🔧 Uso

### 1. Configurar variables de entorno

Copia `.env.example` a `.env` y completa tus credenciales:
```bash
cp .env.example .env
```

### 2. Ingestar un PDF a Supabase

```bash
python ingest.py
```

Esto extrae el texto, lo divide en chunks, genera embeddings y almacena todo en Supabase.

### 3. Usar el agente RAG interactivo

```bash
python agente1.py
```

Escribe tu pregunta y el sistema buscará la información relevante en los documentos.

### 4. Usar el notebook completo

Abre `notebooks/RAG-Lovable-Gemini.ipynb` en Jupyter para ver el flujo completo con visualizaciones.

## 📊 Arquitectura del Pipeline RAG

```
PDF → Extracción de Texto → Chunking (900 chars, overlap 200)
  ↓
Embedding (Gemini embedding-001) → Almacenamiento en Supabase
  ↓
Pregunta del Usuario → Embedding de la pregunta
  ↓
Búsqueda por Similitud Coseno (umbral = 0.7)
  ↓
Contexto Relevante → Gemini 2.5 Flash (Prompt + Contexto)
  ↓
Respuesta Generada
```

## 🔑 Parámetros Configurables

### En `embeddings.py`
- `task_type`: "retrieval_document" para búsqueda de documentos

### En `ingest.py`
- `chunk_size`: Tamaño de los fragmentos (por defecto: 900)
- `chunk_overlap`: Sobreposición entre fragmentos (por defecto: 200)

### En `agente1.py`
- `top_k`: Número de fragmentos a recuperar (por defecto: 6)
- `threshold`: Similitud mínima requerida (por defecto: 0.70)

### En el LLM (Gemini 2.5 Flash)
- `temperature`: 0.1 para respuestas deterministas
- Límite de respuesta: 80 palabras

## 📝 Variables de Entorno

```env
GEMINI_API_KEY=tu_gemini_api_key_aqui
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_supabase_key_aqui
```

## 🛠️ Desarrollo

### Modificar el prompt del LLM

En `agente1.py`, edita el contenido de `SystemMessage`:

```python
system_message = SystemMessage(
    content=(
        "Tu nuevo prompt aquí. "
        "Personaliza según tus necesidades."
    )
)
```

### Cambiar el modelo Gemini

En `embeddings.py`:
```python
# Para embeddings
model="models/gemini-embedding-001"

# Para LLM
model="gemini-2.5-flash"
```

## 📚 Documentación Adicional

- Ver `CLAUDE.md` para detalles técnicos completos
- Ver notebooks en `notebooks/` para ejemplos paso a paso

## 🚀 Deploy

El proyecto está diseñado para funcionar en:
- Máquinas locales (Windows, macOS, Linux)
- Plataformas de hosting (Render, Heroku, etc.)
- Contenedores Docker (ruta compatible con `os.path`)

## 🤝 Contribuciones

Las mejoras son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 👤 Autor

Sebastian Gamarra

## 🙏 Agradecimientos

- Google Generative AI (Gemini)
- LangChain
- Supabase
- pdfplumber
