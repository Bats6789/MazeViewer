from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from enum import Enum


class Dimension(Enum):
    WIDTH = 0
    HEIGHT = 1


class SizeDialog(QDialog):
    def __init__(self, width: int, height: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/SizeDialog.ui", self)

        self.dimension = Dimension.WIDTH

        self.width = width
        self.height = height

        self.widthFirstKey = True
        self.heightFirstKey = True

        self.widthSlider.setSliderPosition(width)
        self.heightSlider.setSliderPosition(height)

        self.widthDisplay.setNum(width)
        self.heightDisplay.setNum(height)

        self.widthSlider.sliderReleased.connect(self.setWidthWithSlider)
        self.heightSlider.sliderReleased.connect(self.setHeightWithSlider)

        self.oKButton.clicked.connect(self.setProps)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    def setWidthWithSlider(self):
        self.width = self.widthSlider.sliderPosition()

    def setHeightWithSlider(self):
        self.height = self.heightSlider.sliderPosition()

    def setProps(self):
        self.setWidthWithSlider()
        self.setHeightWithSlider()

    def keyPressEvent(self, e: QKeyEvent):
        handled = False

        match (self.dimension):
            case Dimension.WIDTH:
                val = self.width
                firstKey = self.widthFirstKey
            case Dimension.HEIGHT:
                val = self.height
                firstKey = self.heightFirstKey

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
                self.widthFirstKey = firstKey
            case Dimension.HEIGHT:
                self.height = val
                self.heightFirstKey = firstKey

        self.widthSlider.setSliderPosition(self.width)
        self.heightSlider.setSliderPosition(self.height)

        if not handled:
            super().keyPressEvent(e)
