# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
from utils import *

import numpy as np
def daily_average(data, monitoring_station: str, pollutant: str) -> list:
    """
    This function returns a list/array with the daily averages for a particular pollutant and monitoring station.
    """
    # Validate monitoring_station and pollutant.
    print(monitoring_station, pollutant)
    try:
        if monitoring_station in ["Harlington", "Marlyebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            data_for_monitoring_station = data[monitoring_station]
            
            average_daily_values = []
            
            for i in range(365):
                hourly_values = []
                for j in range(24):
                    value = data_for_monitoring_station[i * 24 + j][1][pollutant]
                    print(f"{value} : {type(value)} : {value.isdigit()}")
                    if value != "No data": #if there is an appropriate value and not "No Data". (Find better way to see if string can be cast to float)
                        hourly_values.append(float(value))
                mean_value_for_day = meannvalue(hourly_values)
                average_daily_values.append(mean_value_for_day)
            return average_daily_values

        else:
            raise Exception(
                "Invalid arguments passed (either as monitoring station or pollutant")
    except Exception as e:
        print(str(e))

        # Your code goes here



def daily_median(data, monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here


def hourly_average(data, monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here


def monthly_average(data, monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here


def peak_hour_date(data, date, monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here


def count_missing_data(data,  monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here


def fill_missing_data(data, new_value,  monitoring_station, pollutant):
    """Your documentation goes here"""

    # Your code goes here
