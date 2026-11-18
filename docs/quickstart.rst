Quick Start Guide
==================

This guide will get you up and running with MeshedLogo in minutes.

Installation
------------

**From PyPI (recommended):**

.. code-block:: bash

   pip install meshedlogo

**From source (for development):**

.. code-block:: bash

   git clone https://github.com/johnaoga/MeshedLogo.git
   cd MeshedLogo
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev,docs]"

Basic Usage
-----------

Simple Text Logo
~~~~~~~~~~~~~~~~

.. code-block:: python

   from meshedlogo import MeshedLogo

   logo = MeshedLogo()
   logo.generate("HELLO", output_file="output/hello.png")

Custom Colors
~~~~~~~~~~~~~

.. code-block:: python

   logo = MeshedLogo()
   logo.generate(
       "CODE",
       output_file="output/code.png",
       colors=['#00ff00', '#00ffff', '#ff00ff'],
       scale=2.5
   )

Multi-Component Logo
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   logo = MeshedLogo(canvas_size=(2400, 700))

   components = [
       {
           'text': 'MESHED',
           'position': (100, 400),
           'scale': 2.0,
           'colors': ['cyan', 'magenta']
       },
       {
           'text': 'LOGO',
           'position': (1600, 400),
           'scale': 2.0,
           'colors': ['yellow', 'white']
       }
   ]

   logo.generate_multi(components, output_file="output/multi.png")

LaTeX Formulas
~~~~~~~~~~~~~~

Render mathematical formulas using LaTeX syntax:

.. code-block:: python

   logo = MeshedLogo()

   # Euler's formula
   logo.generate("$e^{i\\theta}$", output_file="output/euler.png")

   # Einstein's equation
   logo.generate("$E=mc^2$", output_file="output/einstein.png")

   # Fractions
   logo.generate("$\\frac{a}{b}$", output_file="output/fraction.png")

MEMA & INMA Classic
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   logo = MeshedLogo()
   logo.generate_mema_inma(output_file="mema_inma.png")

Command Line Usage
------------------

.. code-block:: bash

   # Generate a simple logo
   meshedlogo "YOUR TEXT" output/logo.png

   # Run simple examples
   python examples/example_simple.py

   # Run advanced examples
   python examples/example_advanced.py

Running Tests
-------------

.. code-block:: bash

   pytest

**Expected result:** All tests should pass ✓

Project Structure
-----------------

::

   USE THIS:
     └── meshedlogo.MeshedLogo        ← Main class (simple API)

   EXAMPLES:
     └── examples/
         ├── example_simple.py        ← Simple examples
         └── example_advanced.py      ← Advanced examples

   LIBRARY (for advanced use):
     └── src/meshedlogo/
         ├── meshed_logo.py           ← MeshedLogo class
         ├── cli.py                   ← ``meshedlogo`` command
         ├── character_renderer.py
         ├── string_processor.py
         ├── contour_extractor.py
         ├── mesh_generator.py
         └── logo_generator.py

   TESTS:
     └── tests/
         └── test_*.py

Tips
----

1. **Start simple**: Use the ``MeshedLogo`` class
2. **Run examples**: Check ``examples/example_simple.py`` for ideas
3. **Test changes**: Run ``pytest``
4. **Custom colors**: Use hex codes like '#00ff00' or names like 'cyan'
5. **Adjust density**: Higher mesh_density = more triangles = more detail

Next Steps
----------

- Explore :doc:`user_guide` for detailed usage patterns
- See :doc:`examples` for showcase and advanced examples
- Check :doc:`technical` to understand how it works
- Reference :doc:`api_reference` for complete API documentation
