#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 16:08:20 2019

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


def fsm_pedestrians(h_cross, v_cross, h_walk, v_walk, h_light, v_light, pedestrian_state=0):
    f = Digraph('G', format = 'png')
    f.attr(rankdir='LR')
    
    # NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
    #       so that Graphviz recognizes it as a special cluster subgraph
    if (h_cross == 0 and v_cross == 0):
        with f.subgraph(name='clusterA') as g:
            with g.subgraph(name='cluster_0') as c:                  
                c.node('1', shape='circle', width='0.1', fontsize ='10.0')
                c.attr('edge', arrowsize = '0.5', fontsize ='10.0')
                c.edge('1', '1')
                if pedestrian_state == 1:
                    c.node('1', style='filled', color='grey')
                c.attr(label='Pedestrian', fontsize ='9.0')
                c.attr(color='lightgrey')
                
            with g.subgraph(name='cluster_1') as c:
                c.attr('node', shape='circle', width='0.1', fontsize ='10.0')
                c.node('h0g', label = '0g')
                c.node('h0y', label = '0y')
                c.node('h0r', label = '0r')
                c.node('h1g', label = '1g')
                c.attr('edge', arrowsize = '0.5', fontsize ='15.0')
                c.edge('h0y', 'h0r', label='h_t_light >= 5')
                c.edge('h0r', 'h0g', label='h_t_light >= 30')
                c.edge('h0g', 'h0y', label='h_t_light >= 25')
                c.edge('h0g', 'h1g', label='3 <= h_t_light <= 9.4')
                c.edge('h1g', 'h0g', label='h_t_light > 9.4')
                c.edge('h0g', 'h0g', label='others')
                c.edge('h0r', 'h0r', label='others')
                c.edge('h0y', 'h0y', label='others')
                c.edge('h1g', 'h1g', label='others')
                c.node('h'+str(h_walk)+h_light, style='filled', color='grey')
                c.attr(label='h_walk \u2297 h_light', fontsize ='15.0')
                c.attr(color='lightgrey')
                
            with g.subgraph(name='cluster_2') as c:
                c.attr('node', shape='circle', width='0.1', fontsize ='10.0')  
                c.node('v0g', label = '0g')
                c.node('v0y', label = '0y')
                c.node('v0r', label = '0r')
                c.node('v1g', label = '1g')
                c.attr('edge', arrowsize = '0.5', fontsize ='15.0')
                c.edge('v0y', 'v0r', label='v_t_light >= 5')
                c.edge('v0r', 'v0g', label='v_t_light >= 30')
                c.edge('v0g', 'v0y', label='v_t_light >= 25')
                c.edge('v0g', 'v1g', label='3 <= v_t_light <= 9.4')
                c.edge('v1g', 'v0g', label='v_t_light > 9.4')
                c.edge('v0g', 'v0g', label='others')
                c.edge('v0r', 'v0r', label='others')
                c.edge('v0y', 'v0y', label='others')
                c.edge('v1g', 'v1g', label='others')
                c.node('v'+str(v_walk)+v_light, style='filled', color='grey')
                c.attr(label='v_walk \u2297 v_light', fontsize ='15.0')
                c.attr(color='lightgrey') 
        
            g.attr(color='black') 
            g.attr(label='h_cross == 0 && v_cross == 0')
            g.attr(fontsize='20')
            g.attr(size = '8,5!')
    
    
    elif h_cross == 1:        
        with f.subgraph(name='clusterB') as g: 
              
            with g.subgraph(name='cluster_1') as c:
                c.attr('node', shape='plaintext')
                c.node('toh00g', label = '')
                c.node('toh00r', label = '')
                c.node('toh00y', label = '')
                c.node('toh01g', label = '')
                c.node('toh11g', label = '')
                c.attr('node', shape='circle', width='0.1', fontsize ='15.0')
                c.node('h00g', label = '00g')
                c.node('h00r', label = '00r')
                c.node('h00y', label = '00y')
                c.node('h01g', label = '01g')
                c.node('h11g', label = '11g')
                c.attr('edge', arrowsize = '0.5', fontsize ='15.0', minlen = '1')
                c.edge('h00r', 'h00g', label='h_t_light >= 30')
                c.edge('h00g', 'h00y', label='h_t_light >= 25')
                c.edge('h00y', 'h00r', label='h_t_light >= 5')
                c.edge('h00g', 'h11g', label='3 <= h_t_light <= 9.4')
                c.edge('h01g', 'h00g', label='h_t_light > 9.4')
                c.edge('h00y', 'h00y', label='others')
                c.edge('h00r', 'h00r', label='others')
                c.edge('h00g', 'h00g', label='others')
                c.edge('h01g', 'h01g', label='others')
                c.edge('h11g', 'h11g')
                c.edge('toh00g', 'h00g', label = 'h_light = g && h_walk == 0')
                c.edge('toh00r', 'h00r', label = 'h_light = r')
                c.edge('toh00y', 'h00y', label = 'h_light = y')
                c.edge('toh01g', 'h01g', label = 'h_walk == 1 && t_cross > h_t_sign')
                c.edge('toh11g', 'h11g', label = 'h_walk == 1 && t_cross <= h_t_sign')
                c.node('h'+str(pedestrian_state)+str(h_walk)+h_light, style='filled', color='grey')
                c.attr(label='Pedestrian \u2297 h_walk \u2297 h_light', fontsize ='15.0')
                c.attr(color='lightgrey')
                
            with g.subgraph(name='cluster_2') as c:
                c.attr('node', shape='circle', width='0.1', fontsize ='15.0')  
                c.node('2v0g', label = '0g')
                c.node('2v0y', label = '0y')
                c.node('2v0r', label = '0r')
                c.node('2v1g', label = '1g')
                c.attr('edge', arrowsize = '0.5', fontsize ='15.0')
                c.edge('2v0y', '2v0r', label='v_t_light >= 5')
                c.edge('2v0r', '2v0g', label='v_t_light >= 30')
                c.edge('2v0g', '2v0y', label='v_t_light >= 25')
                c.edge('2v0g', '2v1g', label='3 <= v_t_light <= 9.4')
                c.edge('2v1g', '2v0g', label='v_t_light > 9.4')
                c.edge('2v0g', '2v0g', label='others')
                c.edge('2v0r', '2v0r', label='others')
                c.edge('2v0y', '2v0y', label='others')
                c.edge('2v1g', '2v1g', label='others')
                c.node('2v'+str(v_walk)+v_light, style='filled', color='grey')
                c.attr(label='v_walk \u2297 v_light', fontsize ='15.0')
                c.attr(color='lightgrey') 
                c.edge('h01g', '2v1g', style = 'invis')
            g.attr(color='black') 
            g.attr(label='h_cross == 1')
            g.attr(fontsize='20')
            g.attr(size = '8,5!')
            
    elif v_cross == 1:
        with f.subgraph(name='clusterC') as g: 
              
            with g.subgraph(name='cluster_1') as c:
                c.attr('node', shape='plaintext')
                c.node('tov00g', label = '')
                c.node('tov00r', label = '')
                c.node('tov00y', label = '')
                c.node('tov01g', label = '')
                c.node('tov11g', label = '')
                c.attr('node', shape='circle', width='0.1', fontsize ='15.0')
                c.node('v00g', label = '00g')
                c.node('v00r', label = '00r')
                c.node('v00y', label = '00y')
                c.node('v01g', label = '01g')
                c.node('v11g', label = '11g')
                c.attr('edge', arrowsize = '0.5', fontsize ='15.0', minlen = '1')
                c.edge('v00r', 'v00g', label='v_t_light >= 30')
                c.edge('v00g', 'v00y', label='v_t_light >= 25')
                c.edge('v00y', 'v00r', label='v_t_light >= 5')
                c.edge('v00g', 'v11g', label='3 <= v_t_light <= 9.4')
                c.edge('v01g', 'v00g', label='v_t_light > 9.4')
                c.edge('v00y', 'v00y', label='others')
                c.edge('v00r', 'v00r', label='others')
                c.edge('v00g', 'v00g', label='others')
                c.edge('v01g', 'v01g', label='others')
                c.edge('v11g', 'v11g')
                c.edge('tov00g', 'v00g', label = 'v_light = g && v_walk == 0')
                c.edge('tov00r', 'v00r', label = 'v_light = r')
                c.edge('tov00y', 'v00y', label = 'v_light = y')
                c.edge('tov01g', 'v01g', label = 'v_walk == 1 && t_cross > v_t_sign')
                c.edge('tov11g', 'v11g', label = 'v_walk == 1 && t_cross <= v_t_sign')
                c.node('v'+str(pedestrian_state)+str(v_walk)+v_light, style='filled', color='grey')
                c.attr(label='Pedestrian \u2297 v_walk \u2297 v_light', fontsize ='15.0')
                c.attr(color='lightgrey')
                
            with g.subgraph(name='cluster_2') as c:
                c.attr('node', shape='circle', width='0.1', fontsize ='15.0')  
                c.node('2h0g', label = '0g')
                c.node('2h0y', label = '0y')
                c.node('2h0r', label = '0r')
                c.node('2h1g', label = '1g')
                c.attr('edge', arrowsize = '0.5', fontsize ='15.0')
                c.edge('2h0y', '2h0r', label='h_t_light >= 5')
                c.edge('2h0r', '2h0g', label='h_t_light >= 30')
                c.edge('2h0g', '2h0y', label='h_t_light >= 25')
                c.edge('2h0g', '2h1g', label='3 <= h_t_light <= 9.4')
                c.edge('2h1g', '2h0g', label='h_t_light > 9.4')
                c.edge('2h0g', '2h0g', label='others')
                c.edge('2h0r', '2h0r', label='others')
                c.edge('2h0y', '2h0y', label='others')
                c.edge('2h1g', '2h1g', label='others')
                c.node('2h'+str(h_walk)+h_light, style='filled', color='grey')
                c.attr(label='h_walk \u2297 h_light', fontsize ='15.0')
                c.attr(color='lightgrey') 
                c.edge('v01g', '2h1g', style = 'invis')
            g.attr(color='black') 
            g.attr(label='v_cross == 1')
            g.attr(fontsize='20')
            g.attr(size = '8,5!')
    f.render(dir_path +'imglib/pedestrian_and_sign_and_light/state', view=False, cleanup=False)
#    state = dir_path + '/imglib/pedestrian_and_sign_and_light/('+ str(h_cross) + str(v_cross) + str(h_walk) + str(v_walk) + h_light + v_light +').png'
#    return Image.open(state)
    
def monitor_pedestrians(h_cross, v_cross, h_walk, v_walk, h_light, v_light, pedestrian_state=0):
    fsm_pedestrians(h_cross, v_cross, h_walk, v_walk, h_light, v_light, pedestrian_state)
    state = dir_path + '/imglib/pedestrian_and_sign_and_light/state.png'
    return Image.open(state)




