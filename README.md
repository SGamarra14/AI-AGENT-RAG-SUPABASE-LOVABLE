# RAG-Lovable

Sistema de Retrieval-Augmented Generation (RAG) para análisis de reportes financieros en español.

## Arquitectura

```
PDF → Chunking → Embeddings (Gemini embedding-001) → Supabase (BD vectorial)
                                                            ↓
Usuario → Frontend (Lovable) → Render (Web Service RAG API)
                                        ↓
                        Recuperación por similitud coseno
                                        ↓
                        Gemini 2.5 Flash → Respuesta
```

| Capa | Tecnología | Rol |
|------|-----------|-----|
| Frontend | [Lovable](https://chatflow-buddy-83.lovable.app/) | Interfaz de chat |
| Web Service | Render | Expone la API RAG (`/chat`, `/health`) |
| BD Vectorial | Supabase | Almacena chunks y embeddings |
| Embeddings | Gemini embedding-001 | Vectorización de documentos y preguntas |
| LLM | Gemini 2.5 Flash | Generación de respuestas contextuales |

## Estructura

```
├── app.py              # FastAPI — endpoints /chat y /health (desplegado en Render)
├── retriever.py        # Búsqueda por similitud coseno en Supabase
├── embeddings.py       # Generación de embeddings con Gemini
├── supabase_client.py  # Conexión a Supabase
├── requirements.txt
├── runtime.txt
└── local/              # Archivos de desarrollo (no se despliegan)
    ├── agente.py       # Agente RAG interactivo (CLI)
    ├── ingest.py       # Ingesta de PDFs a Supabase
    ├── pdf_utils.py    # Extracción y chunking de PDFs
    ├── data/           # Documentos PDF fuente
    └── notebooks/      # Notebooks de exploración
```

## Variables de entorno

```env
GEMINI_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
```
