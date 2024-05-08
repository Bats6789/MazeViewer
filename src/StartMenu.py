"""The main entry point for MazeViewer

This file is the main entry point for the MazeViewer project.
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QColorDialog
from MazeView import MazeView
from SizeDialog import SizeDialog
from SpeedDialog import SpeedDialog


class MainWindow(QMainWindow):
    """The main window class for the start menu."""

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/StartMenu.ui', self)

        # Connect page swapping buttons
        self.startButton.clicked.connect(self.goToMazeView)
        self.mazeView = MazeView()
        self.mazeView.backButton.clicked.connect(self.goToMainMenu)
        self.stackedWidget.addWidget(self.mazeView)

        # Algorithms menu options
        # Generators
        self.actionKruskal.triggered.connect(self.kruskalAction)
        self.actionPrim.triggered.connect(self.primAction)
        self.actionBack.triggered.connect(self.backAction)
        self.actionAldousBroder.triggered.connect(self.aldousBroderAction)

        # Solvers

        # Settings menu options
        self.actionActiveCellColor.triggered.connect(self.activeColorAction)
        self.actionInactiveCellColor.triggered.connect(self.inactiveColorAction)
        self.actionObservingColor.triggered.connect(self.observingColorAction)
        self.actionCheckPathColor.triggered.connect(self.checkPathColorAction)
        self.actionSolvePathColor.triggered.connect(self.solvePathColorAction)
        self.actionSize.triggered.connect(self.adjustSize)
        self.actionRunSpeed.triggered.connect(self.adjustSpeed)

    def resizeEvent(self, e):
        """Override of the resizeEvent method.

        Passes any resize event to the mazeViewer.
        """
        super().resizeEvent(e)

        self.mazeView.mazeViewer.refresh()

    def goToMainMenu(self):
        """Go to the first page."""
        self.stackedWidget.setCurrentIndex(0)

    def goToMazeView(self):
        """Go to the second page."""
        self.stackedWidget.setCurrentIndex(1)

    def activeColorAction(self):
        """Starts dialog for assigning the active cell color."""
        dialog = QColorDialog(self.mazeView.mazeViewer.activeColor)
        if dialog.exec():
            self.mazeView.mazeViewer.activeColor = dialog.selectedColor()
            self.mazeView.mazeViewer.redrawMaze()
            self.mazeView.mazeViewer.refresh()

    def inactiveColorAction(self):
        """Starts dialog for assigning the inactive cell color."""
        dialog = QColorDialog(self.mazeView.mazeViewer.inactiveColor)
        if dialog.exec():
            self.mazeView.mazeViewer.inactiveColor = dialog.selectedColor()
            self.mazeView.mazeViewer.redrawMaze()
            self.mazeView.mazeViewer.refresh()

    def observingColorAction(self):
        """Starts dialog for assigning the observing cell color."""
        dialog = QColorDialog(self.mazeView.mazeViewer.observingColor)
        if dialog.exec():
            self.mazeView.mazeViewer.observingColor = dialog.selectedColor()
            self.mazeView.mazeViewer.redrawMaze()
            self.mazeView.mazeViewer.refresh()

    def checkPathColorAction(self):
        """Starts dialog for assigning the path color."""
        dialog = QColorDialog(self.mazeView.mazeViewer.pathColor)
        if dialog.exec():
            self.mazeView.mazeViewer.pathColor = dialog.selectedColor()
            self.mazeView.mazeViewer.redrawMaze()
            self.mazeView.mazeViewer.refresh()

    def solvePathColorAction(self):
        """Starts dialog for assigning the route color."""
        dialog = QColorDialog(self.mazeView.mazeViewer.routeColor)
        if dialog.exec():
            self.mazeView.mazeViewer.routeColor = dialog.selectedColor()
            self.mazeView.mazeViewer.redrawMaze()
            self.mazeView.mazeViewer.refresh()

    def adjustSize(self):
        """Starts dialog for adjusting the size of the maze."""
        mazeViewer = self.mazeView.mazeViewer
        dialog = SizeDialog(mazeViewer.width, mazeViewer.height)
        if dialog.exec():
            self.mazeView.mazeViewer.width = dialog.width
            self.mazeView.mazeViewer.height = dialog.height
            self.mazeView.mazeViewer.reset()
            self.mazeView.clear()

    def adjustSpeed(self):
        """Starts dialog for adjusting the speed of the run operation."""
        dialog = SpeedDialog(self.mazeView.speed)
        if dialog.exec():
            self.mazeView.speed = dialog.speed

    def kruskalAction(self):
        self.mazeView.generator = 'kruskal'

    def primAction(self):
        self.mazeView.generator = 'prim'

    def backAction(self):
        self.mazeView.generator = 'back'

    def aldousBroderAction(self):
        self.mazeView.generator = 'aldous-broder'
