# ca_plotting

Shared matplotlib style for figures in our Google Docs reports.

## Install

```bash
pip install git+https://github.com/Villadslj/ca_plotting.git
# or a fixed version:
pip install git+https://github.com/Villadslj/ca_plotting.git@v0.1.0
```

For development: clone the repo and run `pip install -e .`.

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
