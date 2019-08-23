#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in Jul 2019

@author: Jiaqi Yan and Josefine Graebener
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
    edgecolor = {'00':'black', '01': 'black', '10':'black', '02':'black', '22':'black', '23':'black', '34':'black', '44':'black', '45': 'black', '55':'black', '56':'black', '35':'black', '66':'black', '65':'black'}
    c = Digraph('G', format = 'png')
    c.attr(rankdir='LR',dpi = '500',size='8,5')
    
    if expection:
        c.attr('node', shape='doublecircle', width='0.2', fontsize ='15.0')
        c.node('x',style='filled', color='red')
    else:
        c.attr('node', shape='circle', width='0.1', fontsize ='30.0')
        c.node('0', label='Approach')
        c.node('1', label='Stop') # stop before reaching the signal
        c.node('2', label='Signal') # at the signal
        c.node('3', label='Intersection') # on the intersection
        c.node('4', label='Stop') # Stop in the intersection
        c.node('5', label='Leave') # leaving the intersection
        c.node('6', label='Stop') # Stop while leaving 
        if current_vehicle_state in (0,1,2,3,4,5,6):
            c.node(str(current_vehicle_state), style='filled', color=fillcolor)
            if last_vehicle_state in (0,1,2,3,4,5,6):
                edgecolor[str(last_vehicle_state)+str(current_vehicle_state)] = fillcolor 
        c.attr('edge', arrowsize = '1', fontsize ='20.0')
        c.edge('0', '1', label='"!clear"', fontcolor = edgecolor['01'], color = edgecolor['01']) 
        c.edge('1', '0', label='"clear"', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('0', '2', label='"clear"', fontcolor = edgecolor['02'], color = edgecolor['02'])
        c.edge('2', '2', label='"red || !clear"', fontcolor = edgecolor['22'], color = edgecolor['22'])
        c.edge('2','3', label='"!red && clear"', fontcolor = edgecolor['23'], color = edgecolor['23'])
        c.edge('3', '4', label='"!clear"', fontcolor = edgecolor['34'], color = edgecolor['34'])
        c.edge('4','4', label='"!clear"', fontcolor = edgecolor['44'], color = edgecolor['44'])
        c.edge('4','5', label='"clear"', fontcolor = edgecolor['45'], color = edgecolor['45'])
        c.edge('5','5', label='"clear"', fontcolor = edgecolor['55'], color = edgecolor['55'])
        c.edge('5','6', label='"!clear"', fontcolor = edgecolor['56'], color = edgecolor['56'])
        c.edge('3','5', label='"clear"', fontcolor = edgecolor['35'], color = edgecolor['35'])
        c.edge('6','6', label='"!clear"', fontcolor = edgecolor['66'], color = edgecolor['66'])
        c.edge('6','5', label='"clear"', fontcolor = edgecolor['65'], color = edgecolor['65'])
                       
    c.render('imglib/car', view=False, cleanup=True)
            
    
def monitor_vehicles(last_vehicle_state, current_vehicle_state, expection):
    fsm_vehicles(last_vehicle_state, current_vehicle_state, expection)
    state = dir_path + '/imglib/car.png'
    return Image.open(state)

