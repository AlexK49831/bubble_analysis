# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:38:17 2018

@author: tug74186
"""

import pandas as pd
import os

# Get all bubble images, and not masks
BASE_DIR = '/mnt/tmp/Bubble images/Dataset_1'
extensions = ['test#2 20ppm MIBC/Result # 2 20ppm/', 'test#3 20ppm MIBC/Result # 3 20ppm/', 'test#4 20ppm MIBC/Result test # 4 20ppm', 'test#6 20ppm MIBC/Result test # 6 20ppm', 'test#7 20ppm MIBC/Result test # 7 20ppm']

paths = []
for extension in extensions:
    paths = paths + [os.path.join(BASE_DIR, extension, f) for f in os.listdir(os.path.join(BASE_DIR, extension))]
paths = filter(lambda x: '.csv' in x, paths)

# Loop through all images
for path in paths:
    circles = pd.read_csv(os.path.join(BASE_DIR, path))
    # Read in circles dataframe, and set up dataFrame for annotations
    annotations = pd.DataFrame(columns=['filename', 'width', 'height', 'class', 'xmin', 'xmax', 'ymin', 'ymax'])
    # Loop through all the bubbles, and set the annotations df with appropriate values
    for row in range(len(circles)):
        annotations.set_value(row, 'filename', path)
        annotations['width'].iloc[row] = 1392
        annotations['height'].iloc[row] = 1040
        annotations['class'].iloc[row] = 'bubble'
        annotations['xmin'].iloc[row] = circles['X'].iloc[row] - circles['Radius'].iloc[row]
        annotations['xmax'].iloc[row] = circles['X'].iloc[row] + circles['Radius'].iloc[row]
        annotations['ymin'].iloc[row] = circles['Y'].iloc[row] - circles['Radius'].iloc[row]
        annotations['ymax'].iloc[row] = circles['Y'].iloc[row] + circles['Radius'].iloc[row]
    annotations.to_csv(os.path.join('/mnt/tmp/bubbles/train', path), index=False)