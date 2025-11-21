#!/usr/bin/env python3
"""
Test full logo generation with hole-aware meshing
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meshed_logo import MeshedLogo


def main():
    output_dir = 'test_output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Test 1: Simple text with holes
    print("\n" + "="*60)
    print("Test 1: Generating 'ROAD' logo (has O, A, D with holes)")
    print("="*60)
    
    logo = MeshedLogo()
    logo.set_canvas(1600, 400)
    logo.generate(
        text="ROAD",
        output_file=os.path.join(output_dir, 'road_logo.png'),
        colors=['cyan', 'magenta', 'yellow', 'white'],
        scale=1.5,
        mesh_density=1.0
    )
    print("✓ ROAD logo generated!")
    
    # Test 2: Text with multiple hole types
    print("\n" + "="*60)
    print("Test 2: Generating 'BOARD' logo (has B, O, A, R, D with holes)")
    print("="*60)
    
    logo2 = MeshedLogo()
    logo2.set_canvas(2000, 400)
    logo2.generate(
        text="BOARD",
        output_file=os.path.join(output_dir, 'board_logo.png'),
        colors=['cyan', 'magenta'],
        scale=1.3,
        mesh_density=1.2
    )
    print("✓ BOARD logo generated!")
    
    # Test 3: The classic MEMA logo
    print("\n" + "="*60)
    print("Test 3: Generating 'MEMA' logo (has A with hole)")
    print("="*60)
    
    logo3 = MeshedLogo()
    logo3.set_canvas(1600, 400)
    logo3.generate(
        text="MEMA",
        output_file=os.path.join(output_dir, 'mema_logo_fixed.png'),
        colors=['magenta', 'cyan', 'magenta', 'yellow'],
        scale=1.5,
        mesh_density=1.5
    )
    print("✓ MEMA logo generated!")
    
    print("\n" + "="*60)
    print("✓ All logo generation tests complete!")
    print("="*60)
    print(f"\nOutput files in: {output_dir}/")
    print("  - road_logo.png")
    print("  - board_logo.png")
    print("  - mema_logo_fixed.png")
    print()


if __name__ == '__main__':
    main()
