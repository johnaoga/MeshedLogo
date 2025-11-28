#!/usr/bin/env python3
"""Test hole extraction for formulas - visualize what's being extracted"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from lib.string_processor import StringProcessor, RenderMode
from lib.contour_extractor import ContourExtractor
from meshed_logo import MeshedLogo

output_dir = 'test_output/formula_holes'
os.makedirs(output_dir, exist_ok=True)

def visualize_extraction(formula, filename):
    """Visualize the shape and hole extraction for a formula"""
    print(f"\n{'='*60}")
    print(f"Testing: {formula}")
    print('='*60)
    
    # Process the formula
    processor = StringProcessor()
    processed = processor.process(formula, mode=RenderMode.INDIVIDUAL, width=400, height=400)
    
    print(f"Number of images: {len(processed.images)}")
    print(f"Characters: {processed.characters}")
    
    # Get the formula image
    char_img = processed.images[0]
    
    # Save the raw image
    char_img.save(os.path.join(output_dir, f'{filename}_raw.png'))
    
    # Extract all shapes with holes
    extractor = ContourExtractor()
    all_shapes = extractor.extract_all_shapes_with_openings(
        char_img.matrix, threshold=127, simplify=True, epsilon=3.0, min_area=50
    )
    
    print(f"Found {len(all_shapes)} shapes")
    
    # Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Original image with contours overlaid
    ax1 = axes[0]
    ax1.imshow(1 - char_img.matrix, cmap='gray', origin='upper')
    ax1.set_title(f'Original Image: {formula}')
    
    colors = plt.cm.rainbow(np.linspace(0, 1, max(len(all_shapes), 1)))
    
    for i, (contour, holes) in enumerate(all_shapes):
        # Plot contour
        pts = contour.points
        pts_closed = np.vstack([pts, pts[0]])  # Close the contour
        ax1.plot(pts_closed[:, 0], pts_closed[:, 1], '-', 
                color=colors[i], linewidth=2, label=f'Shape {i+1}')
        
        # Plot holes
        for j, hole in enumerate(holes):
            hole_pts = hole.points
            hole_closed = np.vstack([hole_pts, hole_pts[0]])
            ax1.plot(hole_closed[:, 0], hole_closed[:, 1], '--', 
                    color=colors[i], linewidth=1.5, alpha=0.7)
        
        print(f"  Shape {i+1}: {contour.num_points} pts, {len(holes)} holes, "
              f"x=[{pts[:, 0].min():.0f}-{pts[:, 0].max():.0f}]")
    
    ax1.legend(loc='upper right', fontsize=8)
    ax1.set_xlim(0, char_img.width)
    ax1.set_ylim(char_img.height, 0)
    
    # Right: Shapes filled with different colors
    ax2 = axes[1]
    ax2.set_facecolor('black')
    ax2.set_title(f'Extracted Shapes ({len(all_shapes)} found)')
    
    for i, (contour, holes) in enumerate(all_shapes):
        # Fill the shape
        pts = contour.points
        ax2.fill(pts[:, 0], pts[:, 1], color=colors[i], alpha=0.6)
        ax2.plot(np.append(pts[:, 0], pts[0, 0]), 
                np.append(pts[:, 1], pts[0, 1]), 
                color=colors[i], linewidth=2)
        
        # Mark holes
        for hole in holes:
            hole_pts = hole.points
            ax2.fill(hole_pts[:, 0], hole_pts[:, 1], color='black', alpha=0.8)
            ax2.plot(np.append(hole_pts[:, 0], hole_pts[0, 0]),
                    np.append(hole_pts[:, 1], hole_pts[0, 1]),
                    color='white', linewidth=1, linestyle='--')
    
    ax2.set_xlim(0, char_img.width)
    ax2.set_ylim(char_img.height, 0)
    ax2.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{filename}_analysis.png'), dpi=150)
    plt.close()
    
    print(f"  Saved: {filename}_analysis.png")
    
    return len(all_shapes)

# Test various formulas
print("\n" + "="*60)
print("FORMULA HOLE EXTRACTION TEST")
print("="*60)

formulas = [
    ("$E=mc^2$", "einstein"),
    ("$e^{i\\theta}$", "euler"),
    ("$\\frac{a}{b}$", "fraction"),
    ("$x_1 + y_2$", "subscripts"),
]

for formula, name in formulas:
    num_shapes = visualize_extraction(formula, name)

# Now generate actual logos
print("\n" + "="*60)
print("GENERATING LOGOS")
print("="*60)

logo = MeshedLogo(canvas_size=(1200, 600))

for formula, name in formulas:
    output_file = os.path.join(output_dir, f'{name}_logo.png')
    logo.generate(
        formula,
        output_file=output_file,
        colors=['cyan', 'magenta', 'yellow', 'white'],
        scale=2.5
    )
    print(f"✓ Generated: {name}_logo.png")

print("\n" + "="*60)
print(f"Check {output_dir}/ for:")
print("  - *_raw.png: Raw rendered formula image")
print("  - *_analysis.png: Contour and hole visualization")
print("  - *_logo.png: Final meshed logo")
print("="*60)
