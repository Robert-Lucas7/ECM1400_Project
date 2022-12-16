# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
import json
from reporting import *
from monitoring import get_monitoring_sites_and_species, plot_week_of_pollutant_data_on_graph, display_most_recent_pollutant_data, comparison_of_pollutant_at_monitoring_sites, get_pollution_values_at_monitoring_site
from intelligence import *
import datetime

def main_menu() -> None:
    """Prints the options of the different modules and takes an input to choose which module is to be accessed.
    """
    repeat_again = True
    while repeat_again:
        # Printing the different options
        print("R - Access the PR module")
        print("I - Access the MI module")
        print("M - Access the RM module")
        print("A - Print the About text")
        print("Q - Quit the application")
        inp = input("Select a valid option.\t").upper()
        match inp:  
            case "R": 
                reporting_menu()
            case "I":
                intelligence_menu()
            case "M":
                monitoring_menu()
            case "A":
                about()
            case "Q":
                repeat_again = False
                quit()
            case _:
                print(f"'{inp}' is an invalid input.")


def reporting_menu() -> None:
    """Displays the options for the reporting module"""
    repeat_again = True
    while repeat_again:
        #Prints the options of the reporting module
        print("DA - Daily average")
        print("DM - Daily median")
        print("HA - Hourly average")
        print("MA - Monthly average")
        print("PHD - Peak hour date")
        print("CMD - Count missing data")
        print("FMD - Fill missing data")
        print("Q - Quit to the main menu")

        optionInp = input("Select a valid option\n").upper()
        if optionInp == "Q": 
            repeat_again = False
            print("Returning to the main menu.")
        elif optionInp in ["DA", "DM", "HA", "MA", "PHD", "CMD", "FMD"]:  # If it is a valid input...
            print("Choose The Monitoring Station (H, M, N, or Q to quit):")
            print("H - Harlington")
            print("M - Marylebone Road")
            print("N - N Kensington")
            print("Q - Quit to main menu")
            monitoringStation = ""
            invalidMonitoringStation = True
            while invalidMonitoringStation:
                monitoringStation = input("Enter the monitoring station.\t").upper()
                if monitoringStation in ["H", "M", "N"]:
                    invalidMonitoringStation = False
                elif monitoringStation == "Q":
                    return

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
            print("Q - Quit to main menu")
            pollutant = ""
            invalidPollutant = True
            while invalidPollutant:
                pollutant = input("Enter the pollutant\n").lower()
                if pollutant in ["no", "pm10", "pm25"]: #If user input is a valid pollutant...
                    invalidPollutant = False
                elif pollutant == "Q":
                    return

            data = get_data()
            if data: #If the return from get_data() is not None...
                #If, elif statements for the options displayed in the menu.
                if optionInp == "DA":
                    daily_averages = daily_average(data, monitoringStation, pollutant)
                    if daily_averages:
                        print(f"The daily averages for {pollutant} at {monitoringStation}:")
                        print(f"{','.join(daily_averages)}")
                elif optionInp == "DM":
                    daily_medians = daily_median(data, monitoringStation, pollutant)
                    if daily_medians:
                        print(f"The daily medians for {pollutant} at {monitoringStation}:")
                        print(f"{','.join(daily_medians)}")
                elif optionInp == "HA":
                    hourly_averages = hourly_average(data, monitoringStation, pollutant)
                    print(f"The hourly averages of {pollutant} at {monitoringStation} are:")
                    print(f"{'Hour' : <25}{'Average value' : <25}")
                    for index, average in enumerate(hourly_averages, start= 1):
                        print(f"{index : 03d}:00:00 - {average : <25}")
                elif optionInp == "MA":
                    monthly_averages = monthly_average(data, monitoringStation, pollutant)
                    print(f"The monthly averages of {pollutant} at {monitoringStation} are:")
                    print(f"{'Month' : <25}{'Average Value' : <25}")
                    for index, average in enumerate(monthly_averages, start = 1):
                        print(f"{index : 03d}{average : <25}")
                elif optionInp == "PHD":
                    #Get and validate date - must be in the year of 2021
                    is_valid_date = False
                    date = ""
                    while not is_valid_date:
                        date = input("Enter a valid date in 2021 in the form YYYY-MM-DD")
                        try:
                            converted_date = datetime.datetime.strptime(date, '%Y-%m-%d') #Raises a ValueError if the user input cannot be converted to a datetime object in the specified form.
                            if converted_date == 2021:
                                is_valid_date = True
                            else:
                                print("The date must be in the year 2021")
                        except Exception:
                            print("The date must be in the form YYYY-MM-DD")

                    peak_hour = peak_hour_date(data, date, monitoringStation, pollutant)
                    print(f"The peak pollution of {pollutant} occured at {peak_hour[0]} with a value of {peak_hour[1]} on the {date}")
                elif optionInp == "CMD":
                    count = count_missing_data(data, monitoringStation, pollutant)
                    print(f"There are {count} missing data entries for {pollutant} at {monitoringStation}")
                elif optionInp == "FMD":
                    copy_of_data = fill_missing_data(data, monitoringStation, pollutant)
                    print(json.dumps(copy_of_data, indent = 2))
        else:
            print("Invalid input")


def monitoring_menu():
    """Displays the options for the monitoring module."""
    repeat_again = True
    monitoring_site_and_species = get_monitoring_sites_and_species()
    while repeat_again:
        print("G - Plot a week's worth of pollutant data at a monitoring site on a (G)raph")
        print("R - Displays the most (R)ecent pollutant data at a monitoring site")
        print("P - Display a comparison of (P)ollutant values for the same pollutant at different monitoring sites")
        print("S - Display all pollutant values at the same monitoring (S)ite")
        print("Q - Quit to the main menu.")
        inp = input("Enter an option: \t").upper()
        match inp:
            case "G":
                plot_week_of_pollutant_data_on_graph(monitoring_site_and_species)
            case "R":
                display_most_recent_pollutant_data(monitoring_site_and_species)
            case "P":
                comparison_of_pollutant_at_monitoring_sites(monitoring_site_and_species)
            case "S":
                get_pollution_values_at_monitoring_site(monitoring_site_and_species)
            case "Q":
                repeat_again = False




def intelligence_menu() -> None:
    """Displays the options for the intelligence module."""
    repeat_again = True
    while repeat_again:
        print("R - Find red pixels in the image specified")
        print("C - Find cyan pixels in the image specified")
        print("D - Detect connected components")
        print("S - Detect sorted connected components")
        print("Q - Quit to main menu")
        inp = input("Enter option: \t").upper()
        MARK = None
        match inp:
            case "R":
                find_red_pixels('map.png')
            case "C":
                find_cyan_pixels('map.png')
            case "D":
                valid_colour_input = False
                map_colour = ""
                while not valid_colour_input:
                    map_colour = input("Enter the colour of the map to find connected components - (R)ed or (C)yan: \t").upper()
                    if map_colour in ['R', 'C']:
                        valid_colour_input = True
                    elif map_colour == 'Q':
                        return
                if map_colour == 'R':
                    MARK = detect_connected_components(find_red_pixels('map.png'))
                else:
                    MARK = detect_connected_components(find_cyan_pixels('map.png'))
            case "S":
                if MARK: #If mark is not None...
                    detect_connected_components_sorted(MARK)
                else:
                    print("Please choose the option '(D)etect connected components' first then try again")

            case "Q":
                repeat_again = False
                print("Returning to the main menu.")


def about() -> None:
    """Prints the module code, ECM1400, and a 6-digit candidate number"""
    print("ECM1400 250578")

def quit() -> None:
    """Prints a message saying that the program is being terminated and will not return a value."""
    print("This program is terminating")


if __name__ == '__main__':
    main_menu()
    