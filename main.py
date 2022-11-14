# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def main_menu():
    """
    Prints the options of the different modules and takes an input to choose which module is to be accessed.
    """
    #Printing the different options
    print("R - Access the PR module")
    print("I - Access the MI module")
    print("M - Access the RM module")
    print("A - Print the About text")
    print("Q - Quit the application")

    #Validating the input
    invalidInput = True
    while invalidInput:
        inp = input("Select a valid option").upper()
        match inp: #Should an if elif else be used?
            case "R": #Pollution reporting
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
    """"""
    

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
    main_menu()