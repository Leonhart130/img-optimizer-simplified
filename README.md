# Image Optimizer

---

The **Image Optimizer** is a desktop application built using PyQt6 and Python. It allows users to optimize images by selecting a profile, including optimizing for web usage and resizing images to specific aspect ratios. The application converts images to the WebP format with optimized quality, making it particularly useful for e-commerce to ensure images are efficiently prepared for responsive web use.

## Features

- **Select Profiles**:

  - **Optimize**: General optimization converting images to WebP format with 85/100 quality.
  - **Optimize and Resize**: Optimize and resize images to one of the following aspect ratios:
    - `1:1 (carré)`
    - `3:4 (portrait)`
    - `4:3 (paysage)`
    - `16:9 (large)`
    - `9:16 (vertical)`

- **Image Optimization**:
  - Convert images to the WebP format for optimized web performance.
  - Sanitize filenames.

- **Aspect Ratio Resizing**:
  - Resize images to fit the selected aspect ratio while covering the target dimensions.
  - Automatically crop images to eliminate any black borders and ensure a clean fit.

## Requirements

- Python 3.x
- PyQt6
- Pillow (PIL)

## Installation

1. **Clone the Repository**:

- `git clone git@github.com:Leonhart130/img-optimizer-simplified.git`

2. **Create a Virtual Environment**:

- `python -m venv venv`

3. **Activate the Virtual Environment**:

- On Windows:
  ```
  venv\Scripts\Activate.ps1
  ```
- On macOS/Linux:
  ```
  source venv/bin/activate
  ```

4. **Install Dependencies**:

- `pip install -r requirements.txt`

## Usage

1. **Run the Application**:

`python main.py`

2. **Select a Profile**:

- **Optimize**: Only optimizes images without resizing.
- **Optimize and Resize**: Optimizes and resizes images to the selected aspect ratio.

3. **Choose an Aspect Ratio** (if "Optimize and Resize" is selected):
- `1:1 (carré)`
- `3:4 (portrait)`
- `4:3 (paysage)`
- `16:9 (large)`
- `9:16 (vertical)`

4. **Select Images**:

- Click "Sélectionner les fichiers" to choose images.

5. **Process Images**:

- The application will process and save the images in the appropriate directory (`optimized_images` or `resized_images`).

## Building an Executable

1. **Create the Executable**:

   `pyinstaller --windowed main.py`

2. **Run the Executable**:

   - Navigate to the `dist` directory and run `main.exe` (Windows) or `main` (macOS/Linux).

## License

This project is licensed under the MIT License - see the [https://github.com/Leonhart130/img-optimizer/blob/main/LICENSE](LICENSE) file for details.
