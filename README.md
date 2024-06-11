# Image Optimizer

---

The **Image Optimizer** is a desktop application built using PyQt6 and Python. It allows users to optimize images by selecting a profile and operation, including resizing, cropping, creating thumbnails, and converting to WebP format with optimized quality. This application is particularly useful for e-commerce, ensuring images are optimized for web usage by generating multiple sizes.

## Features

- **Select Profiles**:
  - `3:4` and `4:4`: Ideal for e-commerce product images.
  - `Optimize`: General optimization converting images to WebP format with 85/100 quality.
- **Perform Operations**:
  - `Resize and Crop`: Resize images and crop to specified dimensions.
  - `Create Thumbnail`: Generate thumbnails while maintaining aspect ratio and cropping to exact dimensions.
- **Image Optimization**:
  - Generate multiple sizes for responsive web usage.
  - Handle file naming for CDN optimization.
- **Image Validation**:
  - Ensure image sizes meet specified criteria before processing.

## Requirements

- Python 3.x
- PyQt6
- Pillow (PIL)

## Installation

1. **Clone the Repository**:
   'git clone <repository-url>'
2. **Create a Virtual Environment**:
   'python -m venv venv'
3. **Activate the Virtual Environment**:
   - On Windows:
     'venv\Scripts\activate'
   - On macOS/Linux:
     'source venv/bin/activate'
4. **Install Dependencies**:
   'pip install -r requirements.txt'

## Usage

1. **Run the Application**:
   'python main.py'
2. **Select a Profile**:
   - `3:4`
   - `4:4`
   - `Optimize`
3. **Select an Operation** (not required for `Optimize`):
   - `Resize and Crop`
   - `Create Thumbnail`
4. **Select Images**:
   - Click "Sélectionner les fichiers" to choose images.
5. **Process Images**:
   - The application will process and save the images in the appropriate directory (`product_images` or `optimized_images`).

## Building an Executable

1. **Install PyInstaller**:
   'pip install pyinstaller'
2. **Create the Executable**:
   'pyinstaller --windowed main.py'
3. **Run the Executable**:
   - Navigate to the `dist` directory and run `main.exe` (Windows) or `main` (macOS/Linux).

## License

This project is licensed under the MIT License - see the [https://github.com/Leonhart130/img-optimizer/blob/main/LICENSE](LICENSE) file for details.
