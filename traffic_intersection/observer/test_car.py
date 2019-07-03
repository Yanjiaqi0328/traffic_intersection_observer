#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:38:04 2019

@author: yanjiaqi
"""

import sys
sys.path.append('..')
import os
from PIL import Image
from graphviz import Digraph
import matplotlib.pyplot as plt
import time
dir_path = os.path.dirname(os.path.realpath(__file__))


def fsm_vehicles(vehicle_state):
    c = Digraph('G', format = 'png')
    c.attr(rankdir='LR',dpi = '300',size='2.2,0.6!')
    
    c.attr('node', shape='circle', width='0.08', fontsize ='10.0')
    c.attr('edge', arrowsize = '0.5', fontsize ='10.0')
    c.edge('0', '1', label='"safe"') 
    c.edge('1', '0', label='"unsafe"',fontcolor = '#006400',color='#006400')
    c.edge('0', '0')
    c.edge('1', '1')
    
    c.node(str(vehicle_state), style='filled', color='grey')
   
    c.render('imglib/car', view=False, cleanup=True)
            
    
def monitor_vehicles(pedestrian_state):
    fsm_vehicles(pedestrian_state)
    state = dir_path + '/imglib/car.png'
    return Image.open(state)



