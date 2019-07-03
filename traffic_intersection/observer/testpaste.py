#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 17:51:31 2019

@author: yanjiaqi
"""

import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont,ImageDraw  
import os
import scipy.integrate as integrate
import test_pedestrian, test_light, test_car
dir_path = os.path.dirname(os.path.realpath(__file__))
background_fig = dir_path + '/imglib/as/Slide.png'

def get_background():
    return Image.open(background_fig)
    
def draw_monitor(h_light, v_light, pedestrian_state, vehicle_state, background): 
    test_pedestrian.monitor_pedestrians(pedestrian_state)
    test_light.monitor_light(h_light, v_light)
    test_car.monitor_vehicles(vehicle_state)
    pedestrian_fig = dir_path + '/imglib/pedestrian.png'
    person_fig = Image.open(pedestrian_fig)
    light_fig = dir_path + '/imglib/light.png'
    light_fig = Image.open(light_fig)
    car_fig = dir_path + '/imglib/car.png'
    car_fig = Image.open(car_fig)
    
    
    background.paste(person_fig,(132,550))
    background.paste(light_fig,(580,450))
    background.paste(car_fig,(1050,520))
    fontpath = 'NotoSans-BoldItalic.ttf'
    font = ImageFont.truetype(fontpath, 25)
    smallfont = ImageFont.truetype(fontpath, 18)
    largefont = ImageFont.truetype(fontpath, 40)
    draw = ImageDraw.Draw(background)  
    draw.text((140,300), '\u25CA arrive = destination;',fill=(0,100,0),font=font)
    draw.text((140,330), '\u00AC g -> \u00AC cross the street.',fill=(0,0,0),font=font)
    draw.text((140,360), 't_cross >= t_w -> \u00AC cross the street.',fill=(0,0,0),font=font)
    draw.text((600,300), '\u25CB',fill=(0,100,0),font=largefont)
    draw.text((645,310), 'r;',fill=(0,100,0),font=font)
    draw.text((622,310), '30',fill=(0,100,0),font=smallfont)
    draw.text((675,300), '\u25CB',fill=(0,100,0),font=largefont)
    draw.text((720,310), 'g;',fill=(0,100,0),font=font)
    draw.text((697,310), '25',fill=(0,100,0),font=smallfont)
    draw.text((750,300), '\u25CB',fill=(0,100,0),font=largefont)
    draw.text((795,310), 'y;',fill=(0,100,0),font=font)
    draw.text((772,310), '5',fill=(0,100,0),font=smallfont)    
    draw.text((600,345), '\u25AF\u25CA rr.',fill=(0,0,0),font=font)
    draw.text((1050,310), '\u25CA arrive = destination;',fill=(0,100,0),font=font)
    draw.text((1050,345), '\u25CA\u00AC collision.',fill=(0,0,0),font=font)
    
   

