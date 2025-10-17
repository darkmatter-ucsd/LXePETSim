#!/bin/bash

# Loop over source distances from 1.0 to 12.0 cm
for dist in $(seq 0.0 1.0 15.0)
do
  echo "Running simulation for source_dist=${dist} cm"
  python pet_sim_philips_lxe.py --source_dist ${dist}
done
