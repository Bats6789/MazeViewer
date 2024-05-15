"""The dialog for specifying the Binary-Tree bias.

This file utilizes the layout of a ui file, and adds control
logic to it.
"""

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from enum import Enum


class BinaryTreeBiases(Enum):
    """Enumeration for the methods.

    Attributes:
        NORTH_WEST = 0
        NORTH_EAST = 1
        SOUTH_WEST = 2
        SOUTH_EAST = 3
    """

    NORTH_WEST = 0
    NORTH_EAST = 1
    SOUTH_WEST = 2
    SOUTH_EAST = 3


def biasToString(bias: BinaryTreeBiases):
    match bias:
        case BinaryTreeBiases.NORTH_WEST:
            string = "northwest"

        case BinaryTreeBiases.NORTH_EAST:
            string = "northeast"

        case BinaryTreeBiases.SOUTH_WEST:
            string = "southwest"

        case BinaryTreeBiases.SOUTH_EAST:
            string = "southeast"

    return string


class BinaryTreeDialog(QDialog):
    """The dialog for assigning the Binary-Tree property.

    Args:
        bias (BinaryTreeBiases): The bias for the Binary tree algorithm
        *args (list): The list of arguments to pass to the parent class.
        **kwargs (dict): The key-word arguments to pass to the parent class.

    Attributes:
        bias (BinaryTreeBiases): The bias for the Binary tree algorithm
    """

    def __init__(
        self,
        bias: BinaryTreeBiases = BinaryTreeBiases.NORTH_WEST,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        uic.loadUi("ui/BinaryTreeDialog.ui", self)

        self.bias = bias

        self.northEastRadioButton.clicked.connect(self.clickedNorthEastAction)
        self.northWestRadioButton.clicked.connect(self.clickedNorthWestAction)
        self.southEastRadioButton.clicked.connect(self.clickedSouthEastAction)
        self.southWestRadioButton.clicked.connect(self.clickedSouthWestAction)

        match self.bias:
            case BinaryTreeBiases.NORTH_WEST:
                self.northWestRadioButton.click()

            case BinaryTreeBiases.NORTH_EAST:
                self.northEastRadioButton.click()

            case BinaryTreeBiases.SOUTH_WEST:
                self.southWestRadioButton.click()

            case BinaryTreeBiases.SOUTH_EAST:
                self.southEastRadioButton.click()

    @property
    def bias(self):
        """BinaryTreeBiases: The bias."""
        return self._bias

    @bias.setter
    def bias(self, bias):
        self._bias = bias

    def keyPressEvent(self, e: QKeyEvent):
        """Override for the keyPressEvent.

        Note:
            Mainly for handling shortcut keys.

        Args:
            e (QKeyEvent): The key event.
        """
        kCode = Qt.Key
        match (e.key()):
            case kCode.Key_N:
                self.northWestRadioButton.click()

            case kCode.Key_E:
                self.northEastRadioButton.click()

            case kCode.Key_W:
                self.southWestRadioButton.click()

            case kCode.Key_S:
                self.southEastRadioButton.click()

        super().keyPressEvent(e)

    def clickedNorthWestAction(self):
        self.bias = BinaryTreeBiases.NORTH_WEST

    def clickedNorthEastAction(self):
        self.bias = BinaryTreeBiases.NORTH_EAST

    def clickedSouthWestAction(self):
        self.bias = BinaryTreeBiases.SOUTH_WEST

    def clickedSouthEastAction(self):
        self.bias = BinaryTreeBiases.SOUTH_EAST
