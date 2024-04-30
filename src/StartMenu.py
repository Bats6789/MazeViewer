"""The main entry point for MazeViewer

This file is the main entry point for the MazeViewer project.
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QResizeEvent


class MainWindow(QMainWindow):
    """The main window class for the start menu

    The start menu contains a quit button that terminates the window,
    and a start button to start the project.
    """

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/StartMenu.ui', self)

        # Connect page swapping buttons
        self.startButton.clicked.connect(self.goToSecond)
        self.second = uic.loadUi('ui/MazeViewing.ui')
        self.second.backButton.clicked.connect(self.goToFirst)
        self.stackedWidget.addWidget(self.second)
        pass

    def goToFirst(self):
        """Go to the first page."""
        self.stackedWidget.setCurrentIndex(0)
        pass

    def goToSecond(self):
        """Go to the second page."""
        self.stackedWidget.setCurrentIndex(1)
        e = QResizeEvent(self.geometry().size(), self.geometry().size())
        QCoreApplication.postEvent(self, e)
        pass

    def resizeEvent(self, e):
        super().resizeEvent(e)

        width = e.size().width()
        height = e.size().height()
        minSz = min(width, height)

        self.second.graphicsView.resize(minSz, minSz)
