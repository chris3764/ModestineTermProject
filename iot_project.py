import sys
import socket
import struct
import json
import os

from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton
)

"""
Make the app a button
status of the app
add app (include a box they can type in and then a button to add)
remove + delete the app/txt file from the listing
"""


class Window(QWidget):
    def __init__(self,model):
        super().__init__()
        self.setWindowTitle("Smart Space")
        self._recipe = model
        self.resize(720, 720)
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.thingsTabUI(), "Things")
        tabs.addTab(self.servicesTabUI(), "Services")
        tabs.addTab(self.relationshipsTabUI(), "Relationships")
        tabs.addTab(self.recipeTabUI(), "Recipe")
        tabs.addTab(self.appTabUI(), "Apps")
        layout.addWidget(tabs)

        

    def thingsTabUI(self):
        """Create the Things page UI."""
        thingsTab = QWidget()
        #Window.checkSmartSpace()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("things Option 1"))
        layout.addWidget(QCheckBox("things Option 2"))
        layout.addStretch()
        thingsTab.setLayout(layout)
        return thingsTab

    def servicesTabUI(self):
        """Create the Services page UI."""
        servicesTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("services Option 1"))
        layout.addWidget(QCheckBox("services Option 2"))
        layout.addStretch()
        servicesTab.setLayout(layout)

        return servicesTab

    def relationshipsTabUI(self):
        """Create the Relationships page UI."""
        relationship = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Option 1"))
        layout.addWidget(QCheckBox("OPtion 2"))
        layout.addStretch()
        relationship.setLayout(layout)
        return relationship

    def recipeTabUI(self):
        """Create the Recipe page UI."""
        recipeTab = QWidget()
        layout = QVBoxLayout()
        myButton = QPushButton("new")
        myButton.clicked.connect(self._recipe)
        layout.addWidget(QCheckBox("recipe Option 1"))
        layout.addWidget(QLineEdit("recipe Option 2"))
        layout.addWidget(myButton)
        layout.addStretch()
        recipeTab.setLayout(layout)
        return recipeTab

    def appTabUI(self):
        """Create the App page UI."""
        appTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("app Option 1"))
        layout.addWidget(QCheckBox("app Option 2"))
        layout.addStretch()
        appTab.setLayout(layout)
        return appTab

    def checkSmartSpace():
        #Socket needs to be open in UDP
        print("Checking")
        multicast_group = "232.1.1.1"
        server_address = ("", 1235)
        MCAST_PORT = 1235
        IS_ALL_GROUPS = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if IS_ALL_GROUPS:
            # on this port, receives ALL multicast groups
            sock.bind(('', MCAST_PORT))
        else:
            # on this port, listen ONLY to MCAST_GRP
            sock.bind((multicast_group, MCAST_PORT))
        mreq = struct.pack("4sl", socket.inet_aton(multicast_group), socket.INADDR_ANY)

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True: 
            print(sock.recv(10240))
def newRecipe():
    os.system('python RecipeTab.py')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = newRecipe
    window = Window(model = model)
    window.show()
    sys.exit(app.exec_())