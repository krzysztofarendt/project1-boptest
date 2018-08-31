# -*- coding: utf-8 -*-
"""
This module implements a simple P controller.

"""

class controller(object):
    
    def __init__(self):
        '''Constructor.
        
        '''
        
        self.init_value = 0
        
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
        
        # Controller parameters
        setpoint = 273.15+20
        k_p = 2000
        # Compute control
        e = setpoint - y['TZone']['value']
        value = max(k_p*e,0)
        u = {'QHeat':{'value':value,'unit':'W'}}
        
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
        
        value = self.init_value
        u = {'QHeat':{'value':value,'unit':'W'}}
        
        return u
