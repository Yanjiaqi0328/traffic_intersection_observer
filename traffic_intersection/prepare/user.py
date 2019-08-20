#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Aug 2019

@author: Jiaqi Yan
"""

import threading
import sys

# set a new thread to read user's input
class Read_user_command(threading.Thread):
    index = 0
    #input_str=""

    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while 1:
            input_key = str(sys.stdin.readline()).strip("\n")
            if input_key =='s':   # the user input 's' if he wants to choose/change the vehicle to monitor 
                self.index = 1
                print('You have requested to monitor a vehicle! ')
