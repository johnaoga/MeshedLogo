#!/usr/bin/env python3
"""
Generate the example images and the ``examples.rst`` page for the docs.

Every entry in ``EXAMPLES`` holds the exact code snippet shown in the
documentation. The snippet is executed to produce the image, and the same
snippet is written into ``examples.rst`` next to that image, so the two can
never drift apart. Run by CI before ``sphinx-build``::

    python docs/generate_examples.py            # images + examples.rst
    python docs/generate_examples.py --rst-only # regenerate the page only
"""

import argparse
import os
import random
import sys
import textwrap
import time
from pathlib import Path

import numpy as np

DOCS_DIR = Path(__file__).resolve().parent
IMAGE_DIR = DOCS_DIR / "_static" / "images" / "examples"
RST_PATH = DOCS_DIR / "examples.rst"
SEED = 42

# (section, title, output filename, description, code)
# ``code`` is executed as-is with the current directory set to IMAGE_DIR.
EXAMPLES = [
    # ------------------------------------------------------------------ styles
    ("Rendering Styles", "Default", "default.png",
     "Surface, wireframe and vertices all enabled - the default look.",
     '''
     logo = MeshedLogo()
     logo.generate("MESH", output_file="default.png")
     '''),
    ("Rendering Styles", "Surface Only", "surface_only.png",
     "Display only the filled triangles without wireframe or vertices.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "TEXT",
         output_file="surface_only.png",
         show_wireframe=False,
         show_vertices=False,
         colors=['cyan', 'magenta']
     )
     '''),
    ("Rendering Styles", "Wireframe Only", "wireframe_only.png",
     "Display only the mesh lines without surface or vertices.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "MESH",
         output_file="wireframe_only.png",
         show_surface=False,
         show_vertices=False,
         wireframe_thickness=1.0,
         colors=['cyan']
     )
     '''),
    ("Rendering Styles", "Vertices Only", "vertices_only.png",
     "Display only the vertex points.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "DOTS",
         output_file="vertices_only.png",
         show_surface=False,
         show_wireframe=False,
         vertex_size=15.0,
         colors=['cyan']
     )
     '''),
    ("Rendering Styles", "Thick Wireframe", "combined.png",
     "Surface with a thick wireframe.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "TEXT",
         output_file="combined.png",
         show_surface=True,
         show_wireframe=True,
         wireframe_thickness=2.0,
         colors=['cyan', 'magenta', 'yellow']
     )
     '''),
    ("Rendering Styles", "Invert Mode", "inverted.png",
     "Mesh the background instead of the character: the text becomes a hole "
     "in the meshed background, creating a negative space effect.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "TEXT",
         output_file="inverted.png",
         invert_mode=True,
         invert_margin=50,
         colors=['cyan', 'magenta']
     )
     '''),
    ("Rendering Styles", "Random Vertices", "random_vertices.png",
     "Display 50% of the vertices, randomly selected.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "TEXT",
         output_file="random_vertices.png",
         vertex_mode='random',
         vertex_size=12.0,
         colors=['cyan', 'magenta']
     )
     '''),
    # ------------------------------------------------------------ multi-part
    ("Multi-Component Logos", "Side by Side", "side_by_side.png",
     "Two components with independent colors placed on one canvas.",
     '''
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

     logo.generate_multi(components, output_file="side_by_side.png")
     '''),
    ("Multi-Component Logos", "Stacked", "stacked.png",
     "Components stacked vertically. The y axis grows downwards, so a smaller y places a component higher on the canvas.",
     '''
     logo = MeshedLogo(canvas_size=(1000, 1000))

     components = [
         {
             'text': 'TOP',
             'position': (300, 300),
             'scale': 2.0,
             'colors': ['cyan', 'magenta']
         },
         {
             'text': 'BOTTOM',
             'position': (200, 700),
             'scale': 2.0,
             'colors': ['yellow', 'white']
         }
     ]

     logo.generate_multi(components, output_file="stacked.png")
     '''),
    # ---------------------------------------------------------------- colors
    ("Color Schemes", "Monochrome", "mono.png",
     "A single color.",
     '''
     logo = MeshedLogo()
     logo.generate("TEXT", output_file="mono.png", colors=['white'])
     '''),
    ("Color Schemes", "Dual Color", "dual.png",
     "A two-color gradient, applied left to right across the text bounds.",
     '''
     logo = MeshedLogo()
     logo.generate("TEXT", output_file="dual.png", colors=['cyan', 'magenta'])
     '''),
    ("Color Schemes", "Multi Color", "multi_color.png",
     "Any number of colors can be used in the gradient.",
     '''
     logo = MeshedLogo()
     logo.generate("TEXT", output_file="multi_color.png",
                   colors=['cyan', 'magenta', 'yellow', 'white'])
     '''),
    # --------------------------------------------------------------- density
    ("Mesh Density", "Low Density (Coarse Mesh)", "density_low.png",
     "About 25 interior points for a sparser, more geometric look.",
     '''
     logo = MeshedLogo()
     logo.generate("TEXT", output_file="density_low.png", mesh_density=0.5)
     '''),
    ("Mesh Density", "Default Density", "density_default.png",
     "About 75 interior points - balanced between detail and simplicity.",
     '''
     logo = MeshedLogo()
     logo.generate("TEXT", output_file="density_default.png", mesh_density=1.5)
     '''),
    ("Mesh Density", "High Density (Fine Mesh)", "density_high.png",
     "About 150 interior points for a more detailed mesh.",
     '''
     logo = MeshedLogo()
     logo.generate("TEXT", output_file="density_high.png", mesh_density=3.0)
     '''),
    # -------------------------------------------------------------- complete
    ("Complete Examples", "Neon Effect", "neon.png",
     "A neon wireframe effect with random glowing vertices.",
     '''
     logo = MeshedLogo(background_color='black')
     logo.generate(
         "NEON",
         output_file="neon.png",
         colors=['#00ffff', '#ff00ff', '#ffff00'],
         show_surface=False,
         wireframe_thickness=1.5,
         vertex_mode='random',
         vertex_size=10.0,
         mesh_density=2.0,
         scale=3.0
     )
     '''),
    ("Complete Examples", "Minimalist", "minimal.png",
     "Thin black lines on white.",
     '''
     logo = MeshedLogo(background_color='white')
     logo.generate(
         "MINIMAL",
         output_file="minimal.png",
         colors=['#000000'],
         show_vertices=False,
         wireframe_thickness=0.3,
         mesh_density=1.0,
         scale=2.5
     )
     '''),
    ("Complete Examples", "Abstract Art", "abstract.png",
     "High-density mesh with an RGB gradient.",
     '''
     logo = MeshedLogo(canvas_size=(1200, 1200), background_color='black')
     logo.generate(
         "ART",
         output_file="abstract.png",
         colors=['#ff0000', '#00ff00', '#0000ff'],
         wireframe_thickness=1.0,
         vertex_size=12.0,
         mesh_density=2.5,
         scale=4.0
     )
     '''),
    ("Complete Examples", "Corporate Logo", "corporate.png",
     "A two-word logo with brand colors and no vertices.",
     '''
     logo = MeshedLogo(canvas_size=(2200, 600), background_color='#1a1a1a')

     components = [
         {
             'text': 'MESH',
             'position': (100, 400),
             'scale': 2.5,
             'colors': ['#0088ff', '#00ffff']
         },
         {
             'text': 'TECH',
             'position': (1100, 400),
             'scale': 2.5,
             'colors': ['#00ffff', '#00ff88']
         }
     ]

     logo.generate_multi(
         components,
         name="MeshTech",
         output_file="corporate.png",
         show_vertices=False
     )
     '''),
    ("Complete Examples", "MEMA & INMA Classic", "mema_inma.png",
     "The original tribute logo, with the mathematical formula rendering.",
     '''
     logo = MeshedLogo()
     logo.generate_mema_inma(output_file="mema_inma.png", output_dir=".")
     '''),
    # ----------------------------------------------------------------- latex
    ("LaTeX Formulas", "Euler's Formula", "euler.png",
     "Wrap LaTeX in ``$...$``. Superscripts are rendered as a single glyph group.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "$e^{i\\\\theta}$",
         output_file="euler.png",
         colors=['cyan', 'magenta', 'yellow'],
         scale=3.0
     )
     '''),
    ("LaTeX Formulas", "Einstein's Equation", "einstein.png",
     "The mass-energy equivalence formula.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "$E=mc^2$",
         output_file="einstein.png",
         colors=['yellow', 'white'],
         scale=2.5
     )
     '''),
    ("LaTeX Formulas", "Fractions", "fraction.png",
     "Fractions render with a proper horizontal bar.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "$\\\\frac{a}{b}$",
         output_file="fraction.png",
         colors=['cyan', 'magenta'],
         scale=3.0
     )
     '''),
    ("LaTeX Formulas", "Complex Formula", "mema_formula.png",
     "The complete MEMA/INMA tribute formula, rendered as a single shape via "
     "``RenderMode.SINGLE`` on the lower-level ``LogoGenerator`` API.",
     '''
     from meshedlogo import LogoGenerator, RenderMode

     generator = LogoGenerator(canvas_size=(1200, 600))

     components = [{
         'text': '$\\\\frac{\\\\text{ME}}{\\\\text{IN}}e^{i\\\\theta}$',
         'position': (300, 300),
         'scale': 3.0,
         'colors': ['cyan', 'magenta', 'yellow'],
         'render_mode': RenderMode.SINGLE
     }]

     logo = generator.create_logo('MEMA-INMA Formula', components)
     generator.render_logo(logo, 'mema_formula.png')
     '''),
    ("LaTeX Formulas", "Mixed Text and Formula", "mesh_styled.png",
     "Mix regular text with formula-styled characters.",
     '''
     logo = MeshedLogo()
     logo.generate(
         "m$e$sh",
         output_file="mesh_styled.png",
         colors=['cyan', 'yellow'],
         scale=2.5
     )
     '''),
]

RST_HEADER = """\
Examples Showcase
=================

.. note::

   This page is generated by ``docs/generate_examples.py``. Every image below
   is rendered from the code shown next to it on each documentation build, so
   the pictures always match the current release. Edit the script, not this
   file.

All examples assume:

.. code-block:: python

   from meshedlogo import MeshedLogo

Gallery
-------

.. image:: _static/images/board_logo.png
   :alt: BOARD Logo
   :align: center
   :width: 700px

**BOARD** - Multi-character logo with gradient colors from cyan to magenta, showing the mesh structure and vertices.

.. image:: _static/images/much_logo.png
   :alt: MUCH Logo
   :align: center
   :width: 700px

**MUCH** - Another multi-character example demonstrating mesh generation for various letter shapes including characters with holes.
"""

RST_FOOTER = """\
Command Line
------------

The ``meshedlogo`` command exposes the most common options:

.. code-block:: bash

   meshedlogo "HELLO" output/hello.png
   meshedlogo "NEON" neon.png --no-surface --colors '#00ffff' '#ff00ff'
   meshedlogo --help

   # Use single quotes around LaTeX so the shell does not expand ``$e``
   meshedlogo '$e^{i\\theta}$' euler.png --colors cyan magenta --scale 3

Example Scripts
---------------

.. code-block:: bash

   # Basic usage patterns
   python examples/example_simple.py

   # Lower-level API: renderer, contours, meshes
   python examples/example_advanced.py

Both scripts write their output to an ``output/`` directory.

Tips for Great Logos
--------------------

1. **Choose appropriate mesh density**: Complex characters benefit from higher density
2. **Experiment with colors**: Gradient colors create dynamic effects
3. **Consider the background**: Dark backgrounds work well with bright colors
4. **Use high DPI for printing**: 300+ DPI recommended
5. **Test different rendering modes**: Surface, wireframe, and vertex combinations
6. **Adjust scale for canvas**: Ensure text fits comfortably on canvas
7. **Use invert mode creatively**: Great for special effects and negative space

Further Exploration
-------------------

- See :doc:`user_guide` for detailed API documentation
- See :doc:`technical` to understand the mesh generation process
"""


def underline(title, char):
    return f"{title}\n{char * len(title)}\n"


def render_rst():
    parts = [RST_HEADER]
    current_section = None
    for section, title, filename, description, code in EXAMPLES:
        if section != current_section:
            parts.append("\n" + underline(section, "-"))
            current_section = section
        parts.append("\n" + underline(title, "~"))
        parts.append(f"\n{description}\n")
        parts.append("\n.. code-block:: python\n\n")
        parts.append(textwrap.indent(textwrap.dedent(code).strip(), "   ") + "\n")
        parts.append(f"\n.. image:: _static/images/examples/{filename}\n"
                     f"   :alt: {title}\n   :align: center\n   :width: 600px\n")
    parts.append("\n" + RST_FOOTER)
    return "".join(parts)


def generate_images(only=None):
    from meshedlogo import MeshedLogo

    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    cwd = os.getcwd()
    os.chdir(IMAGE_DIR)
    failures = []
    try:
        for _, title, filename, _, code in EXAMPLES:
            if only and filename not in only:
                continue
            random.seed(SEED)
            np.random.seed(SEED)
            start = time.time()
            try:
                exec(textwrap.dedent(code), {"MeshedLogo": MeshedLogo})
                if not Path(filename).is_file():
                    raise FileNotFoundError(f"snippet did not produce {filename}")
                print(f"  ok   {filename:<22} {time.time() - start:5.1f}s  ({title})")
            except Exception as e:  # keep going so one bad example doesn't hide others
                failures.append((filename, e))
                print(f"  FAIL {filename:<22} {e}", file=sys.stderr)
    finally:
        os.chdir(cwd)
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rst-only", action="store_true", help="Only write examples.rst")
    parser.add_argument("--only", nargs="*", metavar="FILE", help="Generate only these image files")
    args = parser.parse_args()

    RST_PATH.write_text(render_rst(), encoding="utf-8")
    print(f"Wrote {RST_PATH.relative_to(DOCS_DIR.parent)}")

    if args.rst_only:
        return 0

    print(f"Generating {len(args.only or EXAMPLES)} example images into {IMAGE_DIR.relative_to(DOCS_DIR.parent)}/")
    failures = generate_images(set(args.only) if args.only else None)
    if failures:
        print(f"\n{len(failures)} example(s) failed", file=sys.stderr)
        return 1
    print("All examples generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
