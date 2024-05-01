from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from cells import Cell


class MazeViewer(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene = QGraphicsScene()
        self.rects = []
        for y in range(10):
            for x in range(10):
                rect = Cell(0, 0, 100, 100)
                rect.setPos(x * 100, y * 100)
                rect.setBrush(QColor(127, 127, 127, 255))
                self.scene.addItem(rect)
                self.rects.append(rect)

        self.setScene(self.scene)
        self.setSceneRect(0, 0, 1000, 1000)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)

    def drawMaze(self, maze):
        rows = maze.split('\n')
        height = (len(rows) - 1) // 2
        width = (len(rows[0]) - 1) // 2

        for y in range(height):
            for x in range(width):
                i = y * width + x

                xStr = 2 * x + 1
                yStr = 2 * y + 1

                self.rects[i].left = rows[yStr][xStr - 1] == '#'

                self.rects[i].right = rows[yStr][xStr + 1] == '#'

                self.rects[i].top = rows[yStr - 1][xStr] == '#'

                self.rects[i].bottom = rows[yStr + 1][xStr] == '#'

                self.rects[i].setBrush(QColor(255, 255, 255, 255))
