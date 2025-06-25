#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Visualization version of your simulation

import opengate as gate
from pathlib import Path
import opengate.contrib.pet.philipsvereos as pet_vereos
from pet_helpers import add_vereos_digitizer_v1
from opengate.geometry.utility import get_circular_repetition
from opengate.sources.base import get_rad_yield

# Import phantom functions
from phantoms import (
    add_multiple_hot_spheres_phantom,
    add_simple_hot_sphere_phantom,
    add_resolution_test_phantom,
    add_cold_spheres_phantom
)

if __name__ == "__main__":
    sim = gate.Simulation()

    # ============ ENABLE VISUALIZATION ============
    sim.visu = True              # ✅ Enable visualization
    sim.visu_type = "qt"         # Use Qt viewer
    sim.random_seed = "auto"
    sim.number_of_threads = 1
    sim.progress_bar = True
    sim.output_dir = "./output"

    # units
    m = gate.g4_units.m
    mm = gate.g4_units.mm
    cm = gate.g4_units.cm
    sec = gate.g4_units.s
    Bq = gate.g4_units.Bq

    # world
    world = sim.world
    world.size = [2 * m, 2 * m, 2 * m]
    world.material = "G4_AIR"

    # ============ SIMPLIFIED PET FOR VISUALIZATION ============
    pet = pet_vereos.add_pet(sim, "pet")
    
    # Simplify PET system for faster visualization
    module = sim.volume_manager.get_volume("pet_module")
    # Only 4 modules instead of 18 for faster loading
    translations_ring, rotations_ring = get_circular_repetition(
        4, [391.5 * mm, 0, 0], start_angle_deg=0, axis=[0, 0, 1]
    )
    module.translation = translations_ring
    module.rotation = rotations_ring

    # ============ PHANTOM SELECTION ============
    print("🎯 PHANTOM VISUALIZATION MODE")
    print("Choose which phantom to visualize:")
    
    # Option 1: Multiple hot spheres (your current phantom)
    # phantom, sources = add_multiple_hot_spheres_phantom(sim, "multi_sphere")
    # phantom_name = "multiple_hot_spheres"
    
    # Option 2: Simple single hot sphere (original)
    phantom, sources = add_simple_hot_sphere_phantom(sim, "simple")
    phantom_name = "simple_hot_sphere"
    
    print(f"\nVisualizing phantom: {phantom_name}")
    print(f"Number of sources: {len(sources)}")

    # ============ REDUCE ACTIVITY FOR VISUALIZATION ============
    total_yield = get_rad_yield("F18")
    print("Reducing all activities for visualization...")
    for source in sources:
        source.activity = source.activity / 10000  # Much lower for vis

    # ============ MINIMAL PHYSICS FOR VISUALIZATION ============
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option1"
    sim.physics_manager.enable_decay = True
    sim.physics_manager.set_production_cut("world", "all", 1 * m)
    sim.physics_manager.set_production_cut(phantom.name, "all", 10 * mm)

    # ============ NO DIGITIZER IN VISUALIZATION MODE ============
    print("⚠️  Skipping digitizer for visualization")
    
    # ============ VERY SHORT RUN TIME ============
    sim.run_timing_intervals = [[0, 2.0 * sec]]  # Just 2 second

    print(f"\n=== VISUALIZATION READY ===")
    print("🎯 What you should see:")
    print("1. Blue semi-transparent water box (25x25x25 cm)")
    print("2. Multiple colored spheres at different positions:")
    print("   - Red sphere at center (largest)")
    print("   - Green/Yellow spheres along X-axis")
    print("   - Orange/Cyan spheres along Y-axis")
    print("   - Purple sphere at corner")
    print("3. Simplified PET detector ring (4 modules)")
    print("")
    print("🖱️  Controls:")
    print("   - Mouse: Rotate view")
    print("   - Scroll: Zoom in/out")
    print("   - Right-click: Context menu")
    print("   - ESC: Close visualization")
    print("="*40)

    # ============ RUN VISUALIZATION ============
    print("Starting visualization...")
    print("Close the visualization window to continue...")
    
    sim.run()
    
    print("Visualization completed!")