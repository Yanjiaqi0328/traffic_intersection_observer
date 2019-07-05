#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 15:08:13 2019

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

def fsm_light(last_h_light, last_v_light, current_h_light, current_v_light):
    fillcolor = '#00A000'
    edgecolor = {'gryr':'black', 'yrrr': 'black', 'rrrg':'black', 'rgry':'black', 'rygr':'black'}
    c = Digraph('G', format = 'png')
    c.attr(rankdir='TB',dpi = '300',layout = 'circo',size='1.5,1.5!')
    
    if [last_h_light, last_v_light] != [-1,-1]:
        edgecolor[last_h_light+last_v_light+current_h_light+current_v_light] = fillcolor
    
    c.attr('node', shape='circle', width='0.1', fontsize ='15.0')
    c.attr('edge', arrowsize = '0.5', fontsize ='12.0')
    c.edge('gr', 'yr', label='t_light >= 25', fontcolor = edgecolor['gryr'], color = edgecolor['gryr']) 
    c.edge('yr', 'rr', label='t_light >= 5', fontcolor = edgecolor['yrrr'], color = edgecolor['yrrr'])
    c.edge('rr', 'rg', label='t_light >= 0.1', fontcolor = edgecolor['rrrg'], color = edgecolor['rrrg']) 
    c.edge('rg', 'ry', label='t_light >= 25', fontcolor = edgecolor['rgry'], color = edgecolor['rgry'])
    c.edge('ry', 'gr', label='t_light >= 5', fontcolor = edgecolor['rygr'], color = edgecolor['rygr']) 
    
    c.node(current_h_light + current_v_light, style='filled', color=fillcolor)
    c.render('imglib/light', view=False, cleanup=True)
            
    
def monitor_light(last_h_light, last_v_light, current_h_light, current_v_light):
    fsm_light(last_h_light, last_v_light, current_h_light, current_v_light)
    state = dir_path + '/imglib/light.png'
    return Image.open(state)



