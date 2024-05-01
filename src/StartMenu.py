"""The main entry point for MazeViewer

This file is the main entry point for the MazeViewer project.
"""
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QResizeEvent
import subprocess


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
        self.mazeView = uic.loadUi('ui/MazeViewing.ui')
        self.mazeView.backButton.clicked.connect(self.goToMainMenu)
        self.stackedWidget.addWidget(self.mazeView)

        # Connect control buttons for mazeView page
        self.mazeView.generateButton.clicked.connect(self.generate)
        pass

    def goToMainMenu(self):
        """Go to the first page."""
        self.stackedWidget.setCurrentIndex(0)
        pass

    def goToMazeView(self):
        """Go to the second page."""
        self.stackedWidget.setCurrentIndex(1)
        e = QResizeEvent(self.geometry().size(), self.geometry().size())
        QCoreApplication.postEvent(self, e)
        pass

    def resizeEvent(self, e):
        super().resizeEvent(e)

        # For whatever reason, the QGraphicsView won't
        # center the box when center layout is selected.
        # Instead, it centers the left edge. Therefore,
        # we must manually handle the view's geometry.

        # Gather properties
        width = e.size().width()
        height = e.size().height()
        rect = self.mazeView.mazeViewer.geometry()
        y = rect.y()
        margins = self.mazeView.verticalLayout.getContentsMargins()
        sepSpacing = self.mazeView.verticalLayout.spacing()

        # Determine the length of the sides
        horSpacing = margins[0] + margins[2]  # left and right margin
        verSpacing = margins[1] + margins[3]  # top and bottom margin
        heightBuf = y + 2 * sepSpacing + verSpacing  # total space consumed from height
        minSz = int(min(width - horSpacing, height - heightBuf))

        # determine X location
        if width > minSz:
            x = int(width - minSz) // 2
        else:
            x = 0

        # Set properties of the rectangle
        rect.setX(x)
        rect.setWidth(minSz)
        rect.setHeight(minSz)

        # Scale the GraphicsView's view
        self.mazeView.mazeViewer.setGeometry(rect)

    def generate(self):
        cmd = ['\\Users\\bwingard\\C_Projects\\MazeCreator\\bin\\MazeCreator.exe', '-q']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        maze = '\n'.join([line.decode('ASCII').strip('\r\n') for line in process.stdout])
        self.mazeView.mazeViewer.drawMaze(maze)
        self.mazeView.mazeViewer.viewport().update()
