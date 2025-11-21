#!/usr/bin/env python3
"""
Test mesh generation with holes
Verify that interior points respect character boundaries and holes
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.character_renderer import CharacterRenderer
from lib.contour_extractor import ContourExtractor
from lib.mesh_generator import MeshGenerator


def test_character_with_hole(character: str, output_dir: str = 'test_output'):
    """
    Test mesh generation for a character with holes
    
    Args:
        character: Character to test (e.g., 'A', 'O', 'P', 'R', 'D')
        output_dir: Output directory for test visualizations
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Testing mesh generation with holes for: '{character}'")
    print(f"{'='*60}\n")
    
    # Step 1: Render character
    print("Step 1: Rendering character...")
    renderer = CharacterRenderer(default_width=300, default_height=300)
    char_img = renderer.render(character)
    print(f"  - Character rendered: {char_img.matrix.shape}")
    
    # Step 2: Extract contours WITH openings detection
    print("\nStep 2: Extracting contours with openings detection...")
    extractor = ContourExtractor(method='opencv')
    
    # New method: detects traditional holes AND openings
    largest_contour, all_holes = extractor.extract_with_openings(
        char_img.matrix, threshold=127, simplify=True, epsilon=3.0
    )
    
    if not largest_contour:
        print("  ✗ No contours found!")
        return
    
    print(f"  - Largest contour: {largest_contour.num_points} points")
    print(f"  - Total gaps found (holes + openings): {len(all_holes)}")
    
    holes = []
    for i, hole in enumerate(all_holes):
        holes.append(hole.points)
        print(f"  - Gap {i+1}: {hole.num_points} points")
    
    # Step 3: Generate mesh WITHOUT pixel-accurate testing (old behavior)
    print("\nStep 3: Generating mesh WITHOUT pixel-accurate testing (old)...")
    mesh_gen = MeshGenerator()
    mesh_no_holes = mesh_gen.generate(
        largest_contour.points,
        add_interior_points=True,
        num_interior_points=50,
        holes=None,
        character_image=None  # Old: no pixel testing
    )
    print(f"  - Mesh vertices: {mesh_no_holes.num_vertices}")
    print(f"  - Mesh triangles: {mesh_no_holes.num_triangles}")
    
    # Step 4: Generate mesh WITH pixel-accurate testing (new behavior)
    print("\nStep 4: Generating mesh WITH pixel-accurate testing (new)...")
    mesh_with_holes = mesh_gen.generate(
        largest_contour.points,
        add_interior_points=True,
        num_interior_points=50,
        holes=holes if holes else None,
        character_image=char_img.matrix  # New: pixel-accurate testing
    )
    print(f"  - Mesh vertices: {mesh_with_holes.num_vertices}")
    print(f"  - Mesh triangles: {mesh_with_holes.num_triangles}")
    
    # Step 5: Visualize comparison
    print("\nStep 5: Creating visualization...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Mesh Generation Comparison: '{character}'", fontsize=16)
    
    # Plot 1: Character with contours
    axes[0].imshow(char_img.matrix, cmap='gray', alpha=0.5)
    # Plot outer contour
    outer_points = np.vstack([largest_contour.points, largest_contour.points[0]])
    axes[0].plot(outer_points[:, 0], outer_points[:, 1], 'b-', linewidth=2, label='Outer')
    axes[0].fill(outer_points[:, 0], outer_points[:, 1], 'blue', alpha=0.2)
    # Plot all gaps (holes + openings)
    for i, hole in enumerate(holes):
        hole_points = np.vstack([hole, hole[0]])
        axes[0].plot(hole_points[:, 0], hole_points[:, 1], 'r-', linewidth=2, label=f'Gap {i+1}')
        axes[0].fill(hole_points[:, 0], hole_points[:, 1], 'red', alpha=0.3)
    axes[0].set_title(f'Contours\n(1 boundary, {len(holes)} gaps)')
    axes[0].legend()
    axes[0].invert_yaxis()
    axes[0].axis('off')
    
    # Plot 2: Mesh WITHOUT holes
    axes[1].set_facecolor('black')
    axes[1].set_aspect('equal')
    for tri_indices in mesh_no_holes.triangles:
        triangle = mesh_no_holes.points[tri_indices]
        triangle_closed = np.vstack([triangle, triangle[0]])
        axes[1].plot(triangle_closed[:, 0], triangle_closed[:, 1], 
                    'cyan', linewidth=0.5, alpha=0.6)
        axes[1].fill(triangle[:, 0], triangle[:, 1], 'cyan', alpha=0.3)
    axes[1].scatter(mesh_no_holes.points[:, 0], mesh_no_holes.points[:, 1],
                   c='white', s=10, alpha=0.8, zorder=10)
    axes[1].set_title(f'WITHOUT Pixel Testing\n({mesh_no_holes.num_vertices} vertices)')
    axes[1].invert_yaxis()
    axes[1].axis('off')
    
    # Plot 3: Mesh WITH pixel-accurate testing
    axes[2].set_facecolor('black')
    axes[2].set_aspect('equal')
    for tri_indices in mesh_with_holes.triangles:
        triangle = mesh_with_holes.points[tri_indices]
        triangle_closed = np.vstack([triangle, triangle[0]])
        axes[2].plot(triangle_closed[:, 0], triangle_closed[:, 1], 
                    'cyan', linewidth=0.5, alpha=0.6)
        axes[2].fill(triangle[:, 0], triangle[:, 1], 'cyan', alpha=0.3)
    axes[2].scatter(mesh_with_holes.points[:, 0], mesh_with_holes.points[:, 1],
                   c='white', s=10, alpha=0.8, zorder=10)
    axes[2].set_title(f'WITH Pixel Testing\n({mesh_with_holes.num_vertices} vertices)')
    axes[2].invert_yaxis()
    axes[2].axis('off')
    
    # Save
    output_path = os.path.join(output_dir, f'{character}_hole_test.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"  - Saved visualization to: {output_path}")
    plt.close()
    
    print(f"\n{'='*60}")
    print("✓ Test complete!")
    print(f"{'='*60}\n")
    
    return mesh_no_holes, mesh_with_holes


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test mesh generation with holes')
    parser.add_argument('--char', type=str, default='A',
                       help='Character to test (default: A)')
    parser.add_argument('--all', action='store_true',
                       help='Test all common characters with holes')
    parser.add_argument('--output', type=str, default='test_output',
                       help='Output directory for test files')
    
    args = parser.parse_args()
    
    if args.all:
        # Test common characters with holes
        test_chars = ['A', 'B', 'D', 'O', 'P', 'Q', 'R']
        print(f"\nTesting {len(test_chars)} characters with holes: {test_chars}")
        for char in test_chars:
            test_character_with_hole(char, args.output)
    else:
        test_character_with_hole(args.char, args.output)
