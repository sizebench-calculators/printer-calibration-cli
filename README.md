# printcal: 3D printer calibration calculator

A tiny, dependency-free Python CLI and library for the calibration math every 3D printer owner does on paper:

- **E-steps** from a marked-filament test, with the `M92` + `M500` G-code to send
- **Flow rate / extrusion multiplier** from a wall-thickness cube (works with % or Orca/Bambu ratios)
- **Volumetric flow** (mm³/s) and the max speed your hotend can melt
- **Magic layer heights**: multiples of a full Z motor step (0.04 mm on T8 lead screws)

> Prefer a UI? Use the free online versions on **[SizeBench 3D printing calculators](https://sizebench.com/3d-printing)** ([E-steps calculator](https://sizebench.com/e-steps-calculator), EN / PT / ES).

## Install
```bash
pip install git+https://github.com/sizebench-calculators/printer-calibration-cli
```

## CLI
```bash
printcal esteps --current 93 --remaining 23          # mark at 120 mm, extrude 100 mm
# Extruded: 97.0 mm (-3.0%)
# New E-steps: 95.88
# Send:
# M92 E95.88
# M500

printcal flow --current 100 --expected 0.9 --measured 0.95     # New flow: 94.7%
printcal volumetric --speed 150 --layer 0.2 --width 0.45       # 13.5 mm³/s, max 167 mm/s
printcal layers --lead 8 --nozzle 0.4 --target 0.21            # 0.08, 0.12 … 0.32; nearest 0.2
```

## Library
```python
from printcal import esteps, flow, volumetric, magic_layers
esteps(current=93, remaining=23)["new"]   # 95.88
```

## Formulas
| | Formula |
|---|---|
| E-steps | `new = current × requested ÷ (mark − remaining)` |
| Klipper | `new rotation_distance = old × extruded ÷ requested` |
| Flow | `new = current × expected wall ÷ measured wall` |
| Volumetric flow | `layer × line width × speed` (mm³/s) |
| Z full step | `lead ÷ (360° ÷ step angle)` |

## Contributing
Welcome: pressure advance / retraction helpers, Klipper output, translations, more tests. See [CONTRIBUTING.md](CONTRIBUTING.md). Run `pip install -e . pytest && pytest`.

## License
MIT © [SizeBench](https://sizebench.com)
