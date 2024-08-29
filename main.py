import os
import sys
import shutil
import re
from functools import partial
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox,
    QLabel,
    QFileDialog,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QRadioButton,
    QButtonGroup,
)
from PyQt6.QtCore import Qt
from PIL import Image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Optimizer")
        self.selected_profile = ""
        self.selected_aspect_ratio = ""

        layout = QVBoxLayout()

        # Profile Selection
        layout.addWidget(QLabel("1. Sélectionnez un profil:"))
        self.profile_group = QButtonGroup(self)
        optimize_btn = QRadioButton("Optimiser")
        resize_btn = QRadioButton("Optimiser et Redimensionner")
        self.profile_group.addButton(optimize_btn)
        self.profile_group.addButton(resize_btn)
        optimize_btn.clicked.connect(lambda: self.set_profile("optimize"))
        resize_btn.clicked.connect(lambda: self.set_profile("resize"))
        layout.addWidget(optimize_btn)
        layout.addWidget(resize_btn)

        # Aspect Ratio Selection (only for "Optimiser et Redimensionner")
        self.aspect_ratio_group = QButtonGroup(self)
        self.aspect_ratio_labels = [
            "1:1 (carré)",
            "3:4 (portrait)",
            "4:3 (paysage)",
            "16:9 (large)",
            "9:16 (vertical)",
        ]
        self.aspect_ratios = ["1:1", "3:4", "4:3", "16:9", "9:16"]
        self.aspect_ratio_buttons = []

        for i, label in enumerate(self.aspect_ratio_labels):
            btn = QRadioButton(label)
            btn.clicked.connect(partial(self.set_aspect_ratio, self.aspect_ratios[i]))
            self.aspect_ratio_buttons.append(btn)
            layout.addWidget(btn)
            self.aspect_ratio_group.addButton(btn)
            btn.setVisible(False)  # Hidden by default

        # File Selection
        layout.addWidget(QLabel("2. Sélectionnez les images:"))
        select_files_button = QPushButton("Sélectionner les fichiers")
        select_files_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(select_files_button)

        # Feedback Label
        self.callback = QLabel("")
        layout.addWidget(self.callback)

        # Set layout to the central widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def set_profile(self, profile: str):
        """Set selected profile for optimization or optimization and resizing."""
        self.selected_profile = profile
        print(f"Profile set to: {profile}")

        # Show aspect ratio options only if "resize" is selected
        for btn in self.aspect_ratio_buttons:
            btn.setVisible(profile == "resize")

    def set_aspect_ratio(self, ratio: str):
        """Set selected aspect ratio for resizing."""
        self.selected_aspect_ratio = ratio
        print(f"Aspect ratio set to: {ratio}")

    def open_file_dialog(self):
        """Open file dialog to select images and process them."""
        if not self.selected_profile:
            QMessageBox.critical(self, "Erreur", "Choisissez d'abord un profil")
            return

        if self.selected_profile == "resize" and not self.selected_aspect_ratio:
            QMessageBox.critical(self, "Erreur", "Choisissez d'abord un ratio d'aspect")
            return

        file_filter = "Images (*.png *.jpg *.jpeg *.webp)"
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionnez des images", os.getcwd(), file_filter
        )

        if file_paths:
            # Show "Processing" message
            self.callback.setText("Traitement en cours, veuillez patienter...")
            self.callback.setAlignment(Qt.AlignmentFlag.AlignCenter)
            QApplication.processEvents()  # Refresh the GUI to show the message

            # Optimize or create thumbnails based on the selected profile
            status, message = optimize_images(
                self, file_paths, self.selected_profile, self.selected_aspect_ratio
            )

            # Update message after processing
            self.callback.setText(message)
            if status == 0:
                os.startfile(message)  # Open the output directory


def main():
    """Main entry point of the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


def optimize_images(
    parent, file_paths: list[str], profile: str, aspect_ratio: str
) -> tuple:
    """Optimize or resize images based on the selected profile and aspect ratio."""
    output_dir_name = "optimized_images" if profile == "optimize" else "resized_images"
    output_dir = os.path.join(os.path.dirname(file_paths[0]), output_dir_name)

    # Confirm directory override if exists
    if os.path.exists(output_dir):
        reply = QMessageBox.question(
            parent,
            "Confirmation",
            f"Le dossier '{output_dir}' existe déjà, voulez-vous l'écraser?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.No:
            return 1, "Abandonné."
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for file_path in file_paths:
        # Ensure that only image files are processed
        if not file_path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            continue

        with Image.open(file_path) as im:
            new_filename = clean_filename(
                os.path.splitext(os.path.basename(file_path))[0]
            )  # Correct extension handling
            if profile == "optimize":
                im.save(
                    os.path.join(output_dir, f"{new_filename}.webp"),
                    "webp",
                    optimize=True,
                    quality=85,
                )
            else:
                # Resize image based on the selected aspect ratio
                size = get_target_size(aspect_ratio)
                resized_image = resize_image(im, size, aspect_ratio)
                resized_image.save(
                    os.path.join(output_dir, f"{new_filename}.webp"),
                    "webp",
                    optimize=True,
                    quality=85,
                )
        QApplication.processEvents()  # Keep UI responsive during processing

    return 0, output_dir


def clean_filename(filename: str) -> str:
    """Clean the filename for web usage: remove special characters, spaces, and make lowercase."""
    filename = re.sub(
        r"[^a-zA-Z0-9._-]", "_", filename
    )  # Replace invalid characters with underscores
    return filename.lower()


def get_target_size(aspect_ratio: str) -> tuple[int, int]:
    """Determine target size based on aspect ratio."""
    sizes = {
        "1:1": (1200, 1200),
        "3:4": (900, 1200),
        "4:3": (1200, 900),
        "16:9": (1600, 900),
        "9:16": (900, 1600),
    }
    return sizes[aspect_ratio]


def resize_image(image: Image, size: tuple[int, int]) -> Image:
    """Resize the image while maintaining the specified aspect ratio by covering the target size."""
    target_width, target_height = size
    img_width, img_height = image.size

    # Calculate the scale factors to cover the target dimensions
    width_ratio = target_width / img_width
    height_ratio = target_height / img_height

    # Choose the larger scale factor to cover the whole area
    scale_factor = max(width_ratio, height_ratio)

    # Calculate the new dimensions after resizing
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)

    # Resize the image to cover the target area
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Calculate the coordinates to crop the center of the image
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    right = left + target_width
    bottom = top + target_height

    # Crop the centered part of the image to the target size
    cropped_image = resized_image.crop((left, top, right, bottom))
    return cropped_image


if __name__ == "__main__":
    main()
