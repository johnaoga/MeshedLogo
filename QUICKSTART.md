# MeshedLogo - Quick Start Guide

## 🚀 Getting Started

### Installation
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already installed)
pip install -r requirements.txt
```

### Basic Usage

#### 1. Simple Text Logo
```python
from meshed_logo import MeshedLogo

logo = MeshedLogo()
logo.generate("HELLO", output_file="output/hello.png")
```

#### 2. Custom Colors
```python
logo = MeshedLogo()
logo.generate(
    "CODE",
    output_file="output/code.png",
    colors=['#00ff00', '#00ffff', '#ff00ff'],
    scale=2.5
)
```

#### 3. Multi-Component Logo
```python
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
```

#### 4. MEMA & INMA Classic
```python
logo = MeshedLogo()
logo.generate_mema_inma(output_file="mema_inma.png")
```

## 📂 Project Structure

```
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
```

## 🏃 Running Examples

```bash
# Simple examples (recommended)
python bin/example_simple.py

# Advanced examples (full features)
python bin/example_advanced.py

# CLI tool
python bin/generate_logo.py "YOUR TEXT" output/logo.png
```

## 🧪 Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Or use unittest
python -m unittest discover tests
```

**Expected result:** All 28 tests should pass ✓

## 🎨 API Reference

### MeshedLogo Class

#### Methods

**`generate(text, output_file, ...)`**
Generate simple text logo
- `text`: Text to render
- `output_file`: Output path
- `colors`: List of colors (optional)
- `scale`: Scale factor (default: 2.0)
- `mesh_density`: Interior point density (default: 1.5)
- `show_wireframe`: Show edges (default: True)
- `show_vertices`: Show vertices (default: True)
- `dpi`: Resolution (default: 300)

**`generate_multi(components, name, output_file, ...)`**
Generate multi-component logo
- `components`: List of component dicts
- `name`: Logo name
- `output_file`: Output path

**`generate_mema_inma(output_file, output_dir)`**
Generate MEMA & INMA classic logo

**`set_canvas(width, height)`**
Update canvas size

**`set_background(color)`**
Update background color

## ✨ Tips

1. **Start simple**: Use `meshed_logo.py` MeshedLogo class
2. **Run examples**: Check `bin/example_simple.py` for ideas
3. **Test changes**: Run `python tests/run_tests.py`
4. **Custom colors**: Use hex codes like '#00ff00' or names like 'cyan'
5. **Adjust density**: Higher mesh_density = more triangles = more detail

## 📖 Full Documentation

See `README.md` for complete documentation.

## 🐛 Troubleshooting

**Black logos?**
- Fixed! ContourExtractor now properly handles binary matrices

**Import errors?**
- Make sure you're in the project root directory
- Check that venv is activated

**Test failures?**
- Run `pip install -r requirements.txt` again
- Check that all dependencies are installed

**Need help?**
- Check `bin/example_simple.py` for working examples
- See test files in `tests/` for usage patterns
