import pet_helpers as p
import os
from pathlib import Path
import uproot
import numpy as np
import pandas as pd
import argparse

# ------------------------
# Parse command-line arguments
# ------------------------
parser = argparse.ArgumentParser(description="Find coincidences in PET ROOT files.")
parser.add_argument(
    "--pattern",
    type=str,
    default="*derenzo*.root",
    help="Glob pattern for ROOT files (e.g., '*hot_point*.root')."
)
parser.add_argument(
    "--material",
    type=str,
    default="LXe",
    help="Detector material name (e.g., LXe, LYSO, BGO)."
)
parser.add_argument(
    "--source_dist",
    type=float,
    default=0.0,
    help="Source distance to detector center in cm (e.g., 0.0, 25.0, 50.0)."
)
args = parser.parse_args()

# ------------------------
# Setup
# ------------------------
cwd = os.getcwd()
folder = Path(cwd) / 'output_radius_plot'
if not folder.is_dir():
    raise RuntimeError(f'ERROR: {folder} is not a folder.')
print(f"CWD: {cwd}")
print(f"Output folder: {folder}")
print(f"File pattern: {args.pattern}")
print(f"Material: {args.material}")
print(f"Source distance: {args.source_dist} mm")

# ------------------------
# Main loop
# ------------------------
for root_file in folder.glob(args.pattern):
    print(f"\n📂 Processing file: {root_file.name}")

    try:
        f = uproot.open(root_file)
        singles5 = f['Singles5']
        data = singles5.arrays()
    except Exception as e:
        print(f"❌ Failed to open {root_file.name}: {e}")
        continue

    global_time = np.array(data["GlobalTime"])
    x = np.array(data["PostPosition_X"])
    y = np.array(data["PostPosition_Y"])
    z = np.array(data["PostPosition_Z"])
    energy = np.array(data["TotalEnergyDeposit"])
    print(f"✅ Loaded {len(global_time):,} singles events")

    time_order = np.argsort(global_time)
    sorted_times = global_time[time_order]

    time_window = 4.5  # ns
    coincidences = {k: [] for k in [
        'globalPosX1', 'globalPosY1', 'globalPosZ1',
        'globalPosX2', 'globalPosY2', 'globalPosZ2',
        'time1', 'time2', 'energy1', 'energy2', 'distance'
    ]}
    processed = set()
    n_singles = len(sorted_times)
    print(f"Searching {n_singles:,} singles for coincidences...")

    for i in range(n_singles - 1):
        if i in processed:
            continue
        idx1 = time_order[i]
        time1 = sorted_times[i]
        j = i + 1
        while j < n_singles and (sorted_times[j] - time1) <= time_window:
            if j in processed:
                j += 1
                continue
            idx2 = time_order[j]
            dx, dy, dz = x[idx1] - x[idx2], y[idx1] - y[idx2], z[idx1] - z[idx2]
            distance = np.sqrt(dx**2 + dy**2 + dz**2)
            if distance > 20.0:
                for k, v in zip(
                    ['globalPosX1', 'globalPosY1', 'globalPosZ1', 'globalPosX2', 'globalPosY2', 'globalPosZ2',
                     'time1', 'time2', 'energy1', 'energy2', 'distance'],
                    [x[idx1], y[idx1], z[idx1], x[idx2], y[idx2], z[idx2],
                     global_time[idx1], global_time[idx2], energy[idx1], energy[idx2], distance]):
                    coincidences[k].append(v)
                processed.update({i, j})
                break
            j += 1

    coincidence_data = pd.DataFrame({k: np.array(v) for k, v in coincidences.items()})

    # Smart output name including material and source distance
    csv_name = f"coincidence_{args.material}_src{args.source_dist:.1f}cm.csv"
    csv_path = folder / csv_name
    coincidence_data.to_csv(csv_path, index=False)
    print(f"💾 Saved {len(coincidence_data)} coincidences to {csv_path}")
