"""Il "contesto" dell'Oracolo: un testo markdown caricato da /inserisci.html
che non diventa una stella ne' una citazione, ma viene aggiunto a ogni
prompt mandato a Ollama (vedi `oracle.py`), come istruzione sempre valida.

E' un unico file, non versionato (sta in `data/` come il DB locale):
caricarne uno nuovo sostituisce quello precedente.
"""

from pathlib import Path

from backend import config


def _path() -> Path:
    return Path(config.CONTEXT_PATH)


def read() -> str:
    """Il contesto attuale, o stringa vuota se non e' stato impostato."""
    path = _path()
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").strip()


def write(text: str) -> None:
    """Imposta il contesto; con testo vuoto lo rimuove."""
    path = _path()
    text = text.strip()
    if not text:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
