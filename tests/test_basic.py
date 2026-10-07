"""Basic functionality tests for the installed/importable package."""
import importlib.metadata as importlib_metadata
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pytest  # noqa: E402

import ca_plotting as cap  # noqa: E402


def test_public_api_is_exported():
    for name in ("PAGES", "WIDTHS", "RC", "use", "set_page", "figure", "save",
                 "textwidth", "__version__"):
        assert hasattr(cap, name), f"missing public name {name}"


def test_version_matches_package_metadata():
    assert cap.__version__ == importlib_metadata.version("ca_plotting")


def test_fonts_are_packaged():
    font_dir = Path(cap.style.__file__).parent / "fonts"
    assert font_dir.is_dir()
    assert any(font_dir.glob("*.ttf"))


def test_use_applies_rcparams():
    cap.use()
    assert matplotlib.rcParams["font.size"] == cap.RC["font.size"]
    assert matplotlib.rcParams["savefig.dpi"] == cap.RC["savefig.dpi"]
    assert "DM Sans" in matplotlib.rcParams["font.sans-serif"]


def test_use_serif_font():
    cap.use("serif")
    assert matplotlib.rcParams["font.family"] == ["serif"]
    cap.use()


def test_use_rejects_unknown_font():
    with pytest.raises(ValueError):
        cap.use("comic-sans")


def test_use_accepts_overrides():
    cap.use(**{"lines.linewidth": 2.5})
    assert matplotlib.rcParams["lines.linewidth"] == 2.5
    cap.use()


def test_figure_sizes_follow_page_width():
    fig, ax = cap.figure("full")
    try:
        w, h = fig.get_size_inches()
        assert w == pytest.approx(cap.WIDTHS["full"])
        assert h == pytest.approx(w * 0.62)
        ax.plot([0, 1], [0, 1])
    finally:
        plt.close(fig)


def test_figure_accepts_explicit_width():
    fig, _ = cap.figure(3.0, aspect=0.5)
    try:
        assert tuple(fig.get_size_inches()) == pytest.approx((3.0, 1.5))
    finally:
        plt.close(fig)


def test_set_page_updates_widths():
    try:
        cap.set_page("letter")
        assert cap.textwidth() == pytest.approx(cap.PAGES["letter"])
        assert cap.WIDTHS["full"] == pytest.approx(cap.PAGES["letter"])

        cap.set_page(textwidth_in=5.0)
        assert cap.textwidth() == pytest.approx(5.0)
        assert cap.WIDTHS["half"] == pytest.approx(5.0 * 0.49)

        with pytest.raises(ValueError):
            cap.set_page("tabloid")
    finally:
        cap.set_page("a4")


def test_save_writes_png(tmp_path):
    fig, ax = cap.figure("half")
    try:
        ax.plot([0, 1], [1, 0])
        out = cap.save(fig, os.fspath(tmp_path / "sub" / "fig_test"))
    finally:
        plt.close(fig)
    assert out == tmp_path / "sub" / "fig_test.png"
    assert out.is_file() and out.stat().st_size > 0


def test_save_keeps_figure_size(tmp_path):
    fig, ax = cap.figure("full")
    try:
        ax.plot([0, 1], [0, 1])
        out = cap.save(fig, os.fspath(tmp_path / "sized"), dpi=100)
        expected = tuple(round(v * 100) for v in fig.get_size_inches())
    finally:
        plt.close(fig)
    from PIL import Image

    with Image.open(out) as img:
        assert img.size == pytest.approx(expected, abs=1)
