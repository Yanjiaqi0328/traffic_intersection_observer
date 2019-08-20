#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created in Jun 2019

@author: Jiaqi Yan (jiaqi@caltech.edu)
"""

import sys
sys.path.append('..') # enable importing modules from an upper directory:
from prepare.helper import *
import time, platform, warnings, matplotlib, random
import components.scheduler as scheduler
import observer.testpaste as monitor
import observer.schedulerpaste as scheduler_monitor
import prepare.user as user
import datetime
import threading
if platform.system() == 'Darwin': # if the operating system is MacOS
#    matplotlib.use('macosx')
    matplotlib.use('Qt5Agg')
else: # if the operating system is Linux or Windows
    try:
        import PySide2 # if pyside2 is installed
        matplotlib.use('Qt5Agg')
    except ImportError:
        warnings.warn('Using the TkAgg backend, this may affect performance. Consider installing pyside2 for Qt5Agg backend')
        matplotlib.use('TkAgg') # this may be slower
import matplotlib.animation as animation
import matplotlib.pyplot as plt


             
# set randomness
if not options.random_simulation:
    random.seed(options.random_seed)
    np.random.seed(options.np_random_seed)

# creates figure
fig = plt.figure()
ax = fig.add_axes([0.005,0.4,0.4,0.65]) # get rid of white border original:[0,0.2,0.4,0.65]
if not options.show_axes:
    fig1 = plt.gca()
    fig1.axes.get_xaxis().set_visible(False)
    fig1.axes.get_yaxis().set_visible(False)
ax2 = fig.add_axes([0.23,0,1,1]) # get rid of white border
fig2 = plt.gca()
fig2.axes.get_xaxis().set_visible(False)
fig2.axes.get_yaxis().set_visible(False)
ax3 = fig.add_axes([-0.045,0.02,0.5,0.5]) # get rid of white border
fig3 = plt.gca()
fig3.axes.get_xaxis().set_visible(False)
fig3.axes.get_yaxis().set_visible(False)


# sampling time
dt = options.dt

#if true, pedestrians can cross street and cars cannot cross
def safe_to_walk(green_duration, light_color, light_time):
    walk_sign_delay = green_duration / 8.
    return light_color == 'green' and light_time >= 3 and light_time <= (green_duration / 4. + walk_sign_delay)

def get_remaining_walk_time(safe_to_walk, walk_sign_duration, light_time):
    remaining_walking_time = -1
    if safe_to_walk:
        remaining_walking_time = abs(walk_sign_duration - light_time + 3)
    return remaining_walking_time

# checks if pedestrian is crossing street
def is_between(lane, person_xy):
    return (distance(lane[0], person_xy) + distance(lane[1], person_xy) == distance(lane[0], lane[1])) and (person_xy not in lane)

# create traffic intersection
traffic_lights = traffic_signals.TrafficLights(yellow_max = 10, green_max = 50, random_start = True)
# create planner
planner = scheduler.Scheduler()
# enable user's input
user_command = user.Read_user_command()
user_command.start()
print('If you want to choose/change the vehicle to be monitored, please press "s". ')

background = intersection.get_background()
observer = monitor.get_background()
schedulerobserver = scheduler_monitor.get_background()

# default states (fsm)
vehicle_id = 0
pedestrian_id = 0
last_state = [-1,-1,-1,-1]

def animate(frame_idx): # update animation by dt
    global background, observer, vehicle_id, pedestrian_id, last_state, schedulerobserver
    h_cross = 0
    v_cross = 0
    
    # if the user has requested to choose a vehicle, then ask for the vehicle id (default to be 1)
    if user_command.index == 1:
        options.vehicle_to_pick = int(input('Please input the ID of vehicle to be monitored: '))
    user_command.index = 0

    pedestrian_spec = 0
    light_spec = 0
    vehicle_spec = 0
    prim_id = -1
    exception = {'pedestrian': False, 'vehicle': False}
    
    ax.clear()
    ax2.clear()
    ax3.clear()
    t0 = time.time()
    deadlocked = False
    global_vars.current_time = frame_idx * dt # update current time from frame index and dt
    green_duration = traffic_lights._max_time['green']
    walk_sign_duration = traffic_lights._walk_sign_duration
    all_components_monitor = []
    """ online frame update """
    # car request
    if with_probability(options.new_car_probability):
        new_start_node, new_end_node, new_car = spawn_car()
        new_car.destination = (new_end_node[2], new_end_node[3]) # add destination
        planner._request_queue.enqueue((new_start_node, new_end_node, new_car)) # planner takes request
    service_count = 0
    original_request_len = planner._request_queue.len()
    while planner._request_queue.len() > 0 and not deadlocked: # if there is at least one live request in the queue
        planner.serve(graph=car_graph.G,traffic_lights=traffic_lights)
        service_count += 1
        if service_count == original_request_len:
            service_count = 0 # reset service count
            if planner._request_queue.len() == original_request_len:
                deadlocked = True
            else:
                original_request_len = planner._request_queue.len()
    planner.clear_stamps()
    
    if with_probability(options.new_pedestrian_probability):
        while True:
            name, begin_node, final_node, the_pedestrian = spawn_pedestrian()
            if  begin_node != final_node:
                break
        pedestrian_id += 1
        _, shortest_path = dijkstra(begin_node, final_node, pedestrian_graph.G, True)
#        if len(shortest_path) != 1:
#            print('gotcha')
#            print(begin_node)
#            print(final_node)
#            print(shortest_path)
        vee = np.random.uniform(20, 40)
        while len(shortest_path) > 1:
                the_pedestrian.prim_queue.enqueue(((shortest_path[0], shortest_path[1], vee), 0))
                del shortest_path[0]
        global_vars.pedestrians_to_keep.add(the_pedestrian)
        the_pedestrian.destination = final_node
        the_pedestrian.id = pedestrian_id
#        if the_pedestrian.id == options.pedestrian_to_pick:
#            all_components_monitor = all_components_monitor + [the_pedestrian]
            
    traffic_lights.update(dt)
    update_traffic_lights(ax, plt, traffic_lights) # for plotting
    vertical_light = traffic_lights.get_states('vertical', 'color')
    horizontal_light = traffic_lights.get_states('horizontal', 'color')
    vertical_walk_safe = safe_to_walk(green_duration, vertical_light, traffic_lights.get_elapsed_time('vertical'))
    horizontal_walk_safe = safe_to_walk(green_duration, horizontal_light, traffic_lights.get_elapsed_time('horizontal'))
    draw_walk_signs(background,traffic_signals.walk_sign_figs['vertical'][vertical_walk_safe], traffic_signals.walk_sign_figs['horizontal'][horizontal_walk_safe])
    
    horizontal_walk_time = get_remaining_walk_time(horizontal_walk_safe, walk_sign_duration, traffic_lights.get_elapsed_time('horizontal'))
    vertical_walk_time = get_remaining_walk_time(vertical_walk_safe, walk_sign_duration, traffic_lights.get_elapsed_time('vertical'))
    # update pedestrians
    monitor_pedestrian_state = 0
    # person.monitor_state: 0- default
    #                       1- not going to cross the street
    #                       2- safe to get crossed
    #                       3- walking sign is on but remaining time is not enough to get crossed
    #                       4- walking sign is off
    if len(global_vars.pedestrians_to_keep) > 0:
        for person in global_vars.pedestrians_to_keep.copy():
            if True:
                person_xy = (person.state[0], person.state[1])
                if person_xy not in (pedestrian_graph.lane1 + pedestrian_graph.lane2 + pedestrian_graph.lane3 + pedestrian_graph.lane4): # if pedestrian is not at any of the nodes then continue  
                    person.prim_next(dt)
                    global_vars.pedestrians_to_keep.add(person)
                    person.monitor_state = 1 
                elif person.continue_walking(pedestrian_graph.lane1, pedestrian_graph.lane2, (-pi/2, pi/2), vertical_walk_time): # if light is green cross the street, or if at a node and facing away from the street i.e. just crossed the street then continue
                    person.prim_next(dt)
                    global_vars.pedestrians_to_keep.add(person)
                elif person.monitor_state != 3:
                    if person.continue_walking(pedestrian_graph.lane3, pedestrian_graph.lane4, (pi, 0), horizontal_walk_time):
                        person.prim_next(dt)
                        global_vars.pedestrians_to_keep.add(person)
                else:
                    person.state[3] = 0
                    if person.monitor_state != 3:
                        person.monitor_state = 4 
                
                 # pedestrians walk faster if not going fast enough to finish crossing the street before walk sign is off or 'false'
#                if is_between(pedestrian_graph.lane1, person_xy) or is_between(pedestrian_graph.lane2, person_xy):
#                    person.walk_faster(vertical_walk_time)
#                elif is_between(pedestrian_graph.lane3, person_xy) or is_between(pedestrian_graph.lane4, person_xy):
#                    person.walk_faster(horizontal_walk_time)
                if person.prim_queue.len() == 0:
                    global_vars.pedestrians_to_keep.remove(person)
                
                if is_between(pedestrian_graph.lane1, person_xy) or is_between(pedestrian_graph.lane2, person_xy) or is_between(pedestrian_graph.lane3, person_xy) or is_between(pedestrian_graph.lane4, person_xy):
                    person.monitor_state = 2 
                    
                if person.id == options.pedestrian_to_pick:
                    all_components_monitor = all_components_monitor + [person]
                    monitor_pedestrian_state = person.monitor_state
                    exception['pedestrian'] = person.is_dead
                    if monitor_pedestrian_state in (2,3,4):
                        if person.state[2] in (-pi/2, pi/2):
                            v_cross = 1
                        elif person.state[2] in (pi, 0):
                            h_cross = 1
                        if monitor_pedestrian_state == 4:
                            pedestrian_spec = 2
                        if monitor_pedestrian_state == 3:
                            pedestrian_spec = 3
                    if (person.state[0],person.state[1]) == person.destination:
                        options.pedestrian_to_pick = pedestrian_id + 20
                        #print('arrived')
                        pedestrian_spec = 1
                        
    # pedestrian_state(for fsm): -1- not appear
    #                             0- wait
    #                             1- walk                          
    if monitor_pedestrian_state == 0:
        pedestrian_state = -1
    elif monitor_pedestrian_state in (1,2):
        pedestrian_state = 1
    else:
        pedestrian_state = 0 
    
    ################################ Update and Generate Visuals ################################ 
    # highlight crossings
    vertical_lane_color = 'g' if vertical_walk_safe else 'r'
    horizontal_lane_color = 'g' if horizontal_walk_safe else 'r'
    if options.highlight_crossings:
        draw_crossings(ax, plt, vertical_lane_color, horizontal_lane_color)
    # update cars
    cars_to_keep = []
    update_cars(cars_to_keep, dt)
    vehicle_state = -1
    
    find_car = False
    for car in cars_to_keep:    
        if car.id == 0: #new car
            vehicle_id += 1
            car.id = vehicle_id
        if car.id == options.vehicle_to_pick:
            find_car = True
            all_components_monitor = all_components_monitor + [car]
            if car.state[0] < 1:
                vehicle_state = 0
                vehicle_spec = 2
            else:
                vehicle_state = 1
                if car.extract_primitive()== False:
                    #print('finish')
                    vehicle_spec = 1
                    all_components_monitor = []
                else:
                    prim_id,_ = car.extract_primitive()
                for person in global_vars.pedestrians_to_keep:
                    no_collision,_ = collision_free(person, car)
                    if not no_collision:
                        exception['vehicle'] = True

    if find_car == False and vehicle_id >= options.vehicle_to_pick:
        options.vehicle_to_pick = vehicle_id + 10
    
    current_state = [horizontal_light[0], vertical_light[0], pedestrian_state, vehicle_state] 
    # updae monitor
    monitor.draw_monitor(last_state, current_state, exception, prim_id, pedestrian_spec, vehicle_spec, observer)
    scheduler_monitor.draw_scheduler_table(cars_to_keep, [horizontal_light[0], vertical_light[0]], schedulerobserver, options.vehicle_to_pick, vehicle_state)
    last_state = current_state
    
    draw_cars(cars_to_keep, background)
    # show honk wavefronts
    if options.show_honks:
        show_wavefronts(ax, dt)
        honk_randomly(cars_to_keep)
    # show bounding boxes
    if options.show_boxes:
        plot_boxes(ax, cars_to_keep)
    # show license plates
    if options.show_plates:
        show_license_plates(ax, cars_to_keep)
    # show primitive ids
    if options.show_prims:
        show_prim_ids(ax, cars_to_keep)
    # show car ids
    if options.show_car_ids:
        show_car_ids(ax, cars_to_keep)
    # show primitive tubes
    if options.show_tubes:
        plot_tubes(ax, cars_to_keep)
    # show traffic light walls
    if options.show_traffic_light_walls:
        plot_traffic_light_walls(ax, traffic_lights)
    if options.show_boxes_monitor:
        plot_boxes_monitor(ax, all_components_monitor)
#     check for collisions and update pedestrian state
    check_for_collisions(cars_to_keep)
    draw_pedestrians(global_vars.pedestrians_to_keep, background) # draw pedestrians to background
    # update background
    the_intersection = [ax.imshow(background, origin="lower")] # update the stage
    background.close()
    background = intersection.get_background()
    the_observer = [ax2.imshow(observer)] # update the stage
    observer.close()
    observer = monitor.get_background()
    #add scheduler monitor
    the_scheduler = [ax3.imshow(schedulerobserver)] # update the stage
    schedulerobserver.close()
    schedulerobserver = scheduler_monitor.get_background()
    
    t1 = time.time()
    elapsed_time = (t1 - t0)
    all_artists = the_intersection + global_vars.cars_to_show + global_vars.crossing_highlights + global_vars.honk_waves + global_vars.boxes + global_vars.curr_tubes + global_vars.ids + global_vars.prim_ids_to_show + global_vars.walls + global_vars.show_traffic_lights + global_vars.walk_signs 
    print('{:.2f}'.format(global_vars.current_time)+'/'+str(options.duration) + ' at ' + str(int(1/elapsed_time)) + ' fps') # print out current time to 2 decimal places
    return all_artists + the_observer + the_scheduler

t0 = time.time()
animate(0)
t1 = time.time()
interval = (t1 - t0)
ani = animation.FuncAnimation(fig, animate, frames=int(options.duration/options.dt), interval=interval, blit=False, repeat=False)
if options.save_video:
    #Writer = animation.writers['ffmpeg']
    writer = animation.FFMpegWriter(fps = options.speed_up_factor*int(1/options.dt), metadata=dict(artist='Traffic Intersection Simulator'), bitrate=-1)
    now = str(datetime.datetime.now())
    ani.save('../movies/monitor' + now + '.avi', dpi=600, writer=writer)
plt.show()

