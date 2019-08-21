#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in Jul 2019

@author: Jiaqi Yan (jiaqi@caltech.edu)
"""

import sys
sys.path.append('..')
import os
from PIL import Image
from graphviz import Digraph
import matplotlib.pyplot as plt
import time
dir_path = os.path.dirname(os.path.realpath(__file__))


def fsm_vehicles(last_vehicle_state, current_vehicle_state, expection=False):
    fillcolor = '#00A000'
    edgecolor = {'00':'black', '01': 'black', '10':'black', '11':'black'}
    c = Digraph('G', format = 'png')
    c.attr(rankdir='LR',dpi = '500',size='8,5')
    
    if expection:
        c.attr('node', shape='doublecircle', width='0.2', fontsize ='15.0')
        c.node('x',style='filled', color='red')
    else:
        c.attr('node', shape='circle', width='0.2', fontsize ='20.0')
        c.node('0', label='Approach')
        c.node('1', label='Stop') # stop at the signal
        c.node('2', label='Signal') # adding teststate
        c.node('3', label='Intersection')
        c.node('4', label='Stop') # Stop in the intersection
        c.node('5', label='Leave')
        c.node('6', label='Stop')
        if current_vehicle_state in (0,1):
            c.node(str(current_vehicle_state), style='filled', color=fillcolor)
            if last_vehicle_state in (0,1):
                edgecolor[str(last_vehicle_state)+str(current_vehicle_state)] = fillcolor 
        c.attr('edge', arrowsize = '1', fontsize ='10.0')
        c.edge('0', '1', label='"!clear"', fontcolor = edgecolor['01'], color = edgecolor['01']) 
        c.edge('1', '0', label='"clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('0', '2', label='"clear"', fontcolor = edgecolor['00'], color = edgecolor['00'])
        c.edge('2', '2', label='"red || !clear"', fontcolor = edgecolor['11'], color = edgecolor['11'])
        c.edge('2','3', label='"!red && clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('3', '4', label='"!clear"', fontcolor = edgecolor['11'], color = edgecolor['11'])
        c.edge('4','4', label='"!clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('4','5', label='"clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('5','5', label='"clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('5','6', label='"!clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('3','5', label='"clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('6','6', label='"!clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('6','5', label='"clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
                       
    c.render('imglib/car', view=False, cleanup=True)
            
    
def monitor_vehicles(last_vehicle_state, current_vehicle_state, expection):
    fsm_vehicles(last_vehicle_state, current_vehicle_state, expection)
    state = dir_path + '/imglib/car.png'
    return Image.open(state)

