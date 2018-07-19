#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 11:30:01 2018

@author: kevin
"""

import sys
sys.path.append('/home/tug74186/Development/bubble_analysis')
import os
import pandas as pd
from skimage.io import imsave, imread
from skimage.draw import circle, circle_perimeter
import numpy as np

BASE_DIR = '/mnt/tmp/Bubble images/Dataset_1'
extensions = ['test#2 20ppm MIBC/Result # 2 20ppm', 'test#3 20ppm MIBC/Result # 3 20ppm', 'test#4 20ppm MIBC/Result test # 4 20ppm', 'test#6 20ppm MIBC/Result test # 6 20ppm', 'test#7 20ppm MIBC/Result test # 7 20ppm', 'test#8 20ppm MIBC/Result test # 8 20ppm', 'test#9 20ppm MIBC/Result test # 9 20ppm', 'test#10 20ppm MIBC/Result test # 10 20ppm']

image_dirs = [os.path.join(BASE_DIR, d) for d in extensions]
image_paths = []
for image_dir in image_dirs:
    for f in filter(lambda x: 'bmp' in x, os.listdir(image_dir)):
        image_paths.append(os.path.join(image_dir, f))


for image_path in image_paths:
    try:
        circles = pd.read_csv(image_path[:-3] + 'csv')
    except IOError:
        print "IOError"
        continue
    image = imread(image_path)
    height, width = image.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    x, y, radiuses = circles['X'], circles['Y'], circles['Radius']
    for row in range(len(x)):
        rr, cc = circle(y[row], x[row], radiuses[row],      shape=image.shape[:2])
        mask[rr, cc] = 1000
    imsave(image_path[:-3] + 'png', mask, as_gray=True)
    #rr, cc = circle_perimeter(y[row], x[row], radiuses[row], shape=image.shape[:2])
    #mask[rr, cc] = 300
    #imsave(image_path[:-4]+'_with_perimeters.png', mask, as_gray=True)

                      