#!/usr/bin/env python3
"""
Generate Logo - Simple command-line interface for logo generation
Usage: python bin/generate_logo.py [TEXT] [OUTPUT_FILE]
"""

import sys
import os
import random
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meshed_logo import MeshedLogo


def main():
    """Main entry point"""
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Parse arguments
    if len(sys.argv) > 1:
        text = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else f'output/{text.lower()}_logo.png'
    else:
        text = "LOGO"
        output_file = "output/logo.png"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else 'output', exist_ok=True)
    
    # Create logo
    logo = MeshedLogo()
    
    print(f"Generating meshed logo for: '{text}'")
    result_file = logo.generate(
        text=text,
        output_file=output_file,
        colors=['cyan', 'magenta', 'yellow', 'white'],
        scale=2.0,
        mesh_density=1.5
    )
    
    print(f"✓ Logo saved to: {result_file}")


if __name__ == "__main__":
    main()
