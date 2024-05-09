"""The dialog for specifying the Growing-Tree properties.

This file utilizes the layout of a ui file, and adds control
logic to it.
"""

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QKeyEvent, QGuiApplication
from PyQt6.QtCore import Qt
from enum import Enum


class GrowingTreeMethods(Enum):
    """Enumeration for the methods.

    Attributes:
        Newest = 0
        Middle = 1
        Oldest = 2
        Random = 3
    """

    NEWEST = 0
    MIDDLE = 1
    OLDEST = 2
    RANDOM = 3


def methodToString(first: GrowingTreeMethods, second: GrowingTreeMethods):
    match (first):
        case GrowingTreeMethods.NEWEST:
            string = "newest"

        case GrowingTreeMethods.MIDDLE:
            string = "middle"

        case GrowingTreeMethods.OLDEST:
            string = "oldest"

        case GrowingTreeMethods.RANDOM:
            string = "random"

    if second is None:
        return string

    return string + "-" + methodToString(second, None)


class GrowingTreeDialog(QDialog):
    """The dialog for assigning the Growing-Tree property.

    Args:
        first (GrowingTreeMethods): The first method for the Growing tree algorithm
        second (GrowingTreeMethods): The second method for the Growing tree algorithm
        split (float): The ratio between them
        *args (list): The list of arguments to pass to the parent class.
        **kwargs (dict): The key-word arguments to pass to the parent class.

    Attributes:
        first (GrowingTreeMethods): The first method for the Growing tree algorithm
        second (GrowingTreeMethods): The second method for the Growing tree algorithm
        split (float): The ratio between them
    """

    def __init__(
        self,
        first: GrowingTreeMethods = GrowingTreeMethods.NEWEST,
        second: GrowingTreeMethods = None,
        split: float = 0.5,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/GrowingTreeDialog.ui", self)

        if first is None and second is not None:
            first, second = second, first
        elif first is None and second is None:
            first = GrowingTreeMethods.NEWEST
        elif second is not None and first.value > second.value:
            first, second = second, first

        if second is not None and first == second:
            second = None

        self._firstKey = True

        self.first = first
        self.second = second
        self.split = split
        self.clickedButtons = 0
        self.clickOrder = []

        self.splitToDisplay()
        self.splitToPosition()

        self.clickedButtons += self.setButton(self.first)
        self.clickedButtons += self.setButton(self.second)

        if self.first is not None:
            self.clickOrder.append(self.first)
        if self.second is not None:
            self.clickOrder.append(self.second)

        self.splitSlider.valueChanged.connect(self.slideToDisplay)
        self.splitLayout.setVisible(self.clickedButtons == 2)

        self.newestButton.clicked.connect(self.clickedNewestAction)
        self.middleButton.clicked.connect(self.clickedMiddleAction)
        self.oldestButton.clicked.connect(self.clickedOldestAction)
        self.randomButton.clicked.connect(self.clickedRandomAction)

    @property
    def split(self) -> float:
        """float: The ratio between methods.

        Curent range is limited between 0.0 and 1.0. Values are clamped to that range.
        """
        return self._split

    @split.setter
    def split(self, split: float):
        if split > 1.0:
            self._split = 1.0
        elif split < 0.0:
            self._split = 0.0
        else:
            self._split = split

    @property
    def first(self):
        """GrowingTreeMethods: The first method."""
        return self._first

    @first.setter
    def first(self, first):
        self._first = first

    @property
    def second(self):
        """GrowingTreeMethods: The second method."""
        return self._second

    @second.setter
    def second(self, second):
        self._second = second

    def keyPressEvent(self, e: QKeyEvent):
        """Override for the keyPressEvent.

        Note:
            Mainly for handling shortcut keys.

        Args:
            e (QKeyEvent): The key event.
        """
        kCode = Qt.Key
        val = int(self.split * 100)
        match (e.key()):
            case num if kCode.Key_0 <= num <= kCode.Key_9:
                num -= kCode.Key_0

                if self._firstKey:
                    self._firstKey = False
                    val = num
                elif val < 10:
                    val *= 10
                    val += num
                elif val == 10 and num == 0:
                    val = 100
                else:
                    val = num

            case kCode.Key_Backspace:
                if val >= 10:
                    val //= 10

            case kCode.Key_Delete:
                if val >= 10:
                    val %= 10

            case kCode.Key_Enter:
                self.accept()

        self.split = val / 100.0

        self.splitToPosition()
        self.splitToDisplay()

        super().keyPressEvent(e)

    def splitToDisplay(self):
        string = str(self.split)
        if len(string) > 4:
            string = string[:4]

        self.splitDisplay.setText(string)

    def splitToPosition(self):
        val = int(self.split * 100)

        self.splitSlider.setSliderPosition(val)

    def positionToSplit(self):
        self.split = self.splitSlider.sliderPosition() / 100.0

    def slideToDisplay(self):
        self.positionToSplit()
        self.splitToDisplay()

    def setButton(self, method):
        if method is None:
            return 0

        match method:
            case GrowingTreeMethods.NEWEST:
                self.newestButton.setChecked(True)

            case GrowingTreeMethods.MIDDLE:
                self.middleButton.setChecked(True)

            case GrowingTreeMethods.OLDEST:
                self.oldestButton.setChecked(True)

            case GrowingTreeMethods.RANDOM:
                self.randomButton.setChecked(True)

        return 1

    def unsetButton(self, method):
        if method is None:
            return 0

        match method:
            case GrowingTreeMethods.NEWEST:
                self.newestButton.setChecked(False)

            case GrowingTreeMethods.MIDDLE:
                self.middleButton.setChecked(False)

            case GrowingTreeMethods.OLDEST:
                self.oldestButton.setChecked(False)

            case GrowingTreeMethods.RANDOM:
                self.randomButton.setChecked(False)

        return 1

    def setPropsFromClickedOrder(self):
        if self.clickedButtons == 1:
            self.first = self.clickOrder[0]
            self.second = None
        else:
            if self.clickOrder[0].value > self.clickOrder[1].value:
                self.first = self.clickOrder[1]
                self.second = self.clickOrder[0]
            else:
                self.first = self.clickOrder[0]
                self.second = self.clickOrder[1]

    def clickedAction(self, method, isChecked):
        isShift = (
            QGuiApplication.queryKeyboardModifiers() & Qt.KeyboardModifier.ShiftModifier
        )

        match self.clickedButtons:
            case 2:
                if isChecked:
                    self.clickedButtons -= self.unsetButton(method)
                    self.clickOrder.remove(method)

                elif isShift:
                    self.unsetButton(self.clickOrder.pop(0))
                    self.setButton(method)
                    self.clickOrder.append(method)

            case 1:
                if not isChecked:
                    if isShift:
                        self.unsetButton(self.clickOrder.pop(0))
                        self.setButton(method)
                        self.clickOrder.append(method)
                        self.first = method
                    else:
                        self.clickedButtons += self.setButton(method)
                        self.clickOrder.append(method)
                else:
                    self.setButton(method)

        self.setPropsFromClickedOrder()
        self.splitLayout.setVisible(self.clickedButtons == 2)

    def clickedNewestAction(self):
        self.newestButton.toggle()
        self.clickedAction(GrowingTreeMethods.NEWEST, self.newestButton.isChecked())

    def clickedMiddleAction(self):
        self.middleButton.toggle()
        self.clickedAction(GrowingTreeMethods.MIDDLE, self.middleButton.isChecked())

    def clickedOldestAction(self):
        self.oldestButton.toggle()
        self.clickedAction(GrowingTreeMethods.OLDEST, self.oldestButton.isChecked())

    def clickedRandomAction(self):
        self.randomButton.toggle()
        self.clickedAction(GrowingTreeMethods.RANDOM, self.randomButton.isChecked())
