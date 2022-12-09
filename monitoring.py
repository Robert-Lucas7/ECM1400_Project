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

#print(json.dumps(get_live_data_from_api(), indent=4))
def get_data_when_refreshed(site_code='MY1',species_code='NO',start_date=None,end_date=None, ):
    endpoint = "http://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={SITECODE}/SpeciesCode={SPECIESCODE}/StartDate={STARTDATE}/EndDate={ENDDATE}/Period={PERIOD}/Units={UNITS}/Step={STEP}/Json"
    url = endpoint.format(
        SITECODE = site_code,
        SPECIESCODE = species_code,
        STARTDATE = start_date,
        ENDDATE= end_date,
        PERIOD = None,
        UNITS = None,
        STEP = None
    )
    res = requests.get(url)
    print(res.json())
    #print(json.dumps(res.json(), indent = 4))
get_data_when_refreshed()
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
