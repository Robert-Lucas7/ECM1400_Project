# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
from reporting import *
from datetime import datetime
import numpy as np
import json


def get_data():
    monitoring_stations = ["Harlington", "Marylebone Road", "N Kensington"]
    data_dict = {}
    for station in monitoring_stations:
        # print(station)
        fileName = f"Pollution-London {monitoring_stations[0]}.csv"
        lines = open(f"./data/{fileName}", 'r').readlines()
        # intialises an uninitialised array of values.
        station_list = np.empty(len(lines) - 1, dtype=object)
        for index, line in enumerate(lines):
            if index != 0:  # if it isn't the first line where the column headers are specified.
                sections = line.rstrip().split(',')

                # date_and_time = datetime.strptime(
                #       f"{sections[0]} {sections[1]}", '%Y-%m-%d %H:%M:%S')
                station_list[index - 1] = (f"{sections[0]} {sections[1]}", {  # index - 1 as the first line is not actual data so each line is 1 index behind
                    "no": sections[2],
                    "pm10": sections[3],
                    "pm25": sections[4]
                })
        data_dict[station] = station_list

    return data_dict


def main_menu():
    """
    Prints the options of the different modules and takes an input to choose which module is to be accessed.
    """
    # Printing the different options
    print("R - Access the PR module")
    print("I - Access the MI module")
    print("M - Access the RM module")
    print("A - Print the About text")
    print("Q - Quit the application")

    # Validating the input
    invalidInput = True
    while invalidInput:
        inp = input("Select a valid option\n").upper()
        match inp:  # Should an if elif else be used?
            case "R":  # Pollution reporting
                reporting_menu()
            case "I":
                intelligence_menu()
            case "M":
                monitoring_menu()
            case "A":
                about()
            case "Q":
                invalidInput = False
                quit()


def reporting_menu():
    """
    Displays the options for the reporting module
    """
    print("DA - Daily average")
    print("DM - Daily median")
    print("HA - Hourly average")
    print("MA - Monthly average")
    print("PHD - Peak hour date")
    print("CMD - Count missing data")
    print("FMD - Fill missing data")
    print("Q - Quit to the main menu")
    # Validate the input
    invalidInput = True
    while invalidInput:
        optionInp = input("Select a valid option\n").upper()
        if optionInp == "Q":
            invalidInput = False
        elif optionInp in ["DA", "DM", "HA", "MA", "PHD", "CMD", "FMD"]:  # it is a valid input
            # choose which monitoring station and pollutant
            print("Choose The Monitoring Station:")
            print("H - Harlington")
            print("M - Marylebone Road")
            print("N - N Kensington")
            monitoringStation = ""
            invalidMonitoringStation = True
            while invalidMonitoringStation:
                monitoringStation = input(
                    "Enter the monitoring station\n").upper()
                if monitoringStation in ["H", "M", "N"]:
                    invalidMonitoringStation = False

            if monitoringStation == "H":
                monitoringStation = "Harlington"
            elif monitoringStation == "M":
                monitoringStation = "Marylebone Road"
            else:
                monitoringStation = "N Kensington"

            print("Choose the pollutant")
            print("NO - Nitric Oxide")
            print("PM10 - PM10 inhalable particulate matter")
            print("PM25 - PM25 inhalable particulate matter")
            pollutant = ""
            invalidPollutant = True
            # Could make these validation loops into a function: func validate(printMessage : str, validInputs : list)
            while invalidPollutant:
                pollutant = input("Enter the pollutant\n").lower()
                if pollutant in ["no", "pm10", "pm25"]:
                    invalidPollutant = False
            data = get_data()
            if optionInp == "DA":
                daily_average(data, monitoringStation, pollutant)
            elif optionInp == "DM":
                daily_median(data, monitoringStation, pollutant)
            elif optionInp == "HA":
                hourly_average(data, monitoringStation, pollutant)
            elif optionInp == "MA":
                monthly_average(data, monitoringStation, pollutant)
            elif optionInp == "PHD":
                peak_hour_date(data, monitoringStation, pollutant)
            elif optionInp == "CMD":
                count_missing_data(data, monitoringStation, pollutant)
            elif optionInp == "FMD":
                fill_missing_data(data, monitoringStation, pollutant)
        else:
            print("Invalid input")


def monitoring_menu():
    """Your documentation goes here"""
    # Your code goes here


def intelligence_menu():
    """Your documentation goes here"""
    # Your code goes here


def about():
    """Your documentation goes here"""
    # Your code goes here


def quit():
    """quit() will print a message saying that the program is being terminated and will not return a value."""
    # Your code goes here
    print("This program is terminating")


if __name__ == '__main__':
    # main_menu()
    '''d = get_data()
    print(d)
    print(len(d["Harlington"]))'''
    print(hourly_average(get_data(), "Harlington", "pm10"))
    #print(daily_median(get_data(), "Harlington", "pm10"))
    # print("END")
    #print(d["N Kensington"])
    #print(len(d["N Kensington"]))
