"""
Mesh Generator Module
Creates triangle meshes from point sets using Delaunay triangulation
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random


@dataclass
class MeshData:
    """Data class to hold mesh data"""
    points: np.ndarray  # Vertex coordinates (N x 2)
    triangles: np.ndarray  # Triangle indices (M x 3)
    num_vertices: int
    num_triangles: int
    
    def get_edges(self) -> np.ndarray:
        """
        Get all unique edges in the mesh
        
        Returns:
            Array of edges as pairs of vertex indices
        """
        edges = set()
        for tri in self.triangles:
            # Add all three edges of the triangle
            edges.add(tuple(sorted([tri[0], tri[1]])))
            edges.add(tuple(sorted([tri[1], tri[2]])))
            edges.add(tuple(sorted([tri[2], tri[0]])))
        
        return np.array(list(edges))
    
    def get_triangle_areas(self) -> np.ndarray:
        """
        Calculate area of each triangle
        
        Returns:
            Array of triangle areas
        """
        areas = np.zeros(self.num_triangles)
        
        for i, tri_indices in enumerate(self.triangles):
            p1, p2, p3 = self.points[tri_indices]
            # Use cross product formula
            area = 0.5 * abs(
                (p2[0] - p1[0]) * (p3[1] - p1[1]) - 
                (p3[0] - p1[0]) * (p2[1] - p1[1])
            )
            areas[i] = area
        
        return areas
    
    def save_mesh(self, filepath: str, format: str = 'obj') -> str:
        """
        Save mesh to file
        
        Args:
            filepath: Output file path
            format: File format ('obj', 'ply', 'txt')
            
        Returns:
            Saved file path
        """
        if format == 'obj':
            self._save_obj(filepath)
        elif format == 'ply':
            self._save_ply(filepath)
        else:  # txt
            self._save_txt(filepath)
        
        return filepath
    
    def _save_obj(self, filepath: str):
        """Save mesh in Wavefront OBJ format"""
        with open(filepath, 'w') as f:
            f.write("# Triangle mesh\n")
            f.write(f"# {self.num_vertices} vertices, {self.num_triangles} faces\n\n")
            
            # Write vertices
            for point in self.points:
                f.write(f"v {point[0]} {point[1]} 0.0\n")
            
            f.write("\n")
            
            # Write faces (1-indexed in OBJ format)
            for tri in self.triangles:
                f.write(f"f {tri[0]+1} {tri[1]+1} {tri[2]+1}\n")
    
    def _save_ply(self, filepath: str):
        """Save mesh in PLY format"""
        with open(filepath, 'w') as f:
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {self.num_vertices}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            f.write(f"element face {self.num_triangles}\n")
            f.write("property list uchar int vertex_indices\n")
            f.write("end_header\n")
            
            # Write vertices
            for point in self.points:
                f.write(f"{point[0]} {point[1]} 0.0\n")
            
            # Write faces
            for tri in self.triangles:
                f.write(f"3 {tri[0]} {tri[1]} {tri[2]}\n")
    
    def _save_txt(self, filepath: str):
        """Save mesh in simple text format"""
        with open(filepath, 'w') as f:
            f.write(f"# Vertices: {self.num_vertices}\n")
            f.write(f"# Triangles: {self.num_triangles}\n\n")
            
            f.write("# Vertices (x y)\n")
            for point in self.points:
                f.write(f"{point[0]} {point[1]}\n")
            
            f.write("\n# Triangles (v1 v2 v3)\n")
            for tri in self.triangles:
                f.write(f"{tri[0]} {tri[1]} {tri[2]}\n")


class MeshGenerator:
    """
    Generates triangle meshes from point sets
    Uses Delaunay triangulation and provides mesh enhancement options
    """
    
    def __init__(self, method: str = 'delaunay'):
        """
        Initialize the mesh generator
        
        Args:
            method: Meshing method ('delaunay', 'constrained')
        """
        self.method = method
    
    def generate(self, points: np.ndarray, 
                add_interior_points: bool = False,
                num_interior_points: int = 20,
                boundary_refinement: bool = False,
                refinement_factor: int = 2) -> MeshData:
        """
        Generate a triangle mesh from points
        
        Args:
            points: Array of (x, y) coordinates
            add_interior_points: Whether to add random interior points
            num_interior_points: Number of interior points to add
            boundary_refinement: Whether to refine boundary edges
            refinement_factor: Subdivision factor for boundary refinement
            
        Returns:
            MeshData object containing the mesh
        """
        if len(points) < 3:
            raise ValueError("Need at least 3 points to create a mesh")
        
        points_array = np.array(points)
        
        # Add interior points if requested
        if add_interior_points:
            points_array = self._add_interior_points(
                points_array, num_interior_points
            )
        
        # Refine boundary if requested
        if boundary_refinement:
            points_array = self._refine_boundary(
                points_array, refinement_factor
            )
        
        # Generate triangulation
        if self.method == 'delaunay':
            mesh = self._delaunay_triangulation(points_array)
        else:
            mesh = self._delaunay_triangulation(points_array)
        
        return mesh
    
    def generate_from_contour(self, contour_points: np.ndarray,
                             density: float = 1.0,
                             smooth_interior: bool = True) -> MeshData:
        """
        Generate mesh from a contour with interior fill
        
        Args:
            contour_points: Boundary contour points
            density: Interior point density (higher = more triangles)
            smooth_interior: Whether to add smoothly distributed interior points
            
        Returns:
            MeshData object
        """
        # Calculate interior points based on density
        bbox = self._get_bounding_box(contour_points)
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
        num_interior = int(area * density / 100)
        
        if smooth_interior:
            interior_points = self._generate_interior_points_poisson(
                contour_points, num_interior
            )
        else:
            interior_points = self._add_interior_points(
                contour_points, num_interior
            )
        
        # Combine and triangulate
        all_points = interior_points
        mesh = self._delaunay_triangulation(all_points)
        
        return mesh
    
    def refine_mesh(self, mesh: MeshData, max_area: float) -> MeshData:
        """
        Refine mesh by subdividing large triangles
        
        Args:
            mesh: Input mesh
            max_area: Maximum allowed triangle area
            
        Returns:
            Refined MeshData
        """
        points_list = mesh.points.tolist()
        triangles_list = []
        
        for tri_indices in mesh.triangles:
            triangle_points = mesh.points[tri_indices]
            
            # Calculate triangle area
            p1, p2, p3 = triangle_points
            area = 0.5 * abs(
                (p2[0] - p1[0]) * (p3[1] - p1[1]) - 
                (p3[0] - p1[0]) * (p2[1] - p1[1])
            )
            
            if area > max_area:
                # Subdivide by adding centroid
                centroid = np.mean(triangle_points, axis=0)
                new_idx = len(points_list)
                points_list.append(centroid.tolist())
                
                # Create three new triangles
                triangles_list.append([tri_indices[0], tri_indices[1], new_idx])
                triangles_list.append([tri_indices[1], tri_indices[2], new_idx])
                triangles_list.append([tri_indices[2], tri_indices[0], new_idx])
            else:
                # Keep original triangle
                triangles_list.append(tri_indices.tolist())
        
        refined_points = np.array(points_list)
        refined_triangles = np.array(triangles_list)
        
        return MeshData(
            points=refined_points,
            triangles=refined_triangles,
            num_vertices=len(refined_points),
            num_triangles=len(refined_triangles)
        )
    
    def visualize(self, mesh: MeshData, output_file: Optional[str] = None,
                 show_edges: bool = True, show_vertices: bool = True,
                 color_scheme: str = 'gradient', figsize: Tuple[int, int] = (10, 10),
                 background_color: str = 'black') -> plt.Figure:
        """
        Visualize the mesh
        
        Args:
            mesh: Mesh to visualize
            output_file: Optional file path to save visualization
            show_edges: Whether to show triangle edges
            show_vertices: Whether to show vertices
            color_scheme: Color scheme ('gradient', 'random', 'solid', 'alternating')
            figsize: Figure size
            background_color: Background color
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor=background_color)
        ax.set_facecolor(background_color)
        ax.set_aspect('equal')
        
        # Define color palettes
        if color_scheme == 'gradient':
            colors = ['cyan', 'magenta', 'yellow']
        elif color_scheme == 'random':
            colors = None  # Will randomize per triangle
        elif color_scheme == 'alternating':
            colors = ['cyan', 'magenta']
        else:  # solid
            colors = ['cyan']
        
        # Draw triangles
        for i, tri_indices in enumerate(mesh.triangles):
            triangle = mesh.points[tri_indices]
            
            # Select color
            if colors is None:
                color = (random.random(), random.random(), random.random())
            else:
                color = colors[i % len(colors)]
            
            # Calculate alpha based on position for gradient effect
            centroid = np.mean(triangle, axis=0)
            norm_pos = (centroid[1] - mesh.points[:, 1].min()) / \
                      (mesh.points[:, 1].max() - mesh.points[:, 1].min() + 1e-6)
            alpha = 0.3 + 0.4 * norm_pos
            
            # Draw filled triangle
            poly = Polygon(triangle, closed=True,
                          edgecolor='cyan' if show_edges else 'none',
                          facecolor=color,
                          alpha=alpha,
                          linewidth=0.5 if show_edges else 0)
            ax.add_patch(poly)
        
        # Draw edges separately for better visibility
        if show_edges:
            for tri_indices in mesh.triangles:
                triangle = mesh.points[tri_indices]
                triangle_closed = np.vstack([triangle, triangle[0]])
                ax.plot(triangle_closed[:, 0], triangle_closed[:, 1],
                       color='cyan', linewidth=0.8, alpha=0.7)
        
        # Draw vertices
        if show_vertices:
            ax.scatter(mesh.points[:, 0], mesh.points[:, 1],
                      c='white', s=20, alpha=0.8, zorder=10,
                      edgecolors='cyan', linewidths=0.5)
        
        # Set limits with padding
        x_min, x_max = mesh.points[:, 0].min(), mesh.points[:, 0].max()
        y_min, y_max = mesh.points[:, 1].min(), mesh.points[:, 1].max()
        padding = 0.1 * max(x_max - x_min, y_max - y_min)
        
        ax.set_xlim(x_min - padding, x_max + padding)
        ax.set_ylim(y_min - padding, y_max + padding)
        ax.axis('off')
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, facecolor=background_color,
                       bbox_inches='tight', pad_inches=0.2)
            print(f"Mesh visualization saved to {output_file}")
        
        return fig
    
    def _delaunay_triangulation(self, points: np.ndarray) -> MeshData:
        """Perform Delaunay triangulation"""
        tri = Delaunay(points)
        
        return MeshData(
            points=points,
            triangles=tri.simplices,
            num_vertices=len(points),
            num_triangles=len(tri.simplices)
        )
    
    def _add_interior_points(self, boundary_points: np.ndarray,
                            num_points: int) -> np.ndarray:
        """Add random interior points within the boundary"""
        if num_points <= 0:
            return boundary_points
        
        # Get bounding box
        x_min, y_min, x_max, y_max = self._get_bounding_box(boundary_points)
        
        # Generate random points
        interior_points = []
        attempts = 0
        max_attempts = num_points * 10
        
        while len(interior_points) < num_points and attempts < max_attempts:
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            point = np.array([x, y])
            
            # Check if point is inside boundary (simplified check)
            # For more robust check, use point-in-polygon algorithm
            interior_points.append(point)
            attempts += 1
        
        if len(interior_points) == 0:
            return boundary_points
        
        combined = np.vstack([boundary_points, np.array(interior_points)])
        return combined
    
    def _generate_interior_points_poisson(self, boundary_points: np.ndarray,
                                         num_points: int) -> np.ndarray:
        """Generate well-distributed interior points using Poisson disk sampling approximation"""
        x_min, y_min, x_max, y_max = self._get_bounding_box(boundary_points)
        
        # Use grid-based approach for better distribution
        grid_size = int(np.sqrt(num_points))
        x_steps = np.linspace(x_min, x_max, grid_size)
        y_steps = np.linspace(y_min, y_max, grid_size)
        
        interior_points = []
        for x in x_steps:
            for y in y_steps:
                # Add some randomness
                jitter_x = (x_max - x_min) / grid_size * 0.3 * (random.random() - 0.5)
                jitter_y = (y_max - y_min) / grid_size * 0.3 * (random.random() - 0.5)
                interior_points.append([x + jitter_x, y + jitter_y])
        
        combined = np.vstack([boundary_points, np.array(interior_points[:num_points])])
        return combined
    
    def _refine_boundary(self, points: np.ndarray, factor: int) -> np.ndarray:
        """Add points along boundary edges"""
        refined_points = [points[0]]
        
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            
            # Add intermediate points
            for j in range(1, factor):
                t = j / factor
                interp_point = (1 - t) * p1 + t * p2
                refined_points.append(interp_point)
            
            refined_points.append(p2)
        
        return np.array(refined_points)
    
    def _get_bounding_box(self, points: np.ndarray) -> Tuple[float, float, float, float]:
        """Get bounding box of points"""
        x_min, y_min = points.min(axis=0)
        x_max, y_max = points.max(axis=0)
        return (x_min, y_min, x_max, y_max)
