"""Customer names, which are Unicode and arrive in every shape.

Names come from spreadsheets, web forms and old exports, so the same customer
can appear as ``'Müller GmbH'``, ``'Mu\u0308ller GmbH'`` (a decomposed umlaut)
or ``'  müller   gmbh '``. The helpers here make them comparable without
changing how they are displayed.
"""
import unicodedata


def normalise_name(name: str) -> str:
    """Canonical display form: NFC, single spaces, no outer whitespace.

    Case and accents are preserved; only invisible differences are removed.
    """
    if name is None:
        raise ValueError("customer name is missing")
    composed = unicodedata.normalize("NFC", str(name))
    return " ".join(composed.split())


def strip_accents(text: str) -> str:
    """Remove combining marks: 'Čapek' -> 'Capek', 'Müller' -> 'Muller'."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def sort_key(name: str) -> tuple:
    """Key for human-friendly ordering: accent- and case-insensitive first.

    The original normalised name is the tie-breaker, so the order is total and
    deterministic ('Capek' before 'Čapek').
    """
    display = normalise_name(name)
    return (strip_accents(display).casefold(), display)


def matches(name: str, query: str) -> bool:
    """True if ``query`` occurs in ``name``, ignoring case and accents."""
    haystack = strip_accents(normalise_name(name)).casefold()
    needle = strip_accents(normalise_name(query)).casefold()
    return needle in haystack


def initials(name: str) -> str:
    """Initials of the first two words, keeping accents: 'Élodie Durand' -> 'ÉD'."""
    words = [word for word in normalise_name(name).split(" ") if word[:1].isalpha()]
    return "".join(word[0].upper() for word in words[:2])


def _graphemes(text: str) -> list:
    """Split into user-perceived characters (base char plus combining marks)."""
    clusters = []
    for ch in text:
        if clusters and unicodedata.combining(ch):
            clusters[-1] += ch
        else:
            clusters.append(ch)
    return clusters


def display_name(name: str, width: int) -> str:
    """Fit ``name`` into ``width`` characters, ending with '…' if cut.

    Never splits a letter from its combining accent, and replaces newlines
    (which some exports contain) with spaces.
    """
    if width < 1:
        raise ValueError("width must be positive")
    clean = normalise_name(name.replace("\r", " ").replace("\n", " "))
    clusters = _graphemes(unicodedata.normalize("NFD", clean))
    if len(clusters) <= width:
        return clean
    kept = "".join(clusters[: width - 1])
    return unicodedata.normalize("NFC", kept) + "…"
