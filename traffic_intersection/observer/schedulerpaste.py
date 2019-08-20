#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on August 19 2019

@author: Josefine Graebener and Jiaqi Yan
"""

import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFont,ImageDraw  
import os
from numpy import pi
import scipy.integrate as integrate
import prepare.queue as queue
import components.scheduler as scheduler
from primitives.load_primitives import get_prim_data
import test_pedestrian, test_light, test_car
dir_path = os.path.dirname(os.path.realpath(__file__))
background_fig = dir_path + '/imglib/as/schedulertable.png'

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

# check whether the object is in the waiting area
def at_waiting_line(object_coordinate, direction):
    wait_at_line = False
    for position in waiting_line[direction]:
        if at_certain_position(object_coordinate, position):
                wait_at_line  = True
                return wait_at_line
    return wait_at_line


def draw_scheduler_table(cars_to_keep, light_color, background,vehicle_state,picked_car,prim_id,picked_ped): 
    fontpath = 'AbhayaLibre-SemiBold.ttf'
    font = ImageFont.truetype(fontpath, 50)
    draw = ImageDraw.Draw(background)  
    # Adding black text into scheduler table if no action
    # Lights Contract Section
    # change color of the text depending on light color
    if light_color[0] == 'r':
        draw.text((1000,210), '?r_h',fill='red',font=font)
        draw.text((440,280), '!r_h',fill='red',font=font)
    else:
        draw.text((440,280), '!r_h',fill='black',font=font)
        draw.text((1000,210), '?r_h',fill='black',font=font)
    if light_color[1] == 'r':
        draw.text((440,210), '?r_v',fill='red',font=font)
        draw.text((1000,280), '!r_v',fill='red',font=font)
    else:
        draw.text((440,210), '?r_v',fill='black',font=font)
        draw.text((1000,280), '!r_v',fill='black',font=font)
    if light_color[3]:
        draw.text((650,280), '!h_walk',fill='green',font=font)
    else:
        draw.text((650,280), '!h_walk',fill='black',font=font)
    if light_color[2]:
        draw.text((1210,280), '!v_walk',fill='green',font=font)
    else:
        draw.text((1210,280), '!v_walk',fill='black',font=font)
    # Vehicle and Scheduler Section
    # state CAR ID
    if picked_car:
        draw.text((270,470), str(picked_car.id),fill='black',font=font)
    if picked_car:
        car_xy = (picked_car.state[2],picked_car.state[3])
        waiting_signal = False
        # show if request queue has cars waiting
        if scheduler.Scheduler.length:
            draw.text((1000,550), 'len(request_queue)',fill='green',font=font)
        # check if car is done
        if at_certain_position(car_xy, picked_car.destination):
            draw.text((440,550), 'not_done',fill='black',font=font)
        else:
            draw.text((440,550), 'not_done',fill='green',font=font)
        # show the reason for rejected request
        if picked_car.state[0] < 2 and not at_certain_position(car_xy, picked_car.destination): 
            if not picked_car.alive_time < 1:
                draw.text((970,710), '!reject',fill='red',font=font)
                draw.text((380,630), '?reject',fill='red',font=font)
            if at_waiting_line(car_xy, 'horizontal'):
                if light_color[0] == 'r':
                    draw.text((440,790),'Red light',fill= 'red',font=font)
                    waiting_signal = True
                elif light_color[0] == 'y':
                    draw.text((440,790),'Not enough time',fill= 'red',font=font) 
                    waiting_signal = True
            elif at_waiting_line(car_xy, 'vertical'):
                if light_color[1] == 'r':
                    draw.text((440,790),'Red light',fill= 'red',font=font)
                    waiting_signal = True
                elif light_color[1] == 'y':
                    draw.text((440,790),'Not enough time',fill= 'red',font=font) 
                    waiting_signal = True
            if not waiting_signal: # if not because of waiting for the signal
                draw.text((440,790),'Not clear',fill= 'red',font=font)
        else:
            draw.text((530,630), '?accept',fill='green',font=font) 
            draw.text((700,630), '?primitives',fill='green',font=font)  
            draw.text((1120,710), '!accept',fill='green',font=font)
            draw.text((1280,710), '!primitives',fill='green',font=font)  
            draw.text((970,710), '!reject',fill='black',font=font)
            draw.text((380,630), '?reject',fill='black',font=font)   
            if prim_id != -1:
                x0 = get_prim_data(prim_id, 'x0')[2:4]
                xf = get_prim_data(prim_id, 'x_f')[2:4]
                x0 = [int(x0[0]), int(x0[1])]
                xf = [int(xf[0]), int(xf[1])]
                draw.text((440,790), 'Guiding prim_id = ' +str(prim_id),fill=(0,100,0),font=font)
                draw.text((950,790), str(x0) + '->'+ str(xf),fill=(0,100,0),font=font)
        # check if the picked car is making a request
        if scheduler.Scheduler.check_car_request:
            draw.text((1000,630), '?request',fill='green',font=font)
            draw.text((440,710), '!request',fill='green',font=font)
    else: # if no car is picked, all text is black
        draw.text((440,710), '!request',fill='black',font=font)
        draw.text((380,630), '?reject',fill='black',font=font)
        draw.text((530,630), '?accept',fill='black',font=font)
        draw.text((700,630), '?primitives',fill='black',font=font)
        draw.text((1000,550), 'len(request_queue)',fill='black',font=font)
        draw.text((1000,630), '?request',fill='black',font=font)
        draw.text((970,710), '!reject',fill='black',font=font)
        draw.text((1120,710), '!accept',fill='black',font=font)
        draw.text((1280,710), '!primitives',fill='black',font=font)
        draw.text((440,550), 'not_done',fill='black',font=font)

    if picked_ped:
        person_xy = (picked_ped.state[0], picked_ped.state[1])
        #if person_xy in (pedestrian_graph.lane1 + pedestrian_graph.lane2) and light_color[0] == 'g':#+ pedestrian_graph.lane3 + pedestrian_graph.lane4):
        #    draw.text((380,1140), '?h_walk',fill='green',font=font)
        if picked_ped.monitor_state in (2,3,4):
            if picked_ped.state[2] in (-pi/2, pi/2) and light_color[2]: # walking S-N left side
                draw.text((560,1140), '?v_walk',fill='green',font=font)
                draw.text((1170,1220), '!v_walk',fill='green',font=font)
                draw.text((440,1060), 't_cross',fill='green',font=font)
                draw.text((1200,1060), 'v_timer',fill='green',font=font)
                draw.text((440,1300), 'Crossing vertically',fill='green',font=font)
            else:
                draw.text((560,1140), '?v_walk',fill='black',font=font)
                draw.text((1170,1220), '!v_walk',fill='black',font=font)
                draw.text((440,1060), 't_cross',fill='black',font=font)
                draw.text((1200,1060), 'v_timer',fill='black',font=font)
            if picked_ped.state[2] in (pi, 0) and light_color[3]: # walking E-W
                draw.text((380,1140), '?h_walk',fill='green',font=font)
                draw.text((800,1220), '!h_walk',fill='green',font=font)
                draw.text((440,1060), 't_cross',fill='green',font=font)
                draw.text((850,1060), 'h_timer',fill='green',font=font)
                draw.text((440,1300), 'Crossing horizontally',fill='green',font=font)
            else:
                draw.text((380,1140), '?h_walk',fill='black',font=font)
                draw.text((800,1220), '!h_walk',fill='black',font=font)
                draw.text((440,1060), 't_cross',fill='black',font=font)
                draw.text((850,1060), 'h_timer',fill='black',font=font)
            if picked_ped.monitor_state == 4:
                draw.text((440,1300), 'Waiting at the signal',fill='red',font=font)   
            if picked_ped.monitor_state == 3:
                draw.text((440,1300), 'Not enough time',fill='black',font=font) 
                draw.text((440,1060), 't_cross',fill='red',font=font) 
                if picked_ped.state[2] in (-pi/2, pi/2):
                    draw.text((1200,1060), 'v_timer',fill='red',font=font)
                if picked_ped.state[2] in (pi, 0):
                    draw.text((850,1060), 'h_timer',fill='red',font=font)
        else:
            draw.text((440,1300), 'Walking',fill='black',font=font) 
            draw.text((440,1060), 't_cross',fill='black',font=font)
            draw.text((380,1140), '?h_walk',fill='black',font=font)
            draw.text((560,1140), '?v_walk',fill='black',font=font)
            draw.text((850,1060), 'h_timer',fill='black',font=font)
            draw.text((1200,1060), 'v_timer',fill='black',font=font)
            draw.text((800,1220), '!h_walk',fill='black',font=font)
            draw.text((1000,1220), '!r_h',fill='black',font=font)
            draw.text((1170,1220), '!v_walk',fill='black',font=font)
            draw.text((1400,1220), '!r_v',fill='black',font=font)       

    else:
    # Pedestrian and light section in black if there is no pedestrian chosen
        draw.text((440,1060), 't_cross',fill='black',font=font)
        draw.text((380,1140), '?h_walk',fill='black',font=font)
        draw.text((560,1140), '?v_walk',fill='black',font=font)
        draw.text((850,1060), 'h_timer',fill='black',font=font)
        draw.text((1200,1060), 'v_timer',fill='black',font=font)
        draw.text((800,1220), '!h_walk',fill='black',font=font)
        draw.text((1000,1220), '!r_h',fill='black',font=font)
        draw.text((1170,1220), '!v_walk',fill='black',font=font)
        draw.text((1400,1220), '!r_v',fill='black',font=font)
    
# Commented out section which gives list of cars for old scheduler table
#     for i in range(len(cars_to_keep)):
#         # only show the first 9 cars in the scheduler table
#         if i < 9:
#             car_xy = (cars_to_keep[i].state[2],cars_to_keep[i].state[3])
#             waiting_signal = False
#             draw.text((25,y_coordinate), str(cars_to_keep[i].id),fill='black', font=font)
#             # if the car stops (and not because it is arrived)
#             if cars_to_keep[i].state[0] < 2 and not at_certain_position(car_xy, cars_to_keep[i].destination): 
#                 draw.text((220,y_coordinate),'Stop',fill= 'red',font=font)
#                 if at_waiting_line(car_xy, 'horizontal'):
#                     if light_color[0] == 'r':
#                         draw.text((500,y_coordinate),'Red light',fill= 'red',font=font)
#                         waiting_signal = True
#                     elif light_color[0] == 'y':
#                         draw.text((500,y_coordinate),'Not enough time',fill= 'red',font=font) 
#                         waiting_signal = True
#                 elif at_waiting_line(car_xy, 'vertical'):
#                     if light_color[1] == 'r':
#                         draw.text((500,y_coordinate),'Red light',fill= 'red',font=font)
#                         waiting_signal = True
#                     elif light_color[1] == 'y':
#                         draw.text((500,y_coordinate),'Not enough time',fill= 'red',font=font) 
#                         waiting_signal = True
#                 if not waiting_signal: # if not because of waiting for the signal
#                     draw.text((500,y_coordinate),'Not clear',fill= 'red',font=font)
# #                if (abs(theta % (-pi/2)) <= 0.1 or abs(theta % (pi/2)) <= 0.1):
# #                    if light_color[1] == 'r':
# #                        draw.text((500,y_coordinate),'Red light',fill= 'red',font=font)
# #                    elif light_color[1] == 'y':
# #                        draw.text((500,y_coordinate),'Not enough time',fill= 'red',font=font)
# #                elif (abs(theta) <= 0.1 or abs(theta % pi) <= 0.1):
# #                    if light_color[0] == 'r':
# #                        draw.text((500,y_coordinate),'Red light',fill= 'red',font=font)
# #                    elif light_color[0] == 'y':
# #                        draw.text((500,y_coordinate),'Not enough time',fill= 'red',font=font)
# #                else:
# #                    draw.text((500,y_coordinate),'Not clear',fill= 'red',font=font)
#             else:
#                 draw.text((220,y_coordinate),'Driving',fill= (0,100,0),font=font)           
#             y_coordinate += 75
      

        