#!/usr/bin/env python3
"""
Test Formula Handling - Verify new $ delimiter formula parsing
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meshed_logo import MeshedLogo


def test_1_mixed_text_formula():
    """Test 1: Mixed text and formula - m$e$sh"""
    print("\n" + "="*60)
    print("Test 1: Mixed Text and Formula - m$e$sh")
    print("="*60)
    
    logo = MeshedLogo(canvas_size=(1400, 600))
    output = logo.generate(
        "m$e$sh",
        output_file="output/test_mesh_formula.png",
        colors=['cyan', 'yellow', 'magenta'],
        scale=2.5
    )
    print(f"✓ Generated: {output}")
    print("  Expected: 'm' (text), 'e' (formula), 's', 'h' (text)")


def test_2_latex_theta():
    """Test 2: LaTeX command \\theta renders as θ using SINGLE mode"""
    print("\n" + "="*60)
    print("Test 2: LaTeX Command - $e^{i\\theta}$ (SINGLE mode)")
    print("="*60)
    
    from lib.string_processor import RenderMode
    from lib.logo_generator import LogoGenerator
    
    generator = LogoGenerator(canvas_size=(1000, 600))
    
    # Use SINGLE mode for proper LaTeX rendering
    components_config = [{
        'text': '$e^{i\\theta}$',
        'position': (300, 300),
        'scale': 2.5,
        'colors': ['yellow', 'cyan', 'white'],
        'is_formula': False,
        'mesh_density': 1.5,
        'render_mode': RenderMode.SINGLE
    }]
    
    logo = generator.create_logo('LaTeX Theta', components_config)
    output = generator.render_logo(logo, 'output/test_latex_theta.png')
    print(f"✓ Generated: {output}")
    print("  Expected: Properly formatted e^{iθ} using matplotlib LaTeX")


def test_3_simple_formula_individual():
    """Test 3: Simple formula in INDIVIDUAL mode (character-by-character)"""
    print("\n" + "="*60)
    print("Test 3: Simple Formula - $x+y$ (INDIVIDUAL mode)")
    print("="*60)
    
    logo = MeshedLogo(canvas_size=(1200, 600))
    output = logo.generate(
        "$x+y$",
        output_file="output/test_simple_individual.png",
        colors=['cyan', 'magenta', 'yellow'],
        scale=2.5
    )
    print(f"✓ Generated: {output}")
    print("  Expected: x, +, y as separate meshes (simple rendering)")


def test_4_escaped_dollar():
    """Test 4: Escaped dollar sign - price \\$5"""
    print("\n" + "="*60)
    print("Test 4: Escaped Dollar - price \\$5")
    print("="*60)
    
    logo = MeshedLogo(canvas_size=(1200, 600))
    output = logo.generate(
        "\\$5",
        output_file="output/test_escaped_dollar.png",
        colors=['green', 'white'],
        scale=2.0
    )
    print(f"✓ Generated: {output}")
    print("  Expected: Literal '$5' text (not formula)")


def test_5_fraction_single_mode():
    """Test 5: Fraction notation \\frac{a}{b} using SINGLE mode"""
    print("\n" + "="*60)
    print("Test 5: Fraction - $\\frac{a}{b}$ (SINGLE mode)")
    print("="*60)
    
    from lib.string_processor import RenderMode
    from lib.logo_generator import LogoGenerator
    
    generator = LogoGenerator(canvas_size=(1000, 600))
    
    # Use SINGLE mode for proper fraction rendering
    components_config = [{
        'text': '$\\frac{\\text{ME}}{\\text{IN}}e^{i\\theta}$',
        'position': (300, 300),
        'scale': 3.0,
        'colors': ['yellow', 'cyan', 'magenta'],
        'is_formula': False,
        'mesh_density': 1.5,
        'render_mode': RenderMode.SINGLE
    }]
    
    logo = generator.create_logo('Fraction', components_config)
    output = generator.render_logo(logo, 'output/test_fraction.png')
    print(f"✓ Generated: {output}")
    print("  Expected: Professional fraction with horizontal bar (matplotlib LaTeX)")


def test_6_einstein_single_mode():
    """Test 6: Einstein's formula using SINGLE mode"""
    print("\n" + "="*60)
    print("Test 6: Einstein Formula - E=$mc^2$ (SINGLE mode)")
    print("="*60)
    
    from lib.string_processor import RenderMode
    from lib.logo_generator import LogoGenerator
    
    generator = LogoGenerator(canvas_size=(1200, 600))
    
    # Use SINGLE mode for proper superscript rendering
    components_config = [{
        'text': '$E=mc^2$',
        'position': (300, 300),
        'scale': 2.5,
        'colors': ['white', 'yellow', 'cyan'],
        'is_formula': False,
        'mesh_density': 1.5,
        'render_mode': RenderMode.SINGLE
    }]
    
    logo = generator.create_logo('Einstein', components_config)
    output = generator.render_logo(logo, 'output/test_einstein.png')
    print(f"✓ Generated: {output}")
    print("  Expected: E=mc² properly formatted with matplotlib LaTeX")


def test_7_multi_component_formulas():
    """Test 7: Multi-component logo with formulas"""
    print("\n" + "="*60)
    print("Test 7: Multi-Component with Formulas")
    print("="*60)
    
    logo = MeshedLogo(canvas_size=(1400, 800))
    
    components = [
        {
            'text': 'ME',
            'position': (100, 500),
            'scale': 2.0,
            'colors': ['magenta', 'cyan'],
            'mesh_density': 1.5
        },
        {
            'text': '/',
            'position': (400, 400),
            'scale': 1.5,
            'colors': ['white'],
            'mesh_density': 0.5
        },
        {
            'text': 'IN',
            'position': (100, 200),
            'scale': 2.0,
            'colors': ['blue', 'cyan'],
            'mesh_density': 1.5
        },
        {
            'text': '$\\times$',
            'position': (500, 350),
            'scale': 1.2,
            'colors': ['yellow'],
            'mesh_density': 0.8
        },
        {
            'text': '$e^{i\\theta}$',
            'position': (650, 350),
            'scale': 1.8,
            'colors': ['yellow', 'white'],
            'mesh_density': 1.2
        }
    ]
    
    output = logo.generate_multi(
        components=components,
        name="MEMA & INMA",
        output_file="output/test_mema_inma_new.png"
    )
    print(f"✓ Generated: {output}")
    print("  Expected: MEMA & INMA logo with properly rendered formula")


def main():
    """Run all formula handling tests"""
    print("\n" + "*"*60)
    print("*" + " Formula Handling Tests ".center(58) + "*")
    print("*"*60)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    try:
        test_1_mixed_text_formula()
        test_2_latex_theta()
        test_3_simple_formula_individual()
        test_4_escaped_dollar()
        test_5_fraction_single_mode()
        test_6_einstein_single_mode()
        test_7_multi_component_formulas()
        
        print("\n" + "="*60)
        print("All formula tests completed! ✓")
        print("Check the 'output/' directory for generated files.")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
