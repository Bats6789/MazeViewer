"""The cells of a maze.

This file utilizes the layout of a ui file, and adds control
logic to it.
"""
from PyQt6.QtWidgets import QGraphicsRectItem, QWidget, QStyleOptionGraphicsItem
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import QPointF, QRect


class Cell(QGraphicsRectItem):
    """The cells of a maze.

    Args:
        *args (list): The list of arguments to pass to the parent class.
        **kwargs (dict): Dictionary of key-word arguments to pass to QWidget.

    Attributes:
        left (bool): True when the left wall exist.
        right (bool): True when the right wall exist.
        top (bool): True when the top wall exist.
        bottom (bool): True when the bottom wall exist.
        char (char): The symbol of the cell.
                        ' ' - empty
                        '#' - wall
                        '*' - route
                        'S' - Start (not visited)
                        's' - Start (visited)
                        'X' - Exit (not visited)
                        'x' - Exit (visited)
        wallColor (QColor): The color of the wall.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left = True
        self.right = True
        self.top = True
        self.bottom = True
        self.char = ' '

        self.wallColor = QColor(0, 0, 0, 255)  # Black

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """Override of the paint method.

        The override is necessary because only some of the walls may be drawn for a cell.
        In addition, a symbol may be drawn over the existing cell (S, X).

        Args:
            painter (QPainter): The painter.
            option (QStyleOptionGraphicsItem): The style options.
            widget (QWidget): The widget.
        """

        # Standard rectangle
        painter.fillRect(self.rect(), self.brush().color())

        # Set pen to wallColor
        pen = painter.pen()
        pen.setColor(self.wallColor)
        painter.setPen(pen)

        # Get the four corners of the rectangle
        xLeft = self.rect().x()
        xRight = xLeft + self.rect().width()
        yTop = self.rect().y()
        yBottom = yTop + self.rect().height()

        # Draw left wall if needed
        p1 = QPointF(xLeft, yTop)
        p2 = QPointF(xLeft, yBottom)
        if self.left:
            painter.drawLine(p1, p2)

        # Always draw the corner points to keep things looking square
        painter.drawPoints(p1, p2)

        # Draw right wall if needed
        p1 = QPointF(xRight, yTop)
        p2 = QPointF(xRight, yBottom)
        if self.right:
            painter.drawLine(p1, p2)

        # Always draw the corner points to keep things looking square
        painter.drawPoints(p1, p2)

        # Draw top wall if needed
        p1 = QPointF(xLeft, yTop)
        p2 = QPointF(xRight, yTop)
        if self.top:
            painter.drawLine(p1, p2)

        # Draw bottom wall if needed
        p1 = QPointF(xLeft, yBottom)
        p2 = QPointF(xRight, yBottom)
        if self.bottom:
            painter.drawLine(p1, p2)

        # Draw char if needed
        if self.char.lower() == 's' or self.char.lower() == 'x':
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

    def getLargestFontSize(self, font: QFont, rect: QRect, text: str) -> int:
        """Gets the largest font to fit in a rectangle.

        Args:
            font (QFont): The font in use.
            rect (QRect): The rectangle for containing the text.
            text (str): The text to fit in the rectangle.

        Returns:
            int: The largest font size that will fit text into rect.
        """
        # Grab initial properties
        ogSz = font.pointSize()
        sz = font.pointSize()
        fontMetrics = QFontMetrics(font)
        boundingRect = fontMetrics.tightBoundingRect(text)
        step = -1 if boundingRect.height() > rect.height() else 1

        # Keep running until the font size fits the rectangle
        while True:
            font.setPointSize(sz + step)
            fontMetrics = QFontMetrics(font)
            boundingRect = fontMetrics.tightBoundingRect(text)

            if sz <= 1:
                break

            # if the font size was too big, shrink it until it fits
            if step < 0:
                sz += step
                if boundingRect.height() < rect.height():
                    break
            # if the font size was too small, grow it until it is too big
            else:
                if boundingRect.height() > rect.height():
                    break
                sz += step

        # Reset font to original size
        font.setPointSize(ogSz)

        return sz
