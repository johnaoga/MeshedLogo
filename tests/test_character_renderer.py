"""Tests for CharacterRenderer"""

import unittest
import numpy as np
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.character_renderer import CharacterRenderer, CharacterImage


class TestCharacterRenderer(unittest.TestCase):
    """Test cases for CharacterRenderer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.renderer = CharacterRenderer(default_width=100, default_height=100)
        self.test_output_dir = "tests/output"
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_renderer_initialization(self):
        """Test renderer initialization"""
        self.assertEqual(self.renderer.default_width, 100)
        self.assertEqual(self.renderer.default_height, 100)
    
    def test_render_basic_character(self):
        """Test rendering a basic character"""
        result = self.renderer.render('A')
        
        self.assertIsInstance(result, CharacterImage)
        self.assertEqual(result.character, 'A')
        self.assertEqual(result.width, 100)
        self.assertEqual(result.height, 100)
        self.assertEqual(result.matrix.shape, (100, 100))
    
    def test_render_with_custom_size(self):
        """Test rendering with custom size"""
        result = self.renderer.render('B', width=200, height=150)
        
        self.assertEqual(result.width, 200)
        self.assertEqual(result.height, 150)
        self.assertEqual(result.matrix.shape, (150, 200))
    
    def test_matrix_values(self):
        """Test that matrix contains only 0 and 1"""
        result = self.renderer.render('X')
        unique_values = np.unique(result.matrix)
        
        self.assertTrue(all(v in [0, 1] for v in unique_values))
    
    def test_save_image(self):
        """Test saving image to file"""
        result = self.renderer.render('M')
        filepath = os.path.join(self.test_output_dir, 'test_m.png')
        saved_path = result.save(filepath)
        
        self.assertEqual(saved_path, filepath)
        self.assertTrue(os.path.exists(filepath))
        self.assertEqual(result.filepath, filepath)
    
    def test_render_with_save_path(self):
        """Test rendering with save_path parameter"""
        filepath = os.path.join(self.test_output_dir, 'test_n.png')
        result = self.renderer.render('N', save_path=filepath)
        
        self.assertTrue(os.path.exists(filepath))
        self.assertEqual(result.filepath, filepath)
    
    def test_render_symbol(self):
        """Test rendering special symbols"""
        result = self.renderer.render('∞')
        
        self.assertIsInstance(result, CharacterImage)
        self.assertEqual(result.character, '∞')
    
    def tearDown(self):
        """Clean up test files"""
        # Optionally remove test files
        pass


if __name__ == '__main__':
    unittest.main()
