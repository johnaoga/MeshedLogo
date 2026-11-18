"""
Command-line interface for MeshedLogo.

Usage::

    meshedlogo "YOUR TEXT" output/logo.png
    meshedlogo '$e^{i\\theta}$' euler.png --colors cyan magenta --scale 3
"""

import argparse
import os
import random
import sys

import numpy as np

from . import __version__
from .meshed_logo import MeshedLogo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meshedlogo",
        description="Generate a triangle-meshed logo from text or a LaTeX formula.",
    )
    parser.add_argument("text", nargs="?", default="LOGO",
                        help="Text to render. Wrap LaTeX in $...$ (default: LOGO)")
    parser.add_argument("output", nargs="?",
                        help="Output PNG path (default: output/<text>_logo.png)")
    parser.add_argument("--colors", nargs="+", default=["cyan", "magenta", "yellow", "white"],
                        help="Gradient colors, left to right")
    parser.add_argument("--scale", type=float, default=2.0, help="Text scale factor")
    parser.add_argument("--mesh-density", type=float, default=1.5, help="Interior point density")
    parser.add_argument("--background", default="black", help="Background color")
    parser.add_argument("--canvas", type=int, nargs=2, metavar=("W", "H"), default=(1200, 800),
                        help="Canvas size in pixels")
    parser.add_argument("--dpi", type=int, default=300, help="Output resolution")
    parser.add_argument("--no-wireframe", action="store_true", help="Hide triangle edges")
    parser.add_argument("--no-vertices", action="store_true", help="Hide vertex dots")
    parser.add_argument("--no-surface", action="store_true", help="Hide filled triangles")
    parser.add_argument("--invert", action="store_true",
                        help="Mesh the background and treat the text as a hole")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (-1 for none)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if args.seed >= 0:
        random.seed(args.seed)
        np.random.seed(args.seed)

    output_file = args.output or os.path.join(
        "output", f"{''.join(c for c in args.text.lower() if c.isalnum()) or 'logo'}_logo.png")
    out_dir = os.path.dirname(output_file)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print(f"Generating meshed logo for: '{args.text}'")
    logo = MeshedLogo(canvas_size=tuple(args.canvas), background_color=args.background)
    result_file = logo.generate(
        text=args.text,
        output_file=output_file,
        colors=args.colors,
        scale=args.scale,
        mesh_density=args.mesh_density,
        show_wireframe=not args.no_wireframe,
        show_vertices=not args.no_vertices,
        show_surface=not args.no_surface,
        invert_mode=args.invert,
        dpi=args.dpi,
    )
    print(f"✓ Logo saved to: {result_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
