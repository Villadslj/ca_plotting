# ca_plotting

Shared matplotlib style for figures in our Google Docs reports.

## Install

```bash
pip install git+https://github.com/Villadslj/ca_plotting.git
# or a fixed version:
pip install git+https://github.com/Villadslj/ca_plotting.git@v0.1.0
```

To update an existing install to the newest commit on `main`:

```bash
pip install --upgrade --force-reinstall git+https://github.com/Villadslj/ca_plotting.git
```

The package version lives in `src/ca_plotting/_version.py` and is read by
`pyproject.toml`, so bumping it there is enough for `pip install --upgrade` to
pick up a new release.

For development: clone the repo and run `pip install -e ".[test]"`.

## Tests

```bash
pytest                 # everything
pytest -m "not slow"   # skip the clean-virtualenv install check
```

`tests/test_clean_install.py` builds the project, installs it into a fresh
virtualenv and verifies that a clean Python can import `ca_plotting`, find the
bundled fonts and create and save a figure.

## Use

```python
import ca_plotting as cap

fig, ax = cap.figure("full")          # "full", "twothirds", "half", or inches
ax.plot(x, y)
ax.set_xlabel("Time [s]")
cap.save(fig, "figures/fig_dose")     # -> figures/fig_dose.png, 300 dpi
```

Use `cap.set_page("letter")` for US Letter (default is A4 with 2.54 cm margins).

## Google Docs

Set the image to "In line with text", then enter the width under
Image options -> Size & rotation (full width on A4 = 15.9 cm). Never drag the corners.

## Rules

- Don't set `fontsize=` by hand.
- Don't use `bbox_inches="tight"`.
