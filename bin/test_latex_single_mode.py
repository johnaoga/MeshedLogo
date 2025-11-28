#!/usr/bin/env python3
"""
Test LaTeX Rendering in SINGLE Mode
Demonstrates proper formula rendering using matplotlib's LaTeX engine
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.string_processor import RenderMode, StringProcessor


def test_1_latex_fraction():
    """Test 1: Fraction with horizontal bar using \\frac"""
    print("\n" + "="*60)
    print("Test 1: LaTeX Fraction - \\frac{a}{b} (SINGLE mode)")
    print("="*60)
    processor = StringProcessor()
    
    # Process in SINGLE mode
    processed = processor.process(
        '$\\frac{a}{b}$',
        mode=RenderMode.SINGLE,
        width=400,
        height=400
    )
    
    # Save the rendered image
    os.makedirs('output', exist_ok=True)
    if processed.images:
        processed.images[0].save('output/test_latex_fraction_single.png')
        print("✓ Generated: output/test_latex_fraction_single.png")
        print("  Expected: Proper fraction with 'a' above horizontal bar, 'b' below")
    else:
        print("❌ No images generated")


def test_2_complex_formula():
    """Test 2: Complex formula with multiple operations"""
    print("\n" + "="*60)
    print("Test 2: Complex Formula - e^{i\\theta} = \\cos\\theta + i\\sin\\theta")
    print("="*60)
    
    processor = StringProcessor()
    
    # Process Euler's formula in SINGLE mode
    processed = processor.process(
        '$e^{i\\theta} = \\cos\\theta + i\\sin\\theta$',
        mode=RenderMode.SINGLE,
        width=800,
        height=300
    )
    
    os.makedirs('output', exist_ok=True)
    if processed.images:
        processed.images[0].save('output/test_euler_formula_single.png')
        print("✓ Generated: output/test_euler_formula_single.png")
        print("  Expected: Properly formatted Euler's formula")
    else:
        print("❌ No images generated")


def test_3_sqrt_and_powers():
    """Test 3: Square root and powers"""
    print("\n" + "="*60)
    print("Test 3: Square Root - \\frac{\\sqrt{x^2 + y^2}}{z}")
    print("="*60)
    
    processor = StringProcessor()
    
    processed = processor.process(
        '$\\frac{\\sqrt{x^2 + y^2}}{z}$',
        mode=RenderMode.SINGLE,
        width=600,
        height=400
    )
    
    os.makedirs('output', exist_ok=True)
    if processed.images:
        processed.images[0].save('output/test_sqrt_formula_single.png')
        print("✓ Generated: output/test_sqrt_formula_single.png")
        print("  Expected: Fraction with square root in numerator")
    else:
        print("❌ No images generated")


def test_4_individual_vs_single():
    """Test 4: Compare INDIVIDUAL vs SINGLE mode for same formula"""
    print("\n" + "="*60)
    print("Test 4: INDIVIDUAL vs SINGLE Mode - $x^2 + y^2$")
    print("="*60)
    
    processor = StringProcessor()
    
    # INDIVIDUAL mode (our custom parser)
    processed_individual = processor.process(
        '$x^2 + y^2$',
        mode=RenderMode.INDIVIDUAL,
        width=200,
        height=200
    )
    
    # SINGLE mode (matplotlib LaTeX)
    processed_single = processor.process(
        '$x^2 + y^2$',
        mode=RenderMode.SINGLE,
        width=600,
        height=300
    )
    
    os.makedirs('output', exist_ok=True)
    
    # Save INDIVIDUAL mode result (first few characters)
    if processed_individual.images:
        for i, img in enumerate(processed_individual.images[:5]):
            img.save(f'output/test_compare_individual_{i}.png')
        print(f"✓ Generated INDIVIDUAL mode: {len(processed_individual.images)} separate characters")
    
    # Save SINGLE mode result
    if processed_single.images:
        processed_single.images[0].save('output/test_compare_single.png')
        print("✓ Generated SINGLE mode: 1 complete formula image")
    
    print("  Expected: INDIVIDUAL = multiple meshes, SINGLE = one formatted image")


def main():
    """Run all LaTeX SINGLE mode tests"""
    print("\n" + "*"*60)
    print("*" + " LaTeX SINGLE Mode Tests ".center(58) + "*")
    print("*"*60)
    
    os.makedirs('output', exist_ok=True)
    
    try:
        test_1_latex_fraction()
        test_2_complex_formula()
        test_3_sqrt_and_powers()
        test_4_individual_vs_single()
        
        print("\n" + "="*60)
        print("All LaTeX SINGLE mode tests completed! ✓")
        print("Check the 'output/' directory for generated files.")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
