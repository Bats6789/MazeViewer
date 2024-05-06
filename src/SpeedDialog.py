from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt


class SpeedDialog(QDialog):
    def __init__(self, speed: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/SpeedDialog.ui', self)

        self.speed = speed
        self.firstKey = True

        self.speedSlider.setSliderPosition(self.speed)
        self.updateDisplay()

        self.speedSlider.valueChanged.connect(self.setSpeedFromSlider)
        self.speedSlider.valueChanged.connect(self.updateDisplay)

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        if speed > 100:
            self._speed = 100
        elif speed < 1:
            self._speed = 1
        else:
            self._speed = speed

    def setSpeedFromSlider(self):
        self.speed = self.speedSlider.sliderPosition()

    def updateDisplay(self):
        self.speedDisplay.setText(f'{self.speed} steps/s')

    def keyPressEvent(self, e: QKeyEvent):
        super().keyPressEvent(e)

        kCode = Qt.Key
        match(e.key()):
            case num if kCode.Key_0 <= num <= kCode.Key_9:
                num -= kCode.Key_0

                if self.firstKey:
                    self.firstKey = False
                    self.speed = num
                elif self.speed < 10:
                    self.speed *= 10
                    self.speed += num
                elif self.speed == 10 and num == 0:
                    self.speed = 100
                else:
                    self.speed = num

            case kCode.Key_Backspace:
                if self.speed >= 10:
                    self.speed //= 10

            case kCode.Key_Delete:
                if self.speed >= 10:
                    self.speed %= 10

        self.speedSlider.setSliderPosition(self.speed)
        self.updateDisplay()
