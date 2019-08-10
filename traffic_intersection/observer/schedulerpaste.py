#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on August 2019

@author: Josefine and Jiaqi
"""

import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont,ImageDraw  
import os
from numpy import pi
import scipy.integrate as integrate
from primitives.load_primitives import get_prim_data
import test_pedestrian, test_light, test_car
dir_path = os.path.dirname(os.path.realpath(__file__))
background_fig = dir_path + '/imglib/as/scheduler_background.png'

def get_background():
    return Image.open(background_fig)

waiting_line = dict()
waiting_line['horizontal'] = ((250,245),(250,310),(250,380),(810,385),(810,450),(810,515))
waiting_line['vertical'] = ((425,665),(500,665),(565,100),(635,100))

def distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

# check whether the object is at certain position
def at_certain_position(object_coordinate, center_of_position):
    return distance(object_coordinate, center_of_position) <= 20


def draw_scheduler_table(cars_to_keep, light_color, background): 
    y_coordinate = 175
    for i in range(len(cars_to_keep)):
        waiting_light = False
        if i < 9:
            fontpath = 'AbhayaLibre-SemiBold.ttf'
            font = ImageFont.truetype(fontpath, 40)
            draw = ImageDraw.Draw(background)  
            draw.text((25,y_coordinate), str(cars_to_keep[i].id),fill='black', font=font)
            if cars_to_keep[i].state[0] < 1:
                draw.text((220,y_coordinate),'Stop',fill= 'red',font=font)
                #print(cars_to_keep[i].id, cars_to_keep[i].state[1], cars_to_keep[i].state[2],cars_to_keep[i].state[3])
                car_xy = (cars_to_keep[i].state[2],cars_to_keep[i].state[3])
                for position in waiting_line['horizontal']:
                    if at_certain_position(car_xy, position):
                        if light_color[0] == 'r':
                            draw.text((500,y_coordinate),'Red light',fill= 'red',font=font)
                            waiting_light = True
                        elif light_color[0] == 'y':
                            draw.text((500,y_coordinate),'Not enough time',fill= 'red',font=font) 
                            waiting_light = True
                if not waiting_light:
                    for position in waiting_line['vertical']:
                        if at_certain_position(car_xy, position):
                            if light_color[1] == 'r':
                                draw.text((500,y_coordinate),'Red light',fill= 'red',font=font)
                                waiting_light = True
                            elif light_color[1] == 'y':
                                draw.text((500,y_coordinate),'Not enough time',fill= 'red',font=font)  
                                waiting_light = True
                if not waiting_light:
                    draw.text((500,y_coordinate),'Not clear',fill= 'red',font=font)
#                if (abs(theta % (-pi/2)) <= 0.1 or abs(theta % (pi/2)) <= 0.1):
#                    if light_color[1] == 'r':
#                        draw.text((500,y_coordinate),'Red light',fill= 'red',font=font)
#                    elif light_color[1] == 'y':
#                        draw.text((500,y_coordinate),'Not enough time',fill= 'red',font=font)
#                elif (abs(theta) <= 0.1 or abs(theta % pi) <= 0.1):
#                    if light_color[0] == 'r':
#                        draw.text((500,y_coordinate),'Red light',fill= 'red',font=font)
#                    elif light_color[0] == 'y':
#                        draw.text((500,y_coordinate),'Not enough time',fill= 'red',font=font)
#                else:
#                    draw.text((500,y_coordinate),'Not clear',fill= 'red',font=font)
            else:
                draw.text((220,y_coordinate),'Driving',fill= (0,100,0),font=font)           
            y_coordinate += 75
      
#background = get_background()
#draw_scheduler_table(10, background)
#background.show()

        