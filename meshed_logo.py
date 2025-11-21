"""
MeshedLogo - Front-facing class for logo generation
Simple interface to generate triangle-meshed logos from text and formulas
"""

from typing import List, Tuple, Dict, Optional
import os
from lib.logo_generator import LogoGenerator


class MeshedLogo:
    """
    Main interface for generating triangle-meshed logos.
    
    Usage:
        logo = MeshedLogo()
        logo.generate("HELLO", output_file="hello.png")
    """
    
    def __init__(self, canvas_size: Tuple[int, int] = (1200, 800),
                 background_color: str = 'black',
                 default_char_size: Tuple[int, int] = (200, 200)):
        """
        Initialize MeshedLogo generator
        
        Args:
            canvas_size: Canvas dimensions (width, height)
            background_color: Background color (e.g., 'black', '#000000')
            default_char_size: Default character dimensions (width, height)
        """
        self.generator = LogoGenerator(
            canvas_size=canvas_size,
            background_color=background_color,
            default_char_size=default_char_size
        )
        self.canvas_size = canvas_size
        self.background_color = background_color
    
    def generate(self, text: str,
                output_file: str = 'logo.png',
                colors: Optional[List[str]] = None,
                position: Optional[Tuple[float, float]] = None,
                scale: float = 2.0,
                mesh_density: float = 1.5,
                show_wireframe: bool = True,
                show_vertices: bool = True,
                show_surface: bool = True,
                wireframe_thickness: float = 0.5,
                vertex_size: float = 8.0,
                vertex_mode: str = 'all',
                invert_mode: bool = False,
                invert_margin: int = 50,
                dpi: int = 300) -> str:
        """
        Generate a simple text logo
        
        Args:
            text: Text to render
            output_file: Output file path
            colors: List of colors (default: ['cyan', 'magenta', 'yellow', 'white'])
            position: Position on canvas (default: centered)
            scale: Text scale factor
            mesh_density: Mesh interior point density
            show_wireframe: Show triangle edges (mesh lines)
            show_vertices: Show vertex points (dots)
            show_surface: Show filled triangles (surface)
            wireframe_thickness: Line thickness for mesh edges
            vertex_size: Size of vertex dots
            vertex_mode: Vertex display mode ('all', 'random', 'none')
            invert_mode: If True, mesh the background and treat character as hole
            invert_margin: Margin (in pixels) around character when in invert mode
            dpi: Output resolution
            
        Returns:
            Path to saved file
        """
        if colors is None:
            colors = ['cyan', 'magenta', 'yellow', 'white']
        
        if position is None:
            # Center horizontally, middle vertically
            position = (self.canvas_size[0] * 0.2, self.canvas_size[1] * 0.5)
        
        # Create component configuration
        components_config = [{
            'text': text,
            'position': position,
            'scale': scale,
            'colors': colors,
            'is_formula': False,
            'mesh_density': mesh_density,
            'invert_mode': invert_mode,
            'invert_margin': invert_margin
        }]
        
        # Generate logo
        logo = self.generator.create_logo(text, components_config)
        
        # Render to file
        self.generator.render_logo(
            logo, output_file,
            show_wireframe=show_wireframe,
            show_vertices=show_vertices,
            show_surface=show_surface,
            wireframe_thickness=wireframe_thickness,
            vertex_size=vertex_size,
            vertex_mode=vertex_mode,
            show_gradient=True,
            dpi=dpi
        )
        
        return output_file
    
    def generate_multi(self, components: List[Dict],
                      name: str = 'Logo',
                      output_file: str = 'logo.png',
                      show_wireframe: bool = True,
                      show_vertices: bool = True,
                      show_surface: bool = True,
                      wireframe_thickness: float = 0.5,
                      vertex_size: float = 8.0,
                      vertex_mode: str = 'all',
                      dpi: int = 300) -> str:
        """
        Generate multi-component logo with custom configuration
        
        Args:
            components: List of component configs, each containing:
                - text: Text to render
                - position: (x, y) position
                - scale: Scale factor
                - colors: List of colors
                - mesh_density: Mesh density (optional)
                - is_formula: Treat as formula (optional)
            name: Logo name
            output_file: Output file path
            show_wireframe: Show triangle edges
            show_vertices: Show vertex points
            dpi: Output resolution
            
        Returns:
            Path to saved file
        """
        # Set defaults for optional fields
        for comp in components:
            comp.setdefault('mesh_density', 1.5)
            comp.setdefault('is_formula', False)
            comp.setdefault('invert_mode', False)
            comp.setdefault('invert_margin', 50)
        
        # Generate logo
        logo = self.generator.create_logo(name, components)
        
        # Render to file
        self.generator.render_logo(
            logo, output_file,
            show_wireframe=show_wireframe,
            show_vertices=show_vertices,
            show_surface=show_surface,
            wireframe_thickness=wireframe_thickness,
            vertex_size=vertex_size,
            vertex_mode=vertex_mode,
            show_gradient=True,
            dpi=dpi
        )
        
        return output_file
    
    def generate_formula(self, formula: str,
                        output_file: str = 'formula.png',
                        colors: Optional[List[str]] = None,
                        position: Optional[Tuple[float, float]] = None,
                        scale: float = 2.0,
                        dpi: int = 300) -> str:
        """
        Generate a mathematical formula logo
        
        Args:
            formula: Mathematical formula string
            output_file: Output file path
            colors: List of colors
            position: Position on canvas
            scale: Scale factor
            dpi: Output resolution
            
        Returns:
            Path to saved file
        """
        if colors is None:
            colors = ['yellow', 'white', 'cyan']
        
        if position is None:
            position = (self.canvas_size[0] * 0.3, self.canvas_size[1] * 0.5)
        
        components_config = [{
            'text': formula,
            'position': position,
            'scale': scale,
            'colors': colors,
            'is_formula': True,
            'mesh_density': 1.2
        }]
        
        logo = self.generator.create_logo(formula, components_config)
        
        self.generator.render_logo(
            logo, output_file,
            show_wireframe=True,
            show_vertices=True,
            show_gradient=True,
            dpi=dpi
        )
        
        return output_file
    
    def generate_mema_inma(self, output_file: str = 'mema_inma_logo.png',
                          output_dir: str = 'output') -> str:
        """
        Generate the classic MEMA & INMA logo
        
        Args:
            output_file: Output file name
            output_dir: Output directory
            
        Returns:
            Path to saved file
        """
        os.makedirs(output_dir, exist_ok=True)
        self.generator.create_mema_inma_logo(output_file, output_dir)
        return os.path.join(output_dir, output_file)
    
    def set_canvas(self, width: int, height: int):
        """Update canvas size"""
        self.canvas_size = (width, height)
        self.generator = LogoGenerator(
            canvas_size=self.canvas_size,
            background_color=self.background_color,
            default_char_size=self.generator.default_char_size
        )
    
    def set_background(self, color: str):
        """Update background color"""
        self.background_color = color
        self.generator = LogoGenerator(
            canvas_size=self.canvas_size,
            background_color=color,
            default_char_size=self.generator.default_char_size
        )
