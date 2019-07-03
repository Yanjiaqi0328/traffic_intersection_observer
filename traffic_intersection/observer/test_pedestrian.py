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

def fsm_pedestrians(pedestrian_state):
    c = Digraph('G', format = 'png')
    c.attr(rankdir='LR',dpi = '200',size='2.2,0.6!')
    
    c.attr('node', shape='circle', width='0.1', fontsize ='15.0')
    c.attr('edge', arrowsize = '0.5', fontsize ='16.0')
    c.edge('0', '1', label='light == g') 
    c.edge('1', '0', label='(light != g)|| (t_cross >= t_w)')
    c.edge('0', '0')
    c.edge('1', '1')
    if pedestrian_state in (0,1):
        c.node(str(pedestrian_state), style='filled', color='grey')
   
    c.render('imglib/pedestrian', view=False, cleanup=True)
            
    
def monitor_pedestrians(pedestrian_state):
    fsm_pedestrians(pedestrian_state)
    state = dir_path + '/imglib/pedestrian.png'
    return Image.open(state)




