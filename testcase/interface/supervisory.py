# -*- coding: utf-8 -*-
"""
This module implements a simple P controller.

"""

class controller(object):
    
    def __init__(self):
        '''Constructor.
        
        '''
        
        self.change = True
        self.init_value = 20+273.15
        
    def compute_control(self,y):
        '''Compute the control input from the measurement.
        
        Parameters
        ----------
        y : dict
            Contains the current values of the measurements.
            {<measurement_name>:<measurement_value>}
            
        Returns
        -------
        u : dict
            Defines the control input to be used for the next step.
            {<input_name> : <input_value>}
        
        '''
        
        # Compute control
        T = y['TZone']['value']
        if T >= 300 and self.change:
            self.change = False
            self.value = 300

        u = {'SetHeat':{'value':self.value,'unit':'K'}}
        
        return u
        
    def initialize(self):
        '''Initialize the control input u.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        u : dict
            Defines the control input to be used for the next step.
            {<input_name> : <input_value>}
        
        '''
        
        self.value = self.init_value
        u = {'SetHeat':{'value':self.value,'unit':'K'}}
        
        return u
