import os
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

        """ Mount layout part """
        layout.addWidget(label1)
        layout.addWidget(self.lith_profile)
        layout.addWidget(self.tys_profile)
        layout.addWidget(label2)
        layout.addWidget(select_files_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def set_profile(self):
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
            file_filter = "Images (*.png *.jpg *.jpeg)"
            response = QFileDialog.getOpenFileNames(
                caption="Sélectionnez une ou plusieurs images",
                directory=os.getcwd(),
                filter=file_filter,
            )
            if response[0]:
                optimize(response[0])


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


def optimize(files_paths: list[str]) -> bool:
    """Optimize images for web,
    Create a folder containing 2 thumbnails for each pictures,

    one for small
    """
    print(files_paths)

    return True


if __name__ == "__main__":
    main()
