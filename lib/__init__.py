"""
Logo Generation Library
A modular system for generating triangle-meshed logos from text and formulas
"""

from lib.character_renderer import CharacterRenderer, CharacterImage
from lib.string_processor import StringProcessor, ProcessedString, RenderMode
from lib.contour_extractor import ContourExtractor, ContourData
from lib.mesh_generator import MeshGenerator, MeshData
from lib.logo_generator import LogoGenerator, Logo, LogoComponent

__all__ = [
    'CharacterRenderer',
    'CharacterImage',
    'StringProcessor',
    'ProcessedString',
    'RenderMode',
    'ContourExtractor',
    'ContourData',
    'MeshGenerator',
    'MeshData',
    'LogoGenerator',
    'Logo',
    'LogoComponent',
]

__version__ = '1.0.0'
