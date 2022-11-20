# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
from utils import *


def daily_average(data, monitoring_station: str, pollutant: str) -> list:
    """
    This function returns a list/array with the daily averages for a particular pollutant and monitoring station.
    """
    # Validate monitoring_station and pollutant.
    print(monitoring_station, pollutant)
    try:
        if monitoring_station in ["Harlington", "Marlyebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            dates_and_data_for_monitoring_station = data[monitoring_station]
            hourly_values = []
            average_daily_values = []
            prev_item = None
            for i in range(len(dates_and_data_for_monitoring_station)):
                current_item = dates_and_data_for_monitoring_station[i]
                if prev_item == None or (current_item[:9] == prev_item[:9]):
                    hourly_values.append(current_item[1][pollutant])

                    if i == len(dates_and_data_for_monitoring_station) - 1:
                        mean_value = meannvalue(hourly_values)
                        hourly_values = []
                        average_daily_values.append(mean_value)

                else:
                    mean_value = meannvalue(hourly_values)
                    hourly_values = []
                    average_daily_values.append(mean_value)

                prev_item = current_item

        else:
            raise Exception(
                "Invalid arguments passed (either as monitoring station or pollutant")
    except Exception as e:
        print(str(e))

        # Your code goes here
daily_average("", "Harlington", "pm10")


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
