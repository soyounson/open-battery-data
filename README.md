# Open Battery Datasets: Degradation & Thermal Runaway

A curated list of **open battery datasets**, and how to get them, for anyone working on battery degradation (SOH / capacity fade) or battery fire / thermal-runaway risk. EV field data gets particular attention.

This repository only collects sources and download tools. It contains no analysis or models.

Every value in the tables was checked against the dataset page or paper (November 2026).
`n/s` = **not stated** by the source. These cells were left blank on purpose rather than guessed.

---

## Quick summary

| Need | Best options |
|---|---|
| EV field data, large scale | EVBattery (464 EVs), RVD (300 EVs) |
| EV field data, Korea (NCM) | Field EV Fleet BMS Telemetry (21 E-GMP taxis) |
| EV field data with a fault / anomaly label | EVBattery (48 abnormal vehicles) |
| LFP cells | MIT/Stanford/TRI, Sandia, CALCE (A123, K2) |
| NCM / NMC cells or packs | Korea EV Fleet, Sandia |
| Cell-level thermal runaway (lab) | NREL Battery Failure Databank |
| Real fire incidents, Korea | NFA EV Fire Statistics (소방청) |

> **Key gap:** no open dataset links an EV's own telemetry to an actual fire event on that vehicle. Fire data and telemetry exist in separate datasets.

---

## Column guide

| Column | Meaning |
|---|---|
| Type | `Degradation`, `Thermal runaway` (lab abuse tests), or `Fire incident` (real-world events) |
| Application | `EV` (car / taxi / bus), `Cell` (lab cell, not in a vehicle), `ESS` (stationary storage) |
| Chemistry | Cathode chemistry: `LFP`, `NCM` (= NMC), `NCA`, `LCO`. `Mixed` = several, not separated by the source |
| Setting | `Lab` (test bench) or `Field` (real-world operation) |
| Amount | Number of vehicles, cells, tests or incidents |
| Max mileage | Largest per-vehicle distance reported (field EV data only) |
| Label | Ground-truth targets included (SOH, capacity, fault, cause, …) |
| Frequency | Sampling interval of the time series |
| Open | `Open` = direct download · `Login` = free account / subscription required · `Request` = data not public, contact owner · `View only` = browse online, no export |

---

## 🇰🇷 Korea

| Name | Type | Application | Chemistry | Setting | Amount | Duration | Max mileage | Label | Frequency | Size | Source | Open |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Field EV Fleet BMS Telemetry (Kookmin Univ., KOTSA, Hansnetwork) | Degradation (internal resistance) | EV (20 taxis + 1 test vehicle; Kia EV6, Hyundai Ioniq 5 / 6) | **NCM** (77.4 kWh pack) | Field | 21 vehicles | Aug 2024 – Jan 2026 | n/s | Vendor SOH (when available); lab-measured resistance for 1 vehicle (AAM15) | 1 s | 25.5 MB (zip, Parquet) | [IEEE DataPort](https://ieee-dataport.org/documents/field-ev-fleet-bms-telemetry-dataset) · DOI 10.21227/0v0g-gz47 | Login (CC BY 4.0) |
| NFA EV Fire Statistics (소방청 전기차 화재 발생 현황) | Fire incident | EV | Mixed (not recorded) | Field | n/s (one row per fire) | Annual updates (page updated 2026-02-12) | — | Ignition cause (major / minor), location, floor, above/below ground, vehicle state, ignition point | Per incident | Small CSV | [data.go.kr](https://www.data.go.kr/data/15138615/fileData.do) | Open (no usage restriction) |

## 🇺🇸 USA

| Name | Type | Application | Chemistry | Setting | Amount | Duration | Max mileage | Label | Frequency | Size | Source | Open |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NASA PCoE Battery Data Set | Degradation | Cell (18650) | n/s | Lab | n/s (18650 cells, e.g. B0005) | Run to end of life (30 % fade, 2 Ah → 1.4 Ah) | — | Capacity per cycle; impedance (Re, Rct) | ~10 Hz | n/s | [NASA PCoE repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/) | Open |
| NASA Randomized Battery Usage (7 sets) | Degradation | Cell (18650) | n/s | Lab | 4 cells per set | n/s | — | Reference charge/discharge cycles (SOH benchmark) | Load step every 1 min (set 5) | n/s | [data.nasa.gov](https://data.nasa.gov/dataset/randomized-battery-usage-5-high-temperature-right-skewed-random-walk) | Open (US Gov. work) |
| CALCE Battery Data (Univ. of Maryland) | Degradation | Cell (prismatic, pouch, cylindrical) | **LCO** (CS2, CX2, PL, PLN) · **LFP** (A123, K2) | Lab | CS2: 15 · CX2: 12 · PL: 16 · A123: 3 · K2: 2 · PLN storage test | n/s | — | Capacity, impedance | n/s | xlsx / txt in zips | [CALCE](https://web.calce.umd.edu/batteries/data/) | Open (citation required) |
| MIT / Stanford / TRI (Severson et al., 2019) | Degradation | Cell (A123 APR18650M1A) | **LFP** | Lab | 124 cells | n/s | — | Cycle life, capacity per cycle | n/s | n/s | [data.matr.io/1](https://data.matr.io/1/) | Open (see site) |
| Sandia Chemistry Comparison (Preger et al., 2020) | Degradation | Cell (18650) | **LFP · NCA · NCM** | Lab | 61 cells | Multi-year | — | Capacity to 80 % | n/s | n/s | [batteryarchive.org](https://www.batteryarchive.org/) | Open |
| NREL Battery Failure Databank | Thermal runaway | Cell (18650, 21700, D-cell) | n/s (various commercial cells) | Lab (abuse tests) | ~300 tests | Spreadsheet updated Feb 2024 | — | Heat output, heat split (body / vents), mass ejected, trigger type (nail, heat, internal short), X-ray video links | Per test | Single xlsx | [NREL / NLR](https://www.nlr.gov/transportation/battery-failure) | Open |
| Sandia Cell ARC Calorimetry Data | Thermal runaway | Cell | n/s | Lab (ARC) | n/s | n/s | — | Self-heating / thermal-runaway onset | n/s | n/s | [Sandia R&D Data Repository](https://www.sandia.gov/ess/tools-resources/rd-data-repository) | Open |
| EPRI BESS Failure Incident Database | Fire incident | ESS (not EV) | Mixed (incl. LFP) | Field | 150 incidents (2018 – 2025) | Tracked since 2011 | — | Root cause (where known), system info | Per incident | Web table | [EPRI Energy Storage Hub](https://energystorage.epri.com/hub/public/en/failure-incident-database.html) | View only |

## 🇨🇳 China

| Name | Type | Application | Chemistry | Setting | Amount | Duration | Max mileage | Label | Frequency | Size | Source | Open |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EVBattery (Tsinghua, Beihang, Peking Univ.) | Degradation + anomaly (fault) | EV | n/s | Field (charging) | 464 vehicles, 3 makers (217 / 198 / 49); ~1.28 M charging snippets | "Several years" | n/s | Capacity (~586 k snippets); abnormal-vehicle label (48 vehicles) | 128 points per snippet (interval n/s) | 1.41 GB (3 × tar.gz) | [figshare](https://doi.org/10.6084/m9.figshare.23301881) · [paper](https://arxiv.org/abs/2201.12358) | Open (CC BY 4.0 on figshare; paper says CC BY-NC-SA, so check before commercial use) |
| RVD: 300 mass-produced NEVs (Huang et al.) | Degradation | EV | n/s | Field | 300 vehicles, 104,621 cycles | n/s | n/s (fleet total > 30 M km) | SOH per cycle | n/s | 182 MB (xlsx) | [IEEE DataPort](https://ieee-dataport.org/documents/real-world-battery-dataset-comprising-operational-data-battery-packs-300-mass-produced) · DOI 10.21227/jyrv-2179 | Login (CC BY 4.0) |
| Real EV dataset: Chengdu e-buses (Fei) | Degradation | EV (bus) | n/s | Field | 5 buses | n/s | n/s | n/s | 10 s (CAN) | n/s | [Mendeley Data](https://data.mendeley.com/datasets/j9ky68gnd3) | Open (CC BY 4.0) |

## 🇩🇪 Germany

| Name | Type | Application | Chemistry | Setting | Amount | Duration | Max mileage | Label | Frequency | Size | Source | Open |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BEVs in Commercial Fleets (RWTH Aachen) | Degradation | EV (geriatric-care fleet) | n/s | Field | 9 vehicles | 2014 – 2016 | 9,062 – 15,308 km per vehicle per year | Capacity from periodic dynamometer tests (3.1 – 13 % fade) | n/s | 82 MB (zip) | [RWTH Publications](https://publications.rwth-aachen.de/record/979878/) · DOI 10.18154/RWTH-2024-01907 | Open (CC BY 4.0) |

## 🇦🇺 Australia / Global

| Name | Type | Application | Chemistry | Setting | Amount | Duration | Max mileage | Label | Frequency | Size | Source | Open |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV FireSafe Global EV Battery Fire Database | Fire incident | EV | Mixed | Field | 1,072 incidents studied | 2010 – present (updated ≥ every 6 months) | — | Cause category, charging state, delayed / secondary thermal runaway | Per incident | — (charts only) | [EV FireSafe](https://www.evfiresafe.com/ev-battery-fire-data) | Request (database not public; for-profit use needs permission) |

---

## Download

```bash
python download.py --list                 # show every dataset and how it can be downloaded
python download.py evbattery rwth_fleet   # download specific datasets
python download.py --all                  # download everything that has a direct link
```

- Files go to `data/<dataset>/`. The `data/` folder is git-ignored.
- Python 3.8+ and the standard library only. No packages to install.
- Datasets marked **Login / Request / View only** can't be downloaded by script. `--list` prints the page to open and what to do.
- Already-downloaded files are skipped, so re-running is safe.

| Script key | Dataset | Auto download |
|---|---|---|
| `evbattery` | EVBattery | ✅ ~1.4 GB |
| `rwth_fleet` | RWTH commercial fleet | ✅ 82 MB |
| `nrel_failure` | NREL Battery Failure Databank | ✅ xlsx |
| `nasa_pcoe` | NASA PCoE Battery Data Set | ✅ zip |
| `calce` | CALCE CS2 + CX2 | ✅ 27 zips |
| `korea_ev_fleet` | Field EV Fleet BMS Telemetry | ❌ IEEE DataPort login |
| `rvd` | RVD 300 vehicles | ❌ IEEE DataPort login |
| `nfa_ev_fire` | NFA EV Fire Statistics | ❌ data.go.kr download button |
| `chengdu_bus` | Chengdu e-buses | ❌ Mendeley "Download All" |
| `severson` | MIT / Stanford / TRI | ❌ data.matr.io web app |
| `sandia` | Sandia chemistry comparison | ❌ batteryarchive.org |
| `nasa_randomized` | NASA Randomized Usage | ❌ data.nasa.gov pages |
| `sandia_arc` | Sandia ARC calorimetry | ❌ Sandia repository page |
| `epri_bess` | EPRI BESS incidents | ❌ view only |
| `ev_firesafe` | EV FireSafe | ❌ email request |

---

## Notes

- Check each dataset's license before you publish results or use it commercially. Several datasets ask you to cite specific papers (CALCE asks for at least three).
- Chemistry is `n/s` where the dataset page and paper don't name it. Don't infer it from the region or vehicle type. Check the data or contact the authors.
- NREL's battery pages now live at `nlr.gov`. The script uses that address.
- Duration and sampling interval for EVBattery, RVD and Severson are not in the source text. Fill them in after opening the data.

## Contributing

Know an open battery dataset that's missing, or a value marked `n/s` that you can confirm? Open an issue or pull request with the source link.
