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


def fsm_vehicles(last_vehicle_state, current_vehicle_state):
    fillcolor = '#006400'
    edgecolor = {'00':'black', '01': 'black', '10':'black', '11':'black'}
    c = Digraph('G', format = 'png')
    c.attr(rankdir='LR',dpi = '300',size='2.2,0.6!')
    
    c.attr('node', shape='circle', width='0.08', fontsize ='10.0')
    if current_vehicle_state in (0,1):
        c.node(str(current_vehicle_state), style='filled', color='grey')
        if last_vehicle_state in (0,1):
            edgecolor[str(last_vehicle_state)+str(current_vehicle_state)] = fillcolor 
    c.attr('edge', arrowsize = '0.5', fontsize ='10.0')
    c.edge('0', '1', label='"safe"', fontcolor = edgecolor['01'], color = edgecolor['01']) 
    c.edge('1', '0', label='"unsafe"', fontcolor = edgecolor['10'], color = edgecolor['10'])
    c.edge('0', '0', fontcolor = edgecolor['00'], color = edgecolor['00'])
    c.edge('1', '1', fontcolor = edgecolor['11'], color = edgecolor['11'])
                   
    c.render('imglib/car', view=False, cleanup=True)
            
    
def monitor_vehicles(last_vehicle_state, current_vehicle_state):
    fsm_vehicles(last_vehicle_state, current_vehicle_state)
    state = dir_path + '/imglib/car.png'
    return Image.open(state)



