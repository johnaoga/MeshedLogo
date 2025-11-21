#!/usr/bin/env python3
"""Test logo generation with characters having openings"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meshed_logo import MeshedLogo

output_dir = 'test_output'
os.makedirs(output_dir, exist_ok=True)

# Test characters with openings (concave shapes)
logo = MeshedLogo()
logo.set_canvas(2000, 400)
logo.generate(
    text="MUCH",
    output_file=os.path.join(output_dir, 'much_logo.png'),
    colors=['cyan', 'magenta', 'yellow', 'white'],
    scale=1.5,
    mesh_density=1.2
)
print("✓ MUCH logo generated (M, U, C, H all have openings)!")
