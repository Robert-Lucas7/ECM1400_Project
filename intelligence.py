# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import numpy as np
from numpy.typing import ArrayLike
from matplotlib import pyplot as mat_plot

class NumpyQueue():
    """
    Creates a circular queue that is implemented with a NumPy array.
    """
    def __init__(self, size : int, type):
        """
        Args:
            size (int): The size of the queue.
            type: The type that the NumPy array should be initialised to.
        """
        self.data_type = type
        self.queue = np.empty(size, dtype=type)
        self.top_pointer = -1
        self.bottom_pointer = -1

    def Enqueue(self, item : any) -> None:
        """
        Adds an item to the tail of the queue.

        Args:
            item (any): The item to add to the queue

        Raises:
            Exception: The queue is full so an item cannot be added.
            ValueError: The item to be added to the queue is a different type to the type specified during the intialisation of the NumPy array 'queue'.
        """
        try:
            if isinstance(item, self.data_type): #if the item to be added is of the same type as the NumPy array 'queue'.
                if self.IsEmpty():
                    self.top_pointer = 0
                    self.bottom_pointer = 0
                elif self.IsFull():
                    raise Exception("Cannot add item: Queue is full.")
                else:
                    self.top_pointer = (self.top_pointer + 1) % self.queue.size # The top (tail) pointer should 'loop' around the end of the array as the queue is circular.
                self.queue[self.top_pointer] = item
            else:
                raise ValueError("Element to be added to the queue must be of the specified type during intialisation.")
        except Exception as e:
            print(e)
        
    def Dequeue(self) -> any:
        """
        Removes and returns an item from the head of the queue.

        Raises:
            Exception: An item cannot be removed from the queue as it is empty.

        Returns:
            any: The item at the head of the queue that has just been removed.
        """
        try:
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
        except Exception as e:
            print(e)

    def IsEmpty(self) -> bool:
        """
        A check for if the queue is empty.

        Returns:
            bool: A boolean value that indicates whether the queue is empty (True = queue is empty, False = queue is NOT empty).
        """
        if self.bottom_pointer == -1 and self.top_pointer == -1:
            return True
        else:
            return False
    def IsFull(self) -> bool:
        """
        A check for if the queue is full.

        Returns:
            bool: A boolean value that indicates whether the queue is full (True = queue is full, False = queue is NOT full).
        """
        if (self.top_pointer + 1) % self.queue.size == self.bottom_pointer:
            return True
        else:
            return False
def validate_filename(filename : str) -> bool:
    """
    Validates a given filename to see if it is suitable to use.

    Args:
        filename (str): The filename to validate.

    Returns:
        bool: True = the file is valid to use, False = the file is NOT valid to use.
    """
    if ['<', '>', ':', '"', "/", '\\', '|', '?', '*'] in filename:
        return False
    for c in filename:
        if int(c) >= 0 and int(c) <= 31: #if the ASCII value of the character is between 0 and 31, it is invalid
            return False
    #Check if jpg, regex search/ match?????
def find_red_pixels(map_filename : str, upper_threshold : int = 100, lower_threshold : int = 50) -> np.ndarray:
    """
    Returns and saves a 2D array of where the red pixels occur in an image.

    Args:
        map_filename (str): The name of the file that will contain where red pixels occur.
        upper_threshold (int, optional): The upper threshold of to decide if a pixel is a red colour (0 - 255). Defaults to 100.
        lower_threshold (int, optional): The lower threshold of to decide if a pixel is a red colour (0 - 255). Defaults to 50.

    Returns:
        ndarray: A 2D array that contains a 255 if a red pixel is at that location or a 0 otherwise.
    """
    try:
        if not validate_filename(map_filename):
            raise ValueError("The map_filename is invalid")
        if not isinstance(map_filename, str) or not isinstance(upper_threshold, int) or not isinstance(lower_threshold, int): #check if default arguments already define the type of the object.
            raise ValueError("The arguments are not of the correct type")
        if (upper_threshold < 0 and upper_threshold > 255) or (lower_threshold < 0 and lower_threshold > 255):
            raise ValueError("The upper_threshold and/or lower_threshold arguments are not in the correct range (0 - 255)")
        
        rgb_img = mat_plot.imread(f'./data/{map_filename}') * 255 # Scales the image returned to have the colour values range from 0 to 255 (to avoid rounding errors)
        red_pixels = np.zeros(rgb_img.shape[:2])
        for row in range(rgb_img.shape[0]): #iterating over every element in the 2D array rgb_img
            for col in range(rgb_img.shape[1]):
                red =rgb_img[row,col][0]
                green = rgb_img[row,col][1]
                blue = rgb_img[row, col][2]
                if red > upper_threshold and green < lower_threshold and blue < lower_threshold: #if conditions met, then pixel is deemed to be red.
                    red_pixels[row, col] = 255 #255 represents white
        mat_plot.imsave('./data/map-red-pixels.jpg', red_pixels, cmap="gray")
        return red_pixels

    except Exception as e:
        print(e)
#find_red_pixels("map.png")
def find_cyan_pixels(map_filename : str, upper_threshold : int = 100, lower_threshold : int = 50) -> np.ndarray:
    """
    Returns and saves a 2D array of where the red pixels occur in an image.

    Args:
        map_filename (str): The name of the file that will contain where cyan pixels occur.
        upper_threshold (int, optional): The upper threshold of to decide if a pixel is a cyan colour (0 - 255). Defaults to 100.
        lower_threshold (int, optional): The lower threshold of to decide if a pixel is a cyan colour (0 - 255). Defaults to 50.

    Returns:
        ndarray: A 2D array that contains a 255 if a cyan pixel is at that location or a 0 otherwise.
    """
    try:
        if not validate_filename(map_filename):
            raise ValueError("The map_filename is invalid")
        if not isinstance(map_filename, str) or not isinstance(upper_threshold, int) or not isinstance(lower_threshold, int): #check if default arguments already define the type of the object.
            raise ValueError("The arguments are not of the correct type")
        if (upper_threshold < 0 and upper_threshold > 255) or (lower_threshold < 0 and lower_threshold > 255):
            raise ValueError("The upper_threshold and/or lower_threshold arguments are not in the correct range (0 - 255)")
        rgb_img = mat_plot.imread(f'./data/{map_filename}') * 255 # returns rgba [red, green, blue, aplha]
        cyan_pixels = np.zeros(rgb_img.shape[:2])# using 3 as saving as a jpg not png so doesn't need the alpha.
        for row in range(rgb_img.shape[0]):
            for col in range(rgb_img.shape[1]):
                red =rgb_img[row,col][0]
                green = rgb_img[row,col][1]
                blue = rgb_img[row, col][2]
                if red < lower_threshold and green > upper_threshold and blue > upper_threshold: #pixel is deemed to be red.
                    cyan_pixels[row, col] = 255
        mat_plot.imsave('./data/map-cyan-pixels.jpg', cyan_pixels, cmap='gray')
        return cyan_pixels
    except Exception as e:
        print(e)
#find_cyan_pixels('map.png')

def find_pixel_neighbours(pixel_location : tuple[int, int], img_shape : tuple[int, int]) -> list[tuple[int, int]]:
    """
    Returns the 8-adjacent neighbours of a pixel at the location defined (pixel_location) by checking if the pixel is at an edge of the image.

    Args:
        pixel_location (tuple[int, int]): The pixel location in the form (row, column).
        img_shape (tuple[int, int]): The shape of the image in the form (rows, columns).

    Raises:
        Exception: The pixel_location argument is outside of the image.

    Returns:
        list[tuple[int, int]]: a list of the positions of the 8-adjacent neighbours of the pixel.
    """
    eight_neighbours = []
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

def detect_connected_components(IMG : ArrayLike) -> np.ndarray:#2 pixels (p, q) are connected if q is in the set of N8(p)
    """
    Returns all 8-connected components in the image, defined in a 2D array, and saves the connected components and sizes to a text file.

    Args:
        IMG (ArrayLike): A binary image as a 2D array.

    Returns:
        ndarray: A 2D ndarray which has a number in each position that indicates which connected component it is associated with (excluding 0 as it indicates that there is no conencted component at that position).
    """
    MARK = np.zeros(IMG.shape[:2], dtype=int) # The shape of MARK is the first two elements in the shape of the image as the RGB/ RGBA values are not needed.
    queue = NumpyQueue(IMG.shape[0] * IMG.shape[1], object)
    cc_number = 1
    for row in range(IMG.shape[0]):
        for col in range(IMG.shape[1]):
            if IMG[row, col] == 255 and MARK[row, col] == 0:
                MARK[row, col] = cc_number #Modification - so that you can find the size and number associated with the connected component.
                queue.Enqueue((row, col))
                while not queue.IsEmpty(): 
                    first_item = queue.Dequeue()
                    eight_neighbours = find_pixel_neighbours(first_item, IMG.shape)
                    for neighbour in eight_neighbours:
                        if IMG[neighbour] == 255 and MARK[neighbour] == 0: #If both the neighbour is a pavement and has not been visited, mark it as visited and add it to the queue.
                            MARK[neighbour] = cc_number
                            queue.Enqueue(neighbour)
                cc_number += 1 #It will look for the next connected component so increment the number of the connected component by 1.
    connected_components = get_connected_components_from_MARK(MARK)
    save_connected_components_to_file(connected_components, 'cc-output-2a')
    return MARK



def get_connected_components_from_MARK(MARK : ArrayLike) -> list[tuple[int, int]]:
    """
    Returns the connected components from MARK as a list of tuples in the form (connected_component_number, connected_component_size).

    Args:
        MARK (ArrayLike): A 2D array which has a number in each position that indicates which connected component it is associated with (excluding 0 as it indicates that there is no conencted component at that position). 

    Returns:
        list[tuple[int, int]]: list of tuples that contain the connected component's number and size respectively.
    """
    connected_component_dict = {}
    for row in range(MARK.shape[0]):#Iterates over the MARK array and if the number (excluding 0) is present in the dictionary then increment it's value by 1, otherwise add the number as the key to the dictionary.
        for col in range(MARK.shape[1]):
            if MARK[row, col] != 0:
                if MARK[row, col] not in connected_component_dict.keys():
                    connected_component_dict[MARK[row, col]] = 1
                else:
                    connected_component_dict[MARK[row, col]] += 1
    return list(connected_component_dict.items())

def save_connected_components_to_file(connected_components : list[tuple[int, int]], filename : str) -> None:
    """
    Saves the list of tuples in the form (connected_component_number, connected_component_size) to a text file

    Args:
        connected_components (list[tuple[int, int]]): list of conencted components in the form [(connected_component_number, connected_component_size)].
        filename (str): the name of the file to save the list of connected components in. 
    """
    #===================== VALIDATE FILENAME HERE =========================
    #======================================================================
    with open(f'./data/{filename}.txt', 'w') as f:
        for number, size in connected_components:
            f.write(f"Connected Component {number}, number of pixels = {size}\n")
        f.write(f"Total number of connected components = {len(connected_components)}")

def detect_connected_components_sorted(MARK : ArrayLike ) -> None: #Finds connected components from 2D array MARK and sorts them in decreasing order.
    
    #======== VALIDATE INPUT ARRAY IS 2D ===================
    #=======================================================
    
    connected_components = get_connected_components_from_MARK(MARK)
    
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
#detect_connected_components_sorted(detect_connected_components(find_red_pixels('map.png')))
