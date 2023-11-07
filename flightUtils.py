from datetime import datetime

def returnBestFlight(flight_data_list):

    all_flight_data = []
    best_price = ['0', 9999]

    # Iterate over the list to access each dictionary
    for flight_data in flight_data_list:
        # Extract the required information
        itineraries = []
        for itinerary in flight_data["itineraries"]:
            segments = []
            for segment in itinerary["segments"]:
                segments.append({
                    "departure": segment["departure"],
                    "arrival": segment["arrival"],
                    "carrierCode": segment["carrierCode"],
                    "duration": segment["duration"],
                    "numberOfStops": segment["numberOfStops"]
                })
            itineraries.append({
                "duration": itinerary["duration"],
                "segments": segments
            })

        price_additional_services = []
        if "additionalServices" in flight_data['price']:
            for service in flight_data["price"]["additionalServices"]:
                price_additional_services.append(service)

        # Create the new flight_data object
        new_flight_data = {
            "id": flight_data["id"],
            "numberOfBookableSeats": flight_data["numberOfBookableSeats"],
            "itineraries": itineraries,
            "price": {
                "currency": flight_data["price"]["currency"],
                "total": flight_data["price"]["total"],
                "base": flight_data["price"]["base"],
                "additionalServices": price_additional_services
            }
        }

        # Print the new flight_data object
        #print(new_flight_data)
        all_flight_data.append(new_flight_data)
        if (float(new_flight_data['price']['total']) < float(best_price[1])):
            best_price = [new_flight_data['id'], new_flight_data['price']['total']]
        

        # Iterate over all_flight_data to find the object with ID
    for flight_data in all_flight_data:
        if flight_data['id'] == best_price[0]:
            return flight_data
           

    print("Something went wrong and it was not able to find the best flight")
    return None

def checkAvailability(date, available_weekdays):
    
    day_of_week = date.strftime("%A")
    if day_of_week in available_weekdays:
        return True
    else:
        return False