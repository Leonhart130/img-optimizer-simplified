import os
from random import randint
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMessageBox,
    QLabel,
    QFileDialog,
    QMainWindow,
    QRadioButton,
    QVBoxLayout,
    QPushButton,
)

from PyQt6.QtWidgets import QButtonGroup

from PIL import Image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Optimizer")
        layout = QVBoxLayout()

        """ Select profile part """
        label1 = QLabel("1. Sélectionnez un profil:")
        self.profile_group = QButtonGroup(self)  # Create a button group

        self.selected_profile = ""
        self.lith_profile = QRadioButton("Lith")
        self.tys_profile = QRadioButton("Tys")
        self.profile_group.addButton(self.lith_profile)
        self.profile_group.addButton(self.tys_profile)

        self.lith_profile.clicked.connect(self.set_profile)
        self.tys_profile.clicked.connect(self.set_profile)

        """ Select files part """
        label2 = QLabel("2. Sélectionnez la/les images:")
        select_files_button = QPushButton("Sélectionner les fichiers")
        select_files_button.clicked.connect(self.open_dialog)

        self.callback = QLabel("")

        """ Mount layout part """
        layout.addWidget(label1)
        layout.addWidget(self.lith_profile)
        layout.addWidget(self.tys_profile)
        layout.addWidget(label2)
        layout.addWidget(select_files_button)
        layout.addWidget(self.callback)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def set_profile(self):
        """Set self.selected_profile
        depending the on radio button checked
        """
        if self.lith_profile.isChecked():
            self.selected_profile = "lith"
            print("Profile set to: lith")
        elif self.tys_profile.isChecked():
            self.selected_profile = "tys"
            print("Profile set to: tys")

    def open_dialog(self):
        """Ensure a profile is selected,
        if not, display a warning modal,
        else launch file explorer modal
        """

        if not self.selected_profile:
            dialog = QMessageBox()
            dialog.setWindowTitle("Erreur")
            dialog.setText("Choisissez d'abord un profil")
            dialog.exec()

        else:
            file_filter = "Images (*.png *.jpg *.jpeg *.webp)"
            response = QFileDialog.getOpenFileNames(
                caption="Sélectionnez une ou plusieurs images",
                directory=os.getcwd(),
                filter=file_filter,
            )
            if response[0]:
                status, message = optimize(response[0], self.selected_profile)
                if status == 0:
                    self.callback.setText(
                        f"Les images ont été sauvegardé dans le dossier {message}"
                    )
                    os.startfile(message)  # Open directory with file explorer
                else:
                    self.callback.setText(
                        "Erreur lors de l'optimisation des images: " + message
                    )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


def optimize(files_paths: list[str], profile: str) -> tuple:
    """Optimize images for web,
    for each files in the files_path list:
    create webp thumbnail of the image (keeping transparency) in 2 sizes depending on profile selected
    give random number name to image for cdn optimization
    and create a new directory named with the filename, with files inside
    """
    profiles = ["lith", "tys"]
    image_sizes = {
        "lith": {
            "small": (225, 300),  # Width: 225, Height: 300
            "large": (500, 667),
        },
        "tys": {
            "small": (150, 150),
            "large": (450, 450),
        },
    }

    if profile not in profiles:
        return 1, "Profile not found"

    saved_path = ""
    for file_path in files_paths:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_dir = os.path.join(os.path.dirname(file_path), base_name)
        saved_path = output_dir
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        random_number = str(
            randint(10000000, 99999999)
        )  # Generate a random 8-digit number

        with Image.open(file_path) as im:
            for size_key, dimensions in image_sizes[profile].items():
                optimized_image = resize_and_crop(
                    im, dimensions
                )  # Work on a copy to preserve the original image
                new_filename = f"{random_number}_{size_key}.webp"
                output_path = os.path.join(output_dir, new_filename)
                optimized_image.save(output_path, "webp", optimize=True, quality=85)
                print(f"Saved {output_path}")

    return 0, saved_path


def resize_and_crop(image: Image, dimensions: tuple[int, int]) -> Image:
    # Calculate the scaling factor needed to resize the image to cover the target size.
    img_width, img_height = image.size
    width_ratio = dimensions[0] / img_width
    height_ratio = dimensions[1] / img_height
    if width_ratio > height_ratio:
        new_width = dimensions[0]
        new_height = int(img_height * width_ratio)
    else:
        new_width = int(img_width * height_ratio)
        new_height = dimensions[1]

    # Resize the image with the calculated dimensions.
    resized_image = image.resize((new_width, new_height))

    # Calculate top-left corner of the crop box.
    left = (new_width - dimensions[0]) // 2
    top = (new_height - dimensions[1]) // 2

    # Crop the centered part of the resized image.
    cropped_image = resized_image.crop(
        (left, top, left + dimensions[0], top + dimensions[1])
    )
    return cropped_image


if __name__ == "__main__":
    main()
