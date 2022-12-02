# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import numpy as np
from matplotlib import pyplot as mat_plot

def find_red_pixels(map_filename, upper_threshold = 100, lower_threshold = 50):
    """Your documentation goes here"""
    rgb_img = mat_plot.imread('./data/map.png') # returns rgba [red, green, blue, aplha]
    rgb_img *= 255
    print(rgb_img)
    #mat_plot.imshow(rgb_img)
    #mat_plot.show()
find_red_pixels('map.png')
def find_cyan_pixels(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here


def detect_connected_components(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def detect_connected_components_sorted(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

