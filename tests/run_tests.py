#!/usr/bin/env python3
"""
Test Runner - Run all unit tests
"""

import unittest
import sys
import os



def run_all_tests():
    """Discover and run all tests"""
    # Create output directory for test artifacts
    os.makedirs('tests/output', exist_ok=True)
    
    # Discover tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
