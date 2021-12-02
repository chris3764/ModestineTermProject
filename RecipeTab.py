# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 10:00:02 2021

@author: cjwal
"""

import sys
import json
import socket

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
    def __init__(self, model, view,outputFile,upload,run):
        """Controller initializer."""
        self._evaluate = model
        self._view = view
        # Connect signals and slots
        self._upload = upload
        self._run = run
        self._connectSignals()
       
        self._outputFile = outputFile
    def _calculateResult(self):
        """Evaluate expressions."""
        result = self._evaluate(expression=self._view.displayText(),outputFile = self._view.inputBox.text())
        self._view.setDisplayText(result)
    def _uploadApp(self):
        result = self._upload(self._view.inputBox.text())
        self._view.setDisplayText(result)
    def _runTheApp(self):
        self._run(self._view.inputBox.text())
    def _buildExpression(self, sub_exp):
        """Build expression."""
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()
        addedOut = sub_exp
        if sub_exp == 'LED_ON':
            addedOut = 'Service call;JRPI;JerrySmartSpace;LED_ON;();10.254.254.64'
        elif sub_exp == 'LED_OFF':
            addedOut = 'Service call;JRPI;JerrySmartSpace;LED_OFF;();10.254.254.64'
        elif sub_exp =='Alarm':
            addedOut = 'Service call;ChristianPi;Modestine;Alarm;();172.20.10.4'
        elif sub_exp =='LightSensor': 
            addedOut = 'Service call;ChristianPi;Modestine;LightSensor;();172.20.10.4'
        else:
            addedOut = sub_exp
        
        expression = self._view.displayText() + addedOut
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        """Connect signals and slots."""
        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C','Upload','Activate App'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['Finalize'].clicked.connect(self._calculateResult)
        self._view.buttons['Upload'].clicked.connect(self._uploadApp)
        self._view.buttons['Activate App'].clicked.connect(self._runTheApp)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
# Create a subclass of QMainWindow to setup the calculator's GUI
class PyCalcUi(QMainWindow):
    """PyCalc's View (GUI)."""
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Recipe/Application Manager')
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
                   'C': (0, 3),
                   'LED_ON': (1, 0),
                   'LED_OFF': (1, 1),
                   'Alarm': (1, 2),
                   'LightSensor': (1, 3),
                   'Activate App': (2, 2),
                   'Upload': (2, 3),
                   '0':(2,0),
                   '1':(2,1),
                   '\n':(3,2),
                   'Finalize': (3, 3),
                  }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(200, 50)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
            self.inputBox = QLineEdit("FileName Box")
            self.inputBox.setFixedSize(200,50)
            buttonsLayout.addWidget(self.inputBox,3,0)
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
def uploadFile(inputFile):
    curApp = open(inputFile,'r')
    myLines = curApp.readlines()
    curApp.close()
    uploadApp = ''
    for line in myLines:
        uploadApp += line
    return uploadApp
def runApp(inputName):
    inputFile = open(inputName,"r")
    myApp = inputFile.readlines()
    inputFile.close()
    
    for line in myApp:
        dataValues = line.split(';')
        for val in dataValues:
            print(val)
        if(dataValues[0]=='R'):
            if len(dataValues)<14:
                print("error invalid file input")
            else:
                data = {
                    "Tweet Type": dataValues[1],
                    "Thing ID": dataValues[2],
                    "Space ID": dataValues[3],
                    "Service Name": dataValues[4],
                    "Service Inputs":dataValues[5] 
                        }
                print(data)
                data_json = json.dumps(data)
        
                try:
                # Create a client socket
                    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                except mySocket.error as err:
                    print("Socket error idk")
        
                ip = '172.20.10.4'
                mySocket.connect((dataValues[6], 6668))
                mySocket.send(bytes(data_json, encoding="utf-8"))
                
            # Receive data from server
                dataFromServer = mySocket.recv(1024)
                mySocket.close()
                response = dataFromServer.decode()
                response = response[-4:-3]
            # Print to received data to console
                if(response == dataValues[7]):
                    
                    data = {
                        "Tweet Type": dataValues[8],
                        "Thing ID": dataValues[9],
                        "Space ID": dataValues[10],
                        "Service Name": dataValues[11],
                        "Service Inputs":dataValues[12] 
                            }
                    data_json = json.dumps(data)
            
            
                # Connect to the Jerry's Pi
                    try:
                # Create a client socket
                        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                    except newSocket.error as err:
                        print("Socket error idk")
                    newSocket.connect((dataValues[13][:-1], 6668))
                    newSocket.send(bytes(data_json, encoding="utf-8"))
            
                # Receive data from server
                    dataFromServer = newSocket.recv(1024)
            
                # Print to received data to console
                else:
                    print("The other service does not activate")
                newSocket.close()          
        else:
            if len(dataValues)<6:
                print("error invalid file input")
            else:
                data = {
                    "Tweet Type": dataValues[0],
                    "Thing ID": dataValues[1],
                    "Space ID": dataValues[2],
                    "Service Name": dataValues[3],
                    "Service Inputs":dataValues[4] 
                        }
                data_json = json.dumps(data)
        
                try:
                # Create a client socket
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                except clientSocket.error as err:
                    print("Socket error idk")
        
            # Connect to the Jerry's Pi
                ipAddress = dataValues[5][:-1]
                
                clientSocket.connect((dataValues[5][:-1], 6668));
                clientSocket.send(bytes(data_json, encoding="utf-8"));
        
            # Receive data from server
                dataFromServer = clientSocket.recv(1024);
        
            # Print to received data to console
                response = dataFromServer.decode()
                
                print(response[-4:-3]);
                
                clientSocket.close()
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
    uploadF = uploadFile
    runner = runApp
    PyCalcCtrl(model=model, view=view,outputFile = outputFile,upload=uploadF,run = runner)
    # Execute calculator's main loop
    sys.exit(pycalc.exec_())

if __name__ == '__main__':
    main()