from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QPointF


class Cell(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True

        self.wallColor = QColor(0, 0, 0, 255)  # Black

    def paint(self, painter: QPainter, option, widget):
        painter.fillRect(self.rect(), self.brush().color())

        pen = painter.pen()
        pen.setColor(self.wallColor)
        painter.setPen(pen)

        xLeft = self.rect().x()
        xRight = xLeft + self.rect().width()
        yTop = self.rect().y()
        yBottom = yTop + self.rect().height()

        p1 = QPointF(xLeft, yTop)
        p2 = QPointF(xLeft, yBottom)
        if self.left:
            painter.drawLine(p1, p2)

        painter.drawPoints(p1, p2)

        p1 = QPointF(xRight, yTop)
        p2 = QPointF(xRight, yBottom)
        if self.right:
            painter.drawLine(p1, p2)

        painter.drawPoints(p1, p2)

        p1 = QPointF(xLeft, yTop)
        p2 = QPointF(xRight, yTop)
        if self.top:
            painter.drawLine(p1, p2)

        p1 = QPointF(xLeft, yBottom)
        p2 = QPointF(xRight, yBottom)
        if self.bottom:
            painter.drawLine(p1, p2)
