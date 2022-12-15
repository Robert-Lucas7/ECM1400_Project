# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification


from types import NoneType
import numpy


def sumvalues(values: list):
    """
    This function sums the values in a list/ array. If a non-numerical value is in the list/array then an exception will be raised.\n
    Args:
        values(list) : list of int or float
    """
    total = 0
    for item in values:

        if type(item) in [int, float, numpy.float64]:
            total += item
        else:
            raise TypeError("An element in the list/array has an incorrect type.")

    return total
    



# print(sumvalues([1, 2.0, "3.15", 4, 5]))


def maxvalue(values: list) -> int:
    """
    Returns the index of the maximum value in a list of numerical values. If there are repeated maximum values, then the index of the first occurence of this value will be returned.\n
    Args:
        values : list of int or float
    """
    # Check if the list is empty
    if len(values) != 0:
        maxVal = None #These will be changed as there will be at least 1 value in the list.
        maxValIndex = 0
        for i in range(0, len(values)):
            # Validate element data type
            if type(values[i]) in [int, float]:
                    if not maxVal:
                        maxVal = values[i]
                        maxValIndex = i
                    elif values[i] > maxVal:
                        maxVal = values[i]
                        maxValIndex = i
            elif type(values[i]) == NoneType:
                pass
            else:
                raise TypeError("An element in the list/array has an incorrect type.")
        return maxValIndex
    else:
        raise ValueError("The List is empty so there is not a maximum value")


# print(maxvalue([1, 2, 1, "2", 5]))


def minvalue(values : list):
    """
    Returns the index of the minimum value in a list of numerical values. If there are repeated minimum values, then the index of the first occurence of this value will be returned.\n
    Args:
        values : list of int or float
    """
    # Check if the list is empty
    length = len(values)
    if length != 0:

        for i in range(0, length):
            # Validate element data type
            if type(values[i]) in [int, float, numpy.float64]:
                if i == 0:
                    minValIndex = 0  # As this will be the highest value at the start
                    minVal = values[0]
                if values[i] < minVal:
                    minVal = values[i]
                    minValIndex = i
            else:
                raise TypeError("An element in the list/array has an incorrect type.")
        return minValIndex
    else:
        raise ValueError("The List is empty so there is not a maximum value")


# print(minvalue([1, 2, 1, 2, 5, -20]))


def meannvalue(values):
    """Returns the mean value from a list/ array of numeric values. 
    Args:
        values : list of int or float"""
    total = sumvalues(values) #Suitable exceptions will be raised here if values is in the incorrect form.
    return total / len(values)


def countvalue(values, x):
    """ Returns the number of occurences of a value x in a list/ array
    Args:
        values : list
        x : any"""
    count = 0
    for item in values:
        if isinstance(item, type(x)) and item == x:
            count += 1
    return count


def find_median(values: list):
    '''Returns the median value of a list of values.

    Args:
        values (list) : list of numeric values
    '''
    sorted_values = insertion_sort(values)
    # even number of elements in the list. e.g. [1,2,3,4,5,6]
    if len(sorted_values) % 2 == 0:
        right_most_middle_element = len(sorted_values) / 2
        return (sorted_values[right_most_middle_element] + sorted_values[right_most_middle_element - 1]) / 2
    else:  # odd number of elements in the list. e.g. [1,2,3,4,5]
        # the index will always be an integer as 1 less of an odd number is even.
        return sorted_values[int((len(sorted_values) - 1)/2)]

    # then going from either end go to the centre (could use recursion - base case len(list) == 1 or len(list) == 2)


def insertion_sort(values: list) -> list:
    '''Returns a sorted list of values by using the insertion sort algorithm.
    
    Args:
        values(list): a list of numeric values (int or float)

    Returns:
        list: a sorted list in ascending order.
    '''
    for i in range(1, len(values)):
        found_location = False
        count = 0
        # i - count != 0 is to test if the start of the list has been reached.
        while (not found_location and (i - count) != 0):
            if type(values[i - count]) in [float, int, numpy.float64] and type(values[i - count - 1]) in [float, int, numpy.float64]:
                if values[i - count] < values[i - count - 1]:
                    temp = values[i - count - 1]
                    values[i - count - 1] = values[i - count]
                    values[i - count] = temp
                    count += 1
                else:
                    found_location = True
            else:
                raise TypeError("List of values contains an item(s) of the incorrect type.")
    return values

