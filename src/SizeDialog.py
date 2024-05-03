from PyQt6 import uic
from PyQt6.QtWidgets import QDialog


class SizeDialog(QDialog):
    def __init__(self, width: int, height: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/SizeDialog.ui', self)

        self.width = width
        self.height = height

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
