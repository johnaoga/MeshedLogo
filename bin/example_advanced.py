"""
Example Usage Script
Demonstrates how to use the logo generation system
"""

import random
import numpy as np
from character_renderer import CharacterRenderer
from string_processor import StringProcessor
from contour_extractor import ContourExtractor
from mesh_generator import MeshGenerator
from logo_generator import LogoGenerator


def example_1_render_single_character():
    """Example 1: Render a single character to binary image"""
    print("=" * 60)
    print("Example 1: Render Single Character")
    print("=" * 60)
    
    renderer = CharacterRenderer(default_width=300, default_height=300, default_thickness=2)
    
    # Render letter 'M'
    m_image = renderer.render('M', save_path='output/example_1_m.png')
    print(f"✓ Rendered 'M': shape={m_image.shape}, saved to {m_image.filepath}")
    
    # Render a symbol
    symbol_image = renderer.render('∞', width=250, height=250, save_path='output/example_1_infinity.png')
    print(f"✓ Rendered '∞': shape={symbol_image.shape}, saved to {symbol_image.filepath}")
    
    print()


def example_2_process_string():
    """Example 2: Process a string to multiple character images"""
    print("=" * 60)
    print("Example 2: Process String to Character Images")
    print("=" * 60)
    
    processor = StringProcessor()
    
    # Process plain text
    result = processor.process("HELLO", save_dir="output/example_2_hello")
    print(f"✓ Processed 'HELLO': {len(result.images)} characters")
    print(f"  Saved to: output/example_2_hello/")
    
    # Process with custom sizes
    result2 = processor.process("XYZ", width=150, height=150, thickness=3,
                               save_dir="output/example_2_xyz")
    print(f"✓ Processed 'XYZ': {len(result2.images)} characters with custom size")
    
    print()


def example_3_extract_contours():
    """Example 3: Extract contours from an image"""
    print("=" * 60)
    print("Example 3: Extract Contours from Image")
    print("=" * 60)
    
    # Create a character image
    renderer = CharacterRenderer(default_width=300, default_height=300)
    char_img = renderer.render('A', save_path='output/example_3_a.png')
    
    # Extract contours
    extractor = ContourExtractor(method='opencv')
    contours = extractor.extract(char_img.matrix, threshold=127, simplify=True, epsilon=2.0)
    
    print(f"✓ Extracted {len(contours)} contours from 'A'")
    for i, contour in enumerate(contours):
        print(f"  Contour {i}: {contour.num_points} points, bbox={contour.get_bounding_box()}")
    
    # Save largest contour points
    largest = extractor.extract_largest(char_img.matrix, simplify=True)
    if largest:
        largest.save_points('output/example_3_contour_points.txt')
        print(f"✓ Saved largest contour ({largest.num_points} points) to output/example_3_contour_points.txt")
    
    print()


def example_4_generate_mesh():
    """Example 4: Generate mesh from points"""
    print("=" * 60)
    print("Example 4: Generate Mesh from Points")
    print("=" * 60)
    
    # Create character and extract contour
    renderer = CharacterRenderer(default_width=300, default_height=300)
    char_img = renderer.render('S')
    
    extractor = ContourExtractor(method='opencv')
    contour = extractor.extract_largest(char_img.matrix, simplify=True, epsilon=3.0)
    
    if contour:
        print(f"✓ Extracted contour with {contour.num_points} points")
        
        # Generate mesh
        generator = MeshGenerator(method='delaunay')
        mesh = generator.generate(contour.points, add_interior_points=True,
                                 num_interior_points=50)
        
        print(f"✓ Generated mesh: {mesh.num_vertices} vertices, {mesh.num_triangles} triangles")
        
        # Visualize
        generator.visualize(mesh, output_file='output/example_4_mesh_s.png',
                          show_edges=True, show_vertices=True,
                          color_scheme='gradient')
        print(f"✓ Saved mesh visualization to output/example_4_mesh_s.png")
        
        # Save mesh data
        mesh.save_mesh('output/example_4_mesh_s.obj', format='obj')
        print(f"✓ Saved mesh data to output/example_4_mesh_s.obj")
        
        # Calculate mesh statistics
        areas = mesh.get_triangle_areas()
        print(f"  Triangle area stats: min={areas.min():.2f}, max={areas.max():.2f}, mean={areas.mean():.2f}")
    
    print()


def example_5_complete_logo():
    """Example 5: Generate complete logo using all components"""
    print("=" * 60)
    print("Example 5: Generate Complete Logo")
    print("=" * 60)
    
    # Create logo generator
    generator = LogoGenerator(
        canvas_size=(1200, 800),
        background_color='black',
        default_char_size=(200, 200)
    )
    
    # Generate MEMA & INMA logo
    print("Generating MEMA & INMA logo...")
    mema_logo = generator.create_mema_inma_logo(
        output_file='example_5_mema_inma.png',
        output_dir='output'
    )
    print(f"✓ MEMA & INMA logo generated: {len(mema_logo.components)} components")
    print(f"  Saved to: output/example_5_mema_inma.png")
    
    # Generate simple text logo
    print("\nGenerating simple text logo...")
    text_logo = generator.create_simple_text_logo(
        text='LOGO',
        output_file='output/example_5_logo.png',
        color_scheme=['cyan', 'magenta', 'yellow', 'white']
    )
    print(f"✓ Text logo 'LOGO' generated: {len(text_logo.components)} components")
    print(f"  Saved to: output/example_5_logo.png")
    
    print()


def example_6_custom_logo():
    """Example 6: Create custom logo with specific configuration"""
    print("=" * 60)
    print("Example 6: Create Custom Logo")
    print("=" * 60)
    
    generator = LogoGenerator(canvas_size=(1000, 600), background_color='#0a0a0a')
    
    # Define custom components
    components_config = [
        {
            'text': 'CODE',
            'position': (100, 300),
            'scale': 2.5,
            'colors': ['#00ff00', '#00ffff'],  # Green to cyan gradient
            'is_formula': False,
            'mesh_density': 2.0
        },
        {
            'text': '∞',
            'position': (700, 300),
            'scale': 2.0,
            'colors': ['#ff00ff', '#ffff00'],  # Magenta to yellow
            'is_formula': False,
            'mesh_density': 1.5
        }
    ]
    
    # Create logo
    logo = generator.create_logo('Custom Logo', components_config)
    
    # Render
    generator.render_logo(logo, 'output/example_6_custom.png',
                         show_wireframe=True, show_vertices=True,
                         show_gradient=True, dpi=300)
    
    print(f"✓ Custom logo generated with {len(logo.components)} components")
    print(f"  Saved to: output/example_6_custom.png")
    
    # Save metadata
    logo.save_metadata('output/example_6_metadata.txt')
    print(f"✓ Metadata saved to: output/example_6_metadata.txt")
    
    print()


def example_7_mesh_refinement():
    """Example 7: Mesh refinement and manipulation"""
    print("=" * 60)
    print("Example 7: Mesh Refinement")
    print("=" * 60)
    
    # Create simple shape
    renderer = CharacterRenderer(default_width=250, default_height=250)
    char_img = renderer.render('O')  # Circle-like shape
    
    extractor = ContourExtractor()
    contour = extractor.extract_largest(char_img.matrix, simplify=True)
    
    if contour:
        generator = MeshGenerator()
        
        # Generate coarse mesh
        coarse_mesh = generator.generate(contour.points, add_interior_points=True,
                                        num_interior_points=20)
        print(f"✓ Coarse mesh: {coarse_mesh.num_vertices} vertices, {coarse_mesh.num_triangles} triangles")
        
        # Visualize coarse mesh
        generator.visualize(coarse_mesh, output_file='output/example_7_coarse.png',
                          color_scheme='alternating')
        print(f"  Saved to: output/example_7_coarse.png")
        
        # Refine mesh
        refined_mesh = generator.refine_mesh(coarse_mesh, max_area=30.0)
        print(f"✓ Refined mesh: {refined_mesh.num_vertices} vertices, {refined_mesh.num_triangles} triangles")
        
        # Visualize refined mesh
        generator.visualize(refined_mesh, output_file='output/example_7_refined.png',
                          color_scheme='alternating')
        print(f"  Saved to: output/example_7_refined.png")
        
        # Get edge information
        edges = refined_mesh.get_edges()
        print(f"  Number of unique edges: {len(edges)}")
    
    print()


def main():
    """Run all examples"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  Logo Generation System - Example Usage".center(58) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")
    
    # Set random seed for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    # Create output directory
    import os
    os.makedirs('output', exist_ok=True)
    
    # Run examples
    try:
        example_1_render_single_character()
        example_2_process_string()
        example_3_extract_contours()
        example_4_generate_mesh()
        example_5_complete_logo()
        example_6_custom_logo()
        example_7_mesh_refinement()
        
        print("=" * 60)
        print("All examples completed successfully! ✓")
        print("Check the 'output/' directory for generated files.")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
