#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 19:10:40 2019

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


def fsm_pedestrians(h_cross, v_cross, h_walk, v_walk, h_light, v_light, pedestrian_state):
    c = Digraph('G', format = 'png')
    c.attr(rankdir='TB',dpi = '180')
    
    # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
    #       so that Graphviz recognizes it as a special cluster subgraph   
    if pedestrian_state == -1:
        c.attr('node', shape='circle', width='0.1', fontsize ='10.0')
        c.attr('edge', arrowsize = '0.5', fontsize ='10.0')
        c.edge('0g0r', '1g0r', label='3 <= h_t_light <= 9.4')
        c.edge('1g0r', '0g0r', label='h_t_light > 9.4')
        c.edge('0g0r', '0y0r', label='h_t_light >= 25')
        c.edge('0y0r', '0r0r', label='h_t_light >= 5')
        c.edge('0r0r', '0r0g', label='h_t_light >= 0.1')
        c.edge('0r0g', '0r1g', label='3 <= v_t_light <= 9.4')
        c.edge('0r1g', '0r0g', label='v_t_light > 9.4')
        c.edge('0r0g', '0r0y', label='v_t_light >= 25')
        c.edge('0r0y', '0g0r', label='h_t_light >= 30')
        
        c.node(str(h_walk)+h_light+str(v_walk)+v_light, style='filled', color='grey')
        c.attr(label='h_walk \u2297 h_light \u2297 v_walk \u2297 v_light', fontsize ='10.0')
        c.attr(color='lightgrey')
          
        c.attr(color='black') 
        c.attr(size = '8,5!')
    else:    
        c.attr('node', shape='circle', width='0.05', fontsize ='20.0')
        c.attr('edge', arrowsize = '0.5', fontsize ='22.0')
        c.edge('10g0r', '11g0r', label='3 <= h_t_l <= 9.4')
        c.edge('11g0r', '10g0r', label='h_t_l > 9.4')
        c.edge('10g0r', '10y0r', label='h_t_l >= 25')
        c.edge('10y0r', '10r0r', label='h_t_l >= 5')
        c.edge('10r0r', '10r0g', label='h_t_l >= 0.1')
        c.edge('10r0g', '10r1g', label='3 <= v_t_l <= 9.4')
        c.edge('10r1g', '10r0g', label='v_t_l > 9.4')
        c.edge('10r0g', '10r0y', label='v_t_l >= 25')
        c.edge('10r0y', '10g0r', label='h_t_l >= 30', len ='0.1')
        
        
        c.edge('10g0r', '00g0r', label='h_cross == 1 || v_cross == 1')
        c.edge('10y0r', '00y0r', label='h_cross == 1 || v_cross == 1')
        c.edge('10r0r', '00r0r', label='h_cross == 1 || v_cross == 1')
        c.edge('10r0g', '00r0g', label='h_cross == 1 || v_cross == 1')
        c.edge('10r0y', '00r0y', label='h_cross == 1 || v_cross == 1')
        c.edge('11g0r', '01g0r', label='(h_cross == 1 && h_t_walk > h_t_sign) || v_cross == 1')
        c.edge('10r1g', '00r1g', label='h_cross == 1 || (v_cross == 1 && v_t_walk > v_t_sign)')
        c.edge('00g0r', '11g0r', label='h_cross == 1 && 3 <= h_t_l <= 9.4')
        c.edge('00r0g', '10r1g', label='v_cross == 1 && 3 <= v_t_l <= 9.4')
        
        c.edge('00g0r', '01g0r', label='3 <= h_t_l <= 9.4')
        c.edge('01g0r', '00g0r', label='h_t_l > 9.4')
        c.edge('00g0r', '00y0r', label='h_t_l >= 25')
        c.edge('00y0r', '00r0r', label='h_t_l >= 5')
        c.edge('00r0r', '00r0g', label='h_t_l >= 0.1')
        c.edge('00r0g', '00r1g', label='3 <= v_t_l <= 9.4')
        c.edge('00r1g', '00r0g', label='v_t_l > 9.4')
        c.edge('00r0g', '00r0y', label='v_t_l>= 25')
        c.edge('00r0y', '00g0r', label='h_t_l >= 30')
        
        
        c.node(str(pedestrian_state)+str(h_walk)+h_light+str(v_walk)+v_light, style='filled', color='grey')
        c.attr(label='pedestrian \u2297 h_walk \u2297 h_light \u2297 v_walk \u2297 v_light', fontsize ='30.0')
        c.attr(size = '8,5!')
    c.render('imglib/pedestrian_and_sign_and_light/state', view=False, cleanup=True)
            
    
def monitor_pedestrians(h_cross, v_cross, h_walk, v_walk, h_light, v_light, pedestrian_state=0):
    fsm_pedestrians(h_cross, v_cross, h_walk, v_walk, h_light, v_light, pedestrian_state)
    state = dir_path + '/imglib/pedestrian_and_sign_and_light/state.png'
    return Image.open(state)


#monitor_pedestrians(0, 0, 1, 0, 'g', 'r', 1).show()

