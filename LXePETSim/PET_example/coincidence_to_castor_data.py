#!/usr/bin/env python3
"""
Convert a single coincidence CSV file into a CASToR-compatible list-mode dataset (.cdf/.cdh).
Automatically detects material and source distance from filename.
"""

import os
import re
import glob
import struct
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy.spatial import cKDTree


# ==============================================
# 1. Command-line argument parsing
# ==============================================
def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a single coincidence CSV into CASToR list-mode input."
    )
    parser.add_argument("--config_option", type=str, default="original",
                        choices=["original", "fine", "super_fine"],
                        help="Which LUT configuration to use.")
    parser.add_argument("--material", type=str, default=None,
                        help="Material name (e.g. LYSO, LXe). If not provided, parsed from file name.")
    parser.add_argument("--source_dist", type=float, default=None,
                        help="Source distance (in cm). If not provided, parsed from file name.")
    parser.add_argument("--input_dir", type=str, default="/Users/yuema/MyCode/LXePETSim/LXePETSim/PET_example/output_radius_plot",
                        help="Directory containing input CSV coincidence files.")
    parser.add_argument("--output_dir", type=str, default="/Users/yuema/MyCode/castor_v3.2/LXePET_Radius_Compare",
                        help="Directory to save .cdf/.cdh files.")
    parser.add_argument("--config_path", type=str, default="/Users/yuema/MyCode/LXePETSim/LXePETSim/castor_reconstruction/castor_configs",
                        help="Path to the LUT configuration files.")
    return parser.parse_args()


# ==============================================
# 2. Header writer
# ==============================================
def write_simple_text_cdh(output_path, data_file_name, num_events, config_name):
    """Write CASToR header file (.cdh)."""
    with open(output_path, "w") as f:
        f.write(f"Data filename: {data_file_name}\n")
        f.write(f"Number of events: {num_events}\n")
        f.write("Data mode: list-mode\n")
        f.write("Data type: PET\n")
        f.write("Start time (s): 0\n")
        f.write("Duration (s): 10\n")

        if "super_fine" in config_name:
            f.write("Scanner name: PET_PHILIPS_VEREOS_SUPER_FINE\n")
        elif "fine" in config_name:
            f.write("Scanner name: PET_PHILIPS_VEREOS_FINE\n")
        elif config_name == "philips_vereos_virtual_crystals":
            f.write("Scanner name: PET_PHILIPS_VEREOS\n")
        else:
            raise ValueError("Unavailable config name")

        f.write("Calibration factor: 1.0\n")
        f.write("Isotope: F-18\n")
        f.write("TOF information flag: 0\n")
        f.write("Attenuation correction flag: 0\n")
        f.write("Normalization correction flag: 0\n")
        f.write("Scatter correction flag: 0\n")
        f.write("Random correction flag: 0\n")
        f.write("Maximum number of lines per event: 1\n")

    print(f"[CDH] Wrote header to: {output_path}")


# ==============================================
# 3. Main function
# ==============================================
def main():
    args = parse_args()

    # Map config option to file names
    OPTION_NAME_MAP = {
        "original": "philips_vereos_virtual_crystals",
        "fine": "philips_vereos_virtual_crystals_fine",
        "super_fine": "philips_vereos_virtual_crystals_super_fine",
    }
    config_name = OPTION_NAME_MAP[args.config_option]

    config_lut = os.path.join(args.config_path, f"{config_name}_binary.lut")

    # ==============================================
    # Find the single matching input file
    # ==============================================
    if args.material and args.source_dist is not None:
        pattern = f"coincidence_{args.material}_src{args.source_dist:.1f}cm.csv"
    else:
        pattern = "coincidence_*.csv"

    candidates = sorted(glob.glob(os.path.join(args.input_dir, pattern)))
    if len(candidates) == 0:
        raise FileNotFoundError(f"No files found matching pattern '{pattern}' in {args.input_dir}")
    elif len(candidates) > 1:
        raise RuntimeError(f"Expected exactly one input file, but found {len(candidates)}:\n" +
                           "\n".join(os.path.basename(f) for f in candidates))

    csv_path = candidates[0]
    basename = os.path.basename(csv_path)
    print(f"[INFO] Using input file: {basename}")

    # ==============================================
    # Parse material and source distance
    # ==============================================
    match = re.match(r"coincidence_([A-Za-z0-9]+)_src([0-9\.]+)cm\.csv", basename)
    if not match:
        raise ValueError(f"Filename does not follow pattern 'coincidence_<material>_src<dist>cm.csv': {basename}")

    material, src_dist_str = match.groups()
    src_dist = float(src_dist_str)

    # Allow override by user arguments
    if args.material:
        material = args.material
    if args.source_dist is not None:
        src_dist = args.source_dist

    print(f"[INFO] Material: {material}")
    print(f"[INFO] Source distance: {src_dist:.1f} cm")

    # ==============================================
    # Load LUT configuration
    # ==============================================
    lut_data = np.fromfile(config_lut, dtype=np.float32).reshape((-1, 6))
    lut_df = pd.DataFrame(lut_data, columns=["x", "y", "z", "vx", "vy", "vz"])
    tree = cKDTree(lut_df[["x", "y", "z"]].values)

    os.makedirs(args.output_dir, exist_ok=True)

    # ==============================================
    # Process the single coincidence file
    # ==============================================
    coinc_data = pd.read_csv(csv_path)
    positions1 = coinc_data[["globalPosX1", "globalPosY1", "globalPosZ1"]].values
    positions2 = coinc_data[["globalPosX2", "globalPosY2", "globalPosZ2"]].values

    _, idx1 = tree.query(positions1)
    _, idx2 = tree.query(positions2)

    output_prefix = f"coincidence_{material}_src{src_dist:.1f}cm_{args.config_option}"
    output_cdf = os.path.join(args.output_dir, f"{output_prefix}.cdf")
    output_cdh = os.path.join(args.output_dir, f"{output_prefix}.cdh")

    # Write .cdf
    with open(output_cdf, "wb") as f:
        for i, (c1, c2) in enumerate(zip(idx1, idx2)):
            data = struct.pack("<III", i, c1, c2)
            f.write(data)

    num_events = len(idx1)
    print(f"[CDF] Wrote {num_events:,} events to {output_cdf}")

    # Write .cdh
    write_simple_text_cdh(output_cdh, data_file_name=output_cdf,
                          num_events=num_events, config_name=config_name)

    print(f"[DONE] Generated:\n  {output_cdf}\n  {output_cdh}")


# ==============================================
# Entry point
# ==============================================
if __name__ == "__main__":
    main()
