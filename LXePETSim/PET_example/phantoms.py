#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opengate as gate
from opengate.sources.base import get_rad_yield

def add_multiple_hot_spheres_phantom(sim, name="multi_sphere_phantom"):
    """
    Add a phantom with multiple hot spheres at different positions and sizes
    for comprehensive PET system evaluation
    """
    # units
    mm = gate.g4_units.mm
    cm = gate.g4_units.cm
    Bq = gate.g4_units.Bq
    sec = gate.g4_units.s

    # colors
    red = [1, 0, 0, 1]
    blue = [0, 0, 1, 0.3]
    green = [0, 1, 0, 1]
    yellow = [1, 1, 0, 1]
    magenta = [1, 0, 1, 1]
    cyan = [0, 1, 1, 1]
    orange = [1, 0.5, 0, 1]

    # main water container
    waterbox = sim.add_volume("Box", f"{name}_waterbox")
    waterbox.size = [25 * cm, 25 * cm, 25 * cm]
    waterbox.translation = [0 * cm, 0 * cm, 0 * cm]
    waterbox.material = "G4_WATER"
    waterbox.color = blue

    # hot sphere configurations
    sphere_configs = [
        # Center sphere - largest, highest activity
        {
            "name": f"{name}_center_large",
            "position": [0 * cm, 0 * cm, 0 * cm],
            "radius": 2.0 * cm,
            "activity": 8e4 * Bq,
            "color": red
        },
        
        # Radial position test - same size, different distances from center
        {
            "name": f"{name}_radial_3cm",
            "position": [4 * cm, 0 * cm, 0 * cm],
            "radius": 1.0 * cm,
            "activity": 4e4 * Bq,
            "color": green
        },
        {
            "name": f"{name}_radial_6cm",
            "position": [7 * cm, 0 * cm, 0 * cm],
            "radius": 1.0 * cm,
            "activity": 4e4 * Bq,
            "color": yellow
        },
        {
            "name": f"{name}_radial_9cm",
            "position": [10 * cm, 0 * cm, 0 * cm],
            "radius": 1.0 * cm,
            "activity": 4e4 * Bq,
            "color": magenta
        },
        
        {
            "name": f"{name}_size_medium",
            "position": [0 * cm, 4 * cm, 0 * cm],
            "radius": 1.0 * cm,
            "activity": 4e4 * Bq,
            "color": orange
        },
    
    ]

    # Create spheres and sources
    sources = []
    total_yield = get_rad_yield("F18")
    
    print(f"Creating {len(sphere_configs)} hot spheres:")
    
    for config in sphere_configs:
        # Create sphere volume
        sphere = sim.add_volume("Sphere", config["name"])
        sphere.mother = waterbox.name
        sphere.rmax = config["radius"]
        sphere.translation = config["position"]
        sphere.material = "G4_WATER"
        sphere.color = config["color"]
        
        # Create corresponding source
        source = sim.add_source("GenericSource", f"{config['name']}_source")
        source.particle = "e+"
        source.energy.type = "F18"
        source.volume = config["name"]
        source.position.type = "sphere"
        source.position.translation = config["position"]  # 手动从配置复制位置
        source.activity = config["activity"] * total_yield
        source.half_life = 6586.26 * sec  # F18 half-life
        
        sources.append(source)
        
        # Print info
        radius_mm = config["radius"] / mm
        activity_kbq = config["activity"] / 1000
        pos_str = f"({config['position'][0]/cm:.1f}, {config['position'][1]/cm:.1f}, {config['position'][2]/cm:.1f}) cm"
        print(f"  {config['name']}: R={radius_mm:.1f}mm, A={activity_kbq:.1f}kBq, pos={pos_str}")

    return waterbox, sources


def add_simple_hot_sphere_phantom(sim, name="simple_sphere"):
    """
    Simple single hot sphere phantom (your original design)
    """
    # units
    mm = gate.g4_units.mm
    cm = gate.g4_units.cm
    Bq = gate.g4_units.Bq
    sec = gate.g4_units.s

    # waterbox
    waterbox = sim.add_volume("Box", f"{name}_waterbox")
    waterbox.size = [10 * cm, 10 * cm, 10 * cm]
    waterbox.translation = [0 * cm, 0 * cm, 0 * cm]
    waterbox.material = "G4_WATER"
    waterbox.color = [0, 0, 1, 0.3]

    # hot sphere
    hot_sphere = sim.add_volume("Sphere", f"{name}_hot_sphere")
    hot_sphere.mother = waterbox.name
    hot_sphere.rmax = 1 * cm
    hot_sphere.material = "G4_WATER"
    hot_sphere.color = [1, 0, 0, 1]

    # source
    source = sim.add_source("GenericSource", f"{name}_source")
    total_yield = get_rad_yield("F18")
    source.particle = "e+"
    source.energy.type = "F18"
    source.volume = f"{name}_hot_sphere"
    source.activity = 1e4 * Bq * total_yield
    source.half_life = 6586.26 * sec

    print(f"Created simple hot sphere: R=10mm, A=10kBq")
    
    return waterbox, [source]


def add_resolution_test_phantom(sim, name="resolution_test"):
    """
    Small spheres at different separations to test resolution limits
    """
    # units
    mm = gate.g4_units.mm
    cm = gate.g4_units.cm
    Bq = gate.g4_units.Bq
    sec = gate.g4_units.s

    # waterbox
    waterbox = sim.add_volume("Box", f"{name}_waterbox")
    waterbox.size = [15 * cm, 15 * cm, 15 * cm]
    waterbox.translation = [0 * cm, 0 * cm, 0 * cm]
    waterbox.material = "G4_WATER"
    waterbox.color = [0, 0, 1, 0.2]

    # Small spheres at different separations
    separations = [1, 2, 3, 4, 5]  # mm
    sphere_configs = []
    
    for i, sep in enumerate(separations):
        # Pair of spheres
        config1 = {
            "name": f"{name}_pair_{sep}mm_a",
            "position": [-sep/2 * mm, i * 2 * cm - 4 * cm, 0 * cm],
            "radius": 0.5 * mm,
            "activity": 1e4 * Bq,
            "color": [1, 0, 0, 1]
        }
        config2 = {
            "name": f"{name}_pair_{sep}mm_b",
            "position": [sep/2 * mm, i * 2 * cm - 4 * cm, 0 * cm],
            "radius": 0.5 * mm,
            "activity": 1e4 * Bq,
            "color": [1, 0, 0, 1]
        }
        sphere_configs.extend([config1, config2])

    # Create spheres and sources
    sources = []
    total_yield = get_rad_yield("F18")
    
    print(f"Creating resolution test phantom with {len(separations)} pairs:")
    
    for config in sphere_configs:
        # Create sphere volume
        sphere = sim.add_volume("Sphere", config["name"])
        sphere.mother = waterbox.name
        sphere.rmax = config["radius"]
        sphere.translation = config["position"]
        sphere.material = "G4_WATER"
        sphere.color = config["color"]
        
        # Create corresponding source
        source = sim.add_source("GenericSource", f"{config['name']}_source")
        source.particle = "e+"
        source.energy.type = "F18"
        source.volume = config["name"]
        source.activity = config["activity"] * total_yield
        source.half_life = 6586.26 * sec
        
        sources.append(source)

    for sep in separations:
        print(f"  Pair separated by {sep}mm")

    return waterbox, sources


def add_cold_spheres_phantom(sim, name="cold_spheres"):
    """
    Phantom with both hot and cold spheres for contrast studies
    """
    # units
    mm = gate.g4_units.mm
    cm = gate.g4_units.cm
    Bq = gate.g4_units.Bq
    sec = gate.g4_units.s

    # main water container with background activity
    waterbox = sim.add_volume("Box", f"{name}_waterbox")
    waterbox.size = [20 * cm, 20 * cm, 20 * cm]
    waterbox.translation = [0 * cm, 0 * cm, 0 * cm]
    waterbox.material = "G4_WATER"
    waterbox.color = [0, 0, 1, 0.2]

    # Hot spheres
    hot_configs = [
        {
            "name": f"{name}_hot_1",
            "position": [4 * cm, 0 * cm, 0 * cm],
            "radius": 1.0 * cm,
            "activity": 5e4 * Bq,
            "color": [1, 0, 0, 1]
        },
        {
            "name": f"{name}_hot_2",
            "position": [-4 * cm, 0 * cm, 0 * cm],
            "radius": 1.5 * cm,
            "activity": 7e4 * Bq,
            "color": [1, 0.5, 0, 1]
        }
    ]

    # Cold spheres (no activity)
    cold_configs = [
        {
            "name": f"{name}_cold_1",
            "position": [0 * cm, 4 * cm, 0 * cm],
            "radius": 1.0 * cm,
            "material": "G4_AIR",
            "color": [0.5, 0.5, 0.5, 1]
        },
        {
            "name": f"{name}_cold_2",
            "position": [0 * cm, -4 * cm, 0 * cm],
            "radius": 1.2 * cm,
            "material": "G4_AIR",
            "color": [0.3, 0.3, 0.3, 1]
        }
    ]

    sources = []
    total_yield = get_rad_yield("F18")

    # Create hot spheres
    for config in hot_configs:
        sphere = sim.add_volume("Sphere", config["name"])
        sphere.mother = waterbox.name
        sphere.rmax = config["radius"]
        sphere.translation = config["position"]
        sphere.material = "G4_WATER"
        sphere.color = config["color"]
        
        source = sim.add_source("GenericSource", f"{config['name']}_source")
        source.particle = "e+"
        source.energy.type = "F18"
        source.volume = config["name"]
        source.activity = config["activity"] * total_yield
        source.half_life = 6586.26 * sec
        sources.append(source)

    # Create cold spheres
    for config in cold_configs:
        sphere = sim.add_volume("Sphere", config["name"])
        sphere.mother = waterbox.name
        sphere.rmax = config["radius"]
        sphere.translation = config["position"]
        sphere.material = config["material"]
        sphere.color = config["color"]

    # Background activity in waterbox
    bg_source = sim.add_source("GenericSource", f"{name}_background")
    bg_source.particle = "e+"
    bg_source.energy.type = "F18"
    bg_source.volume = f"{name}_waterbox"
    bg_source.activity = 500 * Bq * total_yield  # Low background
    bg_source.half_life = 6586.26 * sec
    sources.append(bg_source)

    print("Created hot/cold spheres phantom:")
    print("  2 hot spheres, 2 cold spheres, background activity")

    return waterbox, sources