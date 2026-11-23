#!/usr/bin/env python3
"""Download open battery datasets listed in README.md.

Usage:
    python download.py --list
    python download.py evbattery rwth_fleet
    python download.py --all

Standard library only (Python 3.8+). Files are saved to data/<key>/.
Datasets behind a login or request form are listed with manual steps.
"""

import argparse
import shutil
import sys
import urllib.parse
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
USER_AGENT = "Mozilla/5.0 (battery-datasets downloader)"

CALCE_BASE = "https://web.calce.umd.edu/batteries/data/"
CALCE_FILES = [
    # CS2: 1100 mAh prismatic LCO
    "CS2_3", "CS2_5", "CS2_6", "CS2_7", "CS2_8", "CS2_9", "CS2_21", "CS2_24",
    "CS2_25", "CS2_33", "CS2_34", "CS2_35", "CS2_36", "CS2_37", "CS2_38",
    # CX2: 1350 mAh LCO
    "CX2_3", "CX2_4", "CX2_8", "CX2_16", "CX2_31", "CX2_32", "CX2_33",
    "CX2_34", "CX2_35", "CX2_36", "CX2_37", "CX2_38",
]

# Each entry: name, region, files [(filename, url)] for direct download,
# or "manual" instructions when a script cannot fetch it.
DATASETS = {
    # ---------------- Direct download ----------------
    "evbattery": {
        "name": "EVBattery (464 EVs)",
        "region": "China",
        "files": [
            ("battery_dataset1.tar.gz", "https://ndownloader.figshare.com/files/41076449"),
            ("battery_dataset2.tar.gz", "https://ndownloader.figshare.com/files/41076506"),
            ("battery_dataset3.tar.gz", "https://ndownloader.figshare.com/files/41076458"),
        ],
    },
    "rwth_fleet": {
        "name": "BEVs in Commercial Fleets (RWTH Aachen)",
        "region": "Germany",
        "files": [
            ("Electric_Vehicle_and_Battery_Data.zip",
             "https://publications.rwth-aachen.de/record/979878/files/Electric_Vehicle_and_Battery_Data.zip"),
        ],
    },
    "nrel_failure": {
        "name": "NREL Battery Failure Databank",
        "region": "USA",
        "files": [
            ("battery-failure-databank-revision2-feb24.xlsx",
             "https://www.nlr.gov/media/docs/libraries/tsdc/battery-failure-databank-revision2-feb24.xlsx?sfvrsn=7b7f89_1"),
        ],
    },
    "nasa_pcoe": {
        "name": "NASA PCoE Battery Data Set",
        "region": "USA",
        "files": [
            ("5_Battery_Data_Set.zip",
             "https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip"),
        ],
    },
    "calce": {
        "name": "CALCE Battery Data (CS2 + CX2)",
        "region": "USA",
        "files": [(f"{n}.zip", f"{CALCE_BASE}{n}.zip") for n in CALCE_FILES],
    },
    # ---------------- Manual ----------------
    "korea_ev_fleet": {
        "name": "Field EV Fleet BMS Telemetry (21 Korean EVs)",
        "region": "Korea",
        "manual": "Log in to IEEE DataPort and download the zip: "
                  "https://ieee-dataport.org/documents/field-ev-fleet-bms-telemetry-dataset",
    },
    "nfa_ev_fire": {
        "name": "NFA EV Fire Statistics (소방청 전기차 화재 발생 현황)",
        "region": "Korea",
        "manual": "Open the page and click the CSV download button: "
                  "https://www.data.go.kr/data/15138615/fileData.do",
    },
    "rvd": {
        "name": "RVD: 300 mass-produced NEVs",
        "region": "China",
        "manual": "Log in to IEEE DataPort and download DPANet_RVD_data_zip: "
                  "https://ieee-dataport.org/documents/real-world-battery-dataset-comprising-operational-data-battery-packs-300-mass-produced",
    },
    "chengdu_bus": {
        "name": "Real EV dataset: Chengdu e-buses",
        "region": "China",
        "manual": "Click 'Download All' on Mendeley Data: "
                  "https://data.mendeley.com/datasets/j9ky68gnd3",
    },
    "severson": {
        "name": "MIT / Stanford / TRI (Severson et al., 2019)",
        "region": "USA",
        "manual": "Download the batch files from the web app: https://data.matr.io/1/ "
                  "(loading code: https://github.com/rdbraatz/data-driven-prediction-of-battery-cycle-life-before-capacity-degradation)",
    },
    "sandia": {
        "name": "Sandia Chemistry Comparison (Preger et al., 2020)",
        "region": "USA",
        "manual": "Search 'SNL' on https://www.batteryarchive.org/ and download the cells",
    },
    "nasa_randomized": {
        "name": "NASA Randomized Battery Usage (7 sets)",
        "region": "USA",
        "manual": "Download each set from data.nasa.gov, e.g. "
                  "https://data.nasa.gov/dataset/randomized-battery-usage-5-high-temperature-right-skewed-random-walk",
    },
    "sandia_arc": {
        "name": "Sandia Cell ARC Calorimetry Data",
        "region": "USA",
        "manual": "Download from https://www.sandia.gov/ess/tools-resources/rd-data-repository",
    },
    "kit_nmc": {
        "name": "KIT Comprehensive Battery Aging Dataset (228 NMC cells)",
        "region": "Germany",
        "manual": "Download the archive from RADAR4KIT: https://doi.org/10.35097/1969 "
                  "(log data: https://doi.org/10.35097/kww7jv8ajuvchcah)",
    },
    "stanford_m50t": {
        "name": "Stanford EV Driving-Profile Aging (LG M50T NMC)",
        "region": "USA",
        "manual": "Follow the data link in the article: https://doi.org/10.1016/j.dib.2022.107995",
    },
    "attia": {
        "name": "MIT / Stanford / TRI Fast-Charging Optimization (Attia 2020)",
        "region": "USA",
        "manual": "Download from the web app: https://data.matr.io/1/",
    },
    "lyon_lfp": {
        "name": "Lyon EV and Second-Life Aging (A123 LFP)",
        "region": "France",
        "manual": "Download from Recherche Data Gouv: https://doi.org/10.57745/OLBXKT",
    },
    "hust_lfp": {
        "name": "HUST Discharge-Protocol Dataset (77 LFP cells)",
        "region": "China",
        "manual": "Click 'Download All' on Mendeley Data: https://data.mendeley.com/datasets/nsc7hnsg4s",
    },
    "epri_bess": {
        "name": "EPRI BESS Failure Incident Database",
        "region": "USA",
        "manual": "View only, no export: "
                  "https://energystorage.epri.com/hub/public/en/failure-incident-database.html",
    },
    "ev_firesafe": {
        "name": "EV FireSafe Global EV Battery Fire Database",
        "region": "Australia",
        "manual": "Not public. Request access at hello@evfiresafe.com "
                  "(summary charts: https://www.evfiresafe.com/ev-battery-fire-data)",
    },
}


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def fetch(url, dest):
    """Stream url to dest with a simple progress line. Skips existing files."""
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  skip  {dest.name} (already downloaded)")
        return True
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp, open(tmp, "wb") as out:
            total = int(resp.headers.get("Content-Length") or 0)
            done = 0
            while True:
                chunk = resp.read(1 << 20)
                if not chunk:
                    break
                out.write(chunk)
                done += len(chunk)
                pct = f"{done / total:6.1%}" if total else ""
                print(f"\r  get   {dest.name}  {human(done)} {pct}", end="", flush=True)
        print()
        shutil.move(tmp, dest)
        return True
    except Exception as exc:  # network errors, 404, etc.
        print(f"\n  FAIL  {dest.name}: {exc}")
        if tmp.exists():
            tmp.unlink()
        return False


def download(key):
    ds = DATASETS[key]
    print(f"\n[{key}] {ds['name']} ({ds['region']})")
    if "manual" in ds:
        print(f"  manual: {ds['manual']}")
        return True
    target = DATA_DIR / key
    target.mkdir(parents=True, exist_ok=True)
    ok = True
    for filename, url in ds["files"]:
        ok &= fetch(url, target / filename)
    return ok


def list_datasets():
    print(f"{'key':<16} {'region':<10} {'how':<8} name")
    print("-" * 78)
    for key, ds in DATASETS.items():
        how = "manual" if "manual" in ds else f"auto({len(ds['files'])})"
        print(f"{key:<16} {ds['region']:<10} {how:<8} {ds['name']}")
    print("\nManual datasets:")
    for key, ds in DATASETS.items():
        if "manual" in ds:
            print(f"  {key}: {ds['manual']}")


def main():
    p = argparse.ArgumentParser(description="Download open battery datasets.")
    p.add_argument("keys", nargs="*", help="dataset keys (see --list)")
    p.add_argument("--list", action="store_true", help="list datasets")
    p.add_argument("--all", action="store_true", help="download every auto dataset")
    args = p.parse_args()

    if args.list or (not args.keys and not args.all):
        list_datasets()
        return 0

    keys = [k for k, d in DATASETS.items() if "files" in d] if args.all else args.keys
    unknown = [k for k in keys if k not in DATASETS]
    if unknown:
        print(f"Unknown key(s): {', '.join(unknown)}. Run --list.")
        return 1

    results = {k: download(k) for k in keys}
    failed = [k for k, ok in results.items() if not ok]
    print("\nDone." if not failed else f"\nFinished with errors: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
