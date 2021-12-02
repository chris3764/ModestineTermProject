# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 15:10:44 2021

@author: cjwal
"""

import socket
import json
import sys

inputName = "newerApp.txt"

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
                    newSocket.connect((dataValues[13], 6668))
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
                
runApp(inputName)
