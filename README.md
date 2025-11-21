# Meshed Logo - Triangle Mesh Logo Generator

A professional, modular Python system for generating triangle-meshed logos from text and mathematical formulas. Features a clean API through the `MeshedLogo` class with full test coverage.

**"MEMA & INMA forever"** - Originally created as a tribute in Euler's form: $\frac{ME}{IN} e^{i\theta}$

## 🎯 Features

- **Modular Architecture**: 5 independent, reusable components following OOP principles
- **Character Rendering**: Convert any letter or symbol to binary image matrix
- **String Processing**: Handle plain text and mathematical formulas
- **Contour Extraction**: Extract outline points from images using OpenCV
- **Mesh Generation**: Create triangle meshes using Delaunay triangulation
- **Logo Composition**: Orchestrate all components to create complete logos
- **High Quality Output**: Supports 300+ DPI with gradient colors and wireframe effects

## 📦 Architecture

The system consists of 5 main modules:

### 1. **CharacterRenderer** (`character_renderer.py`)
Renders letters/symbols to binary image matrices.

```python
renderer = CharacterRenderer(default_width=200, default_height=200)
char_img = renderer.render('M', save_path='output/m.png')
# Returns CharacterImage with binary matrix and metadata
```

### 2. **StringProcessor** (`string_processor.py`)
Processes text strings and formulas into character images.

```python
processor = StringProcessor()
result = processor.process("HELLO", save_dir="output/")
# Returns ProcessedString with list of CharacterImages
```

### 3. **ContourExtractor** (`contour_extractor.py`)
Extracts contour/outline points from images.

```python
extractor = ContourExtractor(method='opencv')
contour = extractor.extract_largest(image, simplify=True)
# Returns ContourData with (x,y) points
```

### 4. **MeshGenerator** (`mesh_generator.py`)
Creates triangle meshes from point sets.

```python
generator = MeshGenerator()
mesh = generator.generate(points, add_interior_points=True)
# Returns MeshData with vertices and triangles
```

### 5. **LogoGenerator** (`logo_generator.py`)
Orchestrates all components to generate complete logos.

```python
logo_gen = LogoGenerator(canvas_size=(1200, 800))
logo = logo_gen.create_mema_inma_logo()
# Generates complete meshed logo
```

## 🚀 Installation

1. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Dependencies
- `matplotlib >= 3.8.0` - Visualization and rendering
- `numpy >= 1.26.0` - Numerical operations
- `scipy >= 1.11.0` - Delaunay triangulation
- `Pillow >= 10.0.0` - Image processing
- `opencv-python >= 4.8.0` - Contour extraction

## 💻 Usage

### Quick Start - Simple Logo
```python
from meshed_logo import MeshedLogo

logo = MeshedLogo()
logo.generate("HELLO", output_file="output/hello.png")
```

### Command Line Usage
```bash
# Generate a simple logo
python bin/generate_logo.py "YOUR TEXT" output/logo.png

# Run simple examples
python bin/example_simple.py

# Run advanced examples
python bin/example_advanced.py
```

### Run Tests
```bash
python tests/run_tests.py
```

### Using the MeshedLogo Class

#### 1. Simple Text Logo
```python
from meshed_logo import MeshedLogo

logo = MeshedLogo()
logo.generate("HELLO", output_file="output/hello.png")
```

#### 2. Custom Colors and Scale
```python
logo = MeshedLogo()
logo.generate(
    "CODE",
    output_file="output/code.png",
    colors=['#00ff00', '#00ffff', '#ff00ff'],
    scale=2.5,
    mesh_density=2.0
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

#### 4. Generate MEMA & INMA Logo
```python
logo = MeshedLogo()
logo.generate_mema_inma(output_file="mema_inma.png")
```

### Advanced: Using Individual Modules
For advanced usage, you can import and use individual modules from `lib/`:

```python
from lib.character_renderer import CharacterRenderer
from lib.contour_extractor import ContourExtractor
from lib.mesh_generator import MeshGenerator

# Custom pipeline...
```

See `bin/example_advanced.py` for comprehensive examples.

## 📚 API Reference

### CharacterImage (dataclass)
- `matrix`: Binary numpy array (0=background, 1=character)
- `character`: The rendered character
- `width`, `height`: Image dimensions
- `filepath`: Saved file path (if saved)
- `save(filepath)`: Save image to file

### ContourData (dataclass)
- `points`: numpy array of (x,y) coordinates
- `num_points`: Number of points in contour
- `get_bounding_box()`: Returns (x_min, y_min, x_max, y_max)
- `simplify(epsilon)`: Simplify contour using Douglas-Peucker
- `save_points(filepath)`: Save points to file (.txt, .csv, .npy)

### MeshData (dataclass)
- `points`: Vertex coordinates (N × 2 array)
- `triangles`: Triangle indices (M × 3 array)
- `num_vertices`, `num_triangles`: Counts
- `get_edges()`: Returns unique edges
- `get_triangle_areas()`: Returns array of triangle areas
- `save_mesh(filepath, format)`: Save mesh (.obj, .ply, .txt)

### Logo (dataclass)
- `name`: Logo name
- `components`: List of LogoComponent objects
- `canvas_size`: Canvas dimensions
- `save_metadata(filepath)`: Save logo metadata

## 🎨 Examples

The `example_usage.py` script includes 7 comprehensive examples:

1. **Render Single Character** - Basic character rendering
2. **Process String** - Convert text to multiple images
3. **Extract Contours** - Extract outline points from images
4. **Generate Mesh** - Create triangle mesh from contours
5. **Complete Logo** - Generate full MEMA & INMA logo
6. **Custom Logo** - Create custom logo with specific configuration
7. **Mesh Refinement** - Refine and manipulate meshes

## 🔧 Customization

### Character Rendering Options
- `width`, `height`: Image dimensions
- `thickness`: Font stroke thickness
- Custom fonts: Modify `_get_font()` method

### Mesh Generation Options
- `add_interior_points`: Add random interior points for better triangulation
- `num_interior_points`: Number of interior points
- `boundary_refinement`: Refine boundary edges
- `refinement_factor`: Subdivision factor

### Visualization Options
- `show_edges`: Show triangle edges (wireframe)
- `show_vertices`: Show vertex points
- `color_scheme`: 'gradient', 'random', 'solid', 'alternating'
- `background_color`: Canvas background color
- `dpi`: Output resolution

## 🏗️ Project Structure

```
mema-inma-logo/
├── meshed_logo.py           # Main front-facing class (USE THIS!)
├── lib/                     # Core library modules
│   ├── __init__.py
│   ├── character_renderer.py    # Character to binary image
│   ├── string_processor.py       # String/formula processing
│   ├── contour_extractor.py      # Contour extraction
│   ├── mesh_generator.py         # Triangle mesh generation
│   └── logo_generator.py         # Logo orchestration
├── bin/                     # Executable scripts and examples
│   ├── generate_logo.py         # CLI logo generator
│   ├── example_simple.py        # Simple usage examples
│   └── example_advanced.py      # Advanced usage examples
├── tests/                   # Unit tests
│   ├── test_character_renderer.py
│   ├── test_contour_extractor.py
│   ├── test_mesh_generator.py
│   ├── test_meshed_logo.py
│   └── run_tests.py
├── legacy/                  # Legacy implementations
│   ├── generate_logo.py
│   └── generate_m_only.py
├── requirements.txt         # Dependencies
├── README.md               # This file
└── output/                 # Generated files
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python tests/run_tests.py

# Or use unittest discovery
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_meshed_logo
```

All tests include assertions and create test artifacts in `tests/output/`.

## 🤝 Contributing

This is a modular system designed for extensibility. To add new features:

1. **New character sources**: Extend `CharacterRenderer` with custom rendering methods
2. **New contour algorithms**: Add methods to `ContourExtractor`
3. **New mesh algorithms**: Extend `MeshGenerator` with alternative triangulation methods
4. **New logo templates**: Add factory methods to `LogoGenerator`

## 📝 License

This project was created for MEMA & INMA. Feel free to use and modify for your own projects.

## 🙏 Acknowledgments

- Uses Delaunay triangulation from `scipy.spatial`
- Contour extraction powered by OpenCV
- Visualization with Matplotlib

---

**Enjoy creating mathematical art!** 🎨📐✨

For questions or issues, please refer to the example usage script or module docstrings.
