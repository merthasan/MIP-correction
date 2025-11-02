# X-Ray Image Flat Field Correction

This project implements flat field correction for x-ray images acquired from CsI (Cesium Iodide) and Gadox (Gadolinium Oxysulfide) detectors.

## Project Overview

Flat field correction is used to compensate for:
- Vignetting (brightness falloff at image edges)
- Dust spots on the sensor/lens
- Uneven illumination across the detector
- Non-uniform detector response

## Setup Instructions

### Prerequisites
- Python 3.12 or higher
- Raw image files (not included in repository)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/merthasan/MIP-correction.git
   cd MIP-correction
   ```

2. **Add your image files**
   
   Place your raw image files in the project directory:
   - `dark_images/` - Dark frame images
   - `for_flat_field_correction/` - Flat field images (ff1.raw through ff5.raw)
   - `ff6.raw` - Image to be corrected
   - `ff_corrected.raw` - Reference corrected image (for comparison)

3. **Create a virtual environment**
   
   A virtual environment isolates your project dependencies from your system Python installation.
   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment**
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   You'll see `(venv)` appear in your terminal prompt when activated.

5. **Install required packages**
   
   With the virtual environment activated:
   ```bash
   pip install numpy matplotlib
   ```

### Running the Code

Make sure your virtual environment is activated (you should see `(venv)` in your prompt), then:

```bash
python flat_field_correction.py
```

### Deactivating the Virtual Environment

When you're done working on the project:
```bash
deactivate
```

## About Virtual Environments

### What is a Virtual Environment?
A virtual environment is an isolated Python environment that allows you to:
- Install packages without affecting your system Python
- Use different package versions for different projects
- Keep your project dependencies organized and reproducible

### Why Use One?
- **Isolation**: Prevents conflicts between project dependencies
- **Reproducibility**: Easy to recreate the same environment on another machine
- **Clean**: Keeps your system Python installation clean

### Important Notes
- **Always activate** the virtual environment before working on the project
- The `venv/` directory is **not** tracked by Git (it's in `.gitignore`)
- Each time you clone the repository, you need to recreate the virtual environment
- Package installations inside the venv only affect this project

## Image File Specifications

### Raw Image Format
- **Dimensions**: 2560 × 3072 pixels (width × height)
- **Data type**: 16-bit unsigned integer (uint16)
- **Byte order**: Little-endian
- **No header**: Binary data starts immediately

## Project Structure

```
MIP-correction/
├── README.md                      # This file
├── .gitignore                     # Git ignore rules
├── flat_field_correction.py       # Main correction script
├── venv/                          # Virtual environment (not in Git)
├── dark_images/                   # Dark frame images (not in Git)
├── for_flat_field_correction/     # Flat field images (not in Git)
├── ff6.raw                        # Image to correct (not in Git)
└── ff_corrected.raw               # Reference image (not in Git)
```

## Dependencies

- **NumPy**: Numerical computing and array operations
- **Matplotlib**: Visualization and plotting

## Workflow

1. Load flat field images (ff1-ff5)
2. Create master flat field by computing median
3. Apply flat field correction to ff6
4. Compare with reference image (ff_corrected)
5. Extract and compare histograms

I got an LLM to generate this README file. 