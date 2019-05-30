#!/usr/bin/env python3
# State Monitor
# Jiaqi Yan
# May 17, 2019
import sys
sys.path.append('..')
import numpy as np
import random
import assumes.params as params
import os
from PIL import Image
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
dir_path = os.path.dirname(os.path.realpath(__file__))
observer_fig = dir_path + '/imglib/Blank.png'


def get_background():
    return Image.open(observer_fig)


def monitor_pedestrians(pedestrian_state, background):
    pedestrian_state = dir_path + '/imglib/pedestrian_state/pedestrian_state_' + str(pedestrian_state)+ '.png'
    pedestrian_state_fig = Image.open(pedestrian_state)
    background.paste(pedestrian_state_fig)   



