import sys

# pylint: disable=no-name-in-module
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow

from .ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        @pyqtSlot()
        def input_path_button():
            file = QFileDialog.getOpenFileName(caption="Выберите текстовый файл", directory="/", filter="Text Files (*.txt)")
            if file != "":
                self.inputPathLineEdit.setText(file[0])
        self.inputPathButton.pressed.connect(input_path_button)

        @pyqtSlot()
        def output_path_button():
            folder_dialog = QFileDialog(caption="Выбереите папку", directory="/")
            folder_dialog.setFileMode(QFileDialog.FileMode.Directory)
            folder_dialog.setOption(QFileDialog.Option.ShowDirsOnly)
            folder = folder_dialog.getExistingDirectory()
            if folder != "":
                self.outputPathLineEdit.setText(folder)
        self.outputPathButton.pressed.connect(output_path_button)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
