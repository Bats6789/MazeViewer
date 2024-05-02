from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import QPointF, QRect


class Cell(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True
        self.char = ' '

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

        if self.char != ' ':
            # Set font size
            font = painter.font()
            rect = self.rect()

            rect.setWidth(rect.width() * 0.80)  # We want the text to fit inside the box with some gaps
            rect.setHeight(rect.height() * 0.80)  # 80% was a visually appealing scale

            fontSz = self.getLargestFontSize(font, rect, self.char)
            font.setPointSize(fontSz)
            painter.setFont(font)

            # Find where to place the char so it's centered
            fontMetrics = QFontMetrics(font)
            boundingRect = fontMetrics.tightBoundingRect(self.char)

            xShift = (self.rect().width() - boundingRect.width()) // 2
            yShift = (self.rect().height() - boundingRect.height()) // 2

            # The x shift is a shift to the right
            # The y shift is a shift up
            p = QPointF(xLeft + xShift, yBottom - yShift)

            painter.drawText(p, self.char)

    def getLargestFontSize(self, font: QFont, rect: QRect, text: str):
        ogSz = font.pointSize()
        sz = font.pointSize()
        fontMetrics = QFontMetrics(font)
        boundingRect = fontMetrics.tightBoundingRect(text)
        step = -1 if boundingRect.height() > rect.height() else 1
        # print(step)

        while True:
            font.setPointSize(sz + step)
            fontMetrics = QFontMetrics(font)
            boundingRect = fontMetrics.tightBoundingRect(text)

            if sz <= 1:
                break

            if step < 0:
                sz += step
                if boundingRect.height() < rect.height():
                    break
            else:
                if boundingRect.height() > rect.height():
                    break
                sz += step

        font.setPointSize(ogSz)
        return sz