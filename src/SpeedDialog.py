"""The dialog for specifying the speed property.

This file utilizes the layout of a ui file, and adds control
logic to it.
"""

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt


class SpeedDialog(QDialog):
    """The dialog for assigning the speed property.

    Args:
        speed (int): The speed for the run operation (steps/s).
        *args (list): The list of arguments to pass to the parent class.
        **kwargs (dict): The key-word arguments to pass to the parent class.

    Attributes:
        speed (int): The speed for the run operation (steps/s).
    """

    def __init__(self, speed: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('ui/SpeedDialog.ui', self)

        self.speed = speed
        self._firstKey: bool = True

        self.speedSlider.setSliderPosition(self.speed)
        self.updateDisplay()

        self.speedSlider.valueChanged.connect(self.setSpeedFromSlider)
        self.speedSlider.valueChanged.connect(self.updateDisplay)

    def keyPressEvent(self, e: QKeyEvent):
        """Override for the keyPressEvent.

        Note:
            Mainly for handling shortcut keys.

        Args:
            e (QKeyEvent): The key event.
        """
        super().keyPressEvent(e)

        kCode = Qt.Key
        match(e.key()):
            case num if kCode.Key_0 <= num <= kCode.Key_9:
                num -= kCode.Key_0

                if self._firstKey:
                    self._firstKey = False
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

    @property
    def speed(self):
        """int: The speed of the run operation in steps/s.

        Current range is limited between 1 and 100, and will bound any input
        to those values. e.g. speed = 0 => speed = 1.
        """
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
        """Sets the speed attribute from the current slider position."""
        self.speed = self.speedSlider.sliderPosition()

    def updateDisplay(self):
        """Update the display with the current speed."""
        self.speedDisplay.setText(f'{self.speed} steps/s')
