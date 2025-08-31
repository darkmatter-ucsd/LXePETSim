#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opengate as gate
from pathlib import Path
import opengate.contrib.pet.philipsvereos as pet_vereos
from pet_helpers import add_vereos_digitizer_v1
from pet_helpers import add_LXe_digitizer_v1
from opengate.geometry.utility import get_circular_repetition
from opengate.sources.base import get_rad_yield


# Import our phantom functions
from phantoms import (
    add_multiple_hot_spheres_phantom,
    add_simple_hot_sphere_phantom,
    add_resolution_test_phantom,
    add_cold_spheres_phantom
)

if __name__ == "__main__":
    sim = gate.Simulation()

    # options
    # warning the visualisation is slow !
    sim.visu = False
    sim.visu_type = "qt"
    sim.random_seed = "auto"
    sim.number_of_threads = 1
    sim.progress_bar = True
    sim.output_dir = "./output"
    data_path = Path("data")

    # units
    m = gate.g4_units.m
    mm = gate.g4_units.mm
    cm = gate.g4_units.cm
    sec = gate.g4_units.s
    ps = gate.g4_units.ps
    keV = gate.g4_units.keV
    Bq = gate.g4_units.Bq
    gcm3 = gate.g4_units.g_cm3

    # world
    world = sim.world
    world.size = [2 * m, 2 * m, 2 * m]
    world.material = "G4_AIR"

    # add the Philips Vereos PET
    pet = pet_vereos.add_pet(sim, "pet", shift = 21)

    # If visu is enabled, we simplified the PET system, otherwise it is too slow
    if sim.visu:
        module = sim.volume_manager.get_volume("pet_module")
        # only 2 repetition instead of 18
        translations_ring, rotations_ring = get_circular_repetition(
            2, [391.5 * mm, 0, 0], start_angle_deg=190, axis=[0, 0, 1]
        )
        module.translation = translations_ring
        module.rotation = rotations_ring

    # add table (uncomment if needed)
    # bed = pet_vereos.add_table(sim, "pet")

    # ============ PHANTOM SELECTION ============
    # Choose which phantom to use by uncommenting one of the following

    # Option 1: Multiple hot spheres (recommended for comprehensive testing)
    #phantom, sources = add_multiple_hot_spheres_phantom(sim, "multi_sphere")
    #phantom_name = "multiple_hot_spheres"

    # Option 2: Simple single hot sphere (original)
    phantom, sources = add_simple_hot_sphere_phantom(sim, "simple")
    phantom_name = "simple_hot_sphere"

    # Option 3: Resolution test with small sphere pairs
    # phantom, sources = add_resolution_test_phantom(sim, "resolution")
    # phantom_name = "resolution_test"

    # Option 4: Hot and cold spheres with background
    # phantom, sources = add_cold_spheres_phantom(sim, "hot_cold")
    # phantom_name = "hot_cold_spheres"

    print(f"\nUsing phantom: {phantom_name}")
    print(f"Total sources created: {len(sources)}")

    # Get F18 yield info
    total_yield = get_rad_yield("F18")
    print("Yield for F18 (nb of e+ per decay) : ", total_yield)

    # Adjust activity for visualization mode
    for source in sources:
        source.activity = source.activity * 1
    if sim.visu:
        print("Visualization mode: reducing all activities by factor 1000")
        for source in sources:
            source.activity = source.activity / 1000

    # physics
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option3"
    sim.physics_manager.enable_decay = True
    sim.physics_manager.set_production_cut("world", "all", 1 * m)

    # Set production cuts for phantom volumes
    sim.physics_manager.set_production_cut(phantom.name, "all", 1 * mm)

    # add the PET digitizer
    output_filename = f"output_{phantom_name}.root"
    add_LXe_digitizer_v1(sim, pet, output_filename)

    # add stat actor
    stats = sim.add_actor("SimulationStatisticsActor", "Stats")
    stats.track_types_flag = True
    stats.output_filename = f"stats_{phantom_name}.txt"

    # timing
    sim.run_timing_intervals = [[0,  20.0 * sec]]

    # Print simulation summary
    print(f"\n=== Simulation Summary ===")
    print(f"Phantom: {phantom_name}")
    print(f"Number of sources: {len(sources)}")
    print(f"Simulation time: {sim.run_timing_intervals[0][1] / sec} seconds")
    print(f"Output file: {output_filename}")
    print(f"Stats file: stats_{phantom_name}.txt")
    print("=" * 30)

    # Print simulation summary
    print(f"\n=== Simulation Summary ===")
    print(f"Phantom: {phantom_name}")
    print(f"Number of sources: {len(sources)}")
    print(f"Simulation time: {sim.run_timing_intervals[0][1] / sec} seconds")
    print(f"Output file: {output_filename}")
    print(f"Stats file: stats_{phantom_name}.txt")
    print("=" * 30)

    # go
    sim.run()

    # Print completion info
    print(f"\nSimulation completed!")
    print(f"Check outputs in: {sim.output_dir}")
    print(f"Stats: stats_{phantom_name}.txt")
    print(f"Data: {output_filename}")

    # end
    print(f"\nSimulation completed!")
    print(f"Check outputs in: {sim.output_dir}")
    print(f"Stats: stats_{phantom_name}.txt")
    print(f"Data: {output_filename}")

    # You can access statistics if needed
    # stats = sim.output.get_actor("Stats")
    print(stats)