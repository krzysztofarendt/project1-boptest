# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 18:12:56 2018

@author: dhb-lx
"""

import socket
import json
import pid
import supervisory


class socket_server(object):

    def __init__(self, demo):
        self.sock=socket.socket()
        port=8888
        host='127.0.0.1'
        self.sock.bind((host, port))
        print(self.sock.getsockname())
        self.sock.listen(10)
        self.y_list = ['TZone']
        if demo is 'actuator':
            self.u_list = ['QHeat']
            self.controller = pid.controller()
        elif demo is 'setpoint':
            self.u_list = ['SetHeat']
            self.controller = supervisory.controller()
        else:
            raise ValueError('Unknown demo type {0}.'.format(demo))
        self.u = self.controller.initialize()
    
    def send_control(self,u):
        '''Send control signals to model.
        
        Parameters
        ----------
        u : dict
            Defines the control input data to be used for the step.
            {<input_name> : <input_value>}
             
        '''
        
        # Create message
        msg = json.dumps(u)
        print('Sent:\n{0}'.format(u))
        # Send to socket connection
        self.conn.send(msg)

        
    def receive_measurements(self):
        '''Get sensor signals from model.

        Returns
        -------
        y : dict
            Contains the measurement data at the end of the step.
            {<measurement_name> : <measurement_value>}
        
        '''

        # Accept connection
        self.conn,addr = self.sock.accept()
        # Get data
        data = self.conn.recv(1024)
        # Load json
        y = json.loads(data)
        print('Received:\n{0}'.format(y))

        return y
        
    def get_control(self,y):
        '''Get control signal from a controller.
        
        Parameters
        ----------
        y : dict
            Contains the measurement data at the end of the step.
            {<measurement_name> : <measurement_value>}
        

        Returns
        -------
        u : dict
            Defines the control input data to be used for the step.
            {<input_name> : <input_value>}
        
        '''
        
        # Check if socket is sensor
        if 'TZone' in y.keys():
            # Compute new control
            u = self.controller.compute_control(y)
            self.u = u
        else:
            # Keep same control
            u = self.u
        
        return u
        

        
        
# INITIALIZE SERVER
# -----------------
demo = 'setpoint'

print('Initializing Socket Server for {0}...'.format(demo))
socket_connection = socket_server(demo)
while 1:
    y = socket_connection.receive_measurements()
    u = socket_connection.get_control(y)
    socket_connection.send_control(u)