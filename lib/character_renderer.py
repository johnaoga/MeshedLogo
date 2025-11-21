"""
Character Renderer Module
Renders letters/symbols to binary image matrices with configurable size and thickness
"""

from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os


@dataclass
class CharacterImage:
    """Data class to hold character image data"""
    matrix: np.ndarray
    character: str
    width: int
    height: int
    thickness: int
    filepath: Optional[str] = None
    
    def save(self, filepath: str) -> str:
        """Save the binary image to file"""
        # Convert binary matrix to PIL Image (0->black, 1->white)
        img_array = (self.matrix * 255).astype(np.uint8)
        img = Image.fromarray(img_array, mode='L')
        img.save(filepath)
        self.filepath = filepath
        return filepath
    
    @property
    def shape(self) -> Tuple[int, int]:
        """Return shape of the image matrix"""
        return self.matrix.shape


class CharacterRenderer:
    """
    Renders letters and symbols to binary image matrices
    """
    
    def __init__(self, default_width: int = 200, default_height: int = 200, 
                 default_thickness: int = 2):
        """
        Initialize the character renderer
        
        Args:
            default_width: Default image width in pixels
            default_height: Default image height in pixels
            default_thickness: Default stroke thickness (font weight factor)
        """
        self.default_width = default_width
        self.default_height = default_height
        self.default_thickness = default_thickness
        
    def render(self, character: str, width: Optional[int] = None, 
               height: Optional[int] = None, thickness: Optional[int] = None,
               save_path: Optional[str] = None) -> CharacterImage:
        """
        Render a character to a binary image matrix
        
        Args:
            character: Letter or symbol to render
            width: Image width (uses default if None)
            height: Image height (uses default if None)
            thickness: Stroke thickness (uses default if None)
            save_path: Optional path to save the image
            
        Returns:
            CharacterImage object containing the binary matrix and metadata
        """
        w = width or self.default_width
        h = height or self.default_height
        t = thickness or self.default_thickness
        
        # Create a white image
        img = Image.new('L', (w, h), color=255)
        draw = ImageDraw.Draw(img)
        
        # Try to load a font with appropriate size
        font_size = min(w, h) - 20
        font = self._get_font(font_size, t)
        
        # Get text bounding box to center it
        bbox = draw.textbbox((0, 0), character, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position to center the text
        x = (w - text_width) // 2 - bbox[0]
        y = (h - text_height) // 2 - bbox[1]
        
        # Draw the character in black
        draw.text((x, y), character, fill=0, font=font)
        
        # Convert to numpy array and normalize to binary (0 or 1)
        # 0 = black (character), 1 = white (background)
        matrix = np.array(img)
        binary_matrix = (matrix > 127).astype(np.uint8)
        
        # Create CharacterImage object
        char_img = CharacterImage(
            matrix=binary_matrix,
            character=character,
            width=w,
            height=h,
            thickness=t
        )
        
        # Save if path is provided
        if save_path:
            char_img.save(save_path)
        
        return char_img
    
    def render_custom(self, character: str, points: np.ndarray, 
                     width: int, height: int, thickness: int = 1,
                     save_path: Optional[str] = None) -> CharacterImage:
        """
        Render a character from custom point coordinates
        
        Args:
            character: The character being rendered
            points: Array of (x, y) coordinates defining the character shape
            width: Image width
            height: Image height
            thickness: Line thickness for drawing
            save_path: Optional path to save the image
            
        Returns:
            CharacterImage object containing the binary matrix
        """
        # Create a white image
        img = Image.new('L', (width, height), color=255)
        draw = ImageDraw.Draw(img)
        
        # Normalize points to image dimensions
        if len(points) > 0:
            points_array = np.array(points)
            min_x, min_y = points_array.min(axis=0)
            max_x, max_y = points_array.max(axis=0)
            
            # Scale points to fit in image with some padding
            padding = 20
            scale_x = (width - 2 * padding) / (max_x - min_x) if max_x > min_x else 1
            scale_y = (height - 2 * padding) / (max_y - min_y) if max_y > min_y else 1
            scale = min(scale_x, scale_y)
            
            # Transform points
            transformed_points = []
            for x, y in points_array:
                new_x = (x - min_x) * scale + padding
                new_y = height - ((y - min_y) * scale + padding)  # Flip y-axis
                transformed_points.append((new_x, new_y))
            
            # Draw lines connecting the points
            if len(transformed_points) > 1:
                for i in range(len(transformed_points) - 1):
                    draw.line([transformed_points[i], transformed_points[i + 1]], 
                             fill=0, width=thickness)
                
                # Draw points as circles
                for point in transformed_points:
                    r = thickness + 1
                    draw.ellipse([point[0]-r, point[1]-r, point[0]+r, point[1]+r], 
                               fill=0)
        
        # Convert to binary matrix
        matrix = np.array(img)
        binary_matrix = (matrix > 127).astype(np.uint8)
        
        # Create CharacterImage object
        char_img = CharacterImage(
            matrix=binary_matrix,
            character=character,
            width=width,
            height=height,
            thickness=thickness
        )
        
        # Save if path is provided
        if save_path:
            char_img.save(save_path)
        
        return char_img
    
    def _get_font(self, size: int, thickness: int) -> ImageFont.FreeTypeFont:
        """
        Get an appropriate font for rendering
        
        Args:
            size: Font size
            thickness: Thickness factor (affects font weight)
            
        Returns:
            ImageFont object
        """
        # Try to load a system font
        font_names = [
            # macOS fonts
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            # Common Linux fonts
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            # Windows fonts
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\calibri.ttf",
        ]
        
        for font_path in font_names:
            if os.path.exists(font_path):
                try:
                    return ImageFont.truetype(font_path, size)
                except Exception:
                    continue
        
        # Fall back to default font
        return ImageFont.load_default()


