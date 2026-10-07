"""Shared plotting style for team documents.

    import ca_plotting as cap
    fig, ax = cap.figure("full")
    ...
    cap.save(fig, "out/fig_dispersion")
"""
from ._version import __version__
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

__all__ = ["PAGES", "WIDTHS", "RC", "use", "set_page", "figure", "save",
           "textwidth", "__version__"]
