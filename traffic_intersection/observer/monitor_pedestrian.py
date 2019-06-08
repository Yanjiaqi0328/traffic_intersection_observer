#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 16:23:39 2019

@author: yanjiaqi
"""
import sys
sys.path.append('..')
import os
from PIL import Image
dir_path = os.path.dirname(os.path.realpath(__file__))
observer_fig = dir_path + '/imglib/Blank.png'

def get_background():
    return Image.open(observer_fig)

def monitor_pedestrians(pedestrian_state, background):
    if pedestrian_state ==0:
        pedestrian_state = dir_path + '/imglib/pedestrian_state/fsm_pedestrian_no_appear.png'
    elif pedestrian_state in (1,2):
        pedestrian_state = dir_path + '/imglib/pedestrian_state/fsm_pedestrian_walk.png'
    else:
        pedestrian_state = dir_path + '/imglib/pedestrian_state/fsm_pedestrian_wait.png'
    pedestrian_state_fig = Image.open(pedestrian_state)
    background.paste(pedestrian_state_fig) 
    

