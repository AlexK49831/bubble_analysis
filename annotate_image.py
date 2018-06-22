import config
import pandas as pd
import numpy as np
import os
import math

base_dir = config.IMAGE_BASE_DIR

def annotate_image(path):
    if '.xls' in path:
        return annotate_xls(path)
    elif '.csv' in path:
        return annotate_csv(path)



def annotate_xls(path):
    ret_dict = {}
    bubble_number = "0"
    df = pd.read_excel(os.path.join(base_dir, path), 'Bubble data')
    df = df[1:]
    df.reset_index(inplace=True)
    df.rename(columns={'Center Coord':'X', 'Center Coord.1':'Y', 'Bubble Radius':'Radius'}, inplace=True)
    for bubble_number in range(len(df)):
        # Equation of a circle is (x - h)^2 + (y - k)^2 = r^2
        h = df['X'][bubble_number]
        k = df['Y'][bubble_number]
        r = df['Radius'][bubble_number]
        # Sample 200 random values within a uniform distribution of the circle's possible x values
        random_x_vals = np.random.uniform(low=(h-r), high=(h+r), size=200)
        # x_vals and y_vals are going to be the actual values. For every random x, we have 4 points,
        # name the x and it's corresponding pos/neg y, and the opposite x and it's 2 corresponding y vals
        x_vals = np.ndarray(800)
        y_vals = np.ndarray(800)
        #Initialize first 4 x_vals to be the left-most, right-most, and center points on the circle
        x_vals[0] = h + r
        x_vals[1] = h - r
        x_vals[2] = h
        x_vals[3] = h
        # Initialize first 4 y_vals to be center, center, upper-most, and lower-most points on circle.
        y_vals[0] = k
        y_vals[1] = k
        y_vals[2] = k + r
        y_vals[3] = k - r
        # Each iteration of the loop takes one random_x_val, so we skip every 4 to accommodate.
        for i in range(4, len(x_vals), 4):
            x_vals[i] = random_x_vals[math.floor(i/4)]
            if random_x_vals[math.floor(i/4)] > h:
                x_vals[i+1] = random_x_vals[math.floor(i/4)] - 2 * (random_x_vals[math.floor(i/4)] - h)
            else:
                x_vals[i+1] = random_x_vals[math.floor(i/4)] + 2 * (h - random_x_vals[math.floor(i/4)])
            x_vals[i+2] = x_vals[i]
            x_vals[i+3] = x_vals[i+1]
        for index in range(4, len(x_vals), 4):
            x = x_vals[index]
            pos, neg = quadratic_solver(1, -1*(2*k), x**2 - 2*h*x + h**2 + k**2 - r**2)            
            y_vals[index] = pos
            y_vals[index+1] = pos
            y_vals[index+2] = neg  
            y_vals[index+3] = neg  
        ret_dict.update({str(bubble_number) : dict(all_points_x=x_vals.tolist(), all_points_y=y_vals.tolist(), name='polygon')})
    new_ret = dict(regions=ret_dict)
    new_ret.update(dict(filename=path[:-4]+'.bmp'))
    return new_ret


def annotate_csv(path):
    ret_dict = {}
    bubble_number = "0"
    df = pd.read_csv(os.path.join(base_dir, path))
    for bubble_number in range(len(df)):
        # Equation of a circle is (x - h)^2 + (y - k)^2 = r^2
        h = df['X'][bubble_number]
        k = df['Y'][bubble_number]
        r = df['Radius'][bubble_number]
        # Sample 200 random values within a uniform distribution of the circle's possible x values
        random_x_vals = np.random.uniform(low=(h-r), high=(h+r), size=200)
        # x_vals and y_vals are going to be the actual values. For every random x, we have 4 points,
        # name the x and it's corresponding pos/neg y, and the opposite x and it's 2 corresponding y vals
        x_vals = np.ndarray(800)
        y_vals = np.ndarray(800)
        #Initialize first 4 x_vals to be the left-most, right-most, and center points on the circle
        x_vals[0] = h + r
        x_vals[1] = h - r
        x_vals[2] = h
        x_vals[3] = h
        # Initialize first 4 y_vals to be center, center, upper-most, and lower-most points on circle.
        y_vals[0] = k
        y_vals[1] = k
        y_vals[2] = k + r
        y_vals[3] = k - r
        # Each iteration of the loop takes one random_x_val, so we skip every 4 to accommodate.
        for i in range(4, len(x_vals), 4):
            x_vals[i] = random_x_vals[math.floor(i/4)]
            if random_x_vals[math.floor(i/4)] > h:
                x_vals[i+1] = random_x_vals[math.floor(i/4)] - 2 * (random_x_vals[math.floor(i/4)] - h)
            else:
                x_vals[i+1] = random_x_vals[math.floor(i/4)] + 2 * (h - random_x_vals[math.floor(i/4)])
            x_vals[i+2] = x_vals[i]
            x_vals[i+3] = x_vals[i+1]
        for index in range(4, len(x_vals), 4):
            x = x_vals[index]
            pos, neg = quadratic_solver(1, -1*(2*k), x**2 - 2*h*x + h**2 + k**2 - r**2)            
            y_vals[index] = pos
            y_vals[index+1] = pos
            y_vals[index+2] = neg  
            y_vals[index+3] = neg  
        ret_dict.update({str(bubble_number) : dict(all_points_x=x_vals.tolist(), all_points_y=y_vals.tolist(), name='polygon')})
    new_ret = dict(regions=ret_dict)
    new_ret.update(dict(filename=path[:-4]+'.bmp'))
    return new_ret




def quadratic_solver(a, b, c):
    """Function to Solve a quadratic formula, given it's 3 coefficients.
        Returns the two possible values (plus or minus)"""
    positive = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
    negative = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
    return positive, negative
