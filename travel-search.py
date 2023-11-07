from amadeusAPIconnect import api_connect
from flightUtils import returnBestFlight, checkAvailability
from datetime import datetime, timedelta
import sys
import json

def main():
    # Check if the script is run with the correct number of arguments
    if len(sys.argv) < 2:
        print("Please provide the Authorization Key")
        sys.exit(1)

    # Get the string from the command-line argument
    api_key = sys.argv[1]

    #
    # ==== PARAMS TO BE CHANGED HERE
    #
    start_date = datetime.strptime("2024-03-02", "%Y-%m-%d")
    end_date = datetime.strptime("2024-03-30", "%Y-%m-%d")
    available_weekdays = ["Friday", "Saturday", "Sunday"]
    first_location = "BNE"
    destinations = ["OSA", "HND", "ICN", "HKG"]
    min_days_at_each_location = 5
    #
    # ====
    #
    

    print("Checking for the best prices, please wait.")
        
    returnBestItineraryFinal(destinations,start_date,end_date,available_weekdays,api_key,first_location,min_days_at_each_location)

    #checkBestPricesForEachDestination(destinations,start_date,end_date, available_weekdays,api_key,first_location)


# returns the best price in the period for each destination
def checkBestPricesForEachDestination(destinations,start_date,end_date, available_weekdays,api_key,first_location):
    for destination in destinations:
        best_itinerary = [0,0,0,9999]
        itinerary = returnBestItinerary(start_date, end_date, available_weekdays,api_key,first_location,destination,best_itinerary)
        print(itinerary)


# returns the best itinerary according to the price
def returnBestItineraryFinal(destinations,start_date,end_date, available_weekdays,api_key,first_location,min_days_at_each_location):
    itinerary = []
    last_location = first_location

    while destinations:
        result = createItinerary(destinations,start_date,end_date, available_weekdays,api_key,last_location)
        itinerary.append(result)

        last_location = result[2]
        destinations.remove(result[2])
        start_date = datetime.strptime(result[0], "%Y-%m-%d") + timedelta(days=min_days_at_each_location)

    print(itinerary)
    
    
def createItinerary(destinations,start_date, end_date, available_weekdays,api_key,last_location):
    best_itinerary = [0,0,0,9999]

    for destination in destinations:

        itinerary = returnBestItinerary(start_date, end_date, available_weekdays,api_key,last_location,destination,best_itinerary)

        if itinerary[3] < best_itinerary[3]:
            best_itinerary = itinerary

    print(best_itinerary)
    return best_itinerary


def returnBestItinerary(start_date, end_date, available_weekdays,api_key,originLocationCode,destination,best_itinerary):
    while start_date <= end_date:

        if checkAvailability(start_date, available_weekdays) is True:

            info = initSearch(start_date,api_key,originLocationCode,destination)

            if info[3] < best_itinerary[3]:
                best_itinerary = info 

        start_date += timedelta(days=1)

    return best_itinerary

def initSearch(departureDate, api_key, originLocationCode, destinationLocationCode):
    params = {
            "originLocationCode": originLocationCode,
            "destinationLocationCode": destinationLocationCode,
            "departureDate": departureDate.strftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": "AUD",
            "max" : 5
        }

    data = api_connect(api_key, params)

    if data is None:
        print("No data available")
        sys.exit(1)

    # Access the list of flight data objects
    flight_data_list = data['data']
    # Access the 'dictionaries' field separately
    dictionaries = data['dictionaries']

    target_flight_data = returnBestFlight(flight_data_list)


    #print(f"Best option is for {departureDate} from {originLocationCode} to {destinationLocationCode} is: {target_flight_data['price']['total']} - {target_flight_data['price']['currency']}")
    return [departureDate.strftime("%Y-%m-%d"), originLocationCode, destinationLocationCode, float(target_flight_data['price']['total'])]

    #data
    #price
    #checked_bags
    #duration + numberofstops

main()