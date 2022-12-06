# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
from utils import *
import numpy as np
import copy #https://docs.python.org/3/library/copy.html
def get_data():
    monitoring_stations = ["Harlington", "Marylebone Road", "N Kensington"]
    data_dict = {}
    for station in monitoring_stations:
        
        fileName = f"Pollution-London {station}.csv"
        lines = open(f"./data/{fileName}", 'r').readlines()
        # intialises an uninitialised array of values.
        station_list = np.empty(len(lines) - 1, dtype=object)
        for index, line in enumerate(lines):# should use start = 
            if index != 0:  # if it isn't the first line where the column headers are specified.
                sections = line.rstrip().split(',')

                station_list[index - 1] = (f"{sections[0]} {sections[1]}", {  # index - 1 as the first line is not actual data so each line is 1 index behind
                    "no": sections[2],
                    "pm10": sections[3],
                    "pm25": sections[4]
                })
        data_dict[station] = station_list

    return data_dict
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
            index = 0
            for i in range(12):
                normal_monthly_data = []
                same_month = True
                while same_month:
                    current_month = station_data[index][0][5:7]
                    if len(station_data) == index + 1 or station_data[index + 1][0][5:7] != current_month:
                        same_month = False
                    value = station_data[index][1][pollutant]
                    if value != "No data":
                        normal_monthly_data.append(float(value))
                    index += 1
                monthly_average_data[i] = meannvalue(normal_monthly_data)
            return monthly_average_data


        else:
            raise Exception(
                "Invalid arguments passed (either as monitoring station or pollutant")
    except Exception as e:
        print(str(e))


def peak_hour_date(data, date, monitoring_station, pollutant):
    """
    Return a tuple of the time and value that the max pollution occurs (for a particular pollutant)
    """
    found_date = False
    starting_index = 0
    station_data = data[monitoring_station]
    while not found_date:
        if station_data[starting_index][0][:10] != date :
            starting_index += 1
            print(starting_index, )
            if starting_index >= len(station_data) -1:
                raise Exception("Date is not found in the CSV file.")
        else:
            found_date = True
    #time_and_max_value = ["", -1]
    max_time = ""
    max_value = -1
    for i in range(24):
        if station_data[starting_index + i][1][pollutant] != "No data":
            value = float(station_data[starting_index + i][1][pollutant])
            if value > max_value:
                max_time = station_data[starting_index + i][0][11:19]
                max_value = value
    return max_time, max_value
    


def count_missing_data(data,  monitoring_station, pollutant):
    """
    Returns the number of missing data entries for a given monitoring station and pollutant.\n
    Parameters
    ----------
    data
    monitoring_station
    pollutant
    """
    station_data = data[monitoring_station]
    num_missing_data = 0
    for i in range(len(station_data)):
        value = station_data[i][1][pollutant]
        if value == "No data":
            num_missing_data += 1
    return num_missing_data


def fill_missing_data(data, new_value,  monitoring_station, pollutant):
    """
    Returns a copy of the data with "No data" values are replaced by the parameter new_value.\n
    Parameters
    ----------
    data
    new_value
    monitoring_station
    pollutant
    """
    
    data_copy = copy.deepcopy(data)
    station_data = data_copy[monitoring_station] #array is separated from the data passed as a parameter (NOT passed by reference).
    for _, pollution in station_data:
        if pollution[pollutant] == "No data":
            pollution[pollutant] = new_value
    #data_copy[monitoring_station] = station_data
    print(f"data: {count_missing_data(data, 'Harlington', 'pm10')} data_copy: {count_missing_data(data_copy, 'Harlington', 'pm10')}")
    
    return data_copy
