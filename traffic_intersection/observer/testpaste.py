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
    
def draw_monitor(last_state, current_state, person_spec, background): 
    test_pedestrian.monitor_pedestrians(last_state[2], current_state[2])
    test_light.monitor_light(last_state[0], last_state[1], current_state[0], current_state[1])
    test_car.monitor_vehicles(last_state[3], current_state[3])
    pedestrian_fig = dir_path + '/imglib/pedestrian.png'
    person_fig = Image.open(pedestrian_fig)
    light_fig = dir_path + '/imglib/light.png'
    light_fig = Image.open(light_fig)
    car_fig = dir_path + '/imglib/car.png'
    car_fig = Image.open(car_fig)
    
    background.paste(person_fig,(132,550))
    background.paste(light_fig,(580,450))
    background.paste(car_fig,(1050,520))
    fontpath1 = 'NotoSans-BoldItalic.ttf'
    fontpath = 'AbhayaLibre-SemiBold.ttf'
    font = ImageFont.truetype(fontpath, 28)
    smallfont = ImageFont.truetype(fontpath, 18)
    font1 = ImageFont.truetype(fontpath1, 25)
    largefont = ImageFont.truetype(fontpath1, 40)
    nofill = (0,0,0)
    fill = (0,100,0)
    color = [nofill, nofill, nofill]
    if person_spec in (1,2,3):
        color[person_spec-1] = fill
    draw = ImageDraw.Draw(background)  
    draw.text((140,300), '\u25CA arrive = destination;',fill=color[0],font=font)
    draw.text((140,330), '(\u00AC g) -> (\u00AC cross the street);',fill=color[1],font=font)
    draw.text((140,360), '(t_cross >= t_w) -> (\u00AC cross the street).',fill=color[2],font=font)
    draw.text((600,300), '\u25CB',fill=(0,100,0),font=largefont)
    draw.text((645,310), 'r;',fill=(0,100,0),font=font)
    draw.text((622,310), '30',fill=(0,100,0),font=smallfont)
    draw.text((675,300), '\u25CB',fill=(0,100,0),font=largefont)
    draw.text((720,310), 'g;',fill=(0,100,0),font=font)
    draw.text((697,310), '25',fill=(0,100,0),font=smallfont)
    draw.text((750,300), '\u25CB',fill=(0,100,0),font=largefont)
    draw.text((792,310), 'y;',fill=(0,100,0),font=font)
    draw.text((772,310), '5',fill=(0,100,0),font=smallfont)    
    draw.text((602,344), '\u25A2',fill=(0,0,0),font=font1)
    draw.text((617,345), '\u25CA rr.',fill=(0,0,0),font=font)
    draw.text((1050,310), '\u25CA arrive = destination;',fill=(0,100,0),font=font)
    draw.text((1050,345), '\u25CA\u00AC collision.',fill=(0,0,0),font=font)
    
   
#background = get_background()
#draw_monitor(['g', 'r', 1, 1],['y', 'r', 1, 1], 2, background)
#background.show()
