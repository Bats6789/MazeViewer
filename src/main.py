"""The main entry point for MazeViewer

This file is the main entry point for the MazeViewer project.
"""

import sys
from PyQt6.QtWidgets import QApplication
from StartMenu import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setStyle('Fusion')

    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
