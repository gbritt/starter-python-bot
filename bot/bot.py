# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 09:20:27 2016

@author: gbrittingham
"""

import sys
import random
import os


with open('Responses.txt', 'r') as filestream:
    for line in filestream:
        currentline = line.split(",")
        
print(currentline)
