#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opengate as gate
from pathlib import Path
import opengate.contrib.pet.philipsvereos as pet_vereos
from pet_helpers import add_vereos_digitizer_v1
from opengate.geometry.utility import get_circular_repetition
from opengate.sources.base import get_rad_yield

if __name__ == "__main__":
    sim = gate.Simulation()

    # options
    # warning the visualisation is slow !
    sim.visu = True
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
    world.size = [5 * m, 5 * m, 5 * m]
    world.material = "G4_AIR"

    # add the Philips Vereos PET
    pet = pet_vereos.add_pet(sim, "pet")

    # If visu is enabled, we simplified the PET system, otherwise it is too slow
    if sim.visu:
        module = sim.volume_manager.get_volume("pet_module")
        # only 2 repetition instead of 18
        translations_ring, rotations_ring = get_circular_repetition(
            2, [391.5 * mm, 0, 0], start_angle_deg=190, axis=[0, 0, 1]
        )
        module.translation = translations_ring
        module.rotation = rotations_ring

    # add table
    bed = pet_vereos.add_table(sim, "pet")

    # add a simple waterbox with a hot sphere inside
    waterbox = sim.add_volume("Box", "waterbox")
    waterbox.size = [10 * cm, 10 * cm, 10 * cm]
    waterbox.translation = [0 * cm, -10 * cm, 0 * cm]
    waterbox.material = "G4_WATER"
    waterbox.color = [0, 0, 1, 1]

    hot_sphere = sim.add_volume("Sphere", "hot_sphere")
    hot_sphere.mother = waterbox.name
    hot_sphere.rmax = 5 * cm
    hot_sphere.material = "G4_WATER"
    hot_sphere.color = [1, 0, 0, 1]

    # source for tests
    source = sim.add_source("GenericSource", "hot_sphere_source")
    total_yield = get_rad_yield("F18")
    print("Yield for F18 (nb of e+ per decay) : ", total_yield)
    source.particle = "e+"
    source.energy.type = "F18"
    source.activity = 1e4 * Bq * total_yield
    if sim.visu:
        source.activity = 1 * Bq * total_yield
    source.half_life = 6586.26 * sec

    # physics
    sim.physics_manager.physics_list_name = "G4EmStandardPhysics_option3"
    sim.physics_manager.enable_decay = True
    sim.physics_manager.set_production_cut("world", "all", 1 * m)
    sim.physics_manager.set_production_cut("waterbox", "all", 1 * mm)

    # add the PET digitizer
    add_vereos_digitizer_v1(sim, pet, f"output_vereos.root")

    # add stat actor
    stats = sim.add_actor("SimulationStatisticsActor", "Stats")
    stats.track_types_flag = True
    stats.output_filename = "stats_vereos.txt"

    # timing
    sim.run_timing_intervals = [[0, 2.0 * sec]]

    # go
    sim.run()

    # end
    """print(f"Output statistics are in {stats.output}")
    print(f"Output edep map is in {dose.output}")
    print(f"vv {ct.image} --fusion {dose.output}")
    stats = sim.output.get_actor("Stats")
    print(stats)"""
