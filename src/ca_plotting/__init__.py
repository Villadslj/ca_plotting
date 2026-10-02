"""Shared plotting style for team documents.

    import ca_plotting as cap
    fig, ax = cap.figure("full")
    ...
    cap.save(fig, "out/fig_dispersion")
"""
from .style import (
    PAGES,
    WIDTHS,
    RC,
    use,
    set_page,
    figure,
    save,
    textwidth,
)

__version__ = "0.2.0"
__all__ = ["PAGES", "WIDTHS", "RC", "use", "set_page", "figure", "save",
           "textwidth", "__version__"]
