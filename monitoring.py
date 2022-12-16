import requests
import datetime
import numpy as np
from utils import maxvalue
import math
from time import sleep
import re
# ================================================ Helper Functions ==========================================================

def get_monitoring_sites_and_species() -> dict:
    """Returns information about which pollutants are monitored at each monitoring station and the dates they were first monitored and last monitored.

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

def generate_graph(pollutant_values: list[float], max_height_of_graph: int = 40, num_on_y_axis = 5) -> np.ndarray:
    """Creates a text-based graph represented as a 2D NumPy array that plots the value of a pollutant at a monitoring station.

    Args:
        pollutant_values (list[float]): The values of a pollutant
        max_height_of_graph (int, optional): The maximum height of the graph. Defaults to 40.
        num_on_y_axis (int, optional): The number of values shown on the y-axis (excluding zero). Defaults to 5.

    Returns:
        np.ndarray: A 2D array representing a graph.
    """
    # Need to find the max and min values to ensure the correct scaling
    # Finding the max pollutant value
    print("POLLUTANT VALUES: ", pollutant_values)
    max_value = float(pollutant_values[maxvalue( pollutant_values )])
    max_width_of_graph = 180
    print("MAX VALUE: ", max_value)
    height = math.ceil((max_height_of_graph / max_value) * math.ceil(max_value))
    # Create array of shape fill with blank spaces
    plot = np.full((height, max_width_of_graph), " ")

    # Getting y-axis values
    y_axis_values = []
    longest_value = 0
    for i in range(0, num_on_y_axis+1):
        value = ((max_value/num_on_y_axis) * i)
        value_string = f"{value : .3g}".strip()
        if len(value_string) > longest_value:
            longest_value = len(value_string)
        y_axis_values.append(value_string)

    # Calculating the border widths needed
    border_left_width = longest_value + 1
    border_bottom_height = len(str(len(pollutant_values))) + 1
    # Adding y-axis values
    for value in y_axis_values:
        print("VALUE: ",value)
        for col in range(len(value)):
            row = max_height_of_graph - border_bottom_height - round(((max_height_of_graph - border_bottom_height) / max_value) * float(value))
            plot[row, col] = value[col]
    # Adding x-axis values
    for i in range(len(pollutant_values)):
        num_as_string = str(i)
        # print(num_as_string)
        for index, digit in enumerate(num_as_string):
            #print(index + max_height_of_graph - border_bottom_height + 1, i + border_left_width)
            plot[index + max_height_of_graph - border_bottom_height + 1, i + border_left_width] = digit
    # Plotting data points
    for index, value in enumerate(pollutant_values):
        if value != None:
            row = max_height_of_graph - border_bottom_height - round(((max_height_of_graph - border_bottom_height)/max_value) * value)
            # Validate that this is within the max_width_of_graph otherwise shrink data by making it into days or even weeks
            col = index + border_left_width
            plot[row, col] = 'x'
        #else:
        #    print(index, value)
    # Adding the border
    for row in range(0, max_height_of_graph - border_bottom_height):
        plot[row, border_left_width - 1] = '|'
    for col in range(border_left_width, max_width_of_graph):
        plot[max_height_of_graph - border_bottom_height, col] = '-'
    return plot

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
    res = requests.get(url)
    return res.json()

def get_user_input_for_monitoring_site_or_pollutant(valid_sites_or_pollutants: list[str], is_getting_site : bool) -> str:
    """Gets and returns a user's input for the monitoring site code.

    Args:
        site_codes_and_pollutants (dict): A dictionary containing all valid site codes and their pollutants (with other information)

    Raises:
        ValueError: Is raised if the user enters 'q'/'Q'.

    Returns:
        str: The monitoring site code"""
    valid_site_code = False
    site_code_inp = ""
    print(f"Valid {'site codes' if is_getting_site else 'pollutants'}: {','.join(valid_sites_or_pollutants)} ")
    while not valid_site_code:
        site_code_inp = input(f"Enter the {'site code' if is_getting_site else 'pollutant'}.\t").upper()
        if site_code_inp == "Q":
            raise ValueError("Quit selected")
        elif site_code_inp not in valid_sites_or_pollutants:
            print("Site code is invalid.")
        else:
            valid_site_code = True
    return site_code_inp

def get_most_recent_data_from_API_data(site_code : str, pollutant : str) -> dict:
    """Returns the most recent pollutant data as a dictionary for a specific site and pollutant.

    Args:
        site_code (str): The site code representing the monitoring site.
        pollutant (str): The code for the pollutant.

    Returns:
        dict: The most recent pollutant data as a dictionary with keys of the time and value of the pollutant.
    """
    api_data = get_live_data_from_api(site_code, pollutant)["RawAQData"]["Data"]
    is_most_recent_value = False
    most_recent_value_and_time = {}
    for d in reversed(api_data):
        if d["@Value"] != "":
            most_recent_value_and_time['time'] = d["@MeasurementDateGMT"]
            most_recent_value_and_time['value'] = d['@Value']
            is_most_recent_value = True
            break
    if not is_most_recent_value:
        most_recent_value_and_time['time'] = 'N/A'
        most_recent_value_and_time['value'] = 'N/A'
    return most_recent_value_and_time

def display_data_in_table(headings : list[str], data : dict[str, dict], spaces_left_justified : int = 25) -> None:
    """ Prints the data passed as arguments in a table.

    Args:
        headings (list[str]): The headings of the table as a list.
        data (dict[str, dict]): A dictionary containing pollutant or monitoring site data (in the form: {site_or_pollutant: {'time' : time, 'value' : value}})
        spaces_left_justified (int, optional): How many characters the table contents should be left-justified. Defaults to 25.
    """
    header = ""
    for heading in headings:
        header += f"{ heading : <spaces_left_justified}"
    print(header)
    for site_or_pollutant, pollutant_info in data.items():
        print(f"{site_or_pollutant : <spaces_left_justified}{pollutant_info['time'] : <spaces_left_justified}{pollutant_info['value'] : <spaces_left_justified}")

def get_sites_currently_monitoring_pollutant(monitoring_sites_and_pollutants : dict, pollutant : str) -> list[str]:
    """Returns a list of the monitoring stations currently monitoring a pollutant.

    Args:
        monitoring_sites_and_pollutants (dict): A dictionary containing the monitoring sites and the pollutants that are monitored there (with start and end dates).
        pollutant (str): A pollutant.

    Returns:
        list[str]: A list containing all of the monitoring sites currently monitoring the pollutant.
    """
    sites_currently_monitoring_pollutant = []
    for site, pollutant_dict in monitoring_sites_and_pollutants.items():
        if pollutant_dict.get(pollutant) != None and pollutant_dict[pollutant]["end_date"] == "":  #If the pollutant is a key of pollutant_dict and the pollutant is currently being monitored at the monitoring site. (a key error won't be raised as the 'and' will short circuit)
            sites_currently_monitoring_pollutant.append(site)
    return sites_currently_monitoring_pollutant
# ============================================================================================================================
# ================================================ 4 main functions ==========================================================
def plot_week_of_pollutant_data_on_graph(monitoring_sites_and_pollutants: dict) -> None:
    """Prints a graph of a week of pollutant data at a monitoring site for a particular pollutant and saves it to a text file called 'graph-of-{pollutant}-{date-beginning}.txt'.

    Args:
        monitoring_sites_and_pollutants (dict): A dictionary containing the monitoring sites and pollutants monitored there (with start and end dates)."""
    try:    
        # Validate site code - USER INPUT
        site_code_inp = get_user_input_for_monitoring_site_or_pollutant(monitoring_sites_and_pollutants.keys(), True)
        # Validate pollutant is available at site - USER INPUT
        pollutant_to_plot = get_user_input_for_monitoring_site_or_pollutant(monitoring_sites_and_pollutants[site_code_inp].keys(), False)
        # Validate start_date - ensure that start_date + datetime.timedelta(days=day_difference) is within both bounds (of when the monitoring started or finished - be careful with empty string for "@MonitoringFinished")  - USER INPUT
        when_pollutant_was_last_monitored = None
        if monitoring_sites_and_pollutants[site_code_inp][pollutant_to_plot]['end_date'] == "":
            when_pollutant_was_last_monitored = datetime.date.today()
        else:
            when_pollutant_was_last_monitored = datetime.datetime.strptime(monitoring_sites_and_pollutants[site_code_inp][pollutant_to_plot]['end_date'][:10], '%Y-%m-%d').date()
        print(f"{pollutant_to_plot} at {site_code_inp} was monitored from {monitoring_sites_and_pollutants[site_code_inp][pollutant_to_plot]['start_date']} to {str(when_pollutant_was_last_monitored)}")
        is_valid_start_date = False
        start_date = ""
        regex_pattern = "(199[3-9]|20(0|1)[0-9]|202[0-2])-(0[1-9]|1[0-2])-(0[1-9]|[1-2][1-9]|3[0-1])" #Possible regex pattern for dates (is wrong for some months due to the number of days)
        while not is_valid_start_date:
            start_date = input("Enter the start date in the form YYYY-MM-DD (date closer to the present) to plot the data from.\t")
            try:
                if re.match(regex_pattern, start_date): #if the input is in the correct form.
                    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                    end_date = start_date + datetime.timedelta(days=7)
                    if start_date <= when_pollutant_was_last_monitored and end_date > datetime.datetime.strptime(monitoring_sites_and_pollutants[site_code_inp][pollutant_to_plot]['start_date'][:10], '%Y-%m-%d').date():
                        is_valid_start_date = True
                else:
                    raise ValueError("Date is invalid")
            except ValueError as e:
                print("Date is invalid")
        
        # Validate that there is actually data to plot - raise an exception if there is no data to plot and just inform user (print to terminal) if there is just some missing data
        response_data = get_live_data_from_api(site_code_inp, pollutant_to_plot, start_date, end_date)["RawAQData"]["Data"]
        pollutant_values = [float(d["@Value"]) if d["@Value"] != "" else None for d in response_data]
        graph = generate_graph(pollutant_values)
        #Prints the graph to the terminal
        for row in range(graph.shape[0]):
            string = ""
            for col in range(graph.shape[1]):
                string += graph[row, col]
            print(string)

    except ValueError as e:
        if e.args[0] == "The List is empty so there is not a maximum value":
            print("There is no data to plot in the time frame selected, so returning to the monitoring module menu")
    except Exception as e:
        print("Returning to the monitoring module menu.")
        print(e)

def display_most_recent_pollutant_data(monitoring_sites_and_pollutants: dict) -> None:
    """Prints the most recent pollutant data to the terminal and refreshes this value when new data is available.

    Args:
        monitoring_sites_and_pollutants (dict): A dictionary containing the monitoring sites and pollutants monitored there (with start and end dates)."""
    try:
        
        # Get pollutant and validate - ONLY if they are still monitoring the pollutant - raise exception if the monitoring site has no currently monitored pollutants - USER INPUT
        valid_pollutants = [d["@SpeciesCode"] for d in requests.get("https://api.erg.ic.ac.uk/AirQuality/Information/Species/Json").json()["AirQualitySpecies"]["Species"]]
        pollutant = get_user_input_for_monitoring_site_or_pollutant( valid_pollutants, False)#"NO2"
        # Get site_code and validate - USER INPUT
        sites_currently_monitoring_pollutant = get_sites_currently_monitoring_pollutant(monitoring_sites_and_pollutants, pollutant)
        site_code = get_user_input_for_monitoring_site_or_pollutant(sites_currently_monitoring_pollutant, True) #"WMB"
    
        print("To stop and return to the main menu press 'Ctrl + c'")
        prev_time = -1  # This is not possible
        repeat = True
        while repeat:
            #response_data = get_live_data_from_api(site_code, pollutant)["RawAQData"]["Data"]
            current_time_and_value = get_most_recent_data_from_API_data(site_code, pollutant)
            if current_time_and_value == {'time' : 'N/A','value' : 'N/A'}:
                print(f"There is currently no recent data available for {pollutant} at {site_code}. Returning to the main menu.")
                repeat = False
            elif prev_time != current_time_and_value:
                print(f"The most recent value of {pollutant} at {site_code} at {current_time_and_value['time']} is: {current_time_and_value['value']}")
            prev_time = current_time_and_value
            sleep(5)

    except KeyboardInterrupt:
        print("Returning to monitoring module menu")
    except Exception as e:
        print(f"Something went wrong - returning to the monitoring module menu. ({e})")

def comparison_of_pollutant_at_monitoring_sites(monitoring_sites_and_pollutants: dict) -> None:
    """Shows the most recent value of a specific pollutant at different monitoring sites ('N/A' if no recent pollutant data is available).

    Args:
        monitoring_sites_and_pollutants (dict): A dictionary containing the monitoring sites and pollutants monitored there (with start and end dates)."""
    try:
        # Get a valid pollutant - USER INPUT
        # /Information/Species/Json endpoint to get info about the commonly monitored species.
        valid_pollutants = requests.get("https://api.erg.ic.ac.uk/AirQuality/Information/Species/Json").json()["AirQualitySpecies"]["Species"]

        pollutant_to_compare_sites = get_user_input_for_monitoring_site_or_pollutant(valid_pollutants, False)#"NO2"
        # Iterate over monitoring_sites_and_pollutants to get all of the sites that are currently monitoring them
        sites_currently_monitoring_pollutant = get_sites_currently_monitoring_pollutant(monitoring_sites_and_pollutants, pollutant_to_compare_sites)

        # User picks up to 5 monitoring sites to compare - If there is not data within the past day then the monitoring station will not be compared.
        monitoring_sites_to_compare = [] #["BG1", "BG2", "BX2"]
        add_another_site = True
        view_monitoring_sites = input(f"Enter 'y' to view all monitoring sites currently measuring the {pollutant_to_compare_sites} pollutant").upper()

        if len(view_monitoring_sites) >= 1 and view_monitoring_sites[0] == 'Y':
            print(f"Monitoring sites currently monitoring {pollutant_to_compare_sites}: {','.join(sites_currently_monitoring_pollutant)}")

        while add_another_site and len(monitoring_sites_to_compare) < 5:
            monitoring_sites_to_compare.append( get_user_input_for_monitoring_site_or_pollutant(sites_currently_monitoring_pollutant, True) )
        
        site_and_most_recent_value = {}
        for site in monitoring_sites_to_compare:
            site_and_most_recent_value[site] = get_most_recent_data_from_API_data(site, pollutant_to_compare_sites)

        print(f"{pollutant_to_compare_sites} at {','.join(site_and_most_recent_value.keys())}")
        display_data_in_table(['Monitoring Site', 'Date and time', 'Value'], site_and_most_recent_value)
    except ValueError as e:
        if e.args == "Quit selected":
            print("Quitting - returning to the main menu.")
    except Exception as e:
        print(f"Something went wrong - returning to the main menu. ({e})")

def get_pollution_values_at_monitoring_site(monitoring_sites_and_pollutants: dict) -> None:
    """Shows the most recent pollutant data for a specific monitoring site ('N/A' if no recent pollutant data is available).

    Args:
        monitoring_sites_and_pollutants (dict): A dictionary containing the monitoring sites and pollutants monitored there (with start and end dates)."""
    # Get monitoring site to get current values - USER INPUT
    try:
        site_code = get_user_input_for_monitoring_site_or_pollutant(monitoring_sites_and_pollutants.keys(), True)

        pollutant_data = {}
        for pollutant in monitoring_sites_and_pollutants[site_code].keys():
            pollutant_data[pollutant] = get_most_recent_data_from_API_data(site_code, pollutant)

        print(f"Showing recent values for { site_code }. (N/A means that there is no very recent data available for the pollutant at the monitoring site)")
        display_data_in_table(['Pollutant', 'Date and time', 'Value'], pollutant_data)

    except ValueError as e:
        if e.args == "Quit selected":
            print("Quitting - returning to the main menu")
    except Exception as e:
        print(f"Something went wrong - returning to the main menu. ({e})")
# =============================================================================================================================