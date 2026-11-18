"""
MeshedLogo - Triangle-meshed logo generation from text and formulas

Quick start::

    from meshedlogo import MeshedLogo

    logo = MeshedLogo()
    logo.generate("HELLO", output_file="hello.png")
"""

from importlib.metadata import PackageNotFoundError, version

from .character_renderer import CharacterRenderer, CharacterImage
from .string_processor import StringProcessor, ProcessedString, RenderMode
from .contour_extractor import ContourExtractor, ContourData
from .mesh_generator import MeshGenerator, MeshData
from .logo_generator import LogoGenerator, Logo, LogoComponent
from .meshed_logo import MeshedLogo

try:
    __version__ = version("meshedlogo")
except PackageNotFoundError:  # pragma: no cover - running from a source checkout
    __version__ = "0.0.0.dev0"

__all__ = [
    'MeshedLogo',
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
    '__version__',
]
