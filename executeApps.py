# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 15:10:44 2021

@author: cjwal
"""

import socket
import json
import sys

inputName = "application.txt"

inputFile = open(inputName,"r")
myApp = inputFile.readlines()
inputFile.close()

for line in myApp:
    dataValues = line.split(';')
    if(dataValues[0]=='R'):
        if dataValues.len()<14:
            print("error invalid file input")
        else:
            data = {
                "Tweet Type": dataValues[1],
                "Thing ID": dataValues[2],
                "Space ID": dataValues[3],
                "Service Name": dataValues[4],
                "Service Inputs"dataValues[5]: 
                    }
                data_json = json.dumps(data)
    
            try:
            # Create a client socket
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            except clientSocket.error as err:
                print("Socket error idk")
    
        # Connect to the Jerry's Pi
            clientSocket.connect((dataValues[6], 6668));
            clientSocket.send(bytes(data_json, encoding="utf-8"));
    
        # Receive data from server
            dataFromServer = clientSocket.recv(1024);
    
        # Print to received data to console
            if(dataFromServer.decode() == dataValues[7]):
                data = {
                    "Tweet Type": dataValues[8],
                    "Thing ID": dataValues[9],
                    "Space ID": dataValues[10],
                    "Service Name": dataValues[11],
                    "Service Inputs"dataValues[12]: 
                        }
                data_json = json.dumps(data)
        
        
            # Connect to the Jerry's Pi
                clientSocket.connect((dataValues[13], 6668));
                clientSocket.send(bytes(data_json, encoding="utf-8"));
        
            # Receive data from server
                dataFromServer = clientSocket.recv(1024);
        
            # Print to received data to console
            else:
                print("The other service does not activate")
            clientSocket.close()          
    else:
        if dataValues.len()<6:
            print("error invalid file input")
        else:
            data = {
                "Tweet Type": dataValues[0],
                "Thing ID": dataValues[1],
                "Space ID": dataValues[2],
                "Service Name": dataValues[3],
                "Service Inputs"dataValues[4]: 
                    }
                data_json = json.dumps(data)
    
            try:
            # Create a client socket
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
            except clientSocket.error as err:
                print("Socket error idk")
    
        # Connect to the Jerry's Pi
            clientSocket.connect((dataValues[5], 6668));
            clientSocket.send(bytes(data_json, encoding="utf-8"));
    
        # Receive data from server
            dataFromServer = clientSocket.recv(1024);
    
        # Print to received data to console
            print(dataFromServer.decode());
    
            clientSocket.close()
