from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class MazeViewer(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.scene = QGraphicsScene()
        self.rect = QGraphicsRectItem(0, 0, 100, 100)
        self.rect.setPos(0, 0)
        self.rect.setBrush(QColor(127, 127, 127, 255))
        self.scene.addItem(self.rect)
        self.setScene(self.scene)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        sz = e.size()
        minSz = min(sz.width(), sz.height())
        # self.setFixedSize(minSz, minSz)
        self.setSceneRect(0, 0, minSz, minSz)
        self.fitInView(0, 0, minSz, minSz, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
