"""End-to-end check that a clean Python environment can install and use the package.

Builds the project the same way ``pip install git+https://github.com/Villadslj/ca_plotting.git``
does (PEP 517 build of this source tree), installs it into a fresh virtualenv and
exercises the basic API from that environment.

Marked ``slow`` because it creates a virtualenv and downloads dependencies:
run with ``pytest -m slow`` (or ``pytest -m "not slow"`` to skip).
"""
import os
import re
import subprocess
import venv
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

SMOKE_SCRIPT = """
import matplotlib
matplotlib.use("Agg")
import importlib.metadata as md
from pathlib import Path
import sys

import ca_plotting as cap

assert cap.__version__ == md.version("ca_plotting"), "version metadata mismatch"

# Package data (bundled fonts) must survive installation.
fonts = Path(cap.style.__file__).parent / "fonts"
assert fonts.is_dir() and list(fonts.glob("*.ttf")), "bundled fonts missing"

cap.use()
assert matplotlib.rcParams["font.size"] == cap.RC["font.size"]

cap.set_page("a4")
fig, ax = cap.figure("full")
ax.plot([0, 1], [0, 1])
ax.set_xlabel("Time [s]")
out = cap.save(fig, str(Path(sys.argv[1]) / "fig_smoke"))
assert out.is_file() and out.stat().st_size > 0, "figure was not written"

print(cap.__version__)
"""


def _venv_python(env_dir: Path) -> Path:
    if os.name == "nt":
        return env_dir / "Scripts" / "python.exe"
    return env_dir / "bin" / "python"


def _run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


@pytest.mark.slow
def test_clean_install_from_source_tree(tmp_path):
    env_dir = tmp_path / "venv"
    venv.EnvBuilder(with_pip=True, clear=True).create(env_dir)
    python = _venv_python(env_dir)

    # Same code path as installing straight from the Git repository.
    _run([str(python), "-m", "pip", "install", "--no-input", str(REPO_ROOT)])

    # The package must not be importable from the source tree of this checkout.
    script = tmp_path / "smoke.py"
    script.write_text(SMOKE_SCRIPT)
    result = _run(
        [str(python), str(script), str(tmp_path)],
        cwd=str(tmp_path),
        env={**os.environ, "PYTHONPATH": "", "MPLBACKEND": "Agg"},
    )

    installed_version = result.stdout.strip().splitlines()[-1]
    version_src = (REPO_ROOT / "src" / "ca_plotting" / "_version.py").read_text()
    expected = re.search(r'__version__ = "([^"]+)"', version_src).group(1)
    assert installed_version == expected
