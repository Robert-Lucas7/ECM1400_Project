# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import numpy as np
from matplotlib import pyplot as mat_plot


def find_red_pixels(map_filename, upper_threshold = 100, lower_threshold = 50):
    """
    Returns and saves a 2D array of where the red pixels occur in an image.
    """
    #=============VALIDATE map_filename =======================
    #==========================================================
    rgb_img = mat_plot.imread(f'./data/{map_filename}') * 255 # returns rgba [red, green, blue, aplha]
    shape = rgb_img.shape
    red_pixels = np.zeros((shape[0], shape[1]))# using 3 as saving as a jpg not png so doesn't need the alpha.
    for row in range(shape[0]):
        for col in range(shape[1]):
            red =rgb_img[row,col][0]
            green = rgb_img[row,col][1]
            blue = rgb_img[row, col][2]
            if red > upper_threshold and green < lower_threshold and blue < lower_threshold: #pixel is deemed to be red.
                red_pixels[row, col] = 0
            else:
                red_pixels[row, col] = 1
    mat_plot.imsave('./data/map-red-pixels.jpg', red_pixels, cmap='Greys')
    return red_pixels

def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    Returns and saves a 2D array of where the cyan pixels occur in an image.
    """
    rgb_img = mat_plot.imread(f'./data/{map_filename}') * 255 # returns rgba [red, green, blue, aplha]
    shape = rgb_img.shape
    cyan_pixels = np.zeros((shape[0], shape[1]))# using 3 as saving as a jpg not png so doesn't need the alpha.
    for row in range(shape[0]):
        for col in range(shape[1]):
            red =rgb_img[row,col][0]
            green = rgb_img[row,col][1]
            blue = rgb_img[row, col][2]
            if red < lower_threshold and green > upper_threshold and blue > upper_threshold: #pixel is deemed to be red.
                cyan_pixels[row, col] = 0
            else:
                cyan_pixels[row, col] = 1
    mat_plot.imsave('./data/map-cyan-pixels.jpg', cyan_pixels, cmap='Greys')
    return cyan_pixels
find_cyan_pixels('map.png')

def detect_connected_components(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def detect_connected_components_sorted(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

