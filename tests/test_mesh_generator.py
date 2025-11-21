"""Tests for MeshGenerator"""

import unittest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.mesh_generator import MeshGenerator, MeshData


class TestMeshGenerator(unittest.TestCase):
    """Test cases for MeshGenerator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = MeshGenerator(method='delaunay')
        self.test_output_dir = "tests/output"
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Create simple test points (square)
        self.square_points = np.array([
            [0, 0], [10, 0], [10, 10], [0, 10]
        ])
    
    def test_generator_initialization(self):
        """Test generator initialization"""
        self.assertEqual(self.generator.method, 'delaunay')
    
    def test_generate_basic_mesh(self):
        """Test generating basic mesh"""
        mesh = self.generator.generate(self.square_points)
        
        self.assertIsInstance(mesh, MeshData)
        self.assertGreaterEqual(mesh.num_vertices, 4)
        self.assertGreater(mesh.num_triangles, 0)
        self.assertEqual(mesh.points.shape[1], 2)  # 2D points
    
    def test_generate_with_interior_points(self):
        """Test generating mesh with interior points"""
        mesh = self.generator.generate(
            self.square_points,
            add_interior_points=True,
            num_interior_points=10
        )
        
        # Should have more vertices than original
        self.assertGreater(mesh.num_vertices, len(self.square_points))
        self.assertGreater(mesh.num_triangles, 0)
    
    def test_mesh_get_edges(self):
        """Test getting mesh edges"""
        mesh = self.generator.generate(self.square_points)
        edges = mesh.get_edges()
        
        self.assertIsInstance(edges, np.ndarray)
        self.assertGreater(len(edges), 0)
        self.assertEqual(edges.shape[1], 2)  # Each edge has 2 vertices
    
    def test_mesh_get_triangle_areas(self):
        """Test calculating triangle areas"""
        mesh = self.generator.generate(self.square_points)
        areas = mesh.get_triangle_areas()
        
        self.assertEqual(len(areas), mesh.num_triangles)
        self.assertTrue(all(area >= 0 for area in areas))
    
    def test_refine_mesh(self):
        """Test mesh refinement"""
        mesh = self.generator.generate(self.square_points)
        refined = self.generator.refine_mesh(mesh, max_area=10.0)
        
        self.assertGreaterEqual(refined.num_triangles, mesh.num_triangles)
    
    def test_save_mesh_obj(self):
        """Test saving mesh in OBJ format"""
        mesh = self.generator.generate(self.square_points)
        filepath = os.path.join(self.test_output_dir, 'test_mesh.obj')
        saved_path = mesh.save_mesh(filepath, format='obj')
        
        self.assertEqual(saved_path, filepath)
        self.assertTrue(os.path.exists(filepath))
    
    def test_minimum_points_validation(self):
        """Test that generating mesh with < 3 points raises error"""
        with self.assertRaises(ValueError):
            self.generator.generate(np.array([[0, 0], [1, 1]]))


if __name__ == '__main__':
    unittest.main()
