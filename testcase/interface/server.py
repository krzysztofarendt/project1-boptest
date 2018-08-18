# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 18:12:56 2018

@author: dhb-lx
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 17:55:25 2018

@author: dhb-lx
"""

import socket


class socket_server(object):

    def __init__(self):
        self.sock=socket.socket()
        port=8888
        host='127.0.0.1'
        self.sock.bind((host, port))
        print(self.sock.getsockname())
        self.sock.listen(10)
        self.y_list = ['TZone']
        self.u_list = ['QHeat']
    
    def send_control(self,u):
        '''Send control signals to model.
        
        Parameters
        ----------
        u : dict
            Defines the control input data to be used for the step.
            {<input_name> : <input_value>}
             
        '''
        
        conn,addr = self.sock.accept()
        # Set control inputs if they exist
        if u.keys():
            u_list = []
            for key in u.keys():
                if key in self.u_list:
                    value = str(u[key])
                    print('value: {0}'.format(value))
#                    u_list.append(key)
                    u_list.append(value)
            u_message = ','.join(u_list)
        else:
            u_message = ''
        # Send to socket connection
        conn.send(u_message)
        print('Sent {0}'.format(u_message))
        
    def receive_measurements(self):
        '''Get sensor signals from model.

        Returns
        -------
        y : dict
            Contains the measurement data at the end of the step.
            {<measurement_name> : <measurement_value>}
        
        '''

        conn,addr = self.sock.accept()
        # Get data
        data = conn.recv(1024).split(',')
        # Create measurement dictionary
        y = dict()
        # Parse data into dictionary
        key_index = [x for x in range(len(data)) if x % 2 == 0]
        for i in key_index[:-1]:
            key = data[i]
            if key in self.y_list:
                value = data[i+1]
                y[key] = value
            
            print('Received {0}'.format(y))
            
            return y
        
# INITIALIZE SERVER
# -----------------
print('Initializing Socket Server')
socket_connection = socket_server()
while 1:
    y = socket_connection.receive_measurements()
    u = {'QHeat':60}
    socket_connection.send_control(u)