"""Tests for ContourExtractor"""

import unittest
import numpy as np
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.character_renderer import CharacterRenderer
from lib.contour_extractor import ContourExtractor, ContourData


class TestContourExtractor(unittest.TestCase):
    """Test cases for ContourExtractor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.extractor = ContourExtractor(method='opencv')
        self.renderer = CharacterRenderer(default_width=150, default_height=150)
        self.test_output_dir = "tests/output"
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_extractor_initialization(self):
        """Test extractor initialization"""
        self.assertEqual(self.extractor.method, 'opencv')
    
    def test_extract_from_binary_matrix(self):
        """Test extracting contours from binary matrix"""
        char_img = self.renderer.render('O')
        contours = self.extractor.extract(char_img.matrix)
        
        self.assertIsInstance(contours, list)
        self.assertGreater(len(contours), 0)
        
        for contour in contours:
            self.assertIsInstance(contour, ContourData)
            self.assertGreater(contour.num_points, 0)
    
    def test_extract_largest(self):
        """Test extracting largest contour"""
        char_img = self.renderer.render('A')
        largest = self.extractor.extract_largest(char_img.matrix)
        
        self.assertIsNotNone(largest)
        self.assertIsInstance(largest, ContourData)
        self.assertGreater(largest.num_points, 0)
    
    def test_simplify_contour(self):
        """Test contour simplification"""
        char_img = self.renderer.render('M')
        contour = self.extractor.extract_largest(char_img.matrix, simplify=False)
        
        if contour:
            original_points = contour.num_points
            simplified = contour.simplify(epsilon=5.0)
            
            self.assertIsInstance(simplified, ContourData)
            self.assertLessEqual(simplified.num_points, original_points)
    
    def test_get_bounding_box(self):
        """Test bounding box calculation"""
        char_img = self.renderer.render('S')
        contour = self.extractor.extract_largest(char_img.matrix)
        
        if contour:
            bbox = contour.get_bounding_box()
            self.assertEqual(len(bbox), 4)
            x_min, y_min, x_max, y_max = bbox
            
            self.assertLess(x_min, x_max)
            self.assertLess(y_min, y_max)
    
    def test_save_contour_points(self):
        """Test saving contour points"""
        char_img = self.renderer.render('T')
        contour = self.extractor.extract_largest(char_img.matrix)
        
        if contour:
            filepath = os.path.join(self.test_output_dir, 'test_contour.txt')
            saved_path = contour.save_points(filepath)
            
            self.assertEqual(saved_path, filepath)
            self.assertTrue(os.path.exists(filepath))


if __name__ == '__main__':
    unittest.main()
