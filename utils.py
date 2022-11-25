# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification


def sumvalues(values: list):
    """
    This function sums the values in a list/ array. If a non-numerical value is in the list/array then an exception will be raised.\n
    Parameters
    ----------
    values : list of int or float
    """
    total = 0
    for item in values:

        if type(item) in [int, float]:
            total += item
        else:
            raise TypeError(
                "An element in the list/array has an incorrect type.")

    return total


# print(sumvalues([1, 2.0, "3.15", 4, 5]))


def maxvalue(values: list):
    """
    Returns the index of the maximum value in a list of numerical values. If there are repeated maximum values, then the index of the first occurence of this value will be returned.\n
    Parameters
    ----------
    values : list of int or float
    """
    # Check if the list is empty
    length = len(values)
    if length != 0:

        for i in range(0, length):
            # Validate element data type
            if type(values[i]) in [int, float]:
                if i == 0:
                    maxValIndex = 0  # As this will be the highest value at the start
                    maxVal = values[0]
                if values[i] > maxVal:
                    maxVal = values[i]
                    maxValIndex = i
            else:
                raise TypeError(
                    "An element in the list/array has an incorrect type.")
        return maxValIndex
    else:
        raise Exception("The List is empty so there is not a maximum value")


# print(maxvalue([1, 2, 1, "2", 5]))


def minvalue(values):
    """
    Returns the index of the minimum value in a list of numerical values. If there are repeated minimum values, then the index of the first occurence of this value will be returned.\n
    Parameters
    ----------
    values : list of int or float
    """
    # Check if the list is empty
    length = len(values)
    if length != 0:

        for i in range(0, length):
            # Validate element data type
            if type(values[i]) in [int, float]:
                if i == 0:
                    minValIndex = 0  # As this will be the highest value at the start
                    minVal = values[0]
                if values[i] < minVal:
                    minVal = values[i]
                    minValIndex = i
            else:
                raise TypeError(
                    "An element in the list/array has an incorrect type.")
        return minValIndex
    else:
        raise Exception("The List is empty so there is not a maximum value")


# print(minvalue([1, 2, 1, 2, 5, -20]))


def meannvalue(values):
    """
    Returns the mean value from a list/ array of numeric values. 
    Parameters
    ----------
    values : list of int or float
    """
    total = sumvalues(values)
    return total / len(values)


def countvalue(values, x):
    """
    Returns the number of occurences of a value x in a list/ array
    Parameters
    ----------
    values : list of int or float
    x : int or float
    """
    count = 0
    for item in values:
        if item == x:
            count += 1
    return count

def find_median(values : list):
    '''
    Find the median value of a list of values.
    '''
    sorted_values = insertion_sort(values)
    if len(sorted_values) % 2 == 0: #even number of elements in the list. e.g. [1,2,3,4,5,6]
        right_most_middle_element = int(len(sorted_values) /2)
        return (sorted_values[right_most_middle_element] + sorted_values[right_most_middle_element - 1]) / 2
    else: #odd number of elements in the list. e.g. [1,2,3,4,5]
        return sorted_values[int((len(sorted_values) - 1)/2)] #the index will always be an integer as 1 less of an odd number is even.


    #then going from either end go to the centre (could use recursion - base case len(list) == 1 or len(list) == 2)
def insertion_sort(values : list) -> list:
    '''
    Returns a sorted list of values by using the insertion sort algorithm.\n
    Parameters
    ----------
    values - a list of numeric values (int or float)
    '''
    for i in range(1,len(values)): 
        found_location = False
        count = 0
        while (not found_location and (i - count) != 0): # i - count != 0 is to test if the start of the list has been reached.
            if values[i - count] < values[i - count - 1]:
                temp = values[i - count - 1]
                values[i - count - 1] = values[i - count]
                values[i - count] = temp
                count += 1
            else:
                found_location = True
    return values
#print(find_median([1,3,2,5,4,4]))# 1,2,3,4,4,5
#print(insertion_sort([1,4,7,9,4,2,3,7,8,5,6,0]))
#print(countvalue([1, 2, 3, 4, 5, 4], 4))
