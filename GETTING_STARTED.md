# Build your first project in 10 minutes

**Goal:** create a numbered CAD panel, inspect its dimensions, and connect a layout to robot pick targets. This suggested time assumes Python is installed; setup and downloads may take longer.

## 0–2 minutes: get the files

Choose **Code → Download ZIP** on the repository page, extract it, and open a terminal in the directory containing `README.md` and `labs/`.

Alternatively, with Git installed:

```bash
git clone https://github.com/prapawitintun/How-to-buld-X-Almost-Anything.git
cd How-to-buld-X-Almost-Anything
python --version
```

Use Python 3.10 or later. On Windows, try `py` instead of `python`; on macOS/Linux, your command may be `python3`.

## 2–4 minutes: build a panel

```bash
python labs/01-panel-geometry/main.py --width 180 --height 120 --id P001
```

Open `outputs/panel.svg` in a browser or SVG viewer. It represents a **180 × 120 mm** rectangle labeled **P001**. Display size on your monitor is not a physical scale calibration.

## 4–6 minutes: change the design

```bash
python labs/01-panel-geometry/main.py --width 150 --height 100 --id P002
```

Reopen the SVG. Its dimensions and label change; the second run replaces the first output file.

## 6–8 minutes: compare production layouts

```bash
python labs/03-sheet-packing/main.py
```

On the supplied four-part case, original order uses **2 sheets at 45% utilization**, while height order uses **1 sheet at 90% utilization**. These synthetic rectangles omit cutting margins and kerf spacing.

## 8–10 minutes: connect to robotics

```bash
python labs/07-cad-to-robotics/main.py
python scripts/validate.py
```

Inspect `outputs/cad-to-robotics.json`: part identities and layout positions become reachable target coordinates for a two-link planar arm. Inverse kinematics is checked using forward kinematics. The example does not control a physical robot.

## Troubleshooting

| Message | What to check |
| --- | --- |
| Python is not recognized | Try `py` on Windows or `python3` on macOS/Linux; confirm Python is installed. |
| Cannot open a script | Run commands in the directory containing `labs/`. |
| Missing `catalog.json` | Download the complete repository rather than one script. |

Continue with the [seven labs](README.md#seven-working-starter-labs), [humanoid path](HUMANOID.md), or [contribution guide](CONTRIBUTING.md).
