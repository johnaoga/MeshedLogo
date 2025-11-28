"""
Logo Generator Module
Main orchestrator that uses all components to generate complete logos
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import os

from lib.character_renderer import CharacterRenderer, CharacterImage
from lib.string_processor import StringProcessor, RenderMode, CharacterMetadata
from lib.contour_extractor import ContourExtractor, ContourData
from lib.mesh_generator import MeshGenerator, MeshData


@dataclass
class LogoComponent:
    """Represents a single component of the logo"""
    text: str
    position: Tuple[float, float]
    scale: float
    char_images: List[CharacterImage]
    contours: List[ContourData]
    meshes: List[MeshData]
    color_scheme: List[str]
    metadata: List[CharacterMetadata] = None  # Positioning metadata for formulas


@dataclass
class Logo:
    """Complete logo data"""
    name: str
    components: List[LogoComponent]
    canvas_size: Tuple[int, int]
    background_color: str = 'black'
    
    def save_metadata(self, filepath: str):
        """Save logo metadata to file"""
        with open(filepath, 'w') as f:
            f.write(f"Logo: {self.name}\n")
            f.write(f"Canvas Size: {self.canvas_size}\n")
            f.write(f"Background: {self.background_color}\n")
            f.write(f"Components: {len(self.components)}\n\n")
            
            for i, comp in enumerate(self.components):
                f.write(f"Component {i}: '{comp.text}'\n")
                f.write(f"  Position: {comp.position}\n")
                f.write(f"  Scale: {comp.scale}\n")
                f.write(f"  Characters: {len(comp.char_images)}\n")
                f.write(f"  Meshes: {len(comp.meshes)}\n")
                f.write(f"  Colors: {comp.color_scheme}\n\n")


class LogoGenerator:
    """
    Main logo generator that orchestrates all components
    """
    
    def __init__(self, canvas_size: Tuple[int, int] = (1200, 800),
                 background_color: str = 'black',
                 default_char_size: Tuple[int, int] = (200, 200)):
        """
        Initialize the logo generator
        
        Args:
            canvas_size: Size of the output canvas (width, height)
            background_color: Background color for the logo
            default_char_size: Default character size (width, height)
        """
        self.canvas_size = canvas_size
        self.background_color = background_color
        self.default_char_size = default_char_size
        
        # Initialize components
        self.renderer = CharacterRenderer(
            default_width=default_char_size[0],
            default_height=default_char_size[1]
        )
        self.string_processor = StringProcessor(self.renderer)
        self.contour_extractor = ContourExtractor(method='opencv')
        self.mesh_generator = MeshGenerator(method='delaunay')
    
    def create_logo(self, name: str, components_config: List[Dict]) -> Logo:
        """
        Create a complete logo from configuration
        
        Args:
            name: Logo name
            components_config: List of component configurations, each containing:
                - text: Text or formula to render
                - position: (x, y) position on canvas
                - scale: Scale factor
                - colors: List of colors for the component
                - is_formula: Whether to treat as formula
                - mesh_density: Interior point density for meshing
                
        Returns:
            Logo object
        """
        logo_components = []
        
        for config in components_config:
            component = self._create_component(config)
            logo_components.append(component)
        
        logo = Logo(
            name=name,
            components=logo_components,
            canvas_size=self.canvas_size,
            background_color=self.background_color
        )
        
        return logo
    
    def _calculate_content_bounds(self, logo: Logo) -> Tuple[float, float, float, float]:
        """
        Calculate the bounding box of all rendered content
        
        Args:
            logo: Logo object
            
        Returns:
            Tuple of (min_x, min_y, max_x, max_y)
        """
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        
        for component in logo.components:
            base_x, base_y = component.position
            scale_factor = component.scale * 0.5
            
            # Track cumulative position for multi-image components
            cumulative_x = 0
            current_char_img_idx = -1
            char_img_base_x = 0
            
            for i, mesh in enumerate(component.meshes):
                if mesh is None:
                    continue
                
                # Determine which char_image this mesh belongs to
                char_img_idx = 0
                if len(component.char_images) == 1:
                    char_img_idx = 0
                else:
                    char_img_idx = min(i, len(component.char_images) - 1)
                
                # Check if we're starting a new char_image
                if char_img_idx != current_char_img_idx:
                    current_char_img_idx = char_img_idx
                    char_img_base_x = cumulative_x
                
                # Transform mesh points - must match _render_component logic
                transformed_points = mesh.points.copy()
                
                if len(component.char_images) == 1:
                    # Single image - preserve relative positions
                    transformed_points *= scale_factor
                    transformed_points[:, 0] += base_x
                    transformed_points[:, 1] += base_y
                else:
                    # Multiple images - use cumulative positioning
                    char_x = base_x + char_img_base_x
                    char_y = base_y
                    
                    transformed_points *= scale_factor
                    transformed_points[:, 0] += char_x
                    transformed_points[:, 1] += char_y
                    
                    # Update cumulative position
                    char_width = (transformed_points[:, 0].max() - transformed_points[:, 0].min())
                    cumulative_x = char_img_base_x + char_width + component.scale * 10
                
                # Update bounds
                min_x = min(min_x, transformed_points[:, 0].min())
                min_y = min(min_y, transformed_points[:, 1].min())
                max_x = max(max_x, transformed_points[:, 0].max())
                max_y = max(max_y, transformed_points[:, 1].max())
        
        return min_x, min_y, max_x, max_y
    
    def render_logo(self, logo: Logo, output_file: str,
                   show_wireframe: bool = True,
                   show_vertices: bool = True,
                   show_surface: bool = True,
                   wireframe_thickness: float = 0.5,
                   vertex_size: float = 8.0,
                   vertex_mode: str = 'all',
                   show_gradient: bool = True,
                   dpi: int = 300) -> str:
        """
        Render the logo to an image file
        
        Args:
            logo: Logo object to render
            output_file: Output file path
            show_wireframe: Whether to show mesh edges
            show_vertices: Whether to show vertices
            show_gradient: Whether to use gradient colors
            dpi: Output resolution
            
        Returns:
            Path to saved file
        """
        # Calculate actual content bounds
        min_x, min_y, max_x, max_y = self._calculate_content_bounds(logo)
        
        # Add padding around content
        padding = 50
        content_width = max_x - min_x + 2 * padding
        content_height = max_y - min_y + 2 * padding
        
        # Determine final canvas size
        original_width, original_height = logo.canvas_size
        final_width = max(original_width, content_width)
        final_height = max(original_height, content_height)
        
        # Print warning if canvas size was adjusted
        if final_width > original_width or final_height > original_height:
            print(f"⚠️  Canvas size adjusted from ({original_width}, {original_height}) "
                  f"to ({int(final_width)}, {int(final_height)}) to fit all content")
        
        # Calculate centering offset
        offset_x = (final_width - (max_x - min_x)) / 2 - min_x
        offset_y = (final_height - (max_y - min_y)) / 2 - min_y
        
        # Adjust component positions for centering
        for component in logo.components:
            component.position = (component.position[0] + offset_x, 
                                component.position[1] + offset_y)
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 8), facecolor=logo.background_color)
        ax.set_facecolor(logo.background_color)
        ax.set_aspect('equal')
        
        # Render each component
        for component in logo.components:
            self._render_component(ax, component, show_wireframe, 
                                 show_vertices, show_surface,
                                 wireframe_thickness, vertex_size,
                                 vertex_mode, show_gradient)
        
        # Set canvas limits to final size
        ax.set_xlim(0, final_width)
        ax.set_ylim(0, final_height)
        ax.invert_yaxis()  # Match image coordinate system (Y increases downward)
        ax.axis('off')
        
        # Add title if needed (escape $ to prevent matplotlib from parsing as math)
        title_y = -20
        safe_title = logo.name.replace('$', r'\$')
        ax.text(final_width / 2, title_y, safe_title,
               fontsize=16, color='white', ha='center',
               style='italic', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=dpi, facecolor=logo.background_color,
                   bbox_inches='tight', pad_inches=0.2)
        print(f"Logo '{logo.name}' saved to {output_file}")
        
        return output_file
    
    def create_mema_inma_logo(self, output_file: str = 'mema_inma_logo.png',
                             output_dir: str = 'output') -> Logo:
        """
        Create the MEMA & INMA logo with formula ME/IN * e^(iθ)
        
        Args:
            output_file: Output file name
            output_dir: Output directory
            
        Returns:
            Logo object
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Define logo components
        components_config = [
            # ME (numerator)
            {
                'text': 'ME',
                'position': (100, 200),
                'scale': 2.0,
                'colors': ['magenta', 'cyan'],
                'is_formula': False,
                'mesh_density': 3.0
            },
            # IN (denominator)
            {
                'text': 'IN',
                'position': (100, 500),
                'scale': 2.3,
                'colors': ['blue', 'cyan'],
                'is_formula': False,
                'mesh_density': 1.8
            },
            # Multiplication sign
            {
                'text': '$\\times$',
                'position': (500, 350),
                'scale': 1.2,
                'colors': ['yellow'],
                'is_formula': False,
                'mesh_density': 0.8,
                'render_mode': RenderMode.SINGLE
            },
            # e^(iθ) formula
            {
                'text': '$e^{i\\theta}$',
                'position': (500, 0),
                'scale': 3.5,
                'colors': ['yellow', 'white'],
                'is_formula': False,
                'mesh_density': 2.2,
                'render_mode': RenderMode.SINGLE
            }
        ]
        
        # Create logo
        logo = self.create_logo('MEMA & INMA', components_config)
        
        # Render
        output_path = os.path.join(output_dir, output_file)
        self.render_logo(logo, output_path, show_wireframe=True,
                        show_vertices=True, show_gradient=False)
        
        # Save metadata
        metadata_path = os.path.join(output_dir, 'logo_metadata.txt')
        logo.save_metadata(metadata_path)
        
        return logo
    
    def create_simple_text_logo(self, text: str, output_file: str,
                               color_scheme: List[str] = None) -> Logo:
        """
        Create a simple text logo
        
        Args:
            text: Text to render
            output_file: Output file path
            color_scheme: List of colors (uses default if None)
            
        Returns:
            Logo object
        """
        if color_scheme is None:
            color_scheme = ['cyan', 'magenta', 'yellow', 'white']
        
        # Calculate spacing for characters
        char_width = self.canvas_size[0] / (len(text) + 2)
        center_y = self.canvas_size[1] / 2
        
        components_config = []
        for i, char in enumerate(text):
            components_config.append({
                'text': char,
                'position': (char_width * (i + 1), center_y),
                'scale': 1.5,
                'colors': [color_scheme[i % len(color_scheme)]],
                'is_formula': False,
                'mesh_density': 1.2
            })
        
        # Create and render logo
        logo = self.create_logo(text, components_config)
        self.render_logo(logo, output_file)
        
        return logo
    
    def _create_component(self, config: Dict) -> LogoComponent:
        """Create a logo component from configuration"""
        text = config['text']
        position = config['position']
        scale = config['scale']
        colors = config.get('colors', ['cyan'])
        is_formula = config.get('is_formula', False)
        mesh_density = config.get('mesh_density', 1.0)
        invert_mode = config.get('invert_mode', False)
        invert_margin = config.get('invert_margin', 50)
        
        # Calculate character size based on scale
        char_width = int(self.default_char_size[0] * scale)
        char_height = int(self.default_char_size[1] * scale)
        
        # Get render mode from config (default to INDIVIDUAL)
        render_mode = config.get('render_mode', RenderMode.INDIVIDUAL)
        
        # Process text to get character images
        if is_formula:
            processed = self.string_processor.process_formula(
                text, width=char_width, height=char_height
            )
        else:
            processed = self.string_processor.process(
                text, mode=render_mode,
                width=char_width, height=char_height
            )
        
        # Extract contours and generate meshes for each character
        contours = []
        meshes = []
        
        for char_img in processed.images:
            if invert_mode:
                # INVERT MODE: Mesh the background, character becomes a hole
                # Create a bounding box around the character with margin
                h, w = char_img.matrix.shape
                margin = invert_margin
                
                # Create rectangle boundary (with margin)
                rect_points = np.array([
                    [margin, margin],
                    [w - margin, margin],
                    [w - margin, h - margin],
                    [margin, h - margin]
                ])
                
                # Extract character contour to use as hole
                largest_contour, all_holes = self.contour_extractor.extract_with_openings(
                    char_img.matrix, threshold=127, simplify=True, epsilon=3.0
                )
                
                if largest_contour:
                    # Character contour becomes a hole in the background mesh
                    holes_list = [largest_contour.points]
                    # Add any internal holes from the character too
                    if all_holes:
                        holes_list.extend([hole.points for hole in all_holes])
                    
                    contours.append(largest_contour)  # Store for reference
                    
                    # Generate mesh of the rectangle with character as hole
                    # Invert the character image for proper filtering
                    inverted_img = 1 - char_img.matrix
                    mesh = self.mesh_generator.generate(
                        rect_points,
                        add_interior_points=True,
                        num_interior_points=int(50 * mesh_density),  # More points for background
                        holes=holes_list,
                        character_image=inverted_img  # Inverted for filtering
                    )
                    meshes.append(mesh)
                else:
                    contours.append(None)
                    meshes.append(None)
            else:
                # NORMAL MODE: Mesh the character(s)
                # Use extract_all_shapes_with_openings to handle images with multiple
                # disconnected shapes (like formulas rendered as single images)
                all_shapes = self.contour_extractor.extract_all_shapes_with_openings(
                    char_img.matrix, threshold=127, simplify=True, epsilon=3.0, min_area=50
                )
                
                if all_shapes:
                    # Process each shape found in the image
                    for shape_contour, shape_holes in all_shapes:
                        contours.append(shape_contour)
                        
                        # Extract holes list
                        holes_list = [hole.points for hole in shape_holes] if shape_holes else None
                        
                        # Generate mesh with holes
                        mesh = self.mesh_generator.generate(
                            shape_contour.points,
                            add_interior_points=True,
                            num_interior_points=int(30 * mesh_density),
                            holes=holes_list,
                            character_image=char_img.matrix
                        )
                        meshes.append(mesh)
                else:
                    # Empty contour/mesh
                    contours.append(None)
                    meshes.append(None)
        
        return LogoComponent(
            text=text,
            position=position,
            scale=scale,
            char_images=processed.images,
            contours=contours,
            meshes=meshes,
            color_scheme=colors,
            metadata=processed.metadata
        )
    
    def _render_component(self, ax: plt.Axes, component: LogoComponent,
                         show_wireframe: bool, show_vertices: bool,
                         show_surface: bool, wireframe_thickness: float,
                         vertex_size: float, vertex_mode: str,
                         show_gradient: bool):
        """Render a single logo component"""
        import random
        base_x, base_y = component.position
        
        # Track cumulative x position for proper spacing between separate char_images
        cumulative_x = 0
        
        # Track which char_image each mesh belongs to
        # When multiple meshes come from one image, they should preserve relative positions
        current_char_img_idx = -1
        char_img_base_x = 0
        
        # Note: meshes may be more than char_images when a single image contains
        # multiple shapes (e.g., formulas rendered as one image with multiple characters)
        for i, mesh in enumerate(component.meshes):
            if mesh is None:
                continue
            
            # Determine which char_image this mesh belongs to
            # For formula images with multiple shapes, contours list tracks the mapping
            char_img_idx = 0
            if len(component.char_images) == 1:
                # All meshes from single image - preserve relative positions
                char_img_idx = 0
            else:
                # Multiple images - find which one this mesh belongs to
                # This is approximate: assume meshes are distributed across images
                char_img_idx = min(i, len(component.char_images) - 1)
            
            # Get metadata for this character if available
            metadata = component.metadata[i] if component.metadata and i < len(component.metadata) else None
            
            # Check if we're starting a new char_image
            if char_img_idx != current_char_img_idx:
                current_char_img_idx = char_img_idx
                char_img_base_x = cumulative_x
            
            # Transform mesh points to canvas coordinates
            transformed_points = mesh.points.copy()
            
            # Scale factor
            if metadata and metadata.scale_factor != 1.0:
                scale_factor = component.scale * 0.5 * metadata.scale_factor
            else:
                scale_factor = component.scale * 0.5
            
            # For single-image formulas, preserve relative positions
            if len(component.char_images) == 1:
                # Scale points (they already have correct relative positions from the image)
                transformed_points *= scale_factor
                # Translate to base position
                transformed_points[:, 0] += base_x
                transformed_points[:, 1] += base_y
            else:
                # Multiple images - use cumulative positioning
                char_x = base_x + char_img_base_x
                char_y = base_y
                
                # Apply vertical offset for superscripts/subscripts
                if metadata and metadata.y_offset_factor != 0:
                    y_offset = metadata.y_offset_factor * component.scale * 100
                    char_y += y_offset
                
                transformed_points *= scale_factor
                transformed_points[:, 0] += char_x
                transformed_points[:, 1] += char_y
                
                # Update cumulative position for next character
                char_width = (transformed_points[:, 0].max() - transformed_points[:, 0].min())
                cumulative_x = char_img_base_x + char_width + component.scale * 10
            
            # Select colors for this character
            color_idx = i % len(component.color_scheme)
            primary_color = component.color_scheme[color_idx]
            secondary_color = component.color_scheme[(color_idx + 1) % len(component.color_scheme)]
            
            # Draw filled triangles (surface)
            if show_surface:
                for tri_idx, tri_indices in enumerate(mesh.triangles):
                    triangle = transformed_points[tri_indices]
                    
                    # Calculate gradient
                    if show_gradient:
                        ratio = tri_idx / max(len(mesh.triangles) - 1, 1)
                        alpha = 0.3 + 0.5 * ratio
                        color = primary_color if ratio < 0.5 else secondary_color
                    else:
                        alpha = 0.5
                        color = primary_color
                    
                    # Draw filled triangle
                    poly = Polygon(triangle, closed=True,
                                 edgecolor='none',
                                 facecolor=color,
                                 alpha=alpha,
                                 linewidth=0)
                    ax.add_patch(poly)
            
            # Draw wireframe (mesh lines)
            if show_wireframe:
                for tri_indices in mesh.triangles:
                    triangle = transformed_points[tri_indices]
                    triangle_closed = np.vstack([triangle, triangle[0]])
                    ax.plot(triangle_closed[:, 0], triangle_closed[:, 1],
                           color='cyan', linewidth=wireframe_thickness, alpha=0.6)
            
            # Draw vertices (dots)
            if show_vertices and vertex_mode != 'none':
                if vertex_mode == 'all':
                    # Show all vertices
                    ax.scatter(transformed_points[:, 0], transformed_points[:, 1],
                              c='white', s=vertex_size, alpha=0.7, zorder=10,
                              edgecolors='cyan', linewidths=0.3)
                elif vertex_mode == 'random':
                    # Show random subset of vertices (50%)
                    num_points = len(transformed_points)
                    indices = random.sample(range(num_points), num_points // 2)
                    random_points = transformed_points[indices]
                    ax.scatter(random_points[:, 0], random_points[:, 1],
                              c='white', s=vertex_size, alpha=0.7, zorder=10,
                              edgecolors='cyan', linewidths=0.3)

