# 🧠 LXePET / LYSO PET Simulation and CASToR Reconstruction Pipeline

This repository provides an automated workflow for simulating PET detector responses (LXe or LYSO) in **OpenGATE**, extracting coincidence events, and generating **CASToR-compatible list-mode datasets** for image reconstruction.

---

## 📁 Directory Overview

```
├── auto_run_radius_sim_lxe.sh        # Run LXe simulations at multiple source distances
├── auto_run_radius_sim.sh            # Run LYSO simulations at multiple source distances
├── pet_sim_philips_lxe.py            # OpenGATE LXe simulation (user-provided)
├── pet_sim_philips.py                # OpenGATE LYSO simulation (user-provided)
├── sim_to_coincidence.py             # Convert ROOT → coincidence CSV
├── coincidence_to_castor_data.py     # Convert CSV → CASToR list-mode (.cdf/.cdh)
├── massive_coincidence_to_castor_data.sh
│                                     # Batch-convert all CSVs into CASToR input
└── output_radius_plot/               # Default output directory for intermediate files
```

---

## 🚀 1. Simulation Stage

### Run LXe simulations

```bash
bash auto_run_radius_sim_lxe.sh
```

### Run LYSO simulations

```bash
bash auto_run_radius_sim.sh
```

Each script loops over source distances (0–15 cm) and calls:

```bash
python pet_sim_philips_lxe.py --source_dist <distance>
```

or

```bash
python pet_sim_philips.py --source_dist <distance>
```

Simulated ROOT files are written under:

```
output_radius_plot/
```

---

## ⚙️ 2. ROOT → Coincidence CSV

Convert simulated singles events into coincidence pairs:

```bash
python sim_to_coincidence.py \
  --pattern "*hot_point*.root" \
  --material LXe \
  --source_dist 5.0
```

**Outputs:**

```
output_radius_plot/coincidence_LXe_src5.0cm.csv
```

### Parameters

| Argument        | Description                               | Default          |
| --------------- | ----------------------------------------- | ---------------- |
| `--pattern`     | Glob pattern for input ROOT files         | `*derenzo*.root` |
| `--material`    | Detector material name                    | `LXe`            |
| `--source_dist` | Source distance from detector center (cm) | `0.0`            |

---

## 🧩 3. Coincidence CSV → CASToR Input

Convert a single CSV file into CASToR list-mode format:

```bash
python coincidence_to_castor_data.py \
  --config_option fine \
  --material LXe \
  --source_dist 5.0
```

**Outputs:**

```
/Users/yuema/MyCode/castor_v3.2/LXePET_Radius_Compare/
 ├── coincidence_LXe_src5.0cm_fine.cdf
 └── coincidence_LXe_src5.0cm_fine.cdh
```

### Key arguments

| Argument          | Description                                           | Default                                                 |
| ----------------- | ----------------------------------------------------- | ------------------------------------------------------- |
| `--config_option` | Virtual crystal LUT: `original`, `fine`, `super_fine` | `original`                                              |
| `--material`      | Detector material                                     | auto-parsed from filename                               |
| `--source_dist`   | Source distance (cm)                                  | auto-parsed from filename                               |
| `--input_dir`     | Input CSV folder                                      | `output_radius_plot/`                                   |
| `--output_dir`    | Output folder                                         | `/Users/yuema/MyCode/castor_v3.2/LXePET_Radius_Compare` |
| `--config_path`   | Path to LUT configuration files                       | see script default                                      |

---

## 🧮 4. Batch Conversion

To generate CASToR data for all configurations (3 × 2 × 16 = 96 combinations):

```bash
bash massive_coincidence_to_castor_data.sh
```

This loops over:

* Configurations: `original`, `fine`, `super_fine`
* Materials: `LYSO`, `LXe`
* Source distances: `0–15 cm`

---

## 🧱 5. Output Summary

| Stage        | Input                                     | Output                              | Description                      |
| ------------ | ----------------------------------------- | ----------------------------------- | -------------------------------- |
| Simulation   | OpenGATE geometry (`pet_sim_philips*.py`) | ROOT (`*.root`)                     | Event-level detector data        |
| Conversion 1 | ROOT                                      | `coincidence_<mat>_src<dist>cm.csv` | Paired coincidences              |
| Conversion 2 | CSV                                       | `.cdf` + `.cdh`                     | CASToR-compatible list-mode data |

---

## 🧰 Dependencies

| Package                            | Purpose                             |
| ---------------------------------- | ----------------------------------- |
| `Python ≥3.8`                      | Core language                       |
| `uproot`                           | ROOT → numpy + pandas I/O           |
| `numpy`, `pandas`, `scipy`, `tqdm` | Data processing & progress tracking |
| `OpenGATE`                         | PET Monte-Carlo simulation          |
| `CASToR ≥3.2`                      | Image reconstruction                |

Install Python dependencies:

```bash
pip install uproot pandas numpy scipy tqdm
```

---

## 📸 Example Workflow

```bash
# 1️⃣ Simulate LXe data at multiple source distances
./auto_run_radius_sim_lxe.sh

# 2️⃣ Extract coincidences from ROOT
python sim_to_coincidence.py --pattern "*LXe_src5.0*.root" --material "LXe"

# 3️⃣ Convert to CASToR list-mode format
python coincidence_to_castor_data.py --config_option "fine" --material "LXe" --source_dist 5.0

```

---

## 🧠 Notes

* Time coincidence window is **4.5 ns**.
* Minimum detector separation for valid coincidences is **20 mm**.
* LUT geometry and scanner model (e.g. `PET_PHILIPS_VEREOS_FINE`) are auto-set based on `config_option`.
* Adjust `input_dir` / `output_dir` paths in scripts as needed.
