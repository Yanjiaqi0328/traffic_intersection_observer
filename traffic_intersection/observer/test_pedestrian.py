#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 13:36:06 2019

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

def fsm_pedestrians(last_pedestrian_state, current_pedestrian_state, expection=False):
    fillcolor = '#008000'
    edgecolor = {'00':'black', '01': 'black', '10':'black', '11':'black'}
    c = Digraph('G', format = 'png')
    c.attr(rankdir='LR',dpi = '200',size='2.2,0.6!')
    
    if expection:
        c.node(' ', shape='plaintext', width='0.5', fontsize ='15.0')
        c.attr('node', shape='doublecircle', width='0.1', fontsize ='15.0')
        c.node('x',style='filled', color='red')
        c.edge(' ', 'x', style='invis')
    else:
        c.attr('node', shape='circle', width='0.1', fontsize ='15.0')
        c.node('0')
        c.node('1')
        if current_pedestrian_state in (0,1):
            c.node(str(current_pedestrian_state), style='filled', color=fillcolor)
            if last_pedestrian_state in (0,1):
                edgecolor[str(last_pedestrian_state)+str(current_pedestrian_state)] = fillcolor
        c.attr('edge', arrowsize = '0.5', fontsize ='16.0')
        c.edge('0', '1', label='light == g', fontcolor = edgecolor['01'], color = edgecolor['01']) 
        c.edge('1', '0', label='(light != g)|| (t_cross >= t_w)', fontcolor = edgecolor['10'], color = edgecolor['10'])
        c.edge('0', '0', fontcolor = edgecolor['00'], color = edgecolor['00'])
        c.edge('1', '1', fontcolor = edgecolor['11'], color = edgecolor['11'])
    c.render('imglib/pedestrian', view=False, cleanup=True)
            
    
def monitor_pedestrians(last_pedestrian_state, current_pedestrian_state, expection):
    fsm_pedestrians(last_pedestrian_state, current_pedestrian_state, expection)
    state = dir_path + '/imglib/pedestrian.png'
    return Image.open(state)




