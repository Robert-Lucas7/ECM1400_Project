from utils import countvalue, find_median, insertion_sort, maxvalue, meannvalue, minvalue, sumvalues
import pytest
from statistics import mean, median
def test_sumvalues():
    l = [1,2,3,4,5]
    assert sumvalues(l) == sum(l)

def test_sumvalues_incorrect_type():
    l = [1,'2',3,4,5]
    with pytest.raises(TypeError):
        sumvalues(l)

def test_maxvalue():
    l = [1,2,3,4,5]
    assert l[maxvalue(l)] == max(l)

def test_maxvalue_incorrect_type():
    l = [1,'2',3,4,5]
    with pytest.raises(TypeError):
        maxvalue(l)

def test_maxvalue_empty_list():
    l = []
    with pytest.raises(ValueError):
        maxvalue(l)

def test_minvalue():
    l = [1,2,3,4,5]
    assert l[minvalue(l)] == min(l)

def test_minvalue_incorrect_type():
    l = [1,'2',3,4,5]
    with pytest.raises(TypeError):
        minvalue(l)

def test_minvalue_empty_list():
    l = []
    with pytest.raises(ValueError):
        minvalue(l)

def test_meannvalue():
    l = [1,2,3,4,5]
    assert meannvalue(l) == mean(l)

def test_countvalue():
    l = [1,'2',3,4,5]
    assert countvalue(l, 3) == l.count(3) 

def test_countvalue_empty_list():
    l = []
    assert countvalue(l, 0) == l.count(0)

def test_find__median():
    l = [1,3,2,4,5]
    assert find_median(l) == median(l)

def test_insertion_sort():
    l = [1,3,2,5,4]
    sorted_l_copy = l.copy()
    sorted_l_copy.sort()
    assert insertion_sort(l) == sorted_l_copy

def test_insertions_sort_incorrect_type():
    l = [1,4,'2',3, 5]
    with pytest.raises(TypeError):
        insertion_sort(l)