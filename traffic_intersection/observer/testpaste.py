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
from primitives.load_primitives import get_prim_data
import test_pedestrian, test_light, test_car
dir_path = os.path.dirname(os.path.realpath(__file__))
background_fig = dir_path + '/imglib/as/testmonitor.png'

def get_background():
    return Image.open(background_fig)
    
def draw_monitor(last_state, current_state, exception, prim_id, person_spec, car_spec, background): 
    test_pedestrian.monitor_pedestrians(last_state[2], current_state[2], exception['pedestrian'])
    test_light.monitor_light(last_state[0], last_state[1], current_state[0], current_state[1])
    test_car.monitor_vehicles(last_state[3], current_state[3], exception['vehicle'])
    pedestrian_fig = dir_path + '/imglib/pedestrian.png'
    person_fig = Image.open(pedestrian_fig)
    light_fig = dir_path + '/imglib/light.png'
    light_fig = Image.open(light_fig)
    car_fig = dir_path + '/imglib/car.png'
    car_fig = Image.open(car_fig)

    
    x0 = get_prim_data(prim_id, 'x0')[2:4]
    xf = get_prim_data(prim_id, 'x_f')[2:4]
    x0 = [int(x0[0]), int(x0[1])]
    xf = [int(xf[0]), int(xf[1])]
    fontpath1 = 'NotoSans-BoldItalic.ttf'
    fontpath = 'AbhayaLibre-SemiBold.ttf'
    font = ImageFont.truetype(fontpath, 28)
    smallfont = ImageFont.truetype(fontpath, 23)
    middlefont = ImageFont.truetype(fontpath, 23)
    font1 = ImageFont.truetype(fontpath1, 25)
    largefont = ImageFont.truetype(fontpath1, 40)
    nofill = (0,0,0)
    fill = (0,100,0)
    color_person_spec = [nofill, nofill, nofill]
    color_light_spec = [nofill, nofill, nofill, nofill, nofill]
    color_car_spec = [nofill, nofill]
    if person_spec in (1,2,3):
        color_person_spec[person_spec-1] = fill
        
    if current_state[0]+ current_state[1] == 'rg':
        color_light_spec[0] = fill
        color_light_spec[1] = fill
    elif current_state[0]+current_state[1] == 'ry':
        color_light_spec[0] = fill
        color_light_spec[2] = fill
    elif current_state[0]+current_state[1] == 'gr':
        color_light_spec[0] = fill
        color_light_spec[1] = fill
    elif current_state[0]+current_state[1] == 'yr':
        color_light_spec[0] = fill
        color_light_spec[2] = fill
    elif current_state[0]+current_state[1] == 'rr':
        color_light_spec[0] = fill
        color_light_spec[3] = fill
        
    if car_spec in (1,2):
        color_car_spec[car_spec-1] = fill
        
    # check exception
    if exception['vehicle']:
        color_car_spec[1] = 'red'
        car_fig = car_fig.resize((120,120))
        background.paste(car_fig,(500,1200))
    else:
        #car_fig = car_fig.resize((740,220))
        background.paste(car_fig,(410,1100))
    background.paste(person_fig,(650,80))
    background.paste(light_fig,(650,435))
    
    draw = ImageDraw.Draw(background)  
    draw.text((145,230), '\u25CA arrive = destination;',fill=color_person_spec[0],font=font)
    draw.text((145,270), '(\u00AC g) -> (\u00AC cross the street);',fill=color_person_spec[1],font=font)
    draw.text((145,310), '(t_cross >= t_w) -> \n(\u00AC cross the street).',fill=color_person_spec[2],font=font)  
    draw.text((145,650), '\u25CB',fill=color_light_spec[0],font=largefont)
    draw.text((190,660), 'r;',fill=color_light_spec[0],font=font)
    draw.text((167,660), '30',fill=color_light_spec[0],font=smallfont)
    draw.text((220,650), '\u25CB',fill=color_light_spec[1],font=largefont)
    draw.text((265,660), 'g;',fill=color_light_spec[1],font=font)
    draw.text((242,660), '25',fill=color_light_spec[1],font=smallfont)
    draw.text((295,650), '\u25CB',fill=color_light_spec[2],font=largefont)
    draw.text((337,660), 'y;',fill=color_light_spec[2],font=font)
    draw.text((317,660), '5',fill=color_light_spec[2],font=smallfont)   
    draw.text((145,700), '\u25A2',fill=color_light_spec[3],font=font1)
    draw.text((160,700), '\u25CA rr.',fill=color_light_spec[3],font=font)
    draw.text((145,1300), '\u25CA arrive = destination;',fill=color_car_spec[0],font=font)
    draw.text((145,1330), '\u25A2',fill=color_car_spec[1],font=font1)
    draw.text((160,1330), '\u00AC collision.',fill=color_car_spec[1],font=font)
    
    if prim_id != -1 and not exception['vehicle']:
        draw.text((1275,670), 'Guiding prim_id = ' +str(prim_id),fill=(0,100,0),font=middlefont)
        draw.text((1275,700), str(x0) + '->'+ str(xf),fill=(0,100,0),font=middlefont)
    
   
#background = get_background()
#exception = {'pedestrian': True, 'vehicle': True}
#draw_monitor(['r', 'r', 1, 1],['r', 'g', 1, 0], exception, 99, -1, 2, background)
#background.show()
