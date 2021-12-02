from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 100, 1500, 800)
        self.setWindowTitle("Term Project")
        self.initUI()
    
    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Project Homescreen")
        self.label.move(50, 50)

        self.thingsTab = QtWidgets.QPushButton(self)
        self.thingsTab.setText("Things")
        self.thingsTab.clicked.connect(self.clickedThings)

        self.servicesTab = QtWidgets.QPushButton(self)
        self.servicesTab.setText("Services")
        self.servicesTab.clicked.connect(self.clickedServices)

    def clickedThings(self):
        self.label.setText("Things tab page")
        self.update()

    def clickedServices(self):
        self.label.setText("Services tab page")
        self.update()

    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()