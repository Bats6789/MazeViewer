from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import QCoreApplication, QTimerEvent
from PyQt6.QtGui import QResizeEvent
import subprocess
import os


class MazeView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/MazeViewing.ui', self)

        self.step = -1
        self.speed = 50
        self.steps = []
        self.stepsFile = 'maze.steps'
        self.genBin = os.environ['MAZE_GEN']

        # Connect control buttons for mazeView page
        self.generateButton.clicked.connect(self.generate)
        self.stepBackButton.clicked.connect(self.stepBack)
        self.stepForwardButton.clicked.connect(self.stepForward)
        self.clearButton.clicked.connect(self.clear)
        self.runButton.clicked.connect(self.run)

        # Set visibility for buttons
        self.stepBackButton.setVisible(False)
        self.stepForwardButton.setVisible(False)
        self.clearButton.setVisible(False)
        self.runButton.setVisible(False)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: int):
        if speed > 100:
            self._speed = 100
        elif speed < 1:
            self._speed = 1
        else:
            self._speed = speed

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
        sceneRect = self.mazeViewer.sceneRect()

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

        # Determine ratio
        if sceneRect.width() > sceneRect.height():
            widthScale = 1
            heightScale = sceneRect.height() / sceneRect.width()
        else:
            widthScale = sceneRect.width() / sceneRect.height()
            heightScale = 1

        # Set properties of the rectangle
        rect.setX(x)
        rect.setWidth(int(minSz * widthScale))
        rect.setHeight(int(minSz * heightScale))

        # Scale the GraphicsView's view
        self.mazeViewer.setGeometry(rect)

    def generate(self):
        cmd = [self.genBin, '-q',
               '-v', self.stepsFile,
               str(self.mazeViewer.width), str(self.mazeViewer.height)]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        self.maze = '\n'.join([line.decode('ASCII').strip('\r\n') for line in process.stdout])

        # Change button text
        self.generateButton.setText('Re&generate')

        # Enable back and forward buttons
        self.stepBackButton.setVisible(True)
        self.stepForwardButton.setVisible(True)
        self.runButton.setVisible(True)
        self.clearButton.setVisible(True)
        self.stepForwardButton.setEnabled(True)

        # Prep steps and maze
        self.step = 0
        self.steps = self.importSteps(self.stepsFile)

        self.mazeViewer.drawMaze(self.maze)
        self.refreshMazeView()

    def importSteps(self, fileName):
        file = open(fileName, 'r')

        steps = file.read().split('\n\n')
        return steps

    def stepBack(self):
        if self.step == len(self.steps) - 1:
            self.stepForwardButton.setEnabled(True)

        self.step -= 1

        self.mazeViewer.drawMaze(self.steps[self.step])
        self.refreshMazeView()

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
        # clear the maze
        self.mazeViewer.clearMaze()
        self.generateButton.setText('&Generate')

        # Hide buttons
        self.stepBackButton.setVisible(False)
        self.stepForwardButton.setVisible(False)
        self.clearButton.setVisible(False)
        self.runButton.setVisible(False)

        self.refreshMazeView()

    def refreshMazeView(self):
        # Resize has to be called everytime the maze will be redrawn
        sz = self.geometry().size()
        e = QResizeEvent(sz, sz)
        QCoreApplication.postEvent(self, e)
        self.mazeViewer.refresh()

    def run(self):

        self.step = 0

        # The waiting time is based on milliseconds.
        # The setting is steps/s, so 1/speed = s/steps
        # 1000 ms / s => 1000 * 1/speed
        waitTime = int(1000 * 1 / self.speed)

        # Disable all controls until the run finishes
        self.backButton.setEnabled(False)
        self.generateButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.stepBackButton.setEnabled(False)
        self.stepForwardButton.setEnabled(False)
        self.runButton.setEnabled(False)

        # Start the timer
        self.startTimer(waitTime)

    def timerEvent(self, e: QTimerEvent):
        super().timerEvent(e)

        self.mazeViewer.drawMaze(self.steps[self.step])
        self.mazeViewer.refresh()
        self.step += 1

        if self.step == len(self.steps):
            self.killTimer(e.timerId())

            # Enable all controls until the run finishes
            self.backButton.setEnabled(True)
            self.generateButton.setEnabled(True)
            self.clearButton.setEnabled(True)
            self.stepBackButton.setEnabled(True)
            self.runButton.setEnabled(True)
