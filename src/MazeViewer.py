from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QRectF, Qt
from cells import Cell


class MazeViewer(QGraphicsView):
    def __init__(self, width=10, height=10, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene = QGraphicsScene()
        self.rects = []

        self.inactiveColor = QColor(127, 127, 127, 255)
        self.activeColor = QColor(255, 255, 255, 255)
        self.width = width
        self.height = height
        self.sceneWidth = 1000
        self.sceneHeight = 1000

        self.generateMaze()

        self.setScene(self.scene)

    def generateMaze(self):
        if self.rects != []:
            for rect in self.rects:
                self.scene.removeItem(rect)

        self.rects = []

        if self.width > self.height:
            self.sceneWidth = 1000
            self.sceneHeight = 1000 * self.height / self.width
        else:
            self.sceneWidth = 1000 * self.width / self.height
            self.sceneHeight = 1000

        cellWidth = self.sceneWidth / self.width
        cellHeight = self.sceneHeight / self.height
        cellRect = QRectF(0, 0, cellWidth, cellHeight)

        for y in range(self.height):
            for x in range(self.width):
                rect = Cell(cellRect)
                rect.setPos(x * cellWidth, y * cellHeight)
                rect.setBrush(self.inactiveColor)
                self.scene.addItem(rect)
                self.rects.append(rect)

        self.setSceneRect(0, 0, self.sceneWidth, self.sceneHeight)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: int):
        if width > 20:
            self._width = 20
        elif width < 2:
            self._width = 2
        else:
            self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: int):
        if height > 20:
            self._height = 20
        elif height < 2:
            self._height = 2
        else:
            self._height = height

    @property
    def inactiveColor(self):
        return self._inactiveColor

    @inactiveColor.setter
    def inactiveColor(self, color: QColor):
        self._inactiveColor = color

    @property
    def activeColor(self):
        return self._activeColor

    @activeColor.setter
    def activeColor(self, color: QColor):
        self._activeColor = color

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)

    def redrawMaze(self):
        for y in range(self.height):
            for x in range(self.width):
                i = y * self.width + x

                color = self.inactiveColor

                rect = self.rects[i]
                if not (rect.left and rect.right and rect.top and rect.bottom):
                    color = self.activeColor

                self.rects[i].setBrush(color)

    def drawMaze(self, maze):
        rows = maze.split('\n')

        for y in range(self.height):
            for x in range(self.width):
                i = y * self.width + x

                xStr = 2 * x + 1
                yStr = 2 * y + 1

                color = self.inactiveColor

                rect = self.rects[i]

                rect.left = rows[yStr][xStr - 1] == '#'
                rect.right = rows[yStr][xStr + 1] == '#'
                rect.top = rows[yStr - 1][xStr] == '#'
                rect.bottom = rows[yStr + 1][xStr] == '#'

                rect = self.rects[i]
                if not (rect.left and rect.right and rect.top and rect.bottom):
                    color = self.activeColor

                self.rects[i].char = rows[yStr][xStr]

                self.rects[i].setBrush(color)

    def clearMaze(self):
        for y in range(self.height):
            for x in range(self.width):
                i = y * self.width + x

                self.rects[i].left = True
                self.rects[i].right = True
                self.rects[i].top = True
                self.rects[i].bottom = True

                self.rects[i].char = ' '

                self.rects[i].setBrush(self.inactiveColor)

    def refresh(self):
        # self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.fitInView(self.sceneRect())
        self.viewport().update()

    def reset(self):
        self.generateMaze()
        self.clearMaze()
