# MeshedLogo Documentation

This directory contains the Sphinx documentation for MeshedLogo.

## Building Documentation Locally

### Requirements

Install documentation dependencies:

```bash
pip install sphinx sphinx-rtd-theme myst-parser
```

### Build

```bash
# From the docs directory
make html

# Or from project root
sphinx-build -b html docs docs/_build/html
```

### View Locally

```bash
# Start a local server
cd docs
make serve

# Or manually
cd docs/_build/html
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Documentation Structure

- `index.rst` - Main landing page
- `quickstart.rst` - Getting started guide
- `user_guide.rst` - Detailed usage documentation
- `technical.rst` - Technical details and architecture
- `examples.rst` - Examples showcase
- `api_reference.rst` - Complete API reference
- `conf.py` - Sphinx configuration
- `_static/` - Static files (images, CSS)
- `_templates/` - Custom templates

## Automatic Deployment

Documentation is automatically built and deployed to GitHub Pages on every push to main/master branch via GitHub Actions.

See `.github/workflows/docs.yml` for the CI/CD configuration.

## Writing Documentation

- Use reStructuredText (.rst) format
- Include code examples with syntax highlighting
- Add images to `_static/images/`
- Keep sections organized and clear
- Include links between related pages

## Useful Commands

```bash
# Build HTML
make html

# Clean build artifacts
make clean

# Serve locally
make serve

# Check for broken links
make linkcheck
```

## Resources

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
- [Read the Docs Sphinx Theme](https://sphinx-rtd-theme.readthedocs.io/)
