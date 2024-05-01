from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class MazeViewer(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene = QGraphicsScene()
        self.rects = []
        for y in range(10):
            for x in range(10):
                rect = QGraphicsRectItem(0, 0, 10, 10)
                rect.setPos(x * 10, y * 10)
                rect.setBrush(QColor(127, 127, 127, 255))
                self.scene.addItem(rect)
                self.rects.append(rect)

        self.setScene(self.scene)
        self.setSceneRect(0, 0, 100, 100)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
