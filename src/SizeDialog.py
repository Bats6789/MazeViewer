"""The dialog for specifying the size of a maze.

This file utilizes the layout of a ui file, and adds control
logic to it.
"""

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from enum import Enum


class Dimension(Enum):
    """Enumeration for the properties.

    Attributes:
        Width = 0
        Height = 1
    """
    WIDTH = 0
    HEIGHT = 1


class SizeDialog(QDialog):
    """The dialog for assigning the size properties.

    Args:
        width (int): The width of the maze.
        height (int): The height of the maze.
        *args (list): The list of arguments to pass to the parent class.
        **kwargs (dict): Dictionary of key-word arguments to pass to QWidget.

    Attributes:
        width (int): The width of the maze.
        height (int): The height of the maze.
    """

    def __init__(self, width: int, height: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/SizeDialog.ui", self)

        self.dimension = Dimension.WIDTH

        self.width = width
        self.height = height

        self._widthFirstKey = True
        self._heightFirstKey = True

        self.widthSlider.setSliderPosition(width)
        self.heightSlider.setSliderPosition(height)

        self.widthDisplay.setNum(width)
        self.heightDisplay.setNum(height)

        self.widthSlider.sliderReleased.connect(self.setWidthWithSlider)
        self.heightSlider.sliderReleased.connect(self.setHeightWithSlider)

        self.oKButton.clicked.connect(self.setProps)

    def keyPressEvent(self, e: QKeyEvent):
        """Override for the keyPressEvent.

        Note:
            Mainly for handling shortcut keys.

        Args:
            e (QKeyEvent): The key event.
        """
        handled = False

        match (self.dimension):
            case Dimension.WIDTH:
                val = self.width
                firstKey = self._widthFirstKey
            case Dimension.HEIGHT:
                val = self.height
                firstKey = self._heightFirstKey

        kCode = Qt.Key
        match (e.key()):
            case num if kCode.Key_0 <= num <= kCode.Key_9:
                num -= kCode.Key_0

                if firstKey:
                    firstKey = False
                    val = num
                elif val < 2:
                    val *= 10
                    val += num
                elif val == 2 and num == 0:
                    val = 20
                else:
                    val = num
                handled = True

            case kCode.Key_Backspace:
                if val >= 10:
                    val //= 10
                handled = True

            case kCode.Key_Delete:
                if val >= 10:
                    val %= 10
                handled = True

            case kCode.Key_Space:
                if self.dimension == Dimension.WIDTH:
                    self.dimension = Dimension.HEIGHT
                    val = self.height
                else:
                    self.dimension = Dimension.WIDTH
                    val = self.width
                handled = True

        match (self.dimension):
            case Dimension.WIDTH:
                self.width = val
                self._widthFirstKey = firstKey
            case Dimension.HEIGHT:
                self.height = val
                self._heightFirstKey = firstKey

        self.widthSlider.setSliderPosition(self.width)
        self.heightSlider.setSliderPosition(self.height)

        if not handled:
            super().keyPressEvent(e)

    @property
    def width(self):
        """int: The width of the maze.

        Current range is limited between 2 and 20, and will bound any input
        to those values. e.g. width = 1 => width = 2.
        """
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width

    @property
    def height(self):
        """int: The height of the maze.

        Current range is limited between 2 and 20, and will bound any input
        to those values. e.g. height = 1 => height = 2.
        """
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    def setWidthWithSlider(self):
        """Sets the width attribute from the slider position."""
        self.width = self.widthSlider.sliderPosition()

    def setHeightWithSlider(self):
        """Sets the height attribute from the slider position."""
        self.height = self.heightSlider.sliderPosition()

    def setProps(self):
        """Sets all properties."""
        self.setWidthWithSlider()
        self.setHeightWithSlider()
