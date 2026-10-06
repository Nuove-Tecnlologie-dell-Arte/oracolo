"""Barra di avanzamento colorata, condivisa dai comandi lunghi (tag, embed,
ingest): rossa all'inizio, verde a fine corsa; tutto cio' che segue la barra
(conteggio, tempi, statistiche e la ")]" finale) e' invece dell'arancio usato
per l'indicatore del venv nel prompt della shell (#e0af68)."""

from tqdm import tqdm

_BAR_START = (255, 0, 0)
_BAR_END = (0, 200, 0)
_STATS_ANSI = "\033[38;2;224;175;104m"
_RESET_ANSI = "\033[0m"
# {bar} resta fuori (colorato a parte da tqdm via `colour=`); tutto il resto
# del formato di default (vedi tqdm.std.tqdm.format_meter) e' racchiuso tra
# i due codici ANSI sopra.
BAR_FORMAT = (
    "{desc}: {percentage:3.0f}%|{bar}| "
    + _STATS_ANSI
    + "{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]"
    + _RESET_ANSI
)


def _colour(fraction: float) -> str:
    r, g, b = (round(start + (end - start) * fraction) for start, end in zip(_BAR_START, _BAR_END))
    return f"#{r:02x}{g:02x}{b:02x}"


def new_bar(total: int, desc: str, unit: str = "it") -> tqdm:
    """Barra pronta all'uso: rossa a zero, formato gia' impostato."""
    return tqdm(total=total, desc=desc, unit=unit, colour=_colour(0), bar_format=BAR_FORMAT)


def advance(bar: tqdm, by: int = 1, **stats) -> None:
    """Avanza la barra di `by`, aggiorna il colore in base alla frazione
    completata e, se date, le statistiche a destra (nell'ordine passato:
    set_postfix(**kwargs) le ordinerebbe alfabeticamente, qui no)."""
    bar.update(by)
    if bar.total:
        bar.colour = _colour(bar.n / bar.total)
    if stats:
        bar.set_postfix_str(", ".join(f"{k}={v}" for k, v in stats.items()))
