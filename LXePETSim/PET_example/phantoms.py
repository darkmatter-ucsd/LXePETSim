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
        source.position.translation = config["position"]
        # must set radius for the source, otherwise it defaults to 0 and acts like a point source
        source.position.radius = sphere.rmax
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
    waterbox.size = [20 * cm, 20 * cm, 20 * cm]
    waterbox.translation = [0 * cm, 0 * cm, 0 * cm]
    waterbox.material = "G4_WATER"
    waterbox.color = [0, 0, 1, 0.3]

    # hot sphere
    hot_sphere = sim.add_volume("Sphere", f"{name}_hot_sphere")
    hot_sphere.mother = waterbox.name
    hot_sphere.rmax = 10 * cm
    hot_sphere.material = "G4_WATER"
    hot_sphere.color = [1, 0, 0, 1]

    # source
    source = sim.add_source("GenericSource", f"{name}_source")
    total_yield = get_rad_yield("F18")
    source.particle = "e+"
    source.energy.type = "F18"
    source.position.type = "sphere"
    source.position.radius = 1 * cm 
    source.position.translation = [0, 0, 0] 
    source.position.confine = f"{name}_hot_sphere"  
    source.position.radius = hot_sphere.rmax
    source.activity = 1e4 * Bq * total_yield
    source.half_life = 6586.26 * sec

    print(f"Created simple hot sphere: R=10mm, A=10kBq")
    
    return waterbox, [source]