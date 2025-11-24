#!/bin/bash
# ============================================
# CASToR Reconstruction Script (Robust Version)
# Usage:
#   ./run_castor_recon.sh <material> <source_dist_cm> <option>
# Example:
#   ./run_castor_recon.sh LYSO 0.0 fine
# ============================================

# ---- Check arguments ----
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <material> <source_dist_cm> <option>"
  echo "  option: original | fine | super_fine"
  exit 1
fi

material="$1"
source_dist="$2"
option="$3"

# ---- Verify CASToR binary ----
recon="castor-recon"
if ! command -v "${recon}" &> /dev/null; then
  echo "***** Error: CASToR binary not found in PATH. Please add it before running this script."
  exit 1
fi

# ---- File naming ----
case "$option" in
  original)
    postfix="_original"
    sens="philips_sim_simple_hot_point_all_merged_sensitivity.hdr"
    ;;
  fine)
    postfix="_fine"
    sens="philips_sim_simple_hot_point_all_merged_fine_sensitivity.hdr"
    ;;
  super_fine)
    postfix="_super_fine"
    sens="philips_sim_simple_hot_point_all_merged_super_fine_sensitivity.hdr"
    ;;
  *)
    echo "Error: invalid option '$option'. Must be one of: original, fine, super_fine"
    exit 1
    ;;
esac

# ---- Data filenames ----
datafile="coincidence_${material}_src${source_dist}cm${postfix}.cdh"
output_prefix="${material}_src${source_dist}cm${postfix}"

# ---- Parameter settings ----
verbose="-vb 2"
last_it="-oit -1"
iteration="-it 4:28"
voxels_number="-dim 400,400,1"
fov_size="-fov 100.,100.,10."
offset="-off 0.,0.,0."
optimizer="-opti MLEM"
projector="-proj joseph"
sensitivity="-sens ${sens}"

# ---- Check input files ----
if [ ! -f "${datafile}" ]; then
  echo "Error: data file not found: ${datafile}"
  exit 1
fi
if [ ! -f "${sens}" ]; then
  echo "Warning: sensitivity file not found: ${sens}"
fi

# ---- Run reconstruction ----
echo "=============================================================================================="
echo "Running CASToR reconstruction..."
echo "Material: ${material}"
echo "Source distance: ${source_dist} cm"
echo "Configuration: ${option}"
echo "Data file: ${datafile}"
echo "Output prefix: ${output_prefix}"
echo "=============================================================================================="

${recon} ${verbose} -df "${datafile}" -fout "${output_prefix}" \
  ${last_it} ${iteration} ${voxels_number} ${fov_size} ${offset} \
  ${optimizer} ${projector} ${sensitivity}

# ---- End ----
echo ""
echo "Reconstruction finished. Output saved as ${output_prefix}.*"
exit 0
