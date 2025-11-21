#!/usr/bin/env python3
"""
Simple Examples - Basic usage of MeshedLogo class
"""

import sys
import os
import random
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meshed_logo import MeshedLogo


def example_1_simple_text():
    """Example 1: Generate simple text logo"""
    print("\n" + "="*60)
    print("Example 1: Simple Text Logo")
    print("="*60)
    
    logo = MeshedLogo()
    output = logo.generate("HELLO", output_file="output/hello_logo.png")
    print(f"✓ Generated: {output}")


def example_2_custom_colors():
    """Example 2: Custom colors"""
    print("\n" + "="*60)
    print("Example 2: Custom Colors")
    print("="*60)
    
    logo = MeshedLogo()
    output = logo.generate(
        "CODE",
        output_file="output/code_logo.png",
        colors=['#00ff00', '#00ffff', '#ff00ff'],  # Green, Cyan, Magenta
        scale=2.5
    )
    print(f"✓ Generated: {output}")


def example_3_multi_component():
    """Example 3: Multi-component logo"""
    print("\n" + "="*60)
    print("Example 3: Multi-Component Logo")
    print("="*60)
    
    logo = MeshedLogo(canvas_size=(1400, 700))
    
    components = [
        {
            'text': 'MESHED',
            'position': (100, 400),
            'scale': 2.5,
            'colors': ['cyan', 'magenta'],
            'mesh_density': 2.0
        },
        {
            'text': 'LOGO',
            'position': (800, 400),
            'scale': 2.5,
            'colors': ['yellow', 'white'],
            'mesh_density': 2.0
        }
    ]
    
    output = logo.generate_multi(
        components=components,
        name="Meshed Logo",
        output_file="output/meshed_logo_multi.png"
    )
    print(f"✓ Generated: {output}")


def example_4_mema_inma():
    """Example 4: MEMA & INMA classic logo"""
    print("\n" + "="*60)
    print("Example 4: MEMA & INMA Logo")
    print("="*60)
    
    logo = MeshedLogo()
    output = logo.generate_mema_inma(output_file="mema_inma_final.png")
    print(f"✓ Generated: {output}")


def example_5_different_backgrounds():
    """Example 5: Different background colors"""
    print("\n" + "="*60)
    print("Example 5: Different Backgrounds")
    print("="*60)
    
    backgrounds = [
        ('black', 'output/bg_black.png'),
        ('#0a0a0a', 'output/bg_dark.png'),
        ('#1a1a2e', 'output/bg_navy.png')
    ]
    
    for bg_color, output_file in backgrounds:
        logo = MeshedLogo(background_color=bg_color)
        logo.generate("MESH", output_file=output_file, scale=2.0)
        print(f"✓ Generated {bg_color}: {output_file}")


def main():
    """Run all examples"""
    print("\n" + "*"*60)
    print("*" + " MeshedLogo - Simple Examples ".center(58) + "*")
    print("*"*60)
    
    # Set random seed
    random.seed(42)
    np.random.seed(42)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    try:
        example_1_simple_text()
        example_2_custom_colors()
        example_3_multi_component()
        example_4_mema_inma()
        example_5_different_backgrounds()
        
        print("\n" + "="*60)
        print("All examples completed! ✓")
        print("Check the 'output/' directory for generated files.")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
