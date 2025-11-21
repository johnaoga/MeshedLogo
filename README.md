# MeshedLogo - Triangle Mesh Logo Generator

<p align="center">
  <img src="test_output/much_logo.png" alt="MeshedLogo Example" width="600">
</p>

A professional Python system for generating beautiful triangle-meshed logos from text and mathematical formulas.

**"MEMA & INMA forever"** - Originally created as a tribute in Euler's form: ME/IN e^(iθ)

[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://YOUR_USERNAME.github.io/mema-inma-logo/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Features

- 🎨 **Triangle-based mesh rendering** with Delaunay triangulation
- 🌈 **Gradient color support** for stunning visual effects
- 🔍 **Automatic hole detection** for characters like O, A, B
- ⚙️ **Extensive rendering options**: surface, wireframe, vertices, invert mode
- 📐 **High quality output** with 300+ DPI support
- 🧩 **Modular architecture** with reusable components
- 🧪 **Full test coverage** with comprehensive unit tests

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mema-inma-logo.git
cd mema-inma-logo

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from meshed_logo import MeshedLogo

# Create a simple logo
logo = MeshedLogo()
logo.generate("HELLO", output_file="hello.png")

# Custom colors and styling
logo.generate(
    "CODE",
    output_file="code.png",
    colors=['cyan', 'magenta', 'yellow'],
    scale=2.5,
    mesh_density=2.0
)
```

### Command Line

```bash
# Generate a logo
python bin/generate_logo.py "YOUR TEXT" output/logo.png

# Run examples
python bin/example_simple.py
python bin/example_advanced.py

# Run tests
python tests/run_tests.py
```

## 📖 Documentation

**[📚 Full Documentation](https://YOUR_USERNAME.github.io/mema-inma-logo/)**

- [Quick Start Guide](https://YOUR_USERNAME.github.io/mema-inma-logo/quickstart.html) - Get started in minutes
- [User Guide](https://YOUR_USERNAME.github.io/mema-inma-logo/user_guide.html) - Detailed usage and customization
- [Technical Details](https://YOUR_USERNAME.github.io/mema-inma-logo/technical.html) - Architecture and algorithms
- [Examples Showcase](https://YOUR_USERNAME.github.io/mema-inma-logo/examples.html) - Visual examples and code
- [API Reference](https://YOUR_USERNAME.github.io/mema-inma-logo/api_reference.html) - Complete API documentation

## 🎨 Examples

<p align="center">
  <img src="test_output/board_logo.png" alt="BOARD Logo" width="600">
  <br>
  <em>Multi-character logo with gradient colors and mesh wireframe</em>
</p>

See the [Examples page](https://YOUR_USERNAME.github.io/mema-inma-logo/examples.html) in the documentation for more examples and showcase.

## 🏗️ Project Structure

```
mema-inma-logo/
├── meshed_logo.py       # Main API class
├── lib/                 # Core library modules
├── bin/                 # CLI and example scripts
├── tests/               # Unit tests
├── docs/                # Sphinx documentation
└── requirements.txt     # Dependencies
```

## 🧪 Testing

All components are fully tested:

```bash
python tests/run_tests.py
```

Test coverage includes character rendering, contour extraction, mesh generation, and complete logo creation.

## 📦 Dependencies

- matplotlib >= 3.8.0
- numpy >= 1.26.0
- scipy >= 1.11.0
- Pillow >= 10.0.0
- opencv-python >= 4.8.0

## 🤝 Contributing

Contributions are welcome! The modular architecture makes it easy to extend:

- Add new rendering styles
- Implement alternative mesh algorithms
- Create new logo templates
- Improve documentation

## 📝 License

Created for MEMA & INMA. Feel free to use and modify for your own projects.

## 🙏 Acknowledgments

- Delaunay triangulation via `scipy.spatial`
- Contour extraction powered by OpenCV
- Visualization with Matplotlib

---

**For detailed documentation, visit [https://YOUR_USERNAME.github.io/mema-inma-logo/](https://YOUR_USERNAME.github.io/mema-inma-logo/)**
