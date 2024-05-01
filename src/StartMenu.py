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

        # For whatever reason, the QGraphicsView won't
        # center the box when center layout is selected.
        # Instead, it centers the left edge. Therefore,
        # we must manually handle the view's geometry.

        # Gather properties
        width = e.size().width()
        height = e.size().height()
        rect = self.second.graphicsView.geometry()
        y = rect.y()
        margins = self.second.verticalLayout.getContentsMargins()
        sepSpacing = self.second.verticalLayout.spacing()

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

        rect.setX(x)
        rect.setWidth(minSz)
        rect.setHeight(minSz)
        self.second.graphicsView.setGeometry(rect)
