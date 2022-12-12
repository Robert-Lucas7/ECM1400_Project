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
def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date
    
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()

def get_monitoring_sites_and_species() -> dict:
    """Returns information about which pollutants are monitored at each monitoring station and for what period of time

    Returns:
        dict: dictionary containing the monitoring site codes as keys and a nested dictionary of pollutants (and their information) as the values.
    """
    endpoint = "http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json"
    monitoring_site_details =  requests.get(endpoint).json()
    site_codes_and_pollutants_monitored = {}
    for monitoring_site in monitoring_site_details["Sites"]["Site"]:
        site_codes_and_pollutants_monitored[monitoring_site["@SiteCode"]] = {
            monitoring_site_pollutants["@SpeciesCode"] : {
                "start_date" : monitoring_site_pollutants['@DateMeasurementStarted'],
                "end_date" : monitoring_site_pollutants['@DateMeasurementFinished']
            }
         for monitoring_site_pollutants in (monitoring_site["Species"] if type(monitoring_site["Species"]) == list else [monitoring_site["Species"]])}
    return site_codes_and_pollutants_monitored
print(json.dumps(get_monitoring_sites_and_species(), indent = 4))
def get_monitoring_site_and_species() -> dict:
    """Returns a dictionary containing all of the site codes and pollutants monitored at each site.

    Returns:
        dict: dictionary containing all site codes as the keys. The values are a nested dictionary with keys of: "SiteName" and "Species" (key "Species" contains a list of pollutants monitored at that site)."""
    endpoint = "http://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json"
    monitoring_site_details =  requests.get(endpoint).json()
    site_codes_and_pollutants_monitored = {}
    for site in monitoring_site_details["Sites"]["Site"]: #sites is a dictionary
        print(json.dumps(site, indent = 4))
        site_codes_and_pollutants_monitored[site["@SiteCode"]] = {
            "SiteName" : site["@SiteName"]
        }
        if type(site["Species"]) == list: # As site["Species"] is either a single dictionary or a list of dictionaries.
            site_codes_and_pollutants_monitored[site["@SiteCode"]]["Species"] = [species["@SpeciesCode"] for species in site["Species"]]
        else:
            site_codes_and_pollutants_monitored[site["@SiteCode"]]["Species"] = [site["Species"]["@SpeciesCode"]]
        for species in site_codes_and_pollutants_monitored[site["@SiteCode"]]["Species"]:
            site_codes_and_pollutants_monitored["@SpeciesCode"]["start_date"] = species["@DateMeasurementStarted"]
            species["end_date"] = species["@DateMeasurementFinished"]
    return site_codes_and_pollutants_monitored

def plot_pollutants_on_same_graph(site_codes_and_pollutants : dict, start_date = None, end_date = None) -> None:
    try:
        site_code = input("Enter a site code.")
            
        if site_code not in site_codes_and_pollutants.keys(): #================= DO VALIDATION FOR ALL USER INPUTS ===========================
            pass
        pollutants_to_plot = [] # max three pollutants so graph isn't cluttered.
        inp = ''
        while len(pollutants_to_plot) < 3 and inp.upper() != 'Q':
            inp = input(f"Enter a pollutant from ")#{  ['{pollutant, }' for i, pollutant in enumerate(site_codes_and_pollutants[site_code]['Species']) if i != len(site_codes_and_pollutants[site_code]['Species']) - 1 else pollutant] } (enter Q to stop).\n")
            if inp.upper() in site_codes_and_pollutants[site_code]["Species"]:
                if inp.upper() in pollutants_to_plot:
                    print("Pollutant is already going to be plotted.")
                else:
                    pollutants_to_plot.append(inp.upper())
            elif inp.upper() != "Q":
                print("Enter a valid pollutant. (NO, PM10, or )\n")
        
        data = {}
        for pollutant in pollutants_to_plot:
            response_data = get_live_data_from_api(site_code = site_code, species_code=pollutant)
            print(json.dumps(response_data, indent = 4))
        
    except Exception as e:
        print(e)
#print(get_monitoring_site_and_species())
#plot_pollutants_on_same_graph(get_monitoring_site_and_species())
def rm_function_1(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def rm_function_2(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def rm_function_3(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def rm_function_4(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here
