API Reference
=============

This page provides complete API documentation for all public classes and methods.

MeshedLogo Class
----------------

.. code-block:: python

   from meshed_logo import MeshedLogo

Main user-facing class for generating meshed logos.

Constructor
~~~~~~~~~~~

.. code-block:: python

   MeshedLogo(canvas_size=(1200, 800), background_color='black')

**Parameters:**

- ``canvas_size`` (tuple): Canvas dimensions as (width, height). Default: (1200, 800)
- ``background_color`` (str): Background color. Default: 'black'

Methods
~~~~~~~

generate()
^^^^^^^^^^

Generate a simple text logo.

.. code-block:: python

   generate(
       text: str,
       output_file: str,
       colors: List[str] = None,
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
       dpi: int = 300
   ) -> None

**Parameters:**

- ``text`` (str): Text to render
- ``output_file`` (str): Output file path (PNG)
- ``colors`` (List[str], optional): List of colors for gradient. Default: ['cyan', 'magenta']
- ``scale`` (float): Scale factor for character size. Default: 2.0
- ``mesh_density`` (float): Interior point density multiplier. Default: 1.5
- ``show_wireframe`` (bool): Show triangle edges. Default: True
- ``show_vertices`` (bool): Show vertex dots. Default: True
- ``show_surface`` (bool): Show filled triangles. Default: True
- ``wireframe_thickness`` (float): Line thickness for edges. Default: 0.5
- ``vertex_size`` (float): Size of vertex dots. Default: 8.0
- ``vertex_mode`` (str): Vertex display mode: 'all', 'random', 'none'. Default: 'all'
- ``invert_mode`` (bool): Mesh background instead of character. Default: False
- ``invert_margin`` (int): Margin in pixels for invert mode. Default: 50
- ``dpi`` (int): Output resolution. Default: 300

**Returns:** None (saves to file)

**Example:**

.. code-block:: python

   logo = MeshedLogo()
   logo.generate("HELLO", output_file="hello.png")

generate_multi()
^^^^^^^^^^^^^^^^

Generate a multi-component logo.

.. code-block:: python

   generate_multi(
       components: List[Dict],
       name: str = "Multi Logo",
       output_file: str = "output.png",
       show_wireframe: bool = True,
       show_vertices: bool = True,
       dpi: int = 300
   ) -> None

**Parameters:**

- ``components`` (List[Dict]): List of component dictionaries
- ``name`` (str): Logo name. Default: "Multi Logo"
- ``output_file`` (str): Output file path. Default: "output.png"
- ``show_wireframe`` (bool): Show edges for all components. Default: True
- ``show_vertices`` (bool): Show vertices for all components. Default: True
- ``dpi`` (int): Output resolution. Default: 300

**Component Dictionary Structure:**

.. code-block:: python

   {
       'text': str,           # Required: Text to render
       'position': (int, int), # Required: (x, y) position
       'scale': float,        # Optional: Scale factor
       'colors': List[str]    # Optional: Color list
   }

**Returns:** None (saves to file)

**Example:**

.. code-block:: python

   logo = MeshedLogo(canvas_size=(1400, 700))
   components = [
       {
           'text': 'MESHED',
           'position': (100, 400),
           'scale': 2.5,
           'colors': ['cyan', 'magenta']
       },
       {
           'text': 'LOGO',
           'position': (800, 400),
           'scale': 2.5,
           'colors': ['yellow', 'white']
       }
   ]
   logo.generate_multi(components, output_file="multi.png")

generate_mema_inma()
^^^^^^^^^^^^^^^^^^^^

Generate the classic MEMA & INMA logo.

.. code-block:: python

   generate_mema_inma(
       output_file: str = "mema_inma.png",
       output_dir: str = "output/"
   ) -> None

**Parameters:**

- ``output_file`` (str): Output file name. Default: "mema_inma.png"
- ``output_dir`` (str): Output directory. Default: "output/"

**Returns:** None (saves to file)

**Example:**

.. code-block:: python

   logo = MeshedLogo()
   logo.generate_mema_inma(output_file="mema_inma.png")

set_canvas()
^^^^^^^^^^^^

Update the canvas size.

.. code-block:: python

   set_canvas(width: int, height: int) -> None

**Parameters:**

- ``width`` (int): Canvas width in pixels
- ``height`` (int): Canvas height in pixels

**Returns:** None

**Example:**

.. code-block:: python

   logo.set_canvas(1920, 1080)

set_background()
^^^^^^^^^^^^^^^^

Update the background color.

.. code-block:: python

   set_background(color: str) -> None

**Parameters:**

- ``color`` (str): Background color (hex, name, or RGB)

**Returns:** None

**Example:**

.. code-block:: python

   logo.set_background('#000000')
   logo.set_background('white')

Library Modules (Advanced)
---------------------------

CharacterRenderer
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from lib.character_renderer import CharacterRenderer

Renders characters to binary image matrices.

**Constructor:**

.. code-block:: python

   CharacterRenderer(
       default_width: int = 200,
       default_height: int = 200,
       default_thickness: int = 1
   )

**Methods:**

``render(char, width, height, thickness, save_path)``
  Render a single character.
  
  - Returns: ``CharacterImage``

CharacterImage (dataclass)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class CharacterImage:
       matrix: np.ndarray      # Binary matrix (0=char, 1=background)
       character: str          # The rendered character
       width: int              # Image width
       height: int             # Image height
       filepath: str = None    # Saved file path

       def save(self, filepath: str) -> str:
           """Save image to file"""

StringProcessor
~~~~~~~~~~~~~~~

.. code-block:: python

   from lib.string_processor import StringProcessor

Processes text strings and mathematical formulas.

**Constructor:**

.. code-block:: python

   StringProcessor(
       char_width: int = 200,
       char_height: int = 200
   )

**Methods:**

``process(text, save_dir)``
  Process a string into character images.
  
  - Returns: ``ProcessedString``

ProcessedString (dataclass)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class ProcessedString:
       text: str                        # Original text
       characters: List[CharacterImage] # List of character images
       num_characters: int              # Number of characters
       render_mode: RenderMode          # NORMAL or FORMULA

ContourExtractor
~~~~~~~~~~~~~~~~

.. code-block:: python

   from lib.contour_extractor import ContourExtractor

Extracts contour points from images.

**Constructor:**

.. code-block:: python

   ContourExtractor(method: str = 'opencv')

**Methods:**

``extract_largest(image, simplify, epsilon)``
  Extract the largest contour from an image.
  
  - Returns: ``ContourData``

``extract_with_holes(image, simplify, epsilon)``
  Extract outer contour and interior holes.
  
  - Returns: ``(ContourData, List[ContourData])``

ContourData (dataclass)
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class ContourData:
       points: np.ndarray      # (N, 2) array of (x,y) coordinates
       num_points: int         # Number of points

       def get_bounding_box(self) -> Tuple[float, float, float, float]:
           """Returns (x_min, y_min, x_max, y_max)"""

       def simplify(self, epsilon: float = 2.0) -> 'ContourData':
           """Simplify using Douglas-Peucker algorithm"""

       def save_points(self, filepath: str, format: str = 'auto'):
           """Save points to file (.txt, .csv, .npy)"""

MeshGenerator
~~~~~~~~~~~~~

.. code-block:: python

   from lib.mesh_generator import MeshGenerator

Creates triangle meshes from point sets.

**Constructor:**

.. code-block:: python

   MeshGenerator()

**Methods:**

``generate(points, add_interior_points, num_interior_points, filter_by_image)``
  Generate a triangle mesh from points.
  
  - Returns: ``MeshData``

``visualize(mesh_data, show_edges, show_points)``
  Visualize a mesh using matplotlib.

MeshData (dataclass)
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class MeshData:
       points: np.ndarray      # (N, 2) array of vertex coordinates
       triangles: np.ndarray   # (M, 3) array of triangle indices
       num_vertices: int       # Number of vertices
       num_triangles: int      # Number of triangles

       def get_edges(self) -> np.ndarray:
           """Returns unique edges as (E, 2) array"""

       def get_triangle_areas(self) -> np.ndarray:
           """Returns array of triangle areas"""

       def save_mesh(self, filepath: str, format: str = 'auto'):
           """Save mesh to file (.obj, .ply, .txt)"""

LogoGenerator
~~~~~~~~~~~~~

.. code-block:: python

   from lib.logo_generator import LogoGenerator

Orchestrates all components to generate complete logos.

**Constructor:**

.. code-block:: python

   LogoGenerator(
       canvas_size: Tuple[int, int] = (1200, 800),
       background_color: str = 'black'
   )

**Methods:**

``render_logo(mesh_data, colors, show_wireframe, show_vertices, **kwargs)``
  Render a single component logo.
  
  - Returns: ``Logo``

``create_multi_logo(components, show_wireframe, show_vertices)``
  Create a multi-component logo.
  
  - Returns: ``Logo``

``create_mema_inma_logo()``
  Create the classic MEMA & INMA logo.
  
  - Returns: ``Logo``

Logo (dataclass)
^^^^^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class Logo:
       name: str                        # Logo name
       components: List[LogoComponent]  # List of components
       canvas_size: Tuple[int, int]     # Canvas dimensions

       def save_metadata(self, filepath: str):
           """Save logo metadata to JSON"""

LogoComponent (dataclass)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   @dataclass
   class LogoComponent:
       text: str              # Component text
       mesh_data: MeshData    # Triangle mesh
       colors: List[str]      # Color list
       position: Tuple[float, float]  # (x, y) position
       scale: float           # Scale factor

Type Hints
----------

All classes and methods include proper type hints for better IDE support:

.. code-block:: python

   from typing import List, Tuple, Optional, Dict
   import numpy as np

   def generate(
       text: str,
       output_file: str,
       colors: Optional[List[str]] = None,
       scale: float = 2.0,
       mesh_density: float = 1.5,
       dpi: int = 300
   ) -> None:
       ...

Error Handling
--------------

The library raises appropriate exceptions:

**ValueError:**
  - Invalid parameters (e.g., negative scale)
  - Empty text input
  - Invalid color format

**FileNotFoundError:**
  - Missing output directory

**RuntimeError:**
  - Contour extraction failure
  - Mesh generation failure

**Example:**

.. code-block:: python

   try:
       logo = MeshedLogo()
       logo.generate("", output_file="empty.png")
   except ValueError as e:
       print(f"Invalid input: {e}")

Constants
---------

**Default Values:**

.. code-block:: python

   DEFAULT_CANVAS_SIZE = (1200, 800)
   DEFAULT_BACKGROUND = 'black'
   DEFAULT_COLORS = ['cyan', 'magenta']
   DEFAULT_SCALE = 2.0
   DEFAULT_MESH_DENSITY = 1.5
   DEFAULT_DPI = 300
   DEFAULT_WIREFRAME_THICKNESS = 0.5
   DEFAULT_VERTEX_SIZE = 8.0

**Vertex Modes:**

.. code-block:: python

   VERTEX_MODE_ALL = 'all'
   VERTEX_MODE_RANDOM = 'random'
   VERTEX_MODE_NONE = 'none'

Versioning
----------

The library follows semantic versioning (SemVer):

- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes

Current version: **1.0.0**

.. code-block:: python

   import meshed_logo
   print(meshed_logo.__version__)  # '1.0.0'
