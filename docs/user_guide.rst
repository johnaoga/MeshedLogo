User Guide
==========

This guide covers detailed usage patterns and customization options for MeshedLogo.

MeshedLogo Class
----------------

The ``MeshedLogo`` class is the main user-facing interface. Import it from the project root:

.. code-block:: python

   from meshed_logo import MeshedLogo

   logo = MeshedLogo(
       canvas_size=(1200, 800),
       background_color='black'
   )

Core Methods
------------

generate()
~~~~~~~~~~

Generate a simple text logo with customization options.

**Signature:**

.. code-block:: python

   logo.generate(
       text,
       output_file,
       colors=None,
       scale=2.0,
       mesh_density=1.5,
       show_wireframe=True,
       show_vertices=True,
       show_surface=True,
       wireframe_thickness=0.5,
       vertex_size=8.0,
       vertex_mode='all',
       invert_mode=False,
       invert_margin=50,
       dpi=300
   )

**Parameters:**

- ``text`` (str): Text to render
- ``output_file`` (str): Output file path
- ``colors`` (list): List of color values for gradient (optional)
- ``scale`` (float): Scale factor (default: 2.0)
- ``mesh_density`` (float): Interior point density (default: 1.5)
- ``show_wireframe`` (bool): Show triangle edges (default: True)
- ``show_vertices`` (bool): Show vertex dots (default: True)
- ``show_surface`` (bool): Show filled triangles (default: True)
- ``wireframe_thickness`` (float): Line thickness for edges (default: 0.5)
- ``vertex_size`` (float): Size of vertex dots (default: 8.0)
- ``vertex_mode`` (str): Vertex display mode: 'all', 'random' (50%), or 'none'
- ``invert_mode`` (bool): Mesh the background instead of character (default: False)
- ``invert_margin`` (int): Margin around character in invert mode (default: 50)
- ``dpi`` (int): Output resolution (default: 300)

**Examples:**

.. code-block:: python

   # Basic logo
   logo.generate("HELLO", output_file="hello.png")

   # Custom colors and scale
   logo.generate(
       "CODE",
       output_file="code.png",
       colors=['cyan', 'magenta', 'yellow'],
       scale=3.0,
       mesh_density=2.0
   )

   # Wireframe only (no surface)
   logo.generate(
       "MESH",
       output_file="mesh.png",
       show_surface=False,
       show_vertices=False,
       wireframe_thickness=1.0
   )

   # Surface only (no wireframe or vertices)
   logo.generate(
       "SURF",
       output_file="surf.png",
       show_wireframe=False,
       show_vertices=False
   )

   # Inverted mode (background meshed)
   logo.generate(
       "TEXT",
       output_file="inverted.png",
       invert_mode=True,
       invert_margin=30
   )

   # Random vertices only
   logo.generate(
       "DOTS",
       output_file="dots.png",
       show_surface=False,
       show_wireframe=False,
       vertex_mode='random',
       vertex_size=15.0
   )

generate_multi()
~~~~~~~~~~~~~~~~

Generate a multi-component logo with multiple text elements.

**Signature:**

.. code-block:: python

   logo.generate_multi(
       components,
       name="Multi Logo",
       output_file="output.png",
       show_wireframe=True,
       show_vertices=True,
       dpi=300
   )

**Parameters:**

- ``components`` (list): List of component dictionaries
- ``name`` (str): Logo name
- ``output_file`` (str): Output file path
- ``show_wireframe`` (bool): Show edges for all components
- ``show_vertices`` (bool): Show vertices for all components
- ``dpi`` (int): Output resolution

**Component Dictionary:**

.. code-block:: python

   {
       'text': 'WORD',           # Required: Text to render
       'position': (x, y),       # Required: Position on canvas
       'scale': 2.5,             # Optional: Scale factor
       'colors': ['#fff', '#0ff'] # Optional: Color list
   }

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
~~~~~~~~~~~~~~~~~~~~

Generate the classic MEMA & INMA logo.

**Signature:**

.. code-block:: python

   logo.generate_mema_inma(
       output_file="mema_inma.png",
       output_dir="output/"
   )

**Parameters:**

- ``output_file`` (str): Output file name
- ``output_dir`` (str): Output directory path

**Example:**

.. code-block:: python

   logo = MeshedLogo()
   logo.generate_mema_inma(output_file="mema_inma.png")

Configuration Methods
---------------------

set_canvas()
~~~~~~~~~~~~

Update the canvas size.

.. code-block:: python

   logo.set_canvas(1920, 1080)

set_background()
~~~~~~~~~~~~~~~~

Update the background color.

.. code-block:: python

   logo.set_background('#000000')  # Black
   logo.set_background('white')    # White

Rendering Options
-----------------

Surface Control
~~~~~~~~~~~~~~~

Control whether filled triangles are displayed:

.. code-block:: python

   # Show only the mesh (wireframe)
   logo.generate("TEXT", show_surface=False, show_vertices=False)

   # Show only the surface (no edges or points)
   logo.generate("TEXT", show_wireframe=False, show_vertices=False)

Wireframe Styling
~~~~~~~~~~~~~~~~~

Customize the wireframe appearance:

.. code-block:: python

   # Thick wireframe
   logo.generate("TEXT", wireframe_thickness=2.0)

   # Thin wireframe
   logo.generate("TEXT", wireframe_thickness=0.3)

Vertex Display
~~~~~~~~~~~~~~

Control vertex point display:

.. code-block:: python

   # All vertices
   logo.generate("TEXT", vertex_mode='all', vertex_size=10.0)

   # Random 50% of vertices
   logo.generate("TEXT", vertex_mode='random', vertex_size=12.0)

   # No vertices
   logo.generate("TEXT", vertex_mode='none')
   # or
   logo.generate("TEXT", show_vertices=False)

Invert Mode
~~~~~~~~~~~

Mesh the background instead of the character:

.. code-block:: python

   # Character becomes a hole in meshed background
   logo.generate(
       "TEXT",
       invert_mode=True,
       invert_margin=50,  # Pixels of margin around character
       colors=['cyan', 'magenta']
   )

This is useful for creating negative space logos or special effects.

Advanced Usage
--------------

Using Individual Modules
~~~~~~~~~~~~~~~~~~~~~~~~

For advanced use cases, you can import and use individual modules from ``lib/``:

.. code-block:: python

   from lib.character_renderer import CharacterRenderer
   from lib.contour_extractor import ContourExtractor
   from lib.mesh_generator import MeshGenerator

   # Render a character
   renderer = CharacterRenderer(default_width=200, default_height=200)
   char_img = renderer.render('M', save_path='output/m.png')

   # Extract contour
   extractor = ContourExtractor(method='opencv')
   contour = extractor.extract_largest(char_img.matrix, simplify=True)

   # Generate mesh
   generator = MeshGenerator()
   mesh = generator.generate(
       contour.points,
       add_interior_points=True,
       num_interior_points=50
   )

See ``bin/example_advanced.py`` for comprehensive examples.

Color Specification
-------------------

Colors can be specified in multiple formats:

.. code-block:: python

   # Hex codes
   colors=['#00ff00', '#00ffff', '#ff00ff']

   # Named colors
   colors=['cyan', 'magenta', 'yellow']

   # RGB tuples (0-1 range)
   colors=[(0, 1, 0), (0, 1, 1), (1, 0, 1)]

   # Single color (no gradient)
   colors=['white']

Output Quality
--------------

Control output resolution with the ``dpi`` parameter:

.. code-block:: python

   # Standard quality (default)
   logo.generate("TEXT", dpi=300)

   # High quality
   logo.generate("TEXT", dpi=600)

   # Screen quality
   logo.generate("TEXT", dpi=150)

Higher DPI values produce larger file sizes but better quality for printing.

Best Practices
--------------

1. **Start with defaults**: The default parameters work well for most cases
2. **Adjust mesh_density**: Increase for complex characters, decrease for simple ones
3. **Use appropriate scale**: Scale 2.0-3.0 works well for most text
4. **Test rendering options**: Try different combinations of surface/wireframe/vertices
5. **Consider canvas size**: Ensure canvas is large enough for your text at the chosen scale
6. **Use high DPI for printing**: 300+ DPI recommended for print output
