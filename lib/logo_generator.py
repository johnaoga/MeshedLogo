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
from lib.string_processor import StringProcessor, RenderMode
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
    
    def render_logo(self, logo: Logo, output_file: str,
                   show_wireframe: bool = True,
                   show_vertices: bool = True,
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
        fig, ax = plt.subplots(1, 1, figsize=(12, 8), facecolor=logo.background_color)
        ax.set_facecolor(logo.background_color)
        ax.set_aspect('equal')
        
        # Render each component
        for component in logo.components:
            self._render_component(ax, component, show_wireframe, 
                                 show_vertices, show_gradient)
        
        # Set canvas limits
        ax.set_xlim(0, logo.canvas_size[0])
        ax.set_ylim(0, logo.canvas_size[1])
        ax.invert_yaxis()  # Match image coordinate system (Y increases downward)
        ax.axis('off')
        
        # Add title if needed
        title_y = -20
        ax.text(logo.canvas_size[0] / 2, title_y, logo.name,
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
                'position': (100, 500),
                'scale': 2.0,
                'colors': ['magenta', 'cyan'],
                'is_formula': False,
                'mesh_density': 1.5
            },
            # Fraction bar
            {
                'text': '/',
                'position': (400, 400),
                'scale': 1.5,
                'colors': ['white'],
                'is_formula': False,
                'mesh_density': 0.5
            },
            # IN (denominator)
            {
                'text': 'IN',
                'position': (100, 200),
                'scale': 2.0,
                'colors': ['blue', 'cyan'],
                'is_formula': False,
                'mesh_density': 1.5
            },
            # Multiplication sign
            {
                'text': '×',
                'position': (500, 350),
                'scale': 1.2,
                'colors': ['yellow'],
                'is_formula': False,
                'mesh_density': 0.8
            },
            # e^(iθ) formula
            {
                'text': 'e',
                'position': (600, 400),
                'scale': 1.8,
                'colors': ['yellow', 'white'],
                'is_formula': True,
                'mesh_density': 1.2
            },
            {
                'text': 'iθ',
                'position': (730, 500),
                'scale': 1.0,
                'colors': ['cyan', 'magenta'],
                'is_formula': True,
                'mesh_density': 1.0
            }
        ]
        
        # Create logo
        logo = self.create_logo('MEMA & INMA', components_config)
        
        # Render
        output_path = os.path.join(output_dir, output_file)
        self.render_logo(logo, output_path, show_wireframe=True,
                        show_vertices=True, show_gradient=True)
        
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
        
        # Calculate character size based on scale
        char_width = int(self.default_char_size[0] * scale)
        char_height = int(self.default_char_size[1] * scale)
        
        # Process text to get character images
        if is_formula:
            processed = self.string_processor.process_formula(
                text, width=char_width, height=char_height
            )
        else:
            processed = self.string_processor.process(
                text, mode=RenderMode.INDIVIDUAL,
                width=char_width, height=char_height
            )
        
        # Extract contours and generate meshes for each character
        contours = []
        meshes = []
        
        for char_img in processed.images:
            # Extract contours WITH openings detection (detects holes AND openings like 'C', 'U', 'H')
            largest_contour, all_holes = self.contour_extractor.extract_with_openings(
                char_img.matrix, threshold=127, simplify=True, epsilon=3.0
            )
            
            if largest_contour:
                contours.append(largest_contour)
                
                # Extract holes list
                holes_list = [hole.points for hole in all_holes] if all_holes else None
                
                # Generate mesh with ALL holes (traditional + openings)
                mesh = self.mesh_generator.generate(
                    largest_contour.points,
                    add_interior_points=True,
                    num_interior_points=int(30 * mesh_density),
                    holes=holes_list,
                    character_image=char_img.matrix  # Still use for triangle filtering
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
            color_scheme=colors
        )
    
    def _render_component(self, ax: plt.Axes, component: LogoComponent,
                         show_wireframe: bool, show_vertices: bool,
                         show_gradient: bool):
        """Render a single logo component"""
        base_x, base_y = component.position
        char_spacing = component.scale * 150  # Spacing between characters
        
        for i, (mesh, char_img) in enumerate(zip(component.meshes, component.char_images)):
            if mesh is None:
                continue
            
            # Calculate character position
            char_x = base_x + i * char_spacing
            char_y = base_y
            
            # Transform mesh points to canvas coordinates
            transformed_points = mesh.points.copy()
            
            # Scale and translate
            scale_factor = component.scale * 0.5
            transformed_points *= scale_factor
            transformed_points[:, 0] += char_x
            transformed_points[:, 1] += char_y
            
            # Select colors for this character
            color_idx = i % len(component.color_scheme)
            primary_color = component.color_scheme[color_idx]
            secondary_color = component.color_scheme[(color_idx + 1) % len(component.color_scheme)]
            
            # Draw triangles
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
            
            # Draw wireframe
            if show_wireframe:
                for tri_indices in mesh.triangles:
                    triangle = transformed_points[tri_indices]
                    triangle_closed = np.vstack([triangle, triangle[0]])
                    ax.plot(triangle_closed[:, 0], triangle_closed[:, 1],
                           color='cyan', linewidth=0.5, alpha=0.6)
            
            # Draw vertices
            if show_vertices:
                ax.scatter(transformed_points[:, 0], transformed_points[:, 1],
                          c='white', s=8, alpha=0.7, zorder=10,
                          edgecolors='cyan', linewidths=0.3)

