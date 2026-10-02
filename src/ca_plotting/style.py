from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager

_FONT_DIR = Path(__file__).parent / "fonts"

# Usable text width in inches for common page setups.
PAGES = {
    "a4": 6.27,       # A4, 2.54 cm margins
    "letter": 6.5,    # US Letter, 1 in margins
}

_FRACTIONS = {"full": 1.0, "twothirds": 0.66, "half": 0.49}
_textwidth = PAGES["a4"]
WIDTHS = {k: _textwidth * f for k, f in _FRACTIONS.items()}

FONTS = {
    "dmsans": {
        "font.family": "sans-serif",
        "font.sans-serif": ["DM Sans", "DejaVu Sans"],
        "mathtext.fontset": "custom",
        "mathtext.rm": "DM Sans",
        "mathtext.it": "DM Sans:italic",
        "mathtext.bf": "DM Sans:bold",
        "mathtext.fallback": "stix",   # Greek letters and symbols DM Sans lacks
    },
    "serif": {
        "font.family": "serif",
        "font.serif": ["STIX Two Text", "STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
    },
}

RC = {
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.linewidth": 0.6,
    "lines.linewidth": 1.0,
    "lines.markersize": 3.5,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.top": True,
    "ytick.right": True,
    "savefig.dpi": 300,
    "savefig.bbox": None,   # never "tight": it changes the final size
}

_applied = False
_fonts_registered = False


def _register_fonts():
    """Make the bundled fonts visible to matplotlib (no system install needed)."""
    global _fonts_registered
    if _fonts_registered:
        return
    for ttf in sorted(_FONT_DIR.glob("*.ttf")):
        font_manager.fontManager.addfont(str(ttf))
    _fonts_registered = True


def use(font="dmsans", **overrides):
    """Apply the team style. `font` is a FONTS key ('dmsans', 'serif').
    Extra rcParams may be passed as overrides."""
    global _applied
    _register_fonts()
    try:
        font_rc = FONTS[font]
    except KeyError:
        raise ValueError(f"unknown font {font!r}; choose from {sorted(FONTS)}")
    mpl.rcParams.update(RC)
    mpl.rcParams.update(font_rc)
    if overrides:
        mpl.rcParams.update(overrides)
    _applied = True


def set_page(page="a4", textwidth_in=None):
    """Select page preset ('a4', 'letter') or give a custom text width in inches."""
    global _textwidth
    if textwidth_in is not None:
        _textwidth = float(textwidth_in)
    else:
        try:
            _textwidth = PAGES[page.lower()]
        except KeyError:
            raise ValueError(f"unknown page {page!r}; choose from {sorted(PAGES)}")
    WIDTHS.clear()
    WIDTHS.update({k: _textwidth * f for k, f in _FRACTIONS.items()})


def textwidth():
    """Current text width in inches."""
    return _textwidth


def figure(width="full", aspect=0.62, **kw):
    """plt.subplots with a document-fixed size. `width` is a WIDTHS key or inches."""
    if not _applied:
        use()
    w = WIDTHS[width] if isinstance(width, str) else float(width)
    kw.setdefault("layout", "constrained")
    return plt.subplots(figsize=(w, w * aspect), **kw)


def save(fig, name, dpi=300):
    """Save as <name>.png at the exact figure size. Returns the path."""
    path = Path(name).with_suffix(".png")
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches=None)
    return path
