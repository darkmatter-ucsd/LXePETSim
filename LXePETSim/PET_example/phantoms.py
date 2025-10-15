#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import opengate as gate
from opengate.sources.base import get_rad_yield
import numpy as np

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
    waterbox.size = [10 * cm, 10 * cm, 10 * cm]
    waterbox.translation = [0 * cm, 0 * cm, 0 * cm]
    # use air for the water box
    waterbox.material = "G4_AIR"
    waterbox.color = blue

    # hot sphere configurations
    sphere_configs = [
        # Center sphere - largest, highest activity
        {
            "name": f"{name}_center_large",
            "position": [0 * cm, 0 * cm, 0 * cm],
            "radius": 2.0 * mm,
            "activity": 2e3 * Bq,
            "color": red
        },
        
        # Radial position test - same size, different distances from center
        {
            "name": f"{name}_radial_3cm",
            "position": [1 * cm, 0 * cm, 0 * cm],
            "radius": 1.0 * mm,
            "activity": 1e3 * Bq,
            "color": green
        },
        {
            "name": f"{name}_radial_6cm",
            "position": [2 * cm, 0 * cm, 0 * cm],
            "radius": 1.0 * mm,
            "activity": 1e3 * Bq,
            "color": yellow
        },
        {
            "name": f"{name}_radial_9cm",
            "position": [3 * cm, 0 * cm, 0 * cm],
            "radius": 1.0 * mm,
            "activity": 1e3 * Bq,
            "color": magenta
        },
        
        {
            "name": f"{name}_size_medium",
            "position": [0 * cm, 1 * cm, 0 * cm],
            "radius": 1.0 * mm,
            "activity": 1e3 * Bq,
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


def add_simple_hot_point_phantom(sim, name="simple_point", source_dist=0.0):
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
    waterbox.size = [30 * cm, 30 * cm, 30 * cm]
    waterbox.translation = [0 * cm, 0 * cm, 0 * cm]
    waterbox.material = "G4_WATER"
    waterbox.color = [0, 0, 1, 0.5]

    # source
    source = sim.add_source("GenericSource", f"{name}_source")
    total_yield = get_rad_yield("F18")
    source.attached_to = waterbox.name
    source.particle = "e+"
    source.energy.type = "F18"
    source.position.type = "point"
    source.position.translation = [source_dist * cm, 0, 0] 
    source.activity = 1e4 * Bq * total_yield
    source.half_life = 6586.26 * sec

    return waterbox, [source]

def add_micro_derenzo_phantom(
    sim,
    name="micro_derenzo",
    rmin_mm=10.0,              # outward offset in mm
    absolute_rmin=True,        # True: place first rod exactly at rmin; False: shift whole sector outward
    activity_ref_bq=2e1,       # reference activity for rods with diameter = 1.0 mm
    rod_length_mm=1.0          # rod length in mm (fixed as requested)
):
    mm = gate.g4_units.mm
    cm = gate.g4_units.cm
    sec = gate.g4_units.s
    Bq = gate.g4_units.Bq

    # Unit conversion
    mm3_to_ml = 1.0 / 1000.0

    # Create waterbox container (slightly larger than rods)
    waterbox = sim.add_volume("Box", f"{name}_waterbox")
    waterbox.size = [10*cm, 10*cm, rod_length_mm*mm + 10*mm]
    waterbox.translation = [0, 0, 0]
    waterbox.material = "G4_AIR"
    waterbox.color = [0.7, 0.7, 0.9, 0.3]

    # Diameters (mm) and number of radial layers (1,2,3,...)
    #rod_diams  = [1.6, 1.4, 1.2, 1.0, 0.8, 0.6]
    #rod_layers = [5,   5,   5,   6,   8,   10]
    rod_diams = [4.8, 4.0, 2.8, 2.4, 1.6, 1.2]
    rod_layers = [3, 4, 5, 6, 8, 10]
    #rod_diams = [2,1,0.5]
    #rod_layers = [2,3,4]
    rod_len = rod_length_mm * mm

    total_yield = get_rad_yield("F18")
    sources = []

    # Convert rmin to length unit
    rmin = rmin_mm * mm

    for i_sector, (d_mm, n_layers) in enumerate(zip(rod_diams, rod_layers)):
        pitch  = 2.0 * d_mm * mm              # rod-to-rod spacing
        r_rod  = (d_mm * mm) / 2.0            # rod radius
        theta  = - i_sector * np.pi / 3.0     # sector rotation (0°, 60°, ...)

        # Rotation matrix for this sector
        R = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta),  np.cos(theta)]])

        # Compute first-layer rod position in local grid
        x1_local, y1_local = 0.0, 1.0 * pitch
        x1, y1 = R @ np.array([x1_local, y1_local])
        r1 = np.hypot(x1, y1)
        if r1 == 0:
            # fallback: use sector middle direction
            u = np.array([np.cos(theta + np.pi/6), np.sin(theta + np.pi/6)])
        else:
            u = np.array([x1, y1]) / r1

        # Sector-wide translation
        if absolute_rmin:
            delta = (rmin - r1) * u
        else:
            delta = rmin * u

        dx, dy = float(delta[0]), float(delta[1])

        # Place rods: layer n has exactly n rods
        for layer in range(1, n_layers + 1):
            for j in range(layer):
                # Local triangular grid coordinates (equilateral)
                x_local = (j - (layer - 1) / 2.0) * pitch
                y_local = layer * (np.sqrt(3)/2) * pitch  # ✅ fixed spacing

                # Rotate to global coordinates and apply offset
                x, y = R @ np.array([x_local, y_local])
                x += dx
                y += dy

                rod_name = f"{name}_sec{i_sector}_d{d_mm:.1f}_L{layer}_j{j}"
                rod = sim.add_volume("Tubs", rod_name)
                rod.mother = waterbox.name
                rod.rmax = r_rod
                rod.rmin = 0
                rod.dz = rod_len / 2.0
                rod.translation = [x, y, 0]
                rod.material = "G4_WATER"
                rod.color = [1, 0, 0, 1]

                # --- Compute rod activity based on diameter² scaling ---
                # Reference: 1.0 mm rods have activity_ref_bq
                activity_bq = activity_ref_bq * (d_mm / 1.0)**2

                # Attach F18 source
                src = sim.add_source("GenericSource", f"{rod_name}_src")
                src.attached_to = rod.name
                src.particle = "e+"
                src.energy.type = "F18"
                src.position.type = "cylinder"
                src.position.radius = rod.rmax
                src.position.dz = rod.dz
                src.direction.type = "iso"
                src.activity = activity_bq * Bq * total_yield
                src.half_life = 6586.26 * sec

                sources.append(src)

    return waterbox, sources
