"""The View for the maze scene

This file utilizes the layout of a ui file, and adds the control
logic to it.
"""
from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from PyQt6.QtCore import QCoreApplication, QTimerEvent, Qt
from PyQt6.QtGui import QResizeEvent, QKeyEvent
from GrowingTreeDialog import GrowingTreeMethods, methodToString
from BinaryTreeDialog import BinaryTreeBiases, biasToString
import subprocess
import os


class MazeView(QWidget):
    """The view for the maze scene.

    Args:
        *args (list): List of arguments to pass to QWidget.
        **kwargs (dict): Dictionary of key-word arguments to pass to QWidget.

    Attributes:
        step (int): The current step for the maze view.
        speed (int): The speed to run through the steps in steps/s.
        steps (list[str]): The list of steps to generate/solve a maze.
        stepsFile (str): The filename for storing the generated steps.
        mazeFile (str): The filename for storing the generated maze.
        genBin (str): The binary for generating mazes.
        solveBin (str): The binary for solving mazes.
        generator (str): The name of the generator to use (default: kruskal).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/MazeViewing.ui", self)

        self.step = -1
        self.speed = 50
        self.steps = []
        self.stepsFile = "maze.steps"
        self.mazeFile = "maze.mz"
        self.genBin = os.environ["MAZE_GEN"]
        self.solveBin = os.environ["MAZE_SOLVE"]
        self.generator = "kruskal"
        self.solver = "depth"
        self.firstMethod = GrowingTreeMethods.NEWEST
        self.secondMethod = None
        self.split = 0.5
        self.bias = BinaryTreeBiases.SOUTH_WEST

        # Connect control buttons for mazeView page
        self.generateButton.clicked.connect(self.generate)
        self.stepBackButton.clicked.connect(self.stepBack)
        self.stepForwardButton.clicked.connect(self.stepForward)
        self.clearButton.clicked.connect(self.clear)
        self.runButton.clicked.connect(self.run)
        self.solveButton.clicked.connect(self.solve)

        # Set visibility for buttons
        self.stepBackButton.setVisible(False)
        self.stepForwardButton.setVisible(False)
        self.clearButton.setVisible(False)
        self.runButton.setVisible(False)
        self.solveButton.setVisible(False)

    @property
    def speed(self):
        """int: The speed of the run operation in steps/s"""
        return self._speed

    @speed.setter
    def speed(self, speed: int):
        if speed > 100:
            self._speed = 100
        elif speed < 1:
            self._speed = 1
        else:
            self._speed = speed

    @property
    def generator(self):
        return self._generator

    @generator.setter
    def generator(self, generator: str):
        self._generator = generator

    def resizeEvent(self, e: QResizeEvent):
        """Override of the resizeEvent method

        Note:
            The override is due to QGraphicsView improper resizing.

        Args:
            e (QResizeEvent): The resize event.
        """
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

    def timerEvent(self, e: QTimerEvent):
        """Override of the timerEvent method

        Note:
            The override is mainly to handle the run operation.

        Args:
            e (QTimerEvent): The timer event.
        """
        super().timerEvent(e)

        self.mazeViewer.drawMaze(self.steps[self.step])
        self.mazeViewer.refresh()

        if self.step == len(self.steps) - 1:
            self.killTimer(e.timerId())

            # Enable all controls until the run finishes
            self.backButton.setEnabled(True)
            self.generateButton.setEnabled(True)
            self.clearButton.setEnabled(True)
            self.stepBackButton.setEnabled(True)
            self.runButton.setEnabled(True)
            self.solveButton.setEnabled(True)
        else:
            self.step += 1

    def keyPressEvent(self, e: QKeyEvent):
        """Override for the keyPressEvent.

        Note:
            Mainly for handling shortcut keys.

        Args:
            e (QKeyEvent): The key event.
        """
        super().keyPressEvent(e)

        kCode = Qt.Key
        match (e.key()):
            case kCode.Key_Home:
                self.step = 0
                self.mazeViewer.drawMaze(self.steps[self.step])
                self.stepBackButton.setEnabled(False)
                self.stepForwardButton.setEnabled(True)
                self.refreshMazeView()

            case kCode.Key_End:
                self.step = len(self.steps) - 1
                self.mazeViewer.drawMaze(self.steps[self.step])
                self.stepBackButton.setEnabled(True)
                self.stepForwardButton.setEnabled(False)
                self.refreshMazeView()

    def generate(self):
        """Generates the maze and steps for building the maze.

        Note:
            This function will generate a file names after stepsFile attribute.
        """
        generator = [self.generator]

        if self.generator == "growing-tree":
            generator.append(methodToString(self.firstMethod, self.secondMethod))
            if self.secondMethod is not None:
                string = str(self.split)
                if len(string) > 4:
                    string = string[0:4]

                generator.append(string)

        elif self.generator == "binary-tree":
            generator.append(biasToString(self.bias))

        cmd = [
            self.genBin,
            "-q",
            "-v",
            self.stepsFile,
            "-a",
            *generator,
            str(self.mazeViewer.width),
            str(self.mazeViewer.height),
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        self.maze = "\n".join(
            [line.decode("ASCII").strip("\r\n") for line in process.stdout]
        )
        file = open(self.mazeFile, "w")
        file.write(self.maze)
        file.close()

        # Change button text
        self.generateButton.setText("Re&generate")

        # Enable back and forward buttons
        self.stepBackButton.setVisible(True)
        self.stepForwardButton.setVisible(True)
        self.runButton.setVisible(True)
        self.solveButton.setVisible(True)
        self.clearButton.setVisible(True)
        self.stepForwardButton.setEnabled(True)

        # Prep steps and maze
        self.step = 0
        self.steps = self.importSteps(self.stepsFile)

        self.mazeViewer.drawMaze(self.maze)
        self.refreshMazeView()

    def importSteps(self, fileName: str) -> list[str]:
        """Imports and parses the steps from fileName.

        Args:
            fileName (str): The file to import.

        Returns:
            list[str]: The list of steps, with each step being a string.
        """
        file = open(fileName, "r")

        steps = file.read().split("\n\n")
        return steps

    def stepBack(self):
        """Reverts the maze state to its previous state."""
        if self.step == len(self.steps) - 1:
            self.stepForwardButton.setEnabled(True)

        self.step -= 1

        self.mazeViewer.drawMaze(self.steps[self.step])
        self.refreshMazeView()

        if self.step == 0:
            self.stepBackButton.setEnabled(False)

    def stepForward(self):
        """Progresses the maze state to its next state."""
        if self.step == 0:
            self.stepBackButton.setEnabled(True)

        self.step += 1
        self.mazeViewer.drawMaze(self.steps[self.step])
        self.mazeViewer.refresh()

        if self.step == len(self.steps) - 1:
            self.stepForwardButton.setEnabled(False)

    def clear(self):
        """Clear the maze and revert it to its original state."""
        # clear the maze
        self.mazeViewer.clearMaze()
        self.generateButton.setText("&Generate")

        # Hide buttons
        self.stepBackButton.setVisible(False)
        self.stepForwardButton.setVisible(False)
        self.clearButton.setVisible(False)
        self.runButton.setVisible(False)
        self.solveButton.setVisible(False)

        self.refreshMazeView()

    def refreshMazeView(self):
        """Resizes and redraws the maze view."""
        # Resize has to be called every time the maze will be redrawn
        sz = self.geometry().size()
        e = QResizeEvent(sz, sz)
        QCoreApplication.postEvent(self, e)
        self.mazeViewer.refresh()

    def run(self):
        """Run through the steps from start to finish.
        Note:
            The buttons will be disabled during the course of the run.
        """
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
        self.solveButton.setEnabled(False)

        # Start the timer
        self.startTimer(waitTime)

    def solve(self):
        cmd = [
            self.solveBin,
            "-q",
            "-v",
            self.stepsFile,
            "-i",
            self.mazeFile,
            "-a",
            self.solver,
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait()
        self.maze = "\n".join(
            [line.decode("ASCII").strip("\r\n") for line in process.stdout]
        )

        self.step = 0
        self.steps = self.importSteps(self.stepsFile)

        self.stepForwardButton.setEnabled(True)
        self.stepBackButton.setEnabled(False)

        self.mazeViewer.drawMaze(self.maze)
        self.refreshMazeView()
