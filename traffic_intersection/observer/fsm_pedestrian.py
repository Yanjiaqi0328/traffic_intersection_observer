#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 19:51:58 2019

@author: yanjiaqi
"""

from graphviz import Digraph

f = Digraph('finite_state_machine (pedestrian)',format='png')
f.attr(rankdir='LR',size='12,15!')

pedestrian_state = 4
state = 'no_appear'
f.attr('node', shape='plaintext')
f.node('')
f.attr('node', shape='circle', width='0.6',fontsize ='15.0')
f.node('0')
f.node('1')


if pedestrian_state in (1,2):
    f.node('1', style='filled', color='grey')
    state = 'walk'
elif pedestrian_state in (3,4):
    f.node('0', style='filled', color='grey')
    state = 'wait'

f.attr('edge', arrowsize = '0.5', fontsize ='10.0')
f.edge('0', '1',label='walk_sign == 1')
f.edge('', '1', label='start')
f.edge('0', '0', label='walk_sign == 0')
f.edge('1', '0', label='(cross==1) && [walk_sign==0 || (walk_sign ==1 && t_cross > t_sign)]')
f.edge('1', '1', label='others')
f.render('imglib/pedestrian_state//fsm_pedestrian_'+ state, view=True, cleanup=True) 

