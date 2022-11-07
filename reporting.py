# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification



def daily_average(data, monitoring_station:str, pollutant:str) -> list:
    """
    This function returns a list/array with the daily averages for a particular pollutant and monitoring station.
    """
    #Validate monitoring_station and pollutant.
    try:
        if monitoring_station in ["Harlington", "Marlyebone Road", "N Kensington"] and pollutant in ["no", "pm10", "pm25"]:
            fileName = f"Pollution-London {monitoring_station}.csv"
            a = []
            with open(f"./data/{fileName}") as f:
                pass
            print(a)

        else:
            raise Exception("Invalid arguments passed (either as monitoring station or pollutant")
    except Exception as e:
        print(str(e))
        ## Your code goes here
daily_average("", "Harlington", "pm10")
def daily_median(data, monitoring_station, pollutant):
    """Your documentation goes here"""
    
    ## Your code goes here
def hourly_average(data, monitoring_station, pollutant):
    """Your documentation goes here"""
    
    ## Your code goes here
def monthly_average(data, monitoring_station, pollutant):
    """Your documentation goes here"""
    
    ## Your code goes here
def peak_hour_date(data, date, monitoring_station,pollutant):
    """Your documentation goes here"""
    
    ## Your code goes here

def count_missing_data(data,  monitoring_station,pollutant):
    """Your documentation goes here"""
    
    ## Your code goes here

def fill_missing_data(data, new_value,  monitoring_station,pollutant):
    """Your documentation goes here"""
    
    ## Your code goes here
