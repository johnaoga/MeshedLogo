# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and
the project uses [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-18

First public release on PyPI.

### Added

- `MeshedLogo` high-level API: `generate`, `generate_multi`, `generate_formula`,
  `generate_mema_inma`.
- Triangle mesh rendering with Delaunay triangulation, gradient colors,
  wireframe/vertex/surface toggles and invert mode.
- Automatic hole detection for characters such as O, A, B.
- LaTeX formula rendering (`$e^{i\theta}$`, `$\frac{a}{b}$`, ...).
- `meshedlogo` command-line tool.
- Sphinx documentation with example images generated on every build.

[Unreleased]: https://github.com/johnaoga/MeshedLogo/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/johnaoga/MeshedLogo/releases/tag/v0.1.0
