"""The viewer for the maze."""

from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QRectF, Qt
from cells import Cell


class MazeViewer(QGraphicsView):
    """The viewer for the maze.

    Args:
        width (int): The width of the maze. Defaults to 10.
        height (int): The height of the maze. Defaults to 10.

    Attributes:
        scene (QGraphicsScene): The scene of the view.
        rects (list[Cell]): The list of cells in the maze.
        inactiveColor (QColor): The color of an inactive cell.
        activeColor (QColor): The color of an active cell.
        width (int): The width of the maze.
        height (int): The height of the maze.
    """

    def __init__(self, width: int = 10, height: int = 10, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene = QGraphicsScene()
        self.rects: list[Cell] = []

        self.inactiveColor = QColor(127, 127, 127, 255)
        self.activeColor = QColor(255, 255, 255, 255)
        self.pathColor = QColor(63, 162, 242, 255)
        self.routeColor = QColor(242, 150, 53, 255)
        self.width = width
        self.height = height
        self._sceneWidth = 1000
        self._sceneHeight = 1000

        self.generateMaze()

        self.setScene(self.scene)

    def resizeEvent(self, e):
        """Override of the resizeEvent method.

        Needed to keep the scene in view.
        """
        super().resizeEvent(e)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)

    @property
    def width(self):
        """int: The width of the maze.

        Current range is limited between 2 and 30, and will bound any input
        to those values. e.g. width = 1 => width = 2.
        """
        return self._width

    @width.setter
    def width(self, width: int):
        if width > 30:
            self._width = 30
        elif width < 2:
            self._width = 2
        else:
            self._width = width

    @property
    def height(self):
        """int: The height of the maze.

        Current range is limited between 2 and 30, and will bound any input
        to those values. e.g. height = 1 => height = 2.
        """
        return self._height

    @height.setter
    def height(self, height: int):
        if height > 30:
            self._height = 30
        elif height < 2:
            self._height = 2
        else:
            self._height = height

    @property
    def inactiveColor(self):
        """QColor: The color of an inactive cell."""
        return self._inactiveColor

    @inactiveColor.setter
    def inactiveColor(self, color: QColor):
        self._inactiveColor = color

    @property
    def activeColor(self):
        """QColor: The color of an active cell."""
        return self._activeColor

    @activeColor.setter
    def activeColor(self, color: QColor):
        self._activeColor = color

    @property
    def routeColor(self):
        """QColor: The color of a route cell."""
        return self._routeColor

    @routeColor.setter
    def routeColor(self, color: QColor):
        self._routeColor = color

    @property
    def routeColor(self):
        """QColor: The color of a route cell."""
        return self._routeColor

    @routeColor.setter
    def routeColor(self, color: QColor):
        self._routeColor = color

    def generateMaze(self):
        """Generates the maze.

        Note:
            Will clear any existing maze before generating.
            MazeViewer::refresh will have to be called in order to update view.
        """
        if self.rects != []:
            for rect in self.rects:
                self.scene.removeItem(rect)

        self.rects = []

        if self.width > self.height:
            self._sceneWidth = 1000
            self._sceneHeight = 1000 * self.height / self.width
        else:
            self._sceneWidth = 1000 * self.width / self.height
            self._sceneHeight = 1000

        cellWidth = self._sceneWidth / self.width
        cellHeight = self._sceneHeight / self.height
        cellRect = QRectF(0, 0, cellWidth, cellHeight)

        for y in range(self.height):
            for x in range(self.width):
                rect = Cell(cellRect)
                rect.setPos(x * cellWidth, y * cellHeight)
                rect.setBrush(self.inactiveColor)
                self.scene.addItem(rect)
                self.rects.append(rect)

        self.setSceneRect(0, 0, self._sceneWidth, self._sceneHeight)

    def redrawMaze(self):
        """Redraws the cells in the maze.

        Note:
            MazeViewer::refresh will have to be called in order to update view.
        """
        for y in range(self.height):
            for x in range(self.width):
                i = y * self.width + x

                color = self.inactiveColor

                rect = self.rects[i]
                if not (rect.left and rect.right and rect.top and rect.bottom):
                    color = self.activeColor

                self.rects[i].setBrush(color)
                self.rects[i].pathColor = self.pathColor
                self.rects[i].routeColor = self.routeColor

    def isRoute(self, c: str) -> bool:
        """Determines if a character is a route.

        Args:
            c (str): The character to detrmine if it's a route.

        Returns:
            True if it is a route (*, s, x)
        """
        return c == '*' or c == 's' or c == 'x'

    def drawMaze(self, maze: str):
        """Draws the maze.

        Args:
            maze (str): The maze to draw.

        Note:
            MazeViewer::refresh will have to be called in order to update view.
        """
        rows = maze.split("\n")

        for y in range(self.height):
            for x in range(self.width):
                i = y * self.width + x

                xStr = 2 * x + 1
                yStr = 2 * y + 1

                color = self.inactiveColor

                rect = self.rects[i]

                # Walls
                rect.left = rows[yStr][xStr - 1] == "#"
                rect.right = rows[yStr][xStr + 1] == "#"
                rect.top = rows[yStr - 1][xStr] == "#"
                rect.bottom = rows[yStr + 1][xStr] == "#"

                # Paths
                if rows[yStr][xStr] == "." or self.isRoute(rows[yStr][xStr]):
                    rect.leftPath = rows[yStr][xStr - 1] == "."
                    rect.rightPath = rows[yStr][xStr + 1] == "."
                    rect.topPath = rows[yStr - 1][xStr] == "."
                    rect.bottomPath = rows[yStr + 1][xStr] == "."
                else:
                    rect.leftPath = False
                    rect.rightPath = False
                    rect.topPath = False
                    rect.bottomPath = False

                # Routes
                if self.isRoute(rows[yStr][xStr]):
                    rect.leftRoute = rows[yStr][xStr - 1] == "*"
                    rect.rightRoute = rows[yStr][xStr + 1] == "*"
                    rect.topRoute = rows[yStr - 1][xStr] == "*"
                    rect.bottomRoute = rows[yStr + 1][xStr] == "*"
                else:
                    rect.leftRoute = False
                    rect.rightRoute = False
                    rect.topRoute = False
                    rect.bottomRoute = False

                rect = self.rects[i]
                if not (rect.left and rect.right and rect.top and rect.bottom):
                    color = self.activeColor

                self.rects[i].char = rows[yStr][xStr]

                self.rects[i].setBrush(color)
                self.rects[i].pathColor = self.pathColor
                self.rects[i].routeColor = self.routeColor

    def clearMaze(self):
        """Resets the maze to factory default.

        Note:
            Only restores walls and symbols. It does not revert to original size.
            MazeViewer::refresh will have to be called in order to update view.
        """
        for y in range(self.height):
            for x in range(self.width):
                i = y * self.width + x

                self.rects[i].left = True
                self.rects[i].right = True
                self.rects[i].top = True
                self.rects[i].bottom = True

                self.rects[i].leftPath = False
                self.rects[i].rightPath = False
                self.rects[i].topPath = False
                self.rects[i].bottomPath = False

                self.rects[i].leftRoute = False
                self.rects[i].rightRoute = False
                self.rects[i].topRoute = False
                self.rects[i].bottomRoute = False

                self.rects[i].char = " "

                self.rects[i].setBrush(self.inactiveColor)
                self.rects[i].pathColor = self.pathColor
                self.rects[i].routeColor = self.routeColor

    def refresh(self):
        """Refresh the view of the maze."""
        # self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.fitInView(self.sceneRect())
        self.viewport().update()

    def reset(self):
        """Reset the maze.

        Note:
            Generates and clears the existing maze.
        """
        self.generateMaze()
        self.clearMaze()
