#!/usr/bin/env python3
"""
Debug Contour Extraction
Visualize each step of the contour extraction process to identify issues
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.character_renderer import CharacterRenderer
from lib.contour_extractor import ContourExtractor


def debug_character_contour(character: str, output_dir: str = 'debug_output'):
    """
    Debug contour extraction for a single character
    
    Args:
        character: Character to debug
        output_dir: Output directory for debug visualizations
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"Debugging contour extraction for: '{character}'")
    print(f"{'='*60}\n")
    
    # Step 1: Render character
    print("Step 1: Rendering character...")
    renderer = CharacterRenderer(default_width=200, default_height=200)
    char_img = renderer.render(character)
    
    print(f"  - Character matrix shape: {char_img.matrix.shape}")
    print(f"  - Matrix data type: {char_img.matrix.dtype}")
    print(f"  - Matrix value range: [{char_img.matrix.min()}, {char_img.matrix.max()}]")
    print(f"  - Unique values: {np.unique(char_img.matrix)}")
    
    # Save rendered character as PNG
    char_png_path = os.path.join(output_dir, f'{character}_1_rendered.png')
    char_img.save(char_png_path)
    print(f"  - Saved rendered character to: {char_png_path}")
    
    # Visualize the binary matrix
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle(f"Contour Extraction Debug: '{character}'", fontsize=16)
    
    # Plot 1: Original rendered matrix
    axes[0, 0].imshow(char_img.matrix, cmap='gray')
    axes[0, 0].set_title('1. Rendered Matrix\n(0=char, 1=background)')
    axes[0, 0].axis('off')
    
    # Step 2: Extract contour
    print("\nStep 2: Extracting contour...")
    extractor = ContourExtractor(method='opencv')
    
    # Get all contours first
    all_contours = extractor.extract(char_img.matrix, threshold=127, simplify=False)
    print(f"  - Total contours found: {len(all_contours)}")
    
    for i, contour in enumerate(all_contours):
        print(f"    Contour {i}: {contour.num_points} points, "
              f"bbox: {contour.get_bounding_box()}")
    
    # Get largest contour
    largest_contour = extractor.extract_largest(char_img.matrix, threshold=127, simplify=False)
    
    if largest_contour:
        print(f"\n  - Largest contour has {largest_contour.num_points} points")
        print(f"  - Bounding box: {largest_contour.get_bounding_box()}")
        print(f"  - Is closed: {largest_contour.is_closed}")
        
        # Save contour points
        contour_txt_path = os.path.join(output_dir, f'{character}_2_contour.txt')
        largest_contour.save_points(contour_txt_path)
        print(f"  - Saved contour points to: {contour_txt_path}")
        
        # Save contour visualization
        contour_png_path = os.path.join(output_dir, f'{character}_2_contour.png')
        largest_contour.save_points(contour_png_path)
        print(f"  - Saved contour visualization to: {contour_png_path}")
        
        # Plot 2: Binarized image (as OpenCV sees it)
        binary = extractor._binarize(char_img.matrix, 127)
        axes[0, 1].imshow(binary, cmap='gray')
        axes[0, 1].set_title('2. Binarized Image\n(255=char, 0=background)')
        axes[0, 1].axis('off')
        
        # Plot 3: All contours
        axes[0, 2].imshow(char_img.matrix, cmap='gray', alpha=0.3)
        # Find index of largest contour by comparing number of points
        largest_idx = all_contours.index(max(all_contours, key=lambda c: c.num_points))
        for i, contour in enumerate(all_contours):
            if contour.is_closed:
                plot_points = np.vstack([contour.points, contour.points[0]])
            else:
                plot_points = contour.points
            color = 'red' if i == largest_idx else 'blue'
            axes[0, 2].plot(plot_points[:, 0], plot_points[:, 1], 
                          color=color, linewidth=2, alpha=0.7)
        axes[0, 2].set_title(f'3. All Contours ({len(all_contours)})\n(red=largest)')
        axes[0, 2].axis('off')
        axes[0, 2].invert_yaxis()
        
        # Plot 4: Largest contour with points
        axes[1, 0].imshow(char_img.matrix, cmap='gray', alpha=0.3)
        if largest_contour.is_closed:
            plot_points = np.vstack([largest_contour.points, largest_contour.points[0]])
        else:
            plot_points = largest_contour.points
        axes[1, 0].plot(plot_points[:, 0], plot_points[:, 1], 
                       'b-', linewidth=2, label='Contour')
        axes[1, 0].scatter(largest_contour.points[:, 0], largest_contour.points[:, 1],
                         c='red', s=10, zorder=5, label='Points')
        axes[1, 0].set_title(f'4. Largest Contour\n({largest_contour.num_points} points)')
        axes[1, 0].legend()
        axes[1, 0].axis('off')
        axes[1, 0].invert_yaxis()
        
        # Step 3: Simplify contour
        print("\nStep 3: Simplifying contour...")
        simplified_contour = largest_contour.simplify(epsilon=3.0)
        print(f"  - Simplified to {simplified_contour.num_points} points")
        
        # Plot 5: Simplified contour
        axes[1, 1].imshow(char_img.matrix, cmap='gray', alpha=0.3)
        if simplified_contour.is_closed:
            plot_points = np.vstack([simplified_contour.points, simplified_contour.points[0]])
        else:
            plot_points = simplified_contour.points
        axes[1, 1].plot(plot_points[:, 0], plot_points[:, 1], 
                       'g-', linewidth=2, label='Simplified')
        axes[1, 1].scatter(simplified_contour.points[:, 0], simplified_contour.points[:, 1],
                         c='red', s=15, zorder=5, label='Points')
        axes[1, 1].set_title(f'5. Simplified Contour\n({simplified_contour.num_points} points)')
        axes[1, 1].legend()
        axes[1, 1].axis('off')
        axes[1, 1].invert_yaxis()
        
        # Plot 6: Contour statistics
        axes[1, 2].axis('off')
        stats_text = f"""
Contour Statistics:
━━━━━━━━━━━━━━━━━
Character: '{character}'
Image Size: {char_img.matrix.shape}

Original Points: {largest_contour.num_points}
Simplified Points: {simplified_contour.num_points}
Reduction: {100 * (1 - simplified_contour.num_points / largest_contour.num_points):.1f}%

Bounding Box:
  x: [{largest_contour.get_bounding_box()[0]}, {largest_contour.get_bounding_box()[2]}]
  y: [{largest_contour.get_bounding_box()[1]}, {largest_contour.get_bounding_box()[3]}]

Is Closed: {largest_contour.is_closed}
Total Contours Found: {len(all_contours)}
        """
        axes[1, 2].text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                       verticalalignment='center')
        
        # Save debug visualization
        debug_path = os.path.join(output_dir, f'{character}_debug_full.png')
        plt.tight_layout()
        plt.savefig(debug_path, dpi=150, bbox_inches='tight')
        print(f"\n  - Saved full debug visualization to: {debug_path}")
        plt.close()
        
        print(f"\n{'='*60}")
        print("✓ Debug complete!")
        print(f"{'='*60}\n")
        
        return largest_contour, simplified_contour
        
    else:
        print("  ✗ ERROR: No contour found!")
        plt.close()
        return None, None


def debug_multiple_characters(characters: str = "MEINMA", output_dir: str = 'debug_output'):
    """Debug contour extraction for multiple characters"""
    print(f"\nDebugging {len(characters)} characters: {characters}")
    
    for char in characters:
        debug_character_contour(char, output_dir)
        print("\n")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Debug contour extraction')
    parser.add_argument('--char', type=str, default='M',
                       help='Character to debug (default: M)')
    parser.add_argument('--all', type=str, default=None,
                       help='Debug all characters in string (e.g., MEMA)')
    parser.add_argument('--output', type=str, default='debug_output',
                       help='Output directory for debug files')
    
    args = parser.parse_args()
    
    if args.all:
        debug_multiple_characters(args.all, args.output)
    else:
        debug_character_contour(args.char, args.output)
