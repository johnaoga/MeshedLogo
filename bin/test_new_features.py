#!/usr/bin/env python3
"""
Test new features:
1. Mesh lines only (no surface)
2. Surface only (no lines)
3. Invert mode (background meshed, character as hole)
4. Line thickness control
5. Vertex modes (all, random, none)
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meshed_logo import MeshedLogo

output_dir = 'test_output'
os.makedirs(output_dir, exist_ok=True)

logo = MeshedLogo()
logo.set_canvas(1600, 400)

# Test 1: Mesh lines only (no surface)
print("\n" + "="*60)
print("Test 1: Mesh lines only (no surface)")
print("="*60)
logo.generate(
    text="MESH",
    output_file=os.path.join(output_dir, 'mesh_lines_only.png'),
    colors=['cyan', 'magenta', 'yellow', 'white'],
    scale=1.5,
    show_wireframe=True,
    show_surface=False,  # No surface
    show_vertices=False,
    wireframe_thickness=1.0
)
print("✓ Mesh lines only generated!")

# Test 2: Surface only (no lines, no dots)
print("\n" + "="*60)
print("Test 2: Surface only (no lines, no dots)")
print("="*60)
logo.generate(
    text="SURF",
    output_file=os.path.join(output_dir, 'surface_only.png'),
    colors=['cyan', 'magenta', 'yellow', 'white'],
    scale=1.5,
    show_wireframe=False,  # No lines
    show_surface=True,
    show_vertices=False  # No dots
)
print("✓ Surface only generated!")

# Test 3: Invert mode (background meshed)
print("\n" + "="*60)
print("Test 3: Invert mode (background meshed, character as hole)")
print("="*60)
logo.generate(
    text="INVERT",
    output_file=os.path.join(output_dir, 'invert_mode.png'),
    colors=['cyan', 'magenta'],
    scale=1.2,
    invert_mode=True,  # Mesh background
    invert_margin=30,  # Margin around character
    show_wireframe=True,
    show_surface=True,
    show_vertices=True
)
print("✓ Invert mode generated!")

# Test 4: Thick lines
print("\n" + "="*60)
print("Test 4: Thick wireframe lines")
print("="*60)
logo.generate(
    text="THICK",
    output_file=os.path.join(output_dir, 'thick_lines.png'),
    colors=['cyan', 'yellow'],
    scale=1.5,
    show_wireframe=True,
    show_surface=True,
    show_vertices=False,
    wireframe_thickness=2.0  # Thick lines
)
print("✓ Thick lines generated!")

# Test 5: Random vertices
print("\n" + "="*60)
print("Test 5: Random vertex dots (50% shown)")
print("="*60)
logo.generate(
    text="RANDOM",
    output_file=os.path.join(output_dir, 'random_vertices.png'),
    colors=['magenta', 'cyan', 'yellow'],
    scale=1.3,
    show_wireframe=True,
    show_surface=True,
    show_vertices=True,
    vertex_mode='random',  # Random subset
    vertex_size=12.0  # Larger dots
)
print("✓ Random vertices generated!")

# Test 6: Large vertices, no wireframe
print("\n" + "="*60)
print("Test 6: Large vertex dots only")
print("="*60)
logo.generate(
    text="DOTS",
    output_file=os.path.join(output_dir, 'dots_only.png'),
    colors=['cyan', 'magenta', 'yellow', 'white'],
    scale=1.5,
    show_wireframe=False,  # No lines
    show_surface=False,  # No surface
    show_vertices=True,
    vertex_mode='all',
    vertex_size=20.0  # Very large dots
)
print("✓ Dots only generated!")

print("\n" + "="*60)
print("✓ All feature tests complete!")
print("="*60)
print(f"\nOutput files in: {output_dir}/")
print("  - mesh_lines_only.png")
print("  - surface_only.png")
print("  - invert_mode.png")
print("  - thick_lines.png")
print("  - random_vertices.png")
print("  - dots_only.png")
print()
