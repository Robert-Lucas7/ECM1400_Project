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

# ================================================ Helper Functions ==========================================================
# ============================================================================================================================


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
    print("URL: " + url)
    res = requests.get(url)
    return res.json()


def get_monitoring_sites_and_species() -> dict:
    """Returns information about which pollutants are monitored at each monitoring station and for what period of time

    Returns:
        dict: dictionary containing the monitoring site codes as keys and a nested dictionary of pollutants (and their information) as the values.
    """
    endpoint = "http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json"
    monitoring_site_details = requests.get(endpoint).json()
    print(json.dumps(monitoring_site_details, indent=4))
    site_codes_and_pollutants_monitored = {}
    for monitoring_site in monitoring_site_details["Sites"]["Site"]:
        site_codes_and_pollutants_monitored[monitoring_site["@SiteCode"]] = {
            monitoring_site_pollutants["@SpeciesCode"]: {
                "start_date": monitoring_site_pollutants['@DateMeasurementStarted'],
                "end_date": monitoring_site_pollutants['@DateMeasurementFinished']
            }
            for monitoring_site_pollutants in (monitoring_site["Species"] if type(monitoring_site["Species"]) == list else [monitoring_site["Species"]])}
    return site_codes_and_pollutants_monitored


def get_user_input_for_monitoring_site(site_codes_and_pollutants: dict) -> str:
    valid_site_code = False
    site_code_inp = ""
    while not valid_site_code:
        site_code_inp = input(
            "Enter the site code you would like to plot the pollutants for.\n").upper()
        if site_code_inp not in site_codes_and_pollutants.keys():
            print("Site code is invalid.")
        else:
            valid_site_code = True
    return site_code_inp


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
