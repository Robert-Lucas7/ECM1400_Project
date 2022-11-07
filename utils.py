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


print(countvalue([1, 2, 3, 4, 5, 4], 4))
