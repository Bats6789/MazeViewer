"""The main entry point for MazeViewer

This file is the main entry point for the MazeViewer project.
"""

import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/StartMenu.ui', self)

        # Connect page swapping buttons
        self.StartButton.clicked.connect(self.goToSecond)
        self.second = uic.loadUi('ui/MazeViewing.ui')
        self.second.BackButton.clicked.connect(self.goToFirst)
        self.stackedWidget.addWidget(self.second)

    def goToFirst(self):
        self.stackedWidget.setCurrentIndex(0)
        print(self.stackedWidget)

    def goToSecond(self):
        self.stackedWidget.setCurrentIndex(1)
        print(self.stackedWidget)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    # window = uic.loadUi('ui/MazeViewing.ui')
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
