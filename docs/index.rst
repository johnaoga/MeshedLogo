MeshedLogo - Triangle Mesh Logo Generator
==========================================

.. image:: _static/images/much_logo.png
   :align: center
   :alt: MeshedLogo Example

A professional, modular Python system for generating beautiful triangle-meshed logos from text and mathematical formulas.

**"MEMA & INMA forever"** - Originally created as a tribute in Euler's form: ME/IN e^(iθ)

✨ Features
-----------

- **Modular Architecture**: 5 independent, reusable components following OOP principles
- **Character Rendering**: Convert any letter or symbol to binary image matrix
- **String Processing**: Handle plain text and mathematical formulas
- **Contour Extraction**: Extract outline points from images using OpenCV
- **Mesh Generation**: Create triangle meshes using Delaunay triangulation
- **Logo Composition**: Orchestrate all components to create complete logos
- **High Quality Output**: Supports 300+ DPI with gradient colors and wireframe effects
- **Hole Detection**: Automatic detection and handling of character holes (e.g., O, A, B)
- **Rendering Options**: Extensive control over surface, wireframe, vertices, and invert modes

🚀 Quick Start
--------------

.. code-block:: python

   from meshed_logo import MeshedLogo

   logo = MeshedLogo()
   logo.generate("HELLO", output_file="output/hello.png")

📚 Documentation
----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   user_guide
   technical
   examples
   api_reference

Installation
------------

1. **Create and activate virtual environment:**

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. **Install dependencies:**

.. code-block:: bash

   pip install -r requirements.txt

Dependencies
~~~~~~~~~~~~

- ``matplotlib >= 3.8.0`` - Visualization and rendering
- ``numpy >= 1.26.0`` - Numerical operations
- ``scipy >= 1.11.0`` - Delaunay triangulation
- ``Pillow >= 10.0.0`` - Image processing
- ``opencv-python >= 4.8.0`` - Contour extraction

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
