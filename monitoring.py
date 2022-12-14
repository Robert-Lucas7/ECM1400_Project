# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification.
#
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations.
#
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#
import json
import requests
import datetime
from matplotlib import pyplot as mat_plot
import numpy as np
from utils import maxvalue
import math
from time import sleep
# ================================================ Helper Functions ==========================================================
def get_monitoring_sites_and_species() -> dict:
    """Returns information about which pollutants are monitored at each monitoring station and for what period of time

    Returns:
        dict: dictionary containing the monitoring site codes as keys and a nested dictionary of pollutants (and their information) as the values."""
    endpoint = "http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json"
    monitoring_site_details = requests.get(endpoint).json()
    site_codes_and_pollutants_monitored = {}
    for monitoring_site in monitoring_site_details["Sites"]["Site"]:
        site_codes_and_pollutants_monitored[monitoring_site["@SiteCode"]] = {
            monitoring_site_pollutants["@SpeciesCode"]: {
                "start_date": monitoring_site_pollutants['@DateMeasurementStarted'],
                "end_date": monitoring_site_pollutants['@DateMeasurementFinished']
            }
            for monitoring_site_pollutants in (monitoring_site["Species"] if type(monitoring_site["Species"]) == list else [monitoring_site["Species"]])}
    return site_codes_and_pollutants_monitored

def generate_graph(pollutant_values : list[float], max_height_of_graph : int = 40, max_width_of_graph : int = 180, num_on_y_axis = 5) -> np.ndarray:
    """Creates a graph represented as a 2D NumPy array that plots the value of a pollutant at a monitoring station.

    Args:
        datetime_and_value_kvps (list[dict[str, float]]): _description_
        max_height_of_graph (int, optional): _description_. Defaults to 40.
        max_width_of_graph (int, optional): _description_. Defaults to 180.
        num_on_y_axis (int, optional): The number of values shown on the y-axis (excluding zero). Defaults to 5.

    Returns:
        np.ndarray: A 2D array that represents a graph.
    """
    
    #Need to find the max and min values to ensure the correct scaling
    max_value = float(pollutant_values[maxvalue(pollutant_values)]) #Finding the max pollutant value
    height = math.ceil( (max_height_of_graph // max_value) * max_value)
    plot = np.full((height, max_width_of_graph), " ") #Create array of shape fill with blank spaces

    #Getting y-axis values
    y_axis_values = []
    longest_value = 0
    for i in range(0,num_on_y_axis+1):
        value = ((max_value/num_on_y_axis) * i)
        value_string = f"{value : .3g}".strip()
        if len(value_string) > longest_value:
            longest_value = len(value_string)
        y_axis_values.append(value_string)
    
    #Calculating the border widths needed
    border_left_width = longest_value + 1
    border_bottom_height = len(str(len(pollutant_values)))  + 1
    #Adding y-axis values
    for value in y_axis_values:
        for col in range(len(value)):
            row = max_height_of_graph - border_bottom_height - round(((max_height_of_graph - border_bottom_height)//max_value) * float(value))
            plot[row, col] = value[col]
    #Adding x-axis values
    for i in range(len(pollutant_values)):
        num_as_string = str(i)
        #print(num_as_string)
        for index, digit in enumerate(num_as_string):
            #print(index + max_height_of_graph - border_bottom_height + 1, i + border_left_width)
            plot[index + max_height_of_graph - border_bottom_height + 1, i + border_left_width] = digit
    #Plotting data points
    for index, value in enumerate(pollutant_values):
        if value != None:
            row = max_height_of_graph - border_bottom_height - round(((max_height_of_graph - border_bottom_height)//max_value) * value)
            col = index + border_left_width #Validate that this is within the max_width_of_graph otherwise shrink data by making it into days or even weeks
            plot[row, col] = 'x'
    #Adding the border
    for row in range(0, max_height_of_graph - border_bottom_height):
        plot[row, border_left_width - 1] = '|'
    for col in range(border_left_width, max_width_of_graph):
        plot[max_height_of_graph - border_bottom_height, col] = '-'
    return plot

def print_graph(graph : np.ndarray) -> None:
    for row in range(graph.shape[0]):
        string = ""
        for col in range(graph.shape[1]):
            string += graph[row, col]
        print(string)

def get_live_data_from_api(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 

    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """

    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + \
        datetime.timedelta(days=1) if end_date is None else end_date

    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"

    url = endpoint.format(
        site_code=site_code,
        species_code=species_code,
        start_date=start_date,
        end_date=end_date
    )
    #print("URL: " + url)
    res = requests.get(url)
    return res.json()

def get_user_input_for_monitoring_site(site_codes_and_pollutants: dict) -> str:
    """Gets and returns a user's input for the monitoring site code.

    Args:
        site_codes_and_pollutants (dict): A dictionary containing all valid site codes and their pollutants (with other information)

    Raises:
        ValueError: Is raised if the user enters 'q'/'Q' to quit to the main menu.

    Returns:
        str: The monitoring site code"""
    valid_site_code = False
    site_code_inp = ""
    while not valid_site_code:
        site_code_inp = input(
            "Enter the site code.\t").upper()
        if site_code_inp == "Q":
            raise ValueError("Quit selected")
        elif site_code_inp not in site_codes_and_pollutants.keys():
            print("Site code is invalid.")
        else:
            valid_site_code = True
    return site_code_inp

def get_user_input_for_pollutant(valid_pollutants : list) -> str:
    is_pollutant_valid = False
    pollutant_inp = ""
    print(f"Valid pollutants: { ','.join(valid_pollutants) }")
    while not is_pollutant_valid:
        pollutant_inp = input("Enter the pollutant.\t").upper()
        if pollutant_inp == "Q":
            raise ValueError("Quit selected")
        elif pollutant_inp not in valid_pollutants:
            print("Pollutant is invalid.")
        else:
            is_pollutant_valid = True
    return pollutant_inp
# ============================================================================================================================

def plot_pollutants_on_graph(monitoring_sites_and_pollutants : dict) -> None:
    #Validate site code - USER INPUT
    site_code_inp = get_user_input_for_monitoring_site()
    #Validate pollutant is available at site - USER INPUT
    pollutant_to_plot = get_user_input_for_pollutant()
    #Validate time period selected - USER INPUT
    time_period = "Week"
    #Validate start_date - ensure that start_date + datetime.timedelta(days=day_difference) is within both bounds (of when the monitoring started or finished - be careful with empty string for "@MonitoringFinished")  - USER INPUT
    start_date = datetime.datetime.strptime("2003-07-02", "%Y-%m-%d").date()
    end_date = start_date + datetime.timedelta(days = 7)

    
    
    response_data = get_live_data_from_api(site_code_inp, pollutant_to_plot, start_date, end_date)["RawAQData"]["Data"] #Validate that there is actually data to plot - raise an exception if there is no data to plot and just inform user (print to terminal) if there is just some missing data
    pollutant_values = [float(d["@Value"]) if d["@Value"] != "" else None for d in response_data ]
    graph = generate_graph(pollutant_values)
    print_graph(graph)

def display_most_recent_pollutant_data(monitoring_sites_and_pollutants : dict): #Test at the beginning of an hour
    #Get site_code and validate - USER INPUT
    site_code = "WMB"
    #Get pollutant and validate - ONLY if they are still monitoring the pollutant - raise exception if the monitoring site has no currently monitored pollutants - USER INPUT
    pollutant = "NO2"

    
    try:
        print("To stop and return to the main menu press 'Ctrl + c'")
        prev_time = -1 # This is not possible
        current_time_and_value = {
            'time' : None,
            'value' : None
        }
        while True:
            response_data = get_live_data_from_api(site_code, pollutant)["RawAQData"]["Data"]
            for i in range(len(response_data) - 1, 0, -1):
                if response_data[i]["@Value"] != "":
                    current_time_and_value['time'] = response_data[i]["@MeasurementDateGMT"]
                    current_time_and_value['value'] = response_data[i]["@Value"]
            if prev_time != current_time_and_value:
                print(f"The most recent value of {pollutant} at {site_code} at {current_time_and_value['time']} is: {current_time_and_value['value']}")
            prev_time = current_time_and_value
            sleep(5)



    except KeyboardInterrupt:
        print("Returning to main menu")
    except Exception as e:print(e)

def comparison_of_pollutant_at_monitoring_sites(monitoring_sites_and_pollutants : dict) -> None:
    #Get a valid pollutant - USER INPUT
    #/Information/Species/Json endpoint to get info about the commonly monitored species.
    valid_pollutants = requests.get("https://api.erg.ic.ac.uk/AirQuality/Information/Species/Json").json()["AirQualitySpecies"]["Species"]
    
    print(valid_pollutants)

    pollutant_to_compare_sites = "NO2"
    #Iterate over monitoring_sites_and_pollutants to get all of the sites that are currently monitoring them
    sites_currently_monitoring_pollutant = []
    for site, pollutant_dict in monitoring_sites_and_pollutants.items():
        if pollutant_dict.get(pollutant_to_compare_sites) != None:
            if pollutant_dict[pollutant_to_compare_sites]["end_date"] == "":
                sites_currently_monitoring_pollutant.append(site)
   
    #User picks up to 5 monitoring sites to compare - If there is not data within the past day then the monitoring station will not be compared.
    monitoring_sites_to_compare = ["BG1", "BG2","BX2"]
    site_and_most_recent_value = {}
    for site in monitoring_sites_to_compare:
        data = get_live_data_from_api(site, pollutant_to_compare_sites)["RawAQData"]["Data"]
        print(data)
        for d in reversed(data): #list of dicts - NEED to iterate backwards.
            if d["@Value"] != "":
                site_and_most_recent_value[site] = {
                    'time' : d["@MeasurementDateGMT"],
                    'value' : d["@Value"]
                }
                break
    print(f"{pollutant_to_compare_sites} at {','.join(site_and_most_recent_value.keys())}")
    print(f"{'Monitoring Site' : <25}{'Date and time' : <25}{'Value' : <25}")
    for site, pollutant_info in site_and_most_recent_value.items():
        print(f"{site : <25}{pollutant_info['time'] : <25}{pollutant_info['value'] : <25}")


comparison_of_pollutant_at_monitoring_sites(get_monitoring_sites_and_species())


def get_pollution_values_at_monitoring_site(monitoring_sites_and_pollutants : dict) -> None:
    #Get monitoring site to get current values - USER INPUT
    try:
        site_code = get_user_input_for_monitoring_site(monitoring_sites_and_pollutants)

        pollutant_data = {}
        for pollutant in monitoring_sites_and_pollutants[site_code].keys():
            data = get_live_data_from_api(site_code, pollutant)["RawAQData"]["Data"]
            is_recent_value = False
            for d in reversed(data):
                if d["@Value"] != "":
                    pollutant_data[pollutant] = {
                        'time' : d["@MeasurementDateGMT"],
                        'value' : d["@Value"]
                    }
                    is_recent_value = True
                    break
            if not is_recent_value:
                pollutant_data[pollutant] = {
                            'time' : 'N/A',
                            'value' : 'N/A'
                        } 

        
        print(f"Showing recent values for { site_code }. (N/A means that there is no very recent data available for the pollutant at the monitoring site)")
        print( f"{'Pollutant' : <25}{ 'Date and time' : <25}{ 'Value' : <25}" )
        for pollutant, pollutant_info in pollutant_data.items():
            print(f"{pollutant : <25}{pollutant_info['time'] : <25}{pollutant_info['value'] : <25}")
    except ValueError as e:
        if e.args == "Quit selected":
            print("Quitting - returning to the main menu")
    except Exception as e:
        print("Something went wrong - returning to the main menu.")

#get_pollution_values_at_monitoring_site(get_monitoring_sites_and_species())











def get_dates_for_query(time_period: str, site_codes_and_pollutants: dict, site_code, pollutants, num_weeks: int = 1) -> tuple[datetime.date, datetime.date]:
    time_period = time_period.upper()

    # USER ENTERS THE START DATE HERE
    # datetime.date.today()   ============== USER WILL ENTER AN ACTUAL DATE HERE ==================
    start_date = datetime.datetime.strptime(
        site_codes_and_pollutants[site_code]["CO"]["start_date"][:10], "%Y-%m-%d").date()
    print(start_date)
    day_difference = -1
    if time_period == "DAY":
        day_difference = 1
    elif time_period == "WEEK":
        if num_weeks <= 52:
            day_difference = 7 * num_weeks
        '''else:  # ====================== DO VALIDATION AT A DIFFERENT LOCATION IN THE CODE =============================================
            raise ValueError(
                "THe maximum number of weeks is 52 from the current date.")'''

    elif time_period == "YEAR":
        day_difference = 52 * 7
    end_date = start_date + datetime.timedelta(days=day_difference)
    # NOTIFY THE USER IF THEIR RANGE OF DATES IS WHEN THE POLLUTANT ISN'T MEASURED/ Monitored
    for pollutant in pollutants:
        if end_date < datetime.datetime.strptime(site_codes_and_pollutants[site_code][pollutant]["start_date"][:10], "%Y-%m-%d").date() or start_date > datetime.datetime.strptime(site_codes_and_pollutants[site_code][pollutant]["end_date"][:10], "%Y-%m-%d").date():
            raise ValueError(
                "The date range selected is outside of the range that the pollutants were monitored for")

    return start_date, end_date


def get_info_about_pollutants_at_site(site_codes_and_pollutants: dict, site_code) -> None:

    print(f"Pollutants monitored at site: {site_code}")
    print(f"{'Pollutant' : <20}{'Start date' : <25}{'End date' : <25}")
    for pollutant, pollutant_info in site_codes_and_pollutants[site_code].items():
        print(
            f"{pollutant : <20}{pollutant_info['start_date'] : <25}{pollutant_info['end_date'] : <25}")


def plot_pollutants_on_same_graph(site_codes_and_pollutants: dict, start_date=None, end_date=None) -> None:

    try:
        # Get site code here
        '''
        valid_site_code = False
        while not valid_site_code:
            site_code_inp = input("Enter the site code you would like to plot the pollutants for.\n")
            if site_code_inp.upper() not in site_codes_and_pollutants.keys():
                print("Site code is invalid.")
            else:
                valid_site_code = True
        '''
        site_code_inp = "VS1"  # Testing
        # Get pollutants to plot here
        #site_code = get_user_input_for_monitoring_site(site_codes_and_pollutants)
        get_info_about_pollutants_at_site(
            site_codes_and_pollutants, site_code_inp)
        stop_adding_pollutants = False
        pollutants_to_plot = ["NO2"]  # TESTING
        '''pollutants_to_plot = []
        while not stop_adding_pollutants:
            
            #print(
            #    f"The pollutant options are: {', '.join(site_codes_and_pollutants[site_code_inp].keys())}")
            pollutant_inp = input(
                "Enter a pollutant code to plot on the graph (or enter 'q'/'Q' to stop adding pollutants)")

            if pollutant_inp.upper() == 'Q':
                stop_adding_pollutants = True
            elif pollutant_inp.upper() not in site_codes_and_pollutants[site_code_inp].keys():
                print(f"Pollutant not available at site code {site_code_inp}")
            elif pollutant_inp not in pollutants_to_plot:
                # "VS1" : [CO, NO2, O3, PM10]
                pollutants_to_plot.append(pollutant_inp.upper())
            else:
                print(f"Pollutant {pollutant_inp} is already being plotted.")

            # All possible pollutants have been added.
            if len(pollutants_to_plot) == len(site_codes_and_pollutants[site_code_inp].keys()):
                stop_adding_pollutants = True
            print(f"Pollutants to plot: {', '.join(pollutants_to_plot)}")
'''
        # Get user input for the time period that they want to plot the graph for:
        # Options: day, week, 6 months, 1 year
        time_period_inp = "Week"  # TESTING

        start_date, end_date = get_dates_for_query(
            time_period_inp, site_codes_and_pollutants, site_code_inp, pollutants_to_plot)
        for pollutant in pollutants_to_plot:
            #pollutant_info = site_codes_and_pollutants[site_code_inp][pollutant]
            pollutant_data = get_live_data_from_api(
                site_code_inp, pollutant, start_date=start_date, end_date=end_date)  # pollutant_info["end_date"][:10])
            print(json.dumps(pollutant_data, indent=4))
    except Exception as e:
        print(e)


# plot_pollutants_on_same_graph(get_monitoring_sites_and_species())
#print(json.dumps(get_monitoring_sites_and_species(), indent=4))


# get_info_about_pollutants_at_site(get_monitoring_sites_and_species())

#get_live_data_from_api("VS1", "CO")

def get_most_recent_pollution_data(site_codes_and_pollutants) -> None:
    pass
    #


def rm_function_1(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here


def rm_function_2(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here


def rm_function_3(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here


def rm_function_4(*args, **kwargs):
    """Your documentation goes here"""
    # Your code goes here
