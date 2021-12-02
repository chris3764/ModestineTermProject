import sys
import socket
import struct
import json
import os
from PyQt5 import QtCore
from PyQt5.QtGui import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Window(QWidget):
    def __init__(self, model, things):
        super().__init__()
        self.things = things
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
        outerLayout = QVBoxLayout()
        #outerLayout.addStretch()
        for t in self.things:
            thingsLayout = QVBoxLayout()
            thing = QLabel("Thing name: " + t['thing_id'])
            thing.setFont(QFont('Arial font', 15))
            #thing.setStyleSheet("border: 1px solid black;")
            thingsLayout.addWidget(thing)

            spaceID = QLabel("Space ID: " + t['space_id'])
            network = QLabel("Network: " + t['network_name'])
            ip = QLabel("IP: " + t['ip'])
            port = QLabel("Port: " + t['port'])
            servicesLabel = QLabel("Services:")
            services = QVBoxLayout()
            for s in t['services']:
                serv = QLabel(s)
                services.addWidget(serv)
            
            thingsInfo = QVBoxLayout()
            thingsInfo.addWidget(spaceID)
            thingsInfo.addWidget(network)
            thingsInfo.addWidget(ip)
            thingsInfo.addWidget(port)
            thingsInfo.addWidget(servicesLabel)
            thingsInfo.addLayout(services)
            
            thingsLayout.addLayout(thingsInfo)
            thingsLayout.addStretch()
            outerLayout.addLayout(thingsLayout)
        thingsTab.setLayout(outerLayout)

        return thingsTab

# thing1 = {
#         "thing_id": thing_id,
#         "space_id": space_id,
#         "network_name": network_name,
#         "ip": ip,
#         "port": port,
#         "services": [service1, service2]
#     }
    def servicesTabUI(self):
        """Create the Services page UI."""
        servicesTab = QWidget()
        layout = QVBoxLayout()
        #layout.addStretch()
        thingsL = []
        self.filterBox = QComboBox()

        for t in self.things:
            thingsL.append(t['thing_id'] + "'s services")
        thingsL.append("Shared Services")

        self.filterBox.addItems(thingsL)
        self.stackedLayout = QStackedLayout()
        self.filterBox.activated.connect(self.switchPage)

        for t in self.things:
            thing1 = QWidget()
            thing1Layout = QFormLayout()
            for s in t['services']:
                thing1Layout.addRow("Service ID: ", QLabel(s))
                #print('asdf')
            thing1.setLayout(thing1Layout)
            self.stackedLayout.addWidget(thing1)
        thing1 = QWidget()
        thing1Layout = QFormLayout()
        thing1Layout.addRow(QLabel("No shared Services"))
        thing1.setLayout(thing1Layout)
        self.stackedLayout.addWidget(thing1)

        layout.addWidget(self.filterBox)
        layout.addLayout(self.stackedLayout)
        servicesTab.setLayout(layout)

        return servicesTab
    
    def switchPage(self):
        self.stackedLayout.setCurrentIndex(self.filterBox.currentIndex())

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
        myButton = QPushButton("New Recipe")
        myButton.clicked.connect(self._recipe)
        layout.addWidget(myButton)
        layout.addStretch()
        recipeTab.setLayout(layout)
        return recipeTab

    def appTabUI(self):
        """Create the App page UI."""
        appTab = QWidget()
        layout = QVBoxLayout()
        file_list = os.listdir(os.getcwd())
        txt_str = ".txt"
        length = len(file_list)
        for i in range(length):
            if txt_str in file_list[i]:
                layout.addWidget(QPushButton(file_list[i]))
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

def parseTweets():
    #TODO: make cleaner
    with open('tweets/CTweets1.json') as f:
        json_data = json.load(f)
    thing_id = json_data[0]['Thing ID']
    space_id = json_data[0]['Space ID']
    network_name = json_data[1]['Network Name']
    ip = json_data[1]['IP']
    port = json_data[1]['Port']
    service1 = json_data[4]['Name']
    service2 = json_data[5]['Name']

    thing1 = {
        "thing_id": thing_id,
        "space_id": space_id,
        "network_name": network_name,
        "ip": ip,
        "port": port,
        "services": [service1, service2]
    }

    with open('tweets/JTweets1.json') as f:
        json_data = json.load(f)
    thing_id = json_data[0]['Thing ID']
    space_id = json_data[0]['Space ID']
    network_name = json_data[1]['Network Name']
    ip = json_data[1]['IP']
    port = json_data[1]['Port']
    service1 = json_data[3]['Name']
    service2 = json_data[4]['Name']

    thing2 = {
        "thing_id": thing_id,
        "space_id": space_id,
        "network_name": network_name,
        "ip": ip,
        "port": port,
        "services": [service1, service2]
    }
    return [thing1, thing2]

def newRecipe():
    os.system('python RecipeTab.py')


if __name__ == "__main__":
    things = parseTweets()
    app = QApplication(sys.argv)
    model = newRecipe
    window = Window(model = model, things = things)
    window.show()
    sys.exit(app.exec_())