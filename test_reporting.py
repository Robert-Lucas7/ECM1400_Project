from reporting import daily_average, daily_median, get_data, hourly_average
import numpy as np
import pytest


def test_get_data_keys():
    data = get_data()
    assert list(data.keys()) == ["Harlington", "Marylebone Road", "N Kensington"]

def test_get_data_values():
    data = get_data()
    for value in data.values():
        assert type(value) == np.ndarray

def test_get_data_non_existent_file():
    assert not get_data(["abcdef"])

def test_daily_average_arguments():
    data = get_data()
    assert not daily_average(data, "mk", "kl")

def test_daily_median_arguments():
    data = get_data()
    assert not daily_median(data, "mk", "kl")

def test_hourly_average_arguments():
    data = get_data()
    assert not hourly_average(data, "mk", "kl")

