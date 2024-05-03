from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtGui import QResizeEvent
import subprocess


class MazeView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/MazeViewing.ui', self)

        self.step = -1
        self.steps = []
        self.stepsFile = 'maze.steps'

        # Connect control buttons for mazeView page
        self.generateButton.clicked.connect(self.generate)
        self.stepBackButton.clicked.connect(self.stepBack)
        self.stepForwardButton.clicked.connect(self.stepForward)
        self.clearButton.clicked.connect(self.clear)

        # Set visibility for buttons
        self.stepBackButton.setVisible(False)
        self.stepForwardButton.setVisible(False)
        self.clearButton.setVisible(False)

    def resizeEvent(self, e):
        super().resizeEvent(e)

        # For whatever reason, the QGraphicsView won't
        # center the box when center layout is selected.
        # Instead, it centers the left edge. Therefore,
        # we must manually handle the view's geometry.

        # Gather properties
        width = e.size().width()
        height = e.size().height()
        rect = self.mazeViewer.geometry()
        y = rect.y()
        margins = self.verticalLayout.getContentsMargins()
        sepSpacing = self.verticalLayout.spacing()

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
        self.mazeViewer.setGeometry(rect)

    def generate(self):
        cmd = ['\\Users\\bwingard\\C_Projects\\MazeCreator\\bin\\MazeCreator.exe',
               '-q',
               '-v', self.stepsFile]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        self.maze = '\n'.join([line.decode('ASCII').strip('\r\n') for line in process.stdout])

        # Change button text
        self.generateButton.setText('Regenerate')

        # Enable back and forward buttons
        self.stepBackButton.setVisible(True)
        self.stepForwardButton.setVisible(True)
        self.clearButton.setVisible(True)
        self.stepForwardButton.setEnabled(True)

        # Prep steps and maze
        self.step = 0
        self.steps = self.importSteps(self.stepsFile)

        # Resize has to be called everytime the maze will be redrawn
        e = QResizeEvent(self.geometry().size(), self.geometry().size())
        QCoreApplication.postEvent(self, e)
        self.mazeViewer.drawMaze(self.maze)
        self.mazeViewer.refresh()

    def importSteps(self, fileName):
        file = open(fileName, 'r')

        steps = file.read().split('\n\n')
        return steps

    def stepBack(self):
        if self.step == len(self.steps) - 1:
            self.stepForwardButton.setEnabled(True)

        self.step -= 1

        # Resize has to be called everytime the maze will be redrawn
        e = QResizeEvent(self.geometry().size(), self.geometry().size())
        QCoreApplication.postEvent(self, e)
        self.mazeViewer.drawMaze(self.steps[self.step])
        self.mazeViewer.refresh()

        if self.step == 0:
            self.stepBackButton.setEnabled(False)

    def stepForward(self):
        if self.step == 0:
            self.stepBackButton.setEnabled(True)

        self.step += 1
        self.mazeViewer.drawMaze(self.steps[self.step])
        self.mazeViewer.refresh()

        if self.step == len(self.steps) - 1:
            self.stepForwardButton.setEnabled(False)

    def clear(self):
        # Resize has to be called everytime the maze will be redrawn
        e = QResizeEvent(self.geometry().size(), self.geometry().size())
        QCoreApplication.postEvent(self, e)

        # clear the maze
        self.mazeViewer.clearMaze()

        # Hide buttons
        self.stepBackButton.setVisible(False)
        self.stepForwardButton.setVisible(False)
        self.clearButton.setVisible(False)
