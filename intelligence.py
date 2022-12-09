# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import numpy as np
from matplotlib import pyplot as mat_plot
from utils import insertion_sort
class NumpyQueue():
    def __init__(self, size, type):
        self.data_type = type
        self.queue = np.empty(size, dtype=type)
        self.top_pointer = -1
        self.bottom_pointer = -1

    def Enqueue(self, item):
        if isinstance(item, self.data_type):
            if self.IsEmpty():
                self.top_pointer = 0
                self.bottom_pointer = 0
            elif self.IsFull():
                raise Exception("Cannot add item: Queue is full.")
            else:
                self.top_pointer = (self.top_pointer + 1) % self.queue.size
            self.queue[self.top_pointer] = item
        else:
            raise Exception("Element to be added to the queue must be of the specified type during intialisation.")
    def Dequeue(self):
        if self.IsEmpty():
            raise Exception("Cannot dequeue item: Queue is empty.")
        elif self.bottom_pointer == self.top_pointer:
            item = self.queue[self.bottom_pointer]
            self.bottom_pointer = -1
            self.top_pointer = -1
            return item
        else:
            self.bottom_pointer = (self.bottom_pointer + 1) % self.queue.size
            return self.queue[self.bottom_pointer]
    def IsEmpty(self):
        if self.bottom_pointer == -1 and self.top_pointer == -1:
            return True
        else:
            return False
    def IsFull(self):
        if (self.top_pointer + 1) % self.queue.size == self.bottom_pointer:
            return True
        else:
            return False
    def Show(self):
        print(self.queue)


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
                red_pixels[row, col] = 0 #0 is white for matplotlib 'greys' colourmap
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
#find_cyan_pixels('map.png')

def find_pixel_neighbours(pixel_location, img_shape):
    #if statements to check if the current pixel is one of the edge pixels.
    eight_neighbours = []
    #print(f"Pixel location: {pixel_location}")
    row = pixel_location[0]
    col = pixel_location[1]
    #Validating whether the pixel_location is within the image size boundaries.
    if row < 0 or row >= img_shape[0] or col < 0 or col >= img_shape[1]:
        raise Exception("Pixel location is outside the image.")

    if col != 0 and row != 0:#If pixel not top left, add top-left diagonal pixel
        eight_neighbours.append((row - 1, col - 1))
    if row != 0:#If pixel not in first row, add neighbour pixel directly above it.
        eight_neighbours.append((row - 1, col))
    if row !=0 and col != img_shape[1] - 1:#If pixel not top right, add top-right diagonal pixel
        eight_neighbours.append((row - 1, col + 1))
    
    if col != 0:# If pixel isn't to the left, add left neighbour pixel
        eight_neighbours.append((row, col - 1))
    if col != img_shape[1] - 1:# If pixel isn't to the right, add right neighbour pixel
        eight_neighbours.append((row, col + 1))
    
    if row != img_shape[0] - 1 and col != 0:# If pixel isn't in the bottom left corner, add pixel diagonally bottom left.
        eight_neighbours.append((row + 1, col - 1))
    if row != img_shape[0] - 1:#If pixel isn't at the bottom, add the pixel below it
        eight_neighbours.append((row + 1, col))
    if row != img_shape[0] - 1 and col != img_shape[1] - 1: #If pixel isn't in the bottom right, add pixel diagonally bottom-right.
        eight_neighbours.append((row + 1, col + 1))
    return eight_neighbours

def detect_connected_components(IMG):#2 pixels (p, q) are connected if q is in the set of N8(p)
    """
    Returns all 8-connected components in the image as a 2D array.
    """
    shape = IMG.shape
    MARK = np.zeros((shape[0], shape[1]), dtype=int)
   
    queue = NumpyQueue(shape[0] * shape[1], object)
    cc_number = 1
    for row in range(shape[0]):
        for col in range(shape[1]):
            if IMG[row, col] == 0 and MARK[row, col] == 0:# IMG[row, col] == 0 (if pixel is white - representing a pavement) - change to 1 for white
                MARK[row, col] = cc_number #Modification
                queue.Enqueue((row, col))
                
                while not queue.IsEmpty(): #like a breadth first search
                    first_item = queue.Dequeue()
                    eight_neighbours = find_pixel_neighbours(first_item, shape)
                    for neighbour in eight_neighbours:
                        if IMG[neighbour] == 0 and MARK[neighbour] == 0:
                            MARK[neighbour] = cc_number
                            queue.Enqueue(neighbour)
                #connected_component_number_and_size.append((connected_component_number, connected_component_size))
                cc_number += 1
    connected_components = get_connected_components_from_MARK(MARK)
    save_connected_components_to_file(connected_components, 'cc-output-2a')
    return MARK

def get_connected_components_from_MARK(MARK):
    connected_component_dict = {}
    for row in range(MARK.shape[0]):
        for col in range(MARK.shape[1]):

            if MARK[row, col] != 0:
                if MARK[row, col] not in connected_component_dict.keys():
                    connected_component_dict[MARK[row, col]] = 1
                else:
                    connected_component_dict[MARK[row, col]] += 1
    return list(connected_component_dict.items())

def save_connected_components_to_file(connected_components : list[tuple], filename : str): #connected_components in form: [(component_number, component_size), ...]
    with open(f'./data/{filename}.txt', 'w') as f:
        for number, size in connected_components:
            f.write(f"Connected Component {number}, number of pixels = {size}\n")
        f.write(f"Total number of connected components = {len(connected_components)}")

def detect_connected_components_sorted(MARK): #Finds connected components from 2D array MARK and sorts them in decreasing order.
    """"""
    #======== VALIDATE INPUT ARRAY IS 2D ===================
    #=======================================================
    #_, connected_component_numbers_and_sizes = get_connected_components(MARK)
    #print(connected_component_numbers_and_sizes)
    #Sort connected_component_sizes in decreasing order
    connected_components = get_connected_components_from_MARK(MARK)
    #print(connected_components)
    #Sort connected components based on size
    #sorted_component_sizes = insertion_sort([x[1] for x in connected_components])
    values = connected_components
    for i in range(1, len(values)):
        found_location = False
        count = 0
        # i - count != 0 is to test if the start of the list has been reached.
        while (not found_location and (i - count) != 0):
            if values[i - count][1] >= values[i - count - 1][1]:
                temp = values[i - count - 1]
                values[i - count - 1] = values[i - count]
                values[i - count] = temp
                count += 1
            else:
                found_location = True

    save_connected_components_to_file(values, 'cc-output-2b')
    two_biggest_components = [x[0] for x in values[:2]]
    print(two_biggest_components)
    two_biggest_components_arr = np.full(MARK.shape, 1)#np.zeros((MARK.shape[0], MARK.shape[1]))
    for row in range(MARK.shape[0]):
        for col in range(MARK.shape[1]):
            if MARK[row, col] in two_biggest_components:
                two_biggest_components_arr[row, col] = 0
    print(two_biggest_components_arr)
    mat_plot.imsave('./data/cc-top-2.jpg', two_biggest_components_arr ,cmap="Greys")




def merge(right, left):
    pass
def merge_sort(L):
    if len(L) < 2:
        return L
    else:
        middle = len(L) // 2
        left = merge_sort(L[:middle])
        right = merge_sort(L[middle:])
        return merge(right, left)

#print(merge_sort([1,2,3,4,3,2,1]))
detect_connected_components_sorted(detect_connected_components(find_red_pixels('map.png')))
