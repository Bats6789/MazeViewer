"""The main entry point for MazeViewer

This file is the main entry point for the MazeViewer project.
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QColorDialog
# from PyQt6.QtCore import QCoreApplication
# from PyQt6.QtGui import QResizeEvent
from MazeView import MazeView


class MainWindow(QMainWindow):
    """The main window class for the start menu

    The start menu contains a quit button that terminates the window,
    and a start button to start the project.
    """

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/StartMenu.ui', self)

        # Connect page swapping buttons
        self.startButton.clicked.connect(self.goToMazeView)
        self.mazeView = MazeView()
        self.mazeView.backButton.clicked.connect(self.goToMainMenu)
        self.stackedWidget.addWidget(self.mazeView)

        # Settings menu options
        self.actionActiveCellColor.triggered.connect(self.activeColorAction)
        self.actionInactiveCellColor.triggered.connect(self.inactiveColorAction)

    def goToMainMenu(self):
        """Go to the first page."""
        self.stackedWidget.setCurrentIndex(0)

    def goToMazeView(self):
        """Go to the second page."""
        self.stackedWidget.setCurrentIndex(1)
        # e = QResizeEvent(self.geometry().size(), self.geometry().size())
        # QCoreApplication.postEvent(self, e)

    def activeColorAction(self):
        dialog = QColorDialog(self.mazeView.mazeViewer.activeColor)
        if dialog.exec():
            self.mazeView.mazeViewer.activeColor = dialog.selectedColor()
            self.mazeView.mazeViewer.redrawMaze()
            self.mazeView.mazeViewer.refresh()

    def inactiveColorAction(self):
        dialog = QColorDialog(self.mazeView.mazeViewer.inactiveColor)
        if dialog.exec():
            self.mazeView.mazeViewer.inactiveColor = dialog.selectedColor()
            self.mazeView.mazeViewer.redrawMaze()
            self.mazeView.mazeViewer.refresh()

    def resizeEvent(self, e):
        super().resizeEvent(e)

        self.mazeView.mazeViewer.refresh()
