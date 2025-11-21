"""Tests for MeshedLogo front-class"""

import unittest
import os
import sys
import numpy as np
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meshed_logo import MeshedLogo


class TestMeshedLogo(unittest.TestCase):
    """Test cases for MeshedLogo"""
    
    def setUp(self):
        """Set up test fixtures"""
        random.seed(42)
        np.random.seed(42)
        
        self.logo = MeshedLogo(canvas_size=(800, 600))
        self.test_output_dir = "tests/output"
        os.makedirs(self.test_output_dir, exist_ok=True)
    
    def test_initialization(self):
        """Test MeshedLogo initialization"""
        self.assertEqual(self.logo.canvas_size, (800, 600))
        self.assertEqual(self.logo.background_color, 'black')
    
    def test_generate_simple(self):
        """Test generating simple text logo"""
        output_file = os.path.join(self.test_output_dir, 'test_simple.png')
        result = self.logo.generate("TEST", output_file=output_file)
        
        self.assertEqual(result, output_file)
        self.assertTrue(os.path.exists(output_file))
    
    def test_generate_with_custom_colors(self):
        """Test generating with custom colors"""
        output_file = os.path.join(self.test_output_dir, 'test_colors.png')
        result = self.logo.generate(
            "ABC",
            output_file=output_file,
            colors=['red', 'green', 'blue']
        )
        
        self.assertTrue(os.path.exists(output_file))
    
    def test_generate_multi_component(self):
        """Test generating multi-component logo"""
        components = [
            {
                'text': 'MULTI',
                'position': (100, 300),
                'scale': 1.5,
                'colors': ['cyan', 'magenta']
            },
            {
                'text': 'TEST',
                'position': (400, 300),
                'scale': 1.5,
                'colors': ['yellow', 'white']
            }
        ]
        
        output_file = os.path.join(self.test_output_dir, 'test_multi.png')
        result = self.logo.generate_multi(components, output_file=output_file)
        
        self.assertTrue(os.path.exists(output_file))
    
    def test_set_canvas(self):
        """Test updating canvas size"""
        self.logo.set_canvas(1000, 800)
        self.assertEqual(self.logo.canvas_size, (1000, 800))
    
    def test_set_background(self):
        """Test updating background color"""
        self.logo.set_background('#123456')
        self.assertEqual(self.logo.background_color, '#123456')
    
    def test_generate_mema_inma(self):
        """Test generating MEMA & INMA logo"""
        output_file = 'test_mema_inma.png'
        result = self.logo.generate_mema_inma(
            output_file=output_file,
            output_dir=self.test_output_dir
        )
        
        expected_path = os.path.join(self.test_output_dir, output_file)
        self.assertEqual(result, expected_path)
        self.assertTrue(os.path.exists(expected_path))


if __name__ == '__main__':
    unittest.main()
