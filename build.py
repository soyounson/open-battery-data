#!/usr/bin/env python3
"""Build README.md and assets/datasets.js from datasets.csv.

datasets.csv is the single source of truth. Edit it, then run:
    python build.py
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = "https://soyounson.github.io/open-battery-data/"

CATEGORIES = [
    ("ev_field", "🚗 EV field data",
     "Battery signals recorded in real vehicles."),
    ("lab_cell", "🔬 Lab cell data",
     "Single cells tested on a bench: cycled to end of life, or abused until thermal runaway. Not from vehicles."),
    ("ev_fire", "🔥 EV fire incidents",
     "Real-world EV fire records, one row per incident. No battery signals."),
    ("ess_fire", "⚡ ESS fire incidents",
     "Failures of stationary energy storage systems. Not EV, but the closest open record of large-pack fires."),
]
SIGNAL_CATS = {"ev_field", "lab_cell"}

ACCESS_ICON = {"Open": "🟢 Open", "Login": "🟡 Login", "Request": "🔴 Request", "View only": "🔴 View only"}
FLAG = {"Korea": "🇰🇷", "USA": "🇺🇸", "China": "🇨🇳", "Germany": "🇩🇪", "Australia": "🇦🇺", "France": "🇫🇷"}


def load():
    with open(ROOT / "datasets.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cell(s):
    return (s or "n/s").replace("|", "\\|")


def country(r):
    c = r["country"]
    return f"{FLAG[c]} {c}" if c in FLAG else "❔ n/s"


def acq(r):
    a, f = r["acquisition"], r["frequency"]
    if f.startswith("Per "):
        return cell(a)
    return f"{cell(a)}<br>**{cell(f)}**"


CHG_ICON = {"Slow": "🐢 Slow", "Fast": "🚀 Fast", "Mixed": "🔀 Mixed", "n/s": "n/s", "n/a": "—"}


def chg(r):
    label = CHG_ICON.get(r["charging"], r["charging"])
    rate = r["charge_rate"]
    return f"**{label}**" + (f"<br>{cell(rate)}" if rate and rate not in ("—", "n/s") else "")


def overview_table(key, rows):
    if key in SIGNAL_CATS:
        out = ["| Dataset | Access | Country | Signals | Acquisition · interval | Charging · C-rate | Chemistry | Scale |",
               "|---|---|---|---|---|---|---|---|"]
        for r in rows:
            out.append(
                f"| **[{cell(r['name'])}](#{r['key']})** [🌏]({PAGES}#{r['key']}) "
                f"| {ACCESS_ICON.get(r['access'], r['access'])} | {country(r)} | {cell(r['signals'])} "
                f"| {acq(r)} | {chg(r)} | {cell(r['chemistry'])} | {cell(r['amount'])} |")
    else:
        out = ["| Dataset | Access | Country | What you get | Records from | Scale |",
               "|---|---|---|---|---|---|"]
        for r in rows:
            out.append(
                f"| **[{cell(r['name'])}](#{r['key']})** [🌏]({PAGES}#{r['key']}) "
                f"| {ACCESS_ICON.get(r['access'], r['access'])} | {country(r)} | {cell(r['signals'])} "
                f"| {cell(r['acquisition'])} | {cell(r['amount'])} |")
    return "\n".join(out)


def details(r):
    fields = [
        ("Access", ACCESS_ICON.get(r["access"], r["access"])), ("License", r["license"]),
        ("Type", r["type"]), ("Application", r["application"]), ("Chemistry", r["chemistry"]),
        ("Setting", r["setting"]), ("Amount", r["amount"]), ("Duration", r["duration"]),
        ("Max mileage", r["max_mileage"]), ("Signals", r["signals"]),
        ("Acquisition", r["acquisition"]), ("Interval", r["frequency"]),
        ("Charging", CHG_ICON.get(r["charging"], r["charging"]) if r["charging"] != "n/a" else ""),
        ("Charge rate", r["charge_rate"]), ("Label", r["label"]),
        ("Size", r["size"]), ("Country", country(r)),
        ("Location on map", f"{r['site']} ({r['location_basis'].lower()})"),
    ]
    if r["doi"]:
        fields.append(("DOI", r["doi"]))
    fields.append(("Source", f"[{r['source_name']}]({r['source_url']})"))
    fields.append(("Download", f"`python download.py {r['key']}`" if r["auto_download"] == "yes"
                   else "Manual (see source)"))
    body = "\n".join(f"| {k} | {cell(v)} |" for k, v in fields if v and v != "—")
    return (f'<a name="{r["key"]}"></a>\n<details>\n<summary><b>{r["name"]}</b> · '
            f'{ACCESS_ICON.get(r["access"], r["access"])} · {r["type"]}</summary>\n\n'
            f"| | |\n|---|---|\n{body}\n\n</details>")


def readme(rows):
    n = {c: sum(r["category"] == c for r in rows) for c, _, _ in CATEGORIES}
    parts = [f"""# Open Battery Data

**{len(rows)} open battery datasets** for degradation (SOH / capacity fade), thermal runaway and fire risk, with how to get each one.
This repository only collects sources and download tools. It contains no analysis or models.

<p align="center">
  <a href="{PAGES}"><img src="assets/map-preview.png" alt="Map of open battery datasets" width="100%"></a>
  <br><b><a href="{PAGES}">🌏 Open the interactive map →</a></b>
</p>

| 🚗 EV field | 🔬 Lab cell | 🔥 EV fire | ⚡ ESS fire |
|:---:|:---:|:---:|:---:|
| **{n['ev_field']}** | **{n['lab_cell']}** | **{n['ev_fire']}** | **{n['ess_fire']}** |

**Access** 🟢 Open: direct download · 🟡 Login: free account or subscription · 🔴 Request / View only: not downloadable

**Charging** 🐢 Slow: AC charging or ≤ 1C · 🚀 Fast: DC fast charging or > 1C · 🔀 Mixed: both in one dataset. No dataset labels charges as fast or slow itself; this is our classification from the stated currents.

**Signals** `V` voltage · `I` current · `T` temperature · `SOC` state of charge · `SOH` state of health · `R` internal resistance

> **Key gap:** no open dataset links an EV's own telemetry to an actual fire on that vehicle. Telemetry and fire records exist only in separate datasets.

`n/s` = **not stated by the source**, left blank on purpose rather than guessed. Values were checked against each dataset's page or paper (November 2026). Tap a dataset name for full details, or 🌏 to see it on the map.
"""]
    for key, title, desc in CATEGORIES:
        group = [r for r in rows if r["category"] == key]
        parts.append(f"## {title}\n\n{desc}\n\n{overview_table(key, group)}\n\n" +
                     "\n\n".join(details(r) for r in group))
    auto = [r for r in rows if r["auto_download"] == "yes"]
    parts.append(f"""## Download

```bash
python download.py --list                 # every dataset and how to get it
python download.py evbattery rwth_fleet   # specific datasets
python download.py --all                  # everything with a direct link ({len(auto)} datasets)
```

- Files go to `data/<dataset>/` (git-ignored). Python 3.8+, standard library only.
- 🟡 and 🔴 datasets can't be fetched by script; `--list` prints the page to open.
- Already-downloaded files are skipped, so re-running is safe.

## Notes

- **Chemistry:** `LFP` lithium iron phosphate · `NCM` (= NMC) nickel cobalt manganese · `NCA` nickel cobalt aluminium · `LCO` lithium cobalt oxide · `Mixed` several, not separated. Chemistry is taken from the dataset page or its paper; where neither states it, an inference is marked \"inferred\" with the reason, otherwise it stays `n/s`.
- **Map location:** EV field data is placed where it was collected when the source says so; otherwise, and for lab data, at the publishing institution. Datasets with no stated location appear under "Location not stated".
- **Licenses:** check each one before publishing results or using data commercially. Several datasets ask you to cite specific papers (CALCE asks for at least three).
- NREL's battery pages now live at `nlr.gov`; the script uses that address.

## Contributing

Know a missing dataset, or can you confirm an `n/s` value? Edit `datasets.csv`, run `python build.py`, and open a pull request with the source link.

| File | Purpose |
|---|---|
| `datasets.csv` | Single source of truth for every dataset |
| `build.py` | Regenerates `README.md` and `assets/datasets.js` |
| `index.html` | Interactive globe and tables (GitHub Pages) |
| `download.py` | Downloads datasets that have direct links |

## License

Code is MIT and the catalog text is CC BY 4.0 (see [LICENSE](LICENSE)). Each dataset keeps its own license, shown in its entry above.
""")
    return "\n\n".join(parts)


def main():
    rows = load()
    (ROOT / "README.md").write_text(readme(rows), encoding="utf-8")
    (ROOT / "assets" / "datasets.js").write_text(
        "// Generated by build.py from datasets.csv. Do not edit by hand.\nwindow.DATASETS = "
        + json.dumps(rows, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print(f"Built README.md and assets/datasets.js ({len(rows)} datasets)")


if __name__ == "__main__":
    main()
