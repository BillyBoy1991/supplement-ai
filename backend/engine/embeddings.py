"""
Embeddings locales con fastembed (all-MiniLM-L6-v2 sobre ONNX Runtime, 384 dims).

fastembed evita arrastrar torch (~2.7 GB): ONNX Runtime ocupa ~50 MB, clave en
el VPS. El modelo se descarga de HuggingFace (~90 MB) la primera vez y queda
cacheado. La carga es un singleton perezoso: importar este módulo no descarga
nada (los tests corren sin red); el coste se paga en la primera llamada real.
"""
import logging

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

_model = None


def _get_model():
    global _model
    if _model is None:
        # Import aquí y no arriba: evita cargar ONNX Runtime al importar el módulo.
        from fastembed import TextEmbedding
        _model = TextEmbedding(EMBEDDING_MODEL)
    return _model


def get_embedding(text: str) -> list[float]:
    """Devuelve el embedding del texto. Cualquier fallo se relanza: el caller decide."""
    try:
        return next(_get_model().embed([text])).tolist()
    except Exception as exc:
        logger.warning("Fallo al generar embedding: %s", exc)
        raise
