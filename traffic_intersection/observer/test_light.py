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


def fsm_light(h_light, v_light):
    c = Digraph('G', format = 'png')
    c.attr(rankdir='TB',dpi = '300',layout = 'circo',size='1.5,1.5!')
    #c.graph_attr.update(rank='min')
    c.attr('node', shape='circle', width='0.1', fontsize ='15.0')
    c.attr('edge', arrowsize = '0.5', fontsize ='12.0')
    c.edge('gr', 'yr', label='t_light >= 25') 
    c.edge('yr', 'rr', label='t_light >= 5')
    c.edge('rr', 'rg', label='t_light >= 0.1') 
    c.edge('rg', 'ry', label='t_light >= 25',fontcolor = '#006400',color='#006400')
    c.edge('ry', 'gr', label='t_light >= 5') 
    
    c.node(h_light+v_light, style='filled', color='grey')
    c.render('imglib/light', view=False, cleanup=True)
            
    
def monitor_light(h_light, v_light):
    fsm_light( h_light, v_light)
    state = dir_path + '/imglib/light.png'
    return Image.open(state)



