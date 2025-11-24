#!/bin/bash
# ================================================================
# Batch runner for run_radius_philips.sh
# Loops over material, source distance, and config option
# Usage: ./run_all_radius_philips.sh
# ================================================================

# Define parameter lists
materials=("LYSO" "LXe")
options=("original" "fine" "super_fine")
distances=$(seq 0.1 0.1 0.9)

# Loop through all combinations
for mat in "${materials[@]}"; do
  for opt in "${options[@]}"; do
    for dist in $distances; do
      echo "---------------------------------------------"
      echo "Running reconstruction: material=${mat}, option=${opt}, source_dist=${dist} cm"
      echo "---------------------------------------------"
      ./run_radius_philips.sh "$mat" "${dist}" "$opt"
      echo ""
    done
  done
done

echo "==============================================================="
echo "All reconstructions completed!"
echo "==============================================================="
