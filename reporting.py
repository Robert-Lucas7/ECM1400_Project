from utils import *
import numpy as np
import copy #https://docs.python.org/3/library/copy.html

def get_data(monitoring_station_files : list[str] = ["Harlington", "Marylebone Road", "N Kensington"]) -> dict[str,object]:
    """Returns a dictionary containing the data from the files specified in the list 'monitoring_station_files'.
    
    Args:
        monitoring_station_files (list[str]): the monitoring stations which have data to be read from a CSV file.

    Returns:
        dict[str,object]: data of the pollutants at the monitoring stations in the format: \n
        {
        "station_0" : [ 
            (date_and_hourly_value, {
                "no" : nitrous_oxide_value,
                "pm10" : pm10_value,
                "pm25" : pm25_value
            })
            , ...
            ]
        "station_1" : ...
    }"""
    try:
        data_dict = {}
        for station in monitoring_station_files:
            fileName = f"Pollution-London {station}.csv"
            lines = open(f"./data/{fileName}", 'r').readlines()
            station_list = np.empty(len(lines) - 1, dtype=object) # Initialising the array which will contain the data from the monitoring station.
            for index, line in enumerate(lines):
                if index != 0:  # if it isn't the first line where the column headers are specified...
                    sections = line.rstrip().split(',')
                    station_list[index - 1] = (f"{sections[0]} {sections[1]}", {  # index - 1 as the first line is not actual data so each line is 1 index behind.
                        "no": sections[2],
                        "pm10": sections[3],
                        "pm25": sections[4]
                    })
            data_dict[station] = station_list

        return data_dict
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Something went wrong ({e})")

def get_daily_averages(data : dict, average_func, monitoring_station: str, pollutant: str) -> list:
    """Returns a list of daily averages (mean or median) over a year (365 days).

    Args:
        data (dict[str, np.ndarray]): the pollution data returned from get_data()
        average_func (function): the average function to be used (meanvalue() or find_median())
        monitoring_station (str): the monitoring station to get the daily averages for
        pollutant (str): the pollutant to get the daily averages for

    Raises:
        ValueError: invalid arguments in monitoring_station or pollutant are passed into the function.

    Returns:
        list: list of daily averages for the particular monitoring station and pollutant"""
    try:
        if monitoring_station in ["Harlington", "Marylebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            average_daily_values = []
            for i in range(365):
                hourly_values = []
                for j in range(24):
                    value = data[monitoring_station][i * 24 + j][1][pollutant] # i * 24 + j is the index of the current pollutant value as there are 24 data entries per day.
                    if value != "No data":
                        hourly_values.append(float(value)) #Parse the value as a float (so the average function can be applied to the list) and add to the list of hourly values.
                if len(hourly_values) != 0:
                    average_value_for_day = average_func(hourly_values) #Apply the average function (mean or median) to the list of hourly values.
                else:
                    average_value_for_day = "N/A"
                average_daily_values.append(average_value_for_day)
            return average_daily_values
        else:
            raise ValueError("Invalid arguments passed (either as monitoring station or pollutant)")
    except IndexError:
        print("The data does not contain the correct amount of data (24 values for each day in a year (365 days))")
    except Exception as e:
       print(f"Something went wrong, returning to the reporting menu ({e}).")


def daily_average(data : dict, monitoring_station: str, pollutant: str) -> list:
    """Returns a list of the daily means of a pollutant at a particular monitoring station.

    Args:
        data (dict[str, np.ndarray]): the pollution data returned from get_data().
        monitoring_station (str): the monitoring station to get the daily means for.
        pollutant (str): the pollutant to get the daily means for.

    Raises:
        ValueError: invalid arguments in monitoring_station or pollutant are passed into the function.

    Returns:
        list: list of the mean values of a pollutant for each day."""
    
    try:
        if monitoring_station in ["Harlington", "Marylebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]: #Check if monitoring_station and pollutant are valid.
            list_of_daily_means = get_daily_averages(data, meannvalue, monitoring_station, pollutant)
            return list_of_daily_means
        else:
            raise ValueError("Invalid arguments passed (either as monitoring station or pollutant)")
    except ValueError:
        print("Invalid arguments passed (either as monitoring station or pollutant)")
    except Exception as e:
        print(f"Something went wrong, returning to the reporting menu ({e}).")


def daily_median(data : dict, monitoring_station: str, pollutant: str) -> list:
    """Returns a list of the daily medians of a pollutant at a particular monitoring station.
    Args:
        data (dict[str, np.ndarray]): the pollution data returned from get_data()
        monitoring_station (str): the monitoring station to get the daily medians for
        pollutant (str): the pollutant to get the daily medians for

    Raises: 
        ValueError: invalid arguments in monitoring_station or pollutant are passed into the function.

    Returns:
        list:  list of the median values of a pollutant for each day"""
    try:
        if monitoring_station in ["Harlington", "Marylebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            list_of_daily_medians = get_daily_averages(data, find_median, monitoring_station, pollutant)
            return list_of_daily_medians
        else:
            raise ValueError("Invalid arguments passed (either as monitoring station or pollutant)")
    except Exception as e:
        print(f"Something went wrong, returning to the reporting menu ({e}).")


def hourly_average(data : dict, monitoring_station : str, pollutant : str) -> list:
    """Returns a list of the mean values of the pollutant for each hour in the day (24 values).

    Args:
        data (dict[str, np.ndarray]): the pollution data returned from get_data().
        monitoring_station (str): the monitoring station to get the hourly averages for.
        pollutant (str): the pollutant to get the hourly averages for.

    Raises:
        ValueError: invalid arguments in monitoring_station or pollutant are passed into the function.

    Returns:
        list: list of the mean values of a pollutant for each hour."""
    try:
        if monitoring_station in ["Harlington", "Marylebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            hour_data = [[] for _ in range(24)] #Initialise a list containing 24 empty lists.
            for i in range(365):
                for j in range(24):
                    value = data[monitoring_station][j + i * 24][1][pollutant]
                    if value != "No data":
                        hour_data[j].append(float(value))
            mean_hour_data = []
            for i in range(24):
                mean_hour_data.append(meannvalue(hour_data[i])) #hour_data[i] is the indivdual array of the hourly values in a day of that pollutant.
            return mean_hour_data
        else:
            raise ValueError("Invalid arguments passed (either as monitoring station or pollutant)")
    except IndexError:
        print("The data does not contain the correct amount of data (24 values for each day in a year (365 days))")
    except Exception as e:
        print(f"Something went wrong, returning to the reporting menu ({e}).")


def monthly_average(data : dict, monitoring_station : str, pollutant : str) -> list :
    """Returns the monthly means for a pollutant at a particular pollutant at a monitoring station

    Args:
        data (dict[str, np.ndarray]): the pollution data returned from get_data().
        monitoring_station (str): the monitoring station to get the monthly averages for.
        pollutant (str): the pollutant to get the monthly averages for.

    Raises:
        ValueError: invalid arguments in monitoring_station or pollutant are passed into the function.

    Returns:
        list: list of the monthly means for a pollutant at a monitoring station."""

    try:
        if monitoring_station in ["Harlington", "Marylebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            monthly_average_data = []
            station_data= data[monitoring_station]
            index = 0
            for i in range(12):
                normal_monthly_data = []
                same_month = True
                while same_month:
                    current_month = station_data[index][0][5:7] #Slice gets the month from the date and time string.
                    if len(station_data) - 1== index or station_data[index + 1][0][5:7] != current_month: # if you have reached the last data entry or the month has changed then set same_month to false.
                        same_month = False
                    value = station_data[index][1][pollutant]
                    if value != "No data":
                        normal_monthly_data.append(float(value))
                    index += 1
                if len(normal_monthly_data) != 0:
                    monthly_average_data.append(meannvalue(normal_monthly_data))
                else:
                    monthly_average_data.append('N/A')
            return monthly_average_data
        else:
            raise ValueError("Invalid arguments passed (either as monitoring station or pollutant)")
    except IndexError:
        print("The data does not contain the correct amount of data (24 values for each day in a year (365 days))")
    except Exception as e:
        print(f"Something went wrong, returning to the reporting menu ({e}).")


def peak_hour_date(data : dict, date : str, monitoring_station : str, pollutant : str) -> tuple:
    """Returns a tuple of the time and value that the max pollution occurs (for a particular pollutant).

    Args:
        data (dict[str, np.ndarray]): the pollution data returned from get_data().
        date (str): the date to find the hour that the peak pollution occurred.
        monitoring_station (str): the monitoring station to get the hour that peak pollution occurred for a pollutant.
        pollutant (str): the pollutant to get the hour that peak pollution occurred for that pollutant.

    Raises:
        ValueError: Invalid arguments passed (either as monitoring station or pollutant) or the date specified isn't present in the data from the file(s).

    Returns:
        tuple: a tuple of the time and value of when the maximum pollution occurred"""
    try:
        if monitoring_station in ["Harlington", "Marylebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            found_date = False
            starting_index = 0
            station_data = data[monitoring_station]
            while not found_date:
                if station_data[starting_index][0][:10] != date :
                    starting_index += 1
                    if starting_index >= len(station_data) -1:
                        raise ValueError("Date is not found in the CSV file.")
                else:
                    found_date = True
            max_time = ""
            max_value = -1 #All pollution values are positive so this will be replaced by a true value instantly
            for i in range(24):
                if station_data[starting_index + i][1][pollutant] != "No data":
                    value = float(station_data[starting_index + i][1][pollutant])
                    if value > max_value:
                        max_time = station_data[starting_index + i][0][11:19] #The time that this max pollution occurred.
                        max_value = value
            return max_time, max_value
        else:
            raise ValueError("Invalid arguments passed (either as monitoring station or pollutant)")
    except ValueError:
        print("Either the date specified is not present in the data files or invalid arguments passed (as monitoring_station or pollutant).")
    except Exception as e:
        print(f"Something went wrong, returning to the reporting menu ({e}).")
    


def count_missing_data(data : dict,  monitoring_station : str, pollutant : str) -> int:
    """Returns the number of missing data entries for a given monitoring station and pollutant.

    Args:
        data (dict[str, np.ndarray]): the pollution data returned from get_data().
        monitoring_station (str): the monitoring station to count the missing data entries for.
        pollutant (str): the pollutant to count the missing data entries for.

    Raises:
        ValueError: Invalid arguments passed (either as monitoring station or pollutant)

    Returns:
        int: the number of missing data entries for that pollutant at the monitoring station"""
    try:
        if monitoring_station in ["Harlington", "Marylebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            num_missing_data = 0
            for i in range(len(data[monitoring_station])):
                value = data[monitoring_station][i][1][pollutant]
                if value == "No data":
                    num_missing_data += 1
            return num_missing_data
        else:
            raise ValueError("Invalid arguments passed (either as monitoring station or pollutant)")
    except Exception as e:
        print(f"Something went wrong, returning to the reporting menu ({e}).")


def fill_missing_data(data : dict[str, object], new_value : float,  monitoring_station : str, pollutant : str) -> dict[str,  object]:
    """Returns a copy of the data with "No data" values replaced by the parameter new_value.

    Args:
        data (dict[str, object]): the pollution data returned from get_data().
        new_value (float): the value to replace empty pollutant entries.
        monitoring_station (str): the monitoring station to fill missing data entries for.
        pollutant (str): the pollutant to fill missing data entries for.

    Raises:
        ValueError: Invalid arguments passed (either as monitoring station or pollutant)

    Returns:
        dict[str, np.ndarray]: a copy of the data dictionary passed into the function with the empty pollutant values replaced with the new_value parameter."""
    try:
        if monitoring_station in ["Harlington", "Marylebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            data_copy = copy.deepcopy(data)
            for _, pollution in data_copy[monitoring_station]: # iterates over the tuples and only the dictionary containing the pollutant values is of importance.
                if pollution[pollutant] == "No data":
                    pollution[pollutant] = new_value
            return data_copy
        else:
            raise ValueError("Invalid arguments passed (either as monitoring station or pollutant)")
    except Exception as e:
        print(f"Something went wrong, returning to the reporting module ({e}).")
