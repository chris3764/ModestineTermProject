# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 10:00:02 2021

@author: cjwal
"""

import sys

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from functools import partial
__version__ = '0.1'
__author__ = 'Leodanis Pozo Ramos'

class PyCalcCtrl:
    """PyCalc Controller class."""
    def __init__(self, model, view,outputFile):
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()
        self._outputFile = outputFile
    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText(),outputFile = self._outputFile)
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
# Create a subclass of QMainWindow to setup the calculator's GUI
class PyCalcUi(QMainWindow):
    """PyCalc's View (GUI)."""
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('PyCalc')
        self.setFixedSize(1000, 1000)
        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        self._createDisplay()
        self._createButtons()
    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QLineEdit()
        # Set some display's properties
        self.display.setFixedHeight(100)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)
    def _createButtons(self):
        """Create the buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {'Service call': (0, 0),
                   'R': (0, 1),
                   ';': (0, 2),
                   '|': (0, 3),
                   'C': (0, 4),
                   'JRPI': (1, 0),
                   'JerrySmartSpace': (1, 1),
                   'LED_ON': (1, 2),
                   'LED_OFF': (1, 3),
                   '10.254.254.64': (1, 4),
                   'ChristianPi': (2, 0),
                   'Modestine': (2, 1),
                   'Alarm': (2, 2),
                   'LightSensor': (2, 3),
                   '192.168.1.149': (2, 4),
                   '()': (3, 0),
                   '0':(3,1),
                   '1':(3,2),
                   '\n':(3,3),
                   '=': (3, 4),
                  }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(200, 50)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)
        
    def setDisplayText(self, text):
        """Set display's text."""
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
            """Get display's text."""
            return self.display.text()

    def clearDisplay(self):
            """Clear the display."""
            self.setDisplayText('')
# Client code
ERROR_MSG = 'ERROR'
def evaluateExpression(expression,outputFile):
    """Evaluate an expression."""
    newApp = open(outputFile, 'w')
    newApp.write(expression)
    newApp.close()
    result = outputFile

    return result
def main():
    """Main function."""
    # Create an instance of QApplication
    outputFile = "application.txt"
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = PyCalcUi()
    view.show()
    # Create instances of the model and the controller
    model = evaluateExpression
    PyCalcCtrl(model=model, view=view,outputFile = outputFile)
    # Execute calculator's main loop
    sys.exit(pycalc.exec_())

if __name__ == '__main__':
    main()