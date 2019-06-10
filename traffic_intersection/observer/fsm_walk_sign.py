#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 19:51:58 2019

@author: yanjiaqi
"""

from graphviz import Digraph

f = Digraph('finite_state_machine (walk_sign)',format='png')
f.attr(rankdir='LR',size='12,15!')

walk_sign_state = 0
f.attr('node', shape='circle', width='0.6',fontsize ='15.0')
f.node('0')
f.node('1')


if walk_sign_state == 0:
    f.node('0', style='filled', color='grey')
    state = 'off'
else:
    f.node('1', style='filled', color='grey')
    state = 'on'

f.attr('edge', arrowsize = '0.5', fontsize ='10.0')
f.edge('0', '1',label='light == g && light_time >= 3')
f.edge('0', '0', label='others')
f.edge('1', '0', label='light_time > 9.4')
f.edge('1', '1', label='others')
f.render('imglib/walk_sign_state//fsm_walk_sign_'+ state, view=True, cleanup=True) 

