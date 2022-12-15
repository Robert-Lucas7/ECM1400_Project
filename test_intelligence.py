from intelligence import *
import pytest

def test_validate_filename_incorrect_characters():
    with pytest.raises(ValueError):
        validate_filename("filename\\text")
def test_validate_filename_incorrect_type():
    with pytest.raises(TypeError):
        validate_filename(999)

def test_validate_colour_thresholds_incorrect_type():
    with pytest.raises(TypeError):
        validate_colour_thresholds('s', True)
def test_validate_colour_thresholds_out_of_range():
    with pytest.raises(ValueError):
        validate_colour_thresholds(256, -1)

def test_find_pixel_neighbours():
    assert find_pixel_neighbours((0,0), (3,3)) == [(0, 1), (1,0), (1,1)]

def test_validate_2D_array_():
    with pytest.raises(ValueError):
        validate_2D_array([1,2,3,4,5])

