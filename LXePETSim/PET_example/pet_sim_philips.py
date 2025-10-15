#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import opengate as gate
from pathlib import Path
import opengate.contrib.pet.philipsvereos as pet_vereos
from pet_helpers import add_vereos_digitizer_v1
from opengate.geometry.utility import get_circular_repetition
from opengate.sources.base import get_rad_yield
import argparse
from phantoms import (
    add_multiple_hot_spheres_phantom,
    add_simple_hot_point_phantom,
    add_micro_derenzo_phantom,
)

# ----------------------------------------------------------------------
# Utility function to create unique filenames with numbered suffix
# ----------------------------------------------------------------------
def get_unique_filename(base_name, ext, outdir="."):
    """
    Generate a unique filename by appending _0, _1, ... until no conflict.
    Returns both the full path and the filename.
    """
    i = 0
    while True:
        fname = f"{base_name}_{i}{ext}"
        fpath = os.path.join(outdir, fname)
        if not os.path.exists(fpath):
            return fpath, fname
        i += 1

parser = argparse.ArgumentParser(description="Simulation parameter.")
parser.add_argument(
    "--source_dist",
    type=float,
    default=0.0,
    help="Source distance to detector center in cm (e.g., 0.0, 25.0, 50.0)."
)
args = parser.parse_args()

if __name__ == "__main__":
    sim = gate.Simulation()
    source_dist = args.source_dist

    # ------------------------------------------------------------------
    # General options
    # ------------------------------------------------------------------
    sim.visu = False
    sim.visu_type = "qt"
    sim.random_seed = "auto"
    sim.number_of_threads = 1
    sim.progress_bar = True
    sim.output_dir = "./output_radius_plot"
    data_path = Path("data")

    # Units
    m = gate.g4_units.m
    mm = gate.g4_units.mm
    cm = gate.g4_units.cm
    sec = gate.g4_units.s
    ps = gate.g4_units.ps
    keV = gate.g4_units.keV
    Bq = gate.g4_units.Bq
    gcm3 = gate.g4_units.g_cm3

    # ------------------------------------------------------------------
    # World
    # ------------------------------------------------------------------
    world = sim.world
    world.size = [2 * m, 2 * m, 2 * m]
    world.material = "G4_AIR"

    # ------------------------------------------------------------------
    # Add the Philips Vereos PET
    # ------------------------------------------------------------------
    pet = pet_vereos.add_pet(sim, "pet")

    # Simplified PET if visualization is enabled
    if sim.visu:
        module = sim.volume_manager.get_volume("pet_module")
        translations_ring, rotations_ring = get_circular_repetition(
            2, [391.5 * mm, 0, 0], start_angle_deg=190, axis=[0, 0, 1]
        )
        module.translation = translations_ring
        module.rotation = rotations_ring

    # ------------------------------------------------------------------
    # Phantom selection
    # ------------------------------------------------------------------
    # Option 1: Multiple hot spheres
    #phantom, sources = add_multiple_hot_spheres_phantom(sim, "multi_sphere")
    #phantom_name = "multiple_hot_spheres"

    # Option 2: Simple single hot sphere
    phantom, sources = add_simple_hot_point_phantom(sim, "simple")
    phantom_name = "simple_hot_point"

    # Option 3: Micro-Derenzo phantom
    # phantom, sources = add_micro_derenzo_phantom(sim, "micro_derenzo")
    # phantom_name = "micro_derenzo"  # safer for filenames

    print(f"\nUsing phantom: {phantom_name}")
    print(f"Total sources created: {len(sources)}")

    # ------------------------------------------------------------------
    # Isotope yield info
    # ------------------------------------------------------------------
    total_yield = get_rad_yield("F18")
    print("Yield for F18 (nb of e+ per decay):", total_yield)

    # ------------------------------------------------------------------
    # Reduce activity in visualization mode
    # ------------------------------------------------------------------
    if sim.visu:
        print("Visualization mode: reducing all activities by factor 100")
        for source in sources:
            source.activity = source.activity / 100

    # ------------------------------------------------------------------
    # Physics
    # ------------------------------------------------------------------
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option3"
    sim.physics_manager.enable_decay = True
    sim.physics_manager.set_production_cut("world", "all", 1 * m)
    sim.physics_manager.set_production_cut(phantom.name, "all", 1 * mm)

    # ------------------------------------------------------------------
    # Output filenames (with automatic numbering)
    # ------------------------------------------------------------------
    base_name = f"output_{phantom_name}_LYSO_src{source_dist}cm"
    output_path, output_filename = get_unique_filename(base_name, ".root", sim.output_dir)

    stats_base = f"stats_{phantom_name}"
    stats_path, stats_filename = get_unique_filename(stats_base, ".txt", sim.output_dir)

    # ------------------------------------------------------------------
    # Add PET digitizer
    # ------------------------------------------------------------------
    add_vereos_digitizer_v1(sim, pet, output_filename)

    # Add simulation statistics actor
    stats = sim.add_actor("SimulationStatisticsActor", "Stats")
    stats.track_types_flag = True
    stats.output_filename = stats_filename

    # ------------------------------------------------------------------
    # Timing
    # ------------------------------------------------------------------
    sim.run_timing_intervals = [[0, 1000.0 * sec]]

    # ------------------------------------------------------------------
    # Print simulation summary
    # ------------------------------------------------------------------
    print("\n=== Simulation Summary ===")
    print(f"Phantom: {phantom_name}")
    print(f"Number of sources: {len(sources)}")
    print(f"Simulation time: {sim.run_timing_intervals[0][1]/sec} seconds")
    print(f"Output file: {output_filename}")
    print(f"Stats file: {stats_filename}")
    print("=" * 30)

    # ------------------------------------------------------------------
    # Run simulation
    # ------------------------------------------------------------------
    sim.run()

    # ------------------------------------------------------------------
    # Print completion info
    # ------------------------------------------------------------------
    print("\nSimulation completed!")
    print(f"Check outputs in: {sim.output_dir}")
    print(f"Stats: {stats_filename}")
    print(f"Data: {output_filename}")
