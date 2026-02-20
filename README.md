# STL Support Generator

A Linux desktop application for generating 3D printing supports for UV resin printers.

## Features

- Load STL files (binary and ASCII)
- Automatic hybrid support generation
- 3D preview with interactive camera controls:
  - Right button: Rotate
  - Left button: Pan
  - Scroll wheel: Zoom
- Guided support editing: Click on supports to delete them
- Export merged STL with supports

## Requirements

- Python 3
- PyQt5
- numpy-stl
- NumPy
- PyOpenGL

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main
```

Or with software rendering (if GPU issues):

```bash
LIBGL_ALWAYS_SOFTWARE=1 python -m src.main
```

## Controls

- **Load STL**: Click the button and select an STL file
- **Generate Supports**: Automatically generate support structures
- **Rotate view**: Right-click and drag
- **Pan view**: Left-click and drag
- **Zoom**: Scroll wheel
- **Delete support**: Click on a support tip (yellow lines)
- **Export**: Save the model with supports as a new STL file

## License

Creative Commons Attribution 4.0 International (CC BY 4.0)
