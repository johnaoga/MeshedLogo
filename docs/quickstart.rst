Quick Start Guide
==================

This guide will get you up and running with MeshedLogo in minutes.

Installation
------------

1. **Create and activate virtual environment:**

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. **Install dependencies:**

.. code-block:: bash

   pip install -r requirements.txt

Basic Usage
-----------

Simple Text Logo
~~~~~~~~~~~~~~~~

.. code-block:: python

   from meshed_logo import MeshedLogo

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

   logo.generate_multi(components, output_file="output/multi.png")

MEMA & INMA Classic
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   logo = MeshedLogo()
   logo.generate_mema_inma(output_file="mema_inma.png")

Command Line Usage
------------------

.. code-block:: bash

   # Generate a simple logo
   python bin/generate_logo.py "YOUR TEXT" output/logo.png

   # Run simple examples
   python bin/example_simple.py

   # Run advanced examples
   python bin/example_advanced.py

Running Tests
-------------

.. code-block:: bash

   # Run all tests
   python tests/run_tests.py

   # Or use unittest
   python -m unittest discover tests

**Expected result:** All tests should pass ✓

Project Structure
-----------------

::

   USE THIS:
     └── meshed_logo.py      ← Main class (simple API)

   EXAMPLES:
     └── bin/
         ├── generate_logo.py       ← CLI tool
         ├── example_simple.py      ← Simple examples
         └── example_advanced.py    ← Advanced examples

   LIBRARY (for advanced use):
     └── lib/
         ├── character_renderer.py
         ├── string_processor.py
         ├── contour_extractor.py
         ├── mesh_generator.py
         └── logo_generator.py

   TESTS:
     └── tests/
         ├── test_*.py
         └── run_tests.py

Tips
----

1. **Start simple**: Use ``meshed_logo.py`` MeshedLogo class
2. **Run examples**: Check ``bin/example_simple.py`` for ideas
3. **Test changes**: Run ``python tests/run_tests.py``
4. **Custom colors**: Use hex codes like '#00ff00' or names like 'cyan'
5. **Adjust density**: Higher mesh_density = more triangles = more detail

Next Steps
----------

- Explore :doc:`user_guide` for detailed usage patterns
- See :doc:`examples` for showcase and advanced examples
- Check :doc:`technical` to understand how it works
- Reference :doc:`api_reference` for complete API documentation
