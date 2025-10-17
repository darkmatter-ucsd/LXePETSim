#!/bin/bash

# Define lists
config_options=("original" "fine" "super_fine")
materials=("LYSO" "LXe")
distances=$(seq 0 15)

# Loop over all combinations
for config in "${config_options[@]}"; do
  for mat in "${materials[@]}"; do
    for dist in $distances; do
      echo "Running for config=$config, material=$mat, source_dist=${dist}.0 cm ..."
      python coincidence_to_castor_data.py \
        --config_option "$config" \
        --material "$mat" \
        --source_dist "${dist}.0"
    done
  done
done
