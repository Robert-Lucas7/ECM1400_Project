# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
from utils import *
import numpy as np


# Higher order function that takes in the average function specified in utils.py
def get_daily_averages(data, average_func, monitoring_station: str, pollutant: str) -> list:
    '''
    Returns a list of daily averages (mean or median).\n
    Parameters
    ----------
    data - the monitoring station data in the form of a numpy array of tuples. The tuples are in the form (date_and_time : str, dictionary of pollution values)
    '''
    try:
        if monitoring_station in ["Harlington", "Marlyebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            data_for_monitoring_station = data[monitoring_station]
            average_daily_values = []
            for i in range(365):
                hourly_values = []
                for j in range(24):
                    value = data_for_monitoring_station[i *
                                                        24 + j][1][pollutant]
                    # if there is an appropriate value and not "No Data". (Find better way to see if string can be cast to float)
                    if value != "No data":
                        hourly_values.append(float(value))
                mean_value_for_day = average_func(hourly_values)
                average_daily_values.append(mean_value_for_day)
            return average_daily_values
        else:
            raise Exception(
                "Invalid arguments passed (either as monitoring station or pollutant")
    except Exception as e:
        print(str(e))


def daily_average(data, monitoring_station: str, pollutant: str) -> list:
    """
    This function returns a list/array with the daily averages for a particular pollutant and monitoring station.
    """
    # Validate monitoring_station and pollutant.
    list_of_daily_means = get_daily_averages(
        data, meannvalue, monitoring_station, pollutant)
    return list_of_daily_means


def daily_median(data, monitoring_station: str, pollutant: str) -> list:
    """
    Returns a list of the daily median values of the pollutant at a specific monitoring station.
    """
    list_of_daily_medians = get_daily_averages(
        data, find_median, monitoring_station, pollutant)
    return list_of_daily_medians


def hourly_average(data, monitoring_station, pollutant):
    """
    Returns a list of hourly averages (24 values)
    """
    try:
        if monitoring_station in ["Harlington", "Marlyebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            hour_data = np.empty((24, 365))
            station_data = data[monitoring_station]
            for i in range(365):
                for j in range(24):
                    value = station_data[j + i * 24][1][pollutant]
                    if value != "No data":
                        hour_data[j][i] = value
            mean_hour_data = np.empty(24)
            for i in range(24):

                mean_hour_data[i] = meannvalue(hour_data[i])
            return mean_hour_data

        else:
            raise Exception(
                "Invalid arguments passed (either as monitoring station or pollutant")
    except Exception as e:
        print(str(e))


def monthly_average(data, monitoring_station, pollutant):
    """
    Returns an array of the monthly averages for a particular pollutant and monitoring station.\n
    Parameters
    ----------
    data - 
    monitoring station - string
    pollutant - string
    """

    try:
        if monitoring_station in ["Harlington", "Marlyebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            monthly_average_data = np.empty(12)
            station_data= data[monitoring_station]
            for i in range(12):
                same_month = True
                while same_month:
                    pass


        else:
            raise Exception(
                "Invalid arguments passed (either as monitoring station or pollutant")
    except Exception as e:
        print(str(e))


def peak_hour_date(data, date, monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here


def count_missing_data(data,  monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here


def fill_missing_data(data, new_value,  monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here
